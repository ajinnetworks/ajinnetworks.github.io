"""Shared Gemini model selection for trend, writing and reviewing."""
import logging
import os
import time

from google import genai
from google.genai import errors, types

logger = logging.getLogger(__name__)
RETRYABLE_CODES = {429, 500, 502, 503, 504}


class GeminiGenerationError(RuntimeError):
    """Generation cannot continue with the configured Gemini models."""


def get_gemini_response(prompt: str) -> str:
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
    raise GeminiGenerationError(f"Gemini candidates exhausted ({detail})")
