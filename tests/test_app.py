from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from app.ai import AIResult, AITimeoutError
from app.config import Settings
from app.main import create_app


class RecordingAI:
    def __init__(self, answer: str = "테스트 응답"):
        self.answer = answer
        self.calls: list[list[dict[str, str]]] = []

    def complete(self, messages):
        self.calls.append(messages)
        return AIResult(self.answer, 12)


class TimeoutAI:
    def complete(self, messages):
        raise AITimeoutError("timeout")


def make_client(tmp_path: Path, ai=None) -> TestClient:
    settings = Settings(
        session_secret="test-secret-that-is-long-enough",
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        ai_api_key="server-only-key",
        ai_model="test-model",
        context_turns=2,
        question_max_chars=40,
    )
    app = create_app(settings=settings, ai_client=ai or RecordingAI())
    return TestClient(app)


def signup(client: TestClient, username: str):
    return client.post(
        "/signup",
        data={"username": username, "password": "password123"},
        follow_redirects=False,
    )


def test_auth_protects_chat_and_allows_signup(tmp_path):
    with make_client(tmp_path) as client:
        response = client.get("/chat", follow_redirects=False)
        assert response.status_code == 303
        assert response.headers["location"] == "/login"

        response = signup(client, "alice")
        assert response.status_code == 303
        assert response.headers["location"] == "/chat"
        assert client.get("/chat").status_code == 200


def test_question_validation_blocks_empty_and_too_long_input(tmp_path):
    ai = RecordingAI()
    with make_client(tmp_path, ai) as client:
        signup(client, "alice")
        response = client.post("/chat", data={"question": "   "})
        assert response.status_code == 422
        response = client.post("/chat", data={"question": "x" * 41})
        assert response.status_code == 422
        assert ai.calls == []


def test_chat_response_is_persisted_and_visible_in_user_logs(tmp_path):
    ai = RecordingAI("안녕하세요")
    with make_client(tmp_path, ai) as client:
        signup(client, "alice")
        response = client.post("/chat", data={"question": "첫 질문"}, follow_redirects=False)
        assert response.status_code == 303

        html = client.get("/chat").text
        assert "첫 질문" in html
        assert "안녕하세요" in html
        assert "server-only-key" not in html

        logs = client.get("/api/me/chats")
        assert logs.status_code == 200
        data = logs.json()
        assert len(data) == 1
        assert data[0]["question"] == "첫 질문"
        assert data[0]["status"] == "success"
        assert data[0]["request_id"]


def test_context_is_bounded_and_isolated_by_user(tmp_path):
    ai = RecordingAI()
    with make_client(tmp_path, ai) as alice:
        signup(alice, "alice")
        alice.post("/chat", data={"question": "A1"})
        alice.post("/chat", data={"question": "A2"})
        alice.post("/chat", data={"question": "A3"})
        alice.post("/chat", data={"question": "A4"})
        last_messages = ai.calls[-1]
        joined = " ".join(message["content"] for message in last_messages)
        assert "A1" not in joined
        assert "A2" in joined
        assert "A3" in joined
        assert "A4" in joined

    ai2 = RecordingAI()
    with make_client(tmp_path, ai2) as bob:
        signup(bob, "bob")
        bob.post("/chat", data={"question": "B1"})
        joined = " ".join(message["content"] for message in ai2.calls[-1])
        assert "A2" not in joined
        assert "A3" not in joined
        assert "B1" in joined


def test_timeout_returns_user_message_and_persists_error_log(tmp_path):
    with make_client(tmp_path, TimeoutAI()) as client:
        signup(client, "alice")
        response = client.post("/chat", data={"question": "느린 질문"}, follow_redirects=False)
        assert response.status_code == 303

        html = client.get("/chat").text
        assert "현재 응답이 지연되고 있어요" in html
        assert "AI_TIMEOUT" in html

        data = client.get("/api/me/chats").json()
        assert data[0]["status"] == "error"
        assert data[0]["error_code"] == "AI_TIMEOUT"


def test_api_logs_require_authentication(tmp_path):
    with make_client(tmp_path) as client:
        response = client.get("/api/me/chats")
        assert response.status_code == 401
