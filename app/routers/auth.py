from __future__ import annotations

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..auth import find_user_by_username, hash_password, verify_password
from ..db import get_db
from ..models import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _render(request: Request, template: str, **context):
    return templates.TemplateResponse(request=request, name=template, context=context)


@router.get("/signup")
def signup_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse("/chat", status_code=status.HTTP_303_SEE_OTHER)
    return _render(request, "signup.html", error=None)


@router.post("/signup")
def signup(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    username = username.strip()
    if len(username) < 3 or len(password) < 8:
        return _render(
            request,
            "signup.html",
            error="아이디는 3자 이상, 비밀번호는 8자 이상이어야 합니다.",
        )
    if find_user_by_username(db, username):
        return _render(request, "signup.html", error="이미 사용 중인 아이디입니다.")

    user = User(username=username, password_hash=hash_password(password))
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        return _render(request, "signup.html", error="이미 사용 중인 아이디입니다.")

    request.session["user_id"] = user.id
    return RedirectResponse("/chat", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/login")
def login_page(request: Request):
    if request.session.get("user_id"):
        return RedirectResponse("/chat", status_code=status.HTTP_303_SEE_OTHER)
    return _render(request, "login.html", error=None)


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = find_user_by_username(db, username.strip())
    if user is None or not verify_password(password, user.password_hash):
        return _render(request, "login.html", error="아이디 또는 비밀번호가 올바르지 않습니다.")
    request.session["user_id"] = user.id
    return RedirectResponse("/chat", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=status.HTTP_303_SEE_OTHER)
