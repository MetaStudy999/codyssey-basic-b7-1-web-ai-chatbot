from __future__ import annotations

import hashlib
import hmac
import secrets
from dataclasses import dataclass

from fastapi import Request

from .db import db_connection

SESSION_COOKIE = "b7_session"
PBKDF2_ITERATIONS = 210_000


@dataclass(slots=True)
class User:
    id: int
    username: str


def hash_password(password: str, salt_hex: str | None = None) -> tuple[str, str]:
    salt = bytes.fromhex(salt_hex) if salt_hex else secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return digest.hex(), salt.hex()


def verify_password(password: str, expected_hash: str, salt_hex: str) -> bool:
    actual_hash, _ = hash_password(password, salt_hex)
    return hmac.compare_digest(actual_hash, expected_hash)


def create_user(username: str, password: str) -> User:
    password_hash, salt = hash_password(password)
    with db_connection() as connection:
        cursor = connection.execute(
            "INSERT INTO users(username, password_hash, password_salt) VALUES (?, ?, ?)",
            (username, password_hash, salt),
        )
        return User(id=int(cursor.lastrowid), username=username)


def authenticate(username: str, password: str) -> User | None:
    with db_connection() as connection:
        row = connection.execute(
            "SELECT id, username, password_hash, password_salt FROM users WHERE username = ?",
            (username,),
        ).fetchone()
    if row is None or not verify_password(password, row["password_hash"], row["password_salt"]):
        return None
    return User(id=row["id"], username=row["username"])


def new_session(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with db_connection() as connection:
        connection.execute("INSERT INTO sessions(user_id, token_hash) VALUES (?, ?)", (user_id, token_hash))
    return token


def delete_session(token: str | None) -> None:
    if not token:
        return
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with db_connection() as connection:
        connection.execute("DELETE FROM sessions WHERE token_hash = ?", (token_hash,))


def current_user(request: Request) -> User | None:
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()
    with db_connection() as connection:
        row = connection.execute(
            """SELECT u.id, u.username
               FROM sessions AS s
               JOIN users AS u ON u.id = s.user_id
               WHERE s.token_hash = ?""",
            (token_hash,),
        ).fetchone()
    if row is None:
        return None
    return User(id=row["id"], username=row["username"])
