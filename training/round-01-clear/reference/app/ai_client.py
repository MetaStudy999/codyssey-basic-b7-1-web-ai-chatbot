from __future__ import annotations

import json
import os
import urllib.error
import urllib.request


class AIServiceError(Exception):
    pass


class AIClient:
    def __init__(self) -> None:
        self.api_url = os.environ.get("AI_API_URL", "").strip()
        self.api_key = os.environ.get("AI_API_KEY", "").strip()
        self.model = os.environ.get("AI_MODEL", "runtime-model").strip()

    def _check_runtime(self) -> None:
        if not self.api_url:
            raise AIServiceError("AI_API_URL 환경변수가 필요합니다.")
        if not self.api_key:
            raise AIServiceError("AI_API_KEY 환경변수가 필요합니다.")

    def answer(self, question: str, history: list[tuple[str, str]]) -> str:
        self._check_runtime()
        messages: list[dict[str, str]] = [
            {
                "role": "system",
                "content": "You are a concise helpful chatbot. Answer the current user using the recent conversation only when relevant.",
            }
        ]
        for prior_question, prior_answer in history:
            messages.append({"role": "user", "content": prior_question})
            messages.append({"role": "assistant", "content": prior_answer})
        messages.append({"role": "user", "content": question})

        payload = {"model": self.model, "messages": messages}
        request = urllib.request.Request(
            self.api_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": "Bearer {}".format(self.api_key),
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise AIServiceError("AI API HTTP 오류 {}".format(exc.code)) from exc
        except urllib.error.URLError as exc:
            raise AIServiceError("AI API 네트워크 오류: {}".format(exc.reason)) from exc
        except TimeoutError as exc:
            raise AIServiceError("AI API timeout") from exc

        try:
            data = json.loads(body)
            if isinstance(data.get("output_text"), str):
                return data["output_text"].strip()
            content = data["choices"][0]["message"]["content"]
        except (json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise AIServiceError("AI API 응답 형식을 해석할 수 없습니다.") from exc

        if not isinstance(content, str) or not content.strip():
            raise AIServiceError("AI API가 빈 응답을 반환했습니다.")
        return content.strip()
