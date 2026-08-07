from __future__ import annotations

import logging
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from .ai import AIClient, AIClientError
from .models import ChatLog, User

logger = logging.getLogger("codyssey.chat")

SYSTEM_MESSAGE = (
    "당신은 간결하고 정확하게 답하는 학습용 AI 챗봇입니다. "
    "대화 기록은 현재 로그인 사용자의 최근 대화만 제공됩니다."
)


def recent_context(db: Session, user_id: int, turns: int) -> list[dict[str, str]]:
    rows = list(
        db.scalars(
            select(ChatLog)
            .where(ChatLog.user_id == user_id, ChatLog.status == "success")
            .order_by(ChatLog.created_at.desc(), ChatLog.id.desc())
            .limit(turns)
        )
    )
    rows.reverse()
    messages: list[dict[str, str]] = [{"role": "system", "content": SYSTEM_MESSAGE}]
    for row in rows:
        messages.append({"role": "user", "content": row.question})
        messages.append({"role": "assistant", "content": row.answer})
    return messages


def save_chat_log(
    db: Session,
    *,
    user: User,
    request_id: str,
    question: str,
    answer: str,
    status: str,
    error_code: str | None,
    latency_ms: int | None,
) -> ChatLog:
    row = ChatLog(
        user_id=user.id,
        request_id=request_id,
        question=question,
        answer=answer,
        status=status,
        error_code=error_code,
        latency_ms=latency_ms,
    )
    db.add(row)
    try:
        db.commit()
        db.refresh(row)
        logger.info("db_save_success user_id=%s request_id=%s chat_id=%s", user.id, request_id, row.id)
    except Exception:
        db.rollback()
        logger.exception("db_save_failure user_id=%s request_id=%s", user.id, request_id)
        raise
    return row


def ask_ai(
    db: Session,
    *,
    user: User,
    question: str,
    ai_client: AIClient,
    context_turns: int,
) -> ChatLog:
    request_id = uuid.uuid4().hex
    logger.info("request_received user_id=%s request_id=%s path=/chat", user.id, request_id)

    messages = recent_context(db, user.id, context_turns)
    messages.append({"role": "user", "content": question})

    logger.info("ai_call_start user_id=%s request_id=%s", user.id, request_id)
    try:
        result = ai_client.complete(messages)
        logger.info(
            "ai_call_success user_id=%s request_id=%s latency_ms=%s",
            user.id,
            request_id,
            result.latency_ms,
        )
        return save_chat_log(
            db,
            user=user,
            request_id=request_id,
            question=question,
            answer=result.text,
            status="success",
            error_code=None,
            latency_ms=result.latency_ms,
        )
    except AIClientError as exc:
        logger.warning(
            "ai_call_failure user_id=%s request_id=%s error_code=%s",
            user.id,
            request_id,
            exc.code,
        )
        message = "AI 응답을 받지 못했습니다. 잠시 후 다시 시도해 주세요."
        if exc.code == "AI_TIMEOUT":
            message = "현재 응답이 지연되고 있어요. 잠시 후 다시 시도해 주세요."
        return save_chat_log(
            db,
            user=user,
            request_id=request_id,
            question=question,
            answer=message,
            status="error",
            error_code=exc.code,
            latency_ms=None,
        )
