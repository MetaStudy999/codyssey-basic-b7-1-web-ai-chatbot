from __future__ import annotations

import time
from dataclasses import dataclass

import httpx


class AIClientError(RuntimeError):
    code = "AI_ERROR"


class AIConfigurationError(AIClientError):
    code = "AI_CONFIG"


class AITimeoutError(AIClientError):
    code = "AI_TIMEOUT"


class AIUpstreamError(AIClientError):
    code = "AI_UPSTREAM"


@dataclass(frozen=True)
class AIResult:
    text: str
    latency_ms: int


class AIClient:
    """Small OpenAI-compatible Chat Completions adapter.

    The browser never receives AI credentials. The endpoint, model, and key are
    read on the server from environment-backed Settings.
    """

    def __init__(self, *, api_key: str, base_url: str, model: str, timeout_seconds: float):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    def complete(self, messages: list[dict[str, str]]) -> AIResult:
        if not self.api_key or not self.model:
            raise AIConfigurationError("AI_API_KEY와 AI_MODEL을 설정해 주세요.")

        started = time.perf_counter()
        try:
            response = httpx.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={"model": self.model, "messages": messages},
                timeout=self.timeout_seconds,
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise AITimeoutError("AI 응답 시간이 초과되었습니다.") from exc
        except httpx.HTTPError as exc:
            raise AIUpstreamError("AI API 호출에 실패했습니다.") from exc

        try:
            text = response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise AIUpstreamError("AI API 응답 형식을 해석하지 못했습니다.") from exc

        latency_ms = int((time.perf_counter() - started) * 1000)
        return AIResult(text=str(text).strip(), latency_ms=latency_ms)
