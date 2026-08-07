# 시스템 아키텍처

```text
Browser
  │  signup/login/chat/logs
  ▼
FastAPI
  ├─ Session auth (server-signed cookie)
  ├─ Chat route + input validation
  ├─ Context builder (current user, recent N successful turns)
  ├─ AI adapter ──HTTPS──> OpenAI-compatible AI API
  └─ SQLAlchemy ────────> SQLite
                          ├─ users
                          └─ chat_logs
```

## 주요 컴포넌트

- `app/routers/auth.py`: 회원가입, 로그인, 로그아웃.
- `app/routers/chat.py`: 보호된 챗봇/로그 화면과 `GET /api/me/chats`.
- `app/services.py`: `question → context → AI → persistence` 비즈니스 흐름과 추적 로그.
- `app/ai.py`: 서버에서만 API key를 사용하며 timeout과 upstream 오류를 분류.
- `app/models.py`: 사용자와 대화 로그 ORM 모델.
- `app/templates/`: Jinja2 웹 UI.

## 추적성

모든 질문에는 `request_id`를 생성한다. 서버 로그의 `request_received`, `ai_call_*`, `db_save_*` 이벤트와 DB의 `chat_logs.request_id`를 같은 값으로 연결한다. DB 행에는 `user_id`도 저장하므로 사용자→요청→AI 호출→저장 결과를 추적할 수 있다.

## Context 경계

AI 입력에 넣는 이전 대화는 현재 로그인 사용자의 `status=success` 로그 중 최근 `CONTEXT_TURNS`개뿐이다. 사용자 간 context가 섞이지 않으며 길이가 무한히 증가하지 않는다.
