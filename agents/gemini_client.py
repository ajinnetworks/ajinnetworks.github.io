"""Shared Gemini model selection for trend, writing and reviewing."""
from functools import lru_cache
import logging
import os
import re
import time

from google import genai
from google.genai import errors, types

logger = logging.getLogger(__name__)
RETRYABLE_CODES = {429, 500, 502, 503, 504}


class GeminiGenerationError(RuntimeError):
    """Generation cannot continue with the configured Gemini models."""


@lru_cache(maxsize=1)
def _anthropic_model():
    import anthropic

    client = anthropic.Anthropic(
        api_key=os.environ["ANTHROPIC_API_KEY"].strip(), timeout=60, max_retries=0
    )
    models = [model.id for model in client.models.list(limit=100)]
    model = next((name for name in models if "sonnet" in name), None)
    if not model:
        raise GeminiGenerationError("Anthropic no Sonnet model available")
    return client, model


def _anthropic_response(prompt: str) -> str:
    try:
        client, model = _anthropic_model()
        response = client.messages.create(
            model=model, max_tokens=8192, messages=[{"role": "user", "content": prompt}]
        )
    except GeminiGenerationError:
        raise
    except Exception as error:
        status = getattr(error, "status_code", type(error).__name__)
        raise GeminiGenerationError(f"Anthropic fallback failed status={status}") from None
    text = "".join(block.text for block in response.content if block.type == "text").strip()
    if not text or response.stop_reason == "max_tokens":
        raise GeminiGenerationError("Anthropic fallback returned empty or truncated content")
    logger.info("Anthropic model=%s status=ok", model)
    return text


_MODEL_ID = re.compile(r"gemini-(\d+)\.(\d+)-(flash-lite|pro|flash)")
_ALIASES = ("gemini-flash-lite-latest", "gemini-pro-latest", "gemini-flash-latest")


def pick_models(model_ids: list[str]) -> list[str]:
    """generateContent 지원 모델 ID 목록에서 후보 선택: 계열(flash-lite, pro, flash)별 최신 버전 + 별칭(최대 4개)."""
    candidates = []
    for model_id in model_ids:
        match = _MODEL_ID.fullmatch(model_id)
        if match:
            major, minor = int(match[1]), int(match[2])
            candidates.append((major, minor, match[3], model_id))
    models = []
    for family in ("flash-lite", "pro", "flash"):
        family_models = [item for item in candidates if item[2] == family]
        if family_models:
            models.append(max(family_models)[-1])
    for alias in _ALIASES:
        if alias in model_ids and len(models) < 4:
            models.append(alias)
    return models


@lru_cache(maxsize=1)
def discover_models(api_key: str) -> tuple[str, ...]:
    """API에서 사용 가능한 Gemini 모델을 조회해 후보를 고른다 (프로세스당 1회)."""
    try:
        with genai.Client(api_key=api_key) as client:
            ids = [
                model.name.rsplit("/", 1)[-1]
                for model in client.models.list()
                if model.name and "generateContent" in (model.supported_actions or [])
            ]
    except errors.APIError as error:
        raise GeminiGenerationError(f"Gemini model discovery HTTP {error.code}") from None
    models = pick_models(ids)
    if not models:
        raise GeminiGenerationError("No supported stable Gemini model found")
    logger.info("Gemini 모델 탐색: %s", ", ".join(models))
    return tuple(models)


def configured_models(api_key: str) -> list[str]:
    """GEMINI_MODELS(쉼표 구분)가 있으면 그대로, 없으면 API에서 탐색."""
    models = list(dict.fromkeys(
        name.strip() for name in os.getenv("GEMINI_MODELS", "").split(",")
        if name.strip()
    ))
    return models or list(discover_models(api_key))


def order_models(models: list[str], prefer: str = "default") -> list[str]:
    """prefer="quality": lite 계열을 뒤로 보내고 flash → pro → 나머지 순 (검수처럼 정확도가 중요한 호출용)."""
    if prefer != "quality":
        return list(models)

    def rank(name: str) -> int:
        if "lite" in name:
            return 3
        if "flash" in name:
            return 0
        if "pro" in name:
            return 1
        return 2

    return sorted(models, key=rank)  # 같은 순위 안에서는 기존 순서 유지 (stable sort)


def get_gemini_response(prompt: str, prefer: str = "default") -> str:
    if getattr(get_gemini_response, "_use_anthropic", False):
        return _anthropic_response(prompt)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise GeminiGenerationError("GEMINI_API_KEY is required")
    models = order_models(configured_models(api_key), prefer)

    client = genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(
            timeout=30000,
            retry_options=types.HttpRetryOptions(attempts=1),
        ),
    )
    pending = models
    failures = {}
    for attempt in (1, 2):
        retry_models = []
        for model in pending:
            try:
                response = client.models.generate_content(model=model, contents=prompt)
            except errors.APIError as error:
                code = error.code
                failures[model] = code
                logger.warning("Gemini model=%s status=%s attempt=%s", model, code, attempt)
                if code in RETRYABLE_CODES:
                    retry_models.append(model)
                elif code != 404:
                    raise GeminiGenerationError(f"Gemini model={model} status={code}") from None
                continue
            except Exception as error:
                raise GeminiGenerationError(
                    f"Gemini model={model} error={type(error).__name__}"
                ) from None

            if response.text and response.text.strip():
                logger.info("Gemini model=%s status=ok attempt=%s", model, attempt)
                return response.text.strip()
            failures[model] = "empty_response"
            logger.warning("Gemini model=%s status=empty_response attempt=%s", model, attempt)
        if attempt == 2 or not retry_models:
            break
        pending = retry_models
        time.sleep(65)

    detail = ", ".join(f"{model}={code}" for model, code in failures.items())
    if os.getenv("ANTHROPIC_API_KEY", "").strip():
        logger.warning("Gemini candidates exhausted (%s), attempting Anthropic", detail)
        text = _anthropic_response(prompt)
        get_gemini_response._use_anthropic = True
        return text
    raise GeminiGenerationError(f"Gemini candidates exhausted ({detail}); Anthropic key unavailable")
