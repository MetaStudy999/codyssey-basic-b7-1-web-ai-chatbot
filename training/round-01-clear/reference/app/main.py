from __future__ import annotations

import logging
import sqlite3
from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from .ai_client import AIClient, AIServiceError
from .auth import SESSION_COOKIE, authenticate, create_user, current_user, delete_session, new_session
from .db import db_connection, init_db

BASE_DIR = Path(__file__).resolve().parents[1]
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("b7-chatbot")

app = FastAPI(title="Codyssey B7-1 Reference Chatbot")


@app.on_event("startup")
def startup() -> None:
    init_db()


def _recent_history(user_id: int, limit: int = 6) -> list[tuple[str, str]]:
    with db_connection() as connection:
        rows = connection.execute(
            """SELECT question, answer
               FROM conversations
               WHERE user_id = ?
               ORDER BY created_at DESC, id DESC
               LIMIT ?""",
            (user_id, limit),
        ).fetchall()
    rows = list(reversed(rows))
    return [(row["question"], row["answer"]) for row in rows]


def _save_conversation(user_id: int, question: str, answer: str) -> None:
    with db_connection() as connection:
        connection.execute(
            "INSERT INTO conversations(user_id, question, answer) VALUES (?, ?, ?)",
            (user_id, question, answer),
        )


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    user = current_user(request)
    return templates.TemplateResponse(request=request, name="home.html", context={"user": user})


@app.get("/signup", response_class=HTMLResponse)
def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html", context={"error": None})


@app.post("/signup")
def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    username = username.strip()
    if len(username) < 3 or len(password) < 8:
        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={"error": "아이디는 3자 이상, 비밀번호는 8자 이상이어야 합니다."},
            status_code=400,
        )
    try:
        user = create_user(username, password)
    except sqlite3.IntegrityError:
        return templates.TemplateResponse(
            request=request,
            name="signup.html",
            context={"error": "이미 사용 중인 아이디입니다."},
            status_code=409,
        )

    token = new_session(user.id)
    response = RedirectResponse(url="/chat", status_code=303)
    response.set_cookie(SESSION_COOKIE, token, httponly=True, samesite="lax", secure=False)
    return response


@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"error": None})


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    user = authenticate(username.strip(), password)
    if user is None:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"error": "아이디 또는 비밀번호가 올바르지 않습니다."},
            status_code=401,
        )
    token = new_session(user.id)
    response = RedirectResponse(url="/chat", status_code=303)
    response.set_cookie(SESSION_COOKIE, token, httponly=True, samesite="lax", secure=False)
    return response


@app.post("/logout")
def logout(request: Request):
    delete_session(request.cookies.get(SESSION_COOKIE))
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(SESSION_COOKIE)
    return response


@app.get("/chat", response_class=HTMLResponse)
def chat_page(request: Request):
    user = current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    history = _recent_history(user.id, limit=10)
    return templates.TemplateResponse(
        request=request,
        name="chat.html",
        context={"user": user, "history": history, "error": None},
    )


@app.post("/chat", response_class=HTMLResponse)
def chat(request: Request, question: str = Form(...)):
    user = current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)

    text = question.strip()
    if not text or len(text) > 1000:
        return templates.TemplateResponse(
            request=request,
            name="chat.html",
            context={
                "user": user,
                "history": _recent_history(user.id, limit=10),
                "error": "질문은 1~1000자로 입력해 주세요.",
            },
            status_code=400,
        )

    logger.info("request_received user_id=%s question_length=%s", user.id, len(text))
    context = _recent_history(user.id, limit=6)
    client = AIClient()

    try:
        logger.info("ai_call user_id=%s context_pairs=%s", user.id, len(context))
        answer = client.answer(text, context)
        logger.info("ai_response_received user_id=%s answer_length=%s", user.id, len(answer))
    except AIServiceError as exc:
        logger.error("ai_call_failed user_id=%s error=%s", user.id, exc)
        return templates.TemplateResponse(
            request=request,
            name="chat.html",
            context={"user": user, "history": _recent_history(user.id, limit=10), "error": "AI 응답 생성 중 오류가 발생했습니다."},
            status_code=502,
        )

    try:
        _save_conversation(user.id, text, answer)
        logger.info("db_save_success user_id=%s", user.id)
    except Exception:
        logger.exception("db_save_failed user_id=%s", user.id)
        return templates.TemplateResponse(
            request=request,
            name="chat.html",
            context={"user": user, "history": _recent_history(user.id, limit=10), "error": "대화 저장 중 오류가 발생했습니다."},
            status_code=500,
        )

    return RedirectResponse(url="/chat", status_code=303)


@app.get("/logs", response_class=HTMLResponse)
def logs_page(request: Request):
    user = current_user(request)
    if user is None:
        return RedirectResponse(url="/login", status_code=303)
    with db_connection() as connection:
        rows = connection.execute(
            """SELECT id, created_at, question, answer
               FROM conversations
               WHERE user_id = ?
               ORDER BY created_at DESC, id DESC""",
            (user.id,),
        ).fetchall()
    return templates.TemplateResponse(
        request=request,
        name="logs.html",
        context={"user": user, "rows": rows},
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
