# B7-1 Reference API / Route Spec

> B7-1 Reference는 Jinja2 SSR 중심 웹 서비스입니다. HTML form route도 API처럼 method/path/input/output을 명확히 기록합니다.

| Method | Path | Auth | Input | Success | Failure |
|---|---|---|---|---|---|
| GET | `/` | Public | - | Home HTML | - |
| GET | `/signup` | Public | - | Signup HTML | - |
| POST | `/signup` | Public | `username`, `password` form | 303 `/chat` + session cookie | 400 validation / 409 duplicate |
| GET | `/login` | Public | - | Login HTML | - |
| POST | `/login` | Public | `username`, `password` form | 303 `/chat` + session cookie | 401 invalid credentials |
| POST | `/logout` | Session | cookie | 303 `/` + cookie delete | - |
| GET | `/chat` | Session required | - | Chat HTML + recent history | 303 `/login` |
| POST | `/chat` | Session required | `question` form | AI call → DB save → 303 `/chat` | 400 input / 502 AI / 500 DB |
| GET | `/logs` | Session required | - | Current user's logs HTML | 303 `/login` |
| GET | `/health` | Public | - | `{"status":"ok"}` | - |

## Chat Pipeline

```text
POST /chat
→ session user 확인
→ question 1~1000자 검증
→ same user 최근 6 Q/A 조회
→ server-side AI API 호출
→ answer 수신
→ conversations 저장
→ redirect GET /chat
```

AI API Key는 Browser/HTML/JavaScript에 전달하지 않습니다.
