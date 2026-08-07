# DB 구조 및 확인 가이드

## ERD

```text
users (1) ─────────< (N) chat_logs

users
- id PK
- username UNIQUE
- password_hash
- created_at

chat_logs
- id PK
- user_id FK -> users.id
- request_id UNIQUE
- created_at
- question
- answer
- status
- error_code nullable
- latency_ms nullable
```

## 평가자 확인 방법

기본 SQLite 경로는 `./chatbot.db`다. 서비스에서 1회 이상 대화한 뒤:

```bash
sqlite3 chatbot.db < scripts/check_logs.sql
```

또는 로그인 상태에서:

```text
GET /api/me/chats
```

두 방법 모두 질문, 응답, 생성 시각, 사용자 연결, `request_id` 추적 정보를 확인할 수 있다.
