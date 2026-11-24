"""Shared Gemini model selection for trend, writing and reviewing."""
from functools import lru_cache
import logging
import os
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


def get_gemini_response(prompt: str) -> str:
    if getattr(get_gemini_response, "_use_anthropic", False):
        return _anthropic_response(prompt)
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    models = list(dict.fromkeys(
        name.strip() for name in os.getenv("GEMINI_MODELS", "").split(",")
        if name.strip()
    ))
    if not api_key or not models:
        raise GeminiGenerationError("GEMINI_API_KEY and GEMINI_MODELS are required")

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
