# B7-1 R01 — Reference Build

## 목적

공식 Mission/Evaluation을 기준으로 **회원가입/로그인 → 로그인 사용자만 AI 질문 → 서버 AI API 호출 → 사용자별 대화 로그 DB 저장/조회 → 외부 배포** 흐름을 가진 FastAPI 웹 챗봇 Reference Complete Version을 준비합니다.

Phase A에서는 실제 AI API Key, 외부 배포 URL, 실제 팀 PR/10+ commits, 실제 DB/Cloud Evidence를 만들었다고 간주하지 않습니다.

## Source of Truth

1. `b7-1-mission.pdf`
2. `b7-1-mission.md`
3. `b7-1-evaluation.md`

## Reference 설계

- FastAPI + Jinja2 SSR
- SQLite
- 회원가입/로그인/로그아웃
- Password: PBKDF2-HMAC-SHA256 + random salt
- Session: random token은 cookie에만 전달, DB에는 SHA-256 hash 저장
- Chat route: 로그인 필수
- Input: 빈 입력 차단 + 1000자 제한
- AI API: server-side only, `AI_API_KEY`/`AI_API_URL`/`AI_MODEL` env
- Context: 같은 사용자 최근 6개 Q/A
- Conversation log: user_id, created_at, question, answer
- 내 로그 조회 화면
- Operational logging: request / AI call / AI response or fail / DB save result
- API failure/timeout은 server crash 없이 사용자 오류로 반환
- Docs: overview, architecture, API, DB, deploy/env, team roles, DB verification

## Reference Complete Path

1. app/env/db 준비
2. signup/login/logout
3. protected chat
4. server-side AI client
5. recent context
6. conversation persistence
7. user-scoped log view
8. error/input validation/logging
9. local verify/tests
10. team collaboration Runtime
11. cloud deployment Runtime
12. external acceptance
13. docs/Evidence
14. CLEAR

## 현재 판정

**Reference Build 진행 중 / Mission 상태 ⬜ NOT STARTED / 실제 AI·배포·팀 Runtime 미시작**
