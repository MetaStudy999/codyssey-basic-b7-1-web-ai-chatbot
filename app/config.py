from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    session_secret: str
    database_url: str = "sqlite:///./chatbot.db"
    ai_api_key: str = ""
    ai_base_url: str = "https://api.openai.com/v1"
    ai_model: str = ""
    ai_timeout_seconds: float = 20.0
    context_turns: int = 4
    question_max_chars: int = 2000
    session_cookie_secure: bool = False

    @classmethod
    def from_env(cls) -> "Settings":
        load_dotenv()
        secret = os.getenv("SESSION_SECRET", "").strip()
        if not secret:
            raise RuntimeError("SESSION_SECRET 환경 변수가 필요합니다.")

        return cls(
            session_secret=secret,
            database_url=os.getenv("DATABASE_URL", "sqlite:///./chatbot.db"),
            ai_api_key=os.getenv("AI_API_KEY", ""),
            ai_base_url=os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/"),
            ai_model=os.getenv("AI_MODEL", ""),
            ai_timeout_seconds=float(os.getenv("AI_TIMEOUT_SECONDS", "20")),
            context_turns=max(1, int(os.getenv("CONTEXT_TURNS", "4"))),
            question_max_chars=max(1, int(os.getenv("QUESTION_MAX_CHARS", "2000"))),
            session_cookie_secure=os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true",
        )
