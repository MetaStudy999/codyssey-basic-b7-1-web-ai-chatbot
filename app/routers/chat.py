from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..ai import AIClient
from ..auth import current_user_optional, require_user
from ..db import get_db
from ..models import ChatLog, User
from ..services import ask_ai

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_ai_client(request: Request) -> AIClient:
    return request.app.state.ai_client


def _chat_rows(db: Session, user_id: int) -> list[ChatLog]:
    return list(
        db.scalars(
            select(ChatLog)
            .where(ChatLog.user_id == user_id)
            .order_by(ChatLog.created_at.asc(), ChatLog.id.asc())
        )
    )


@router.get("/chat")
def chat_page(
    request: Request,
    db: Session = Depends(get_db),
    user: User | None = Depends(current_user_optional),
):
    if user is None:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={"user": user, "chats": _chat_rows(db, user.id), "error": None},
    )


@router.post("/chat")
def chat_submit(
    request: Request,
    question: str = Form(...),
    db: Session = Depends(get_db),
    user: User | None = Depends(current_user_optional),
    ai_client: AIClient = Depends(get_ai_client),
):
    if user is None:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

    question = question.strip()
    max_chars = request.app.state.settings.question_max_chars
    if not question or len(question) > max_chars:
        return templates.TemplateResponse(
            request=request,
            name="chat.html",
            context={
                "user": user,
                "chats": _chat_rows(db, user.id),
                "error": f"질문은 1~{max_chars}자 사이로 입력해 주세요.",
            },
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    ask_ai(
        db,
        user=user,
        question=question,
        ai_client=ai_client,
        context_turns=request.app.state.settings.context_turns,
    )
    return RedirectResponse("/chat", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/logs")
def logs_page(
    request: Request,
    db: Session = Depends(get_db),
    user: User | None = Depends(current_user_optional),
):
    if user is None:
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)
    rows = list(
        db.scalars(
            select(ChatLog)
            .where(ChatLog.user_id == user.id)
            .order_by(ChatLog.created_at.desc(), ChatLog.id.desc())
        )
    )
    return templates.TemplateResponse(
        request=request,
        name="logs.html",
        context={"user": user, "chats": rows},
    )


@router.get("/api/me/chats")
def my_chat_logs(
    user: User = Depends(require_user),
    db: Session = Depends(get_db),
):
    rows = list(
        db.scalars(
            select(ChatLog)
            .where(ChatLog.user_id == user.id)
            .order_by(ChatLog.created_at.desc(), ChatLog.id.desc())
        )
    )
    return JSONResponse(
        [
            {
                "id": row.id,
                "request_id": row.request_id,
                "created_at": row.created_at.isoformat(),
                "question": row.question,
                "answer": row.answer,
                "status": row.status,
                "error_code": row.error_code,
                "latency_ms": row.latency_ms,
            }
            for row in rows
        ]
    )
