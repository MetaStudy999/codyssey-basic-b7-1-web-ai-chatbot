# API / Route 명세

| Method | Path | Auth | 용도 | 주요 응답 |
|---|---|---|---|---|
| GET | `/` | Public | 서비스 소개 | HTML 200 |
| GET | `/health` | Public | 배포 health check | `{"status":"ok"}` |
| GET/POST | `/signup` | Public | 회원가입 | HTML / 303 |
| GET/POST | `/login` | Public | 로그인 | HTML / 303 |
| POST | `/logout` | Login | 로그아웃 | 303 |
| GET | `/chat` | Login | 챗봇 화면 | HTML 200 / login redirect |
| POST | `/chat` | Login | 질문→AI→로그 저장 | 303, validation 422 |
| GET | `/logs` | Login | 현재 사용자 로그 화면 | HTML 200 |
| GET | `/api/me/chats` | Login | 현재 사용자 로그 JSON 조회 | JSON 200 / 401 |

## 예시: 내 로그 조회

```http
GET /api/me/chats
Cookie: session=<signed-session-cookie>
```

```json
[
  {
    "id": 1,
    "request_id": "9e2f...",
    "created_at": "2026-08-08T00:00:00+00:00",
    "question": "배포 방법을 알려줘",
    "answer": "...",
    "status": "success",
    "error_code": null,
    "latency_ms": 842
  }
]
```

`/api/me/chats`는 로그인 세션의 사용자 ID를 기준으로 필터링한다. 다른 사용자의 로그를 지정하는 URL 파라미터를 제공하지 않는다.
