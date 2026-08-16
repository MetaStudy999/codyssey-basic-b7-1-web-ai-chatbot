# B7-1 R01 — Reference Build

## 목적

공식 Mission을 기준으로 **회원가입/로그인 → 로그인 사용자만 AI 질문 → 서버 AI API 호출 → 사용자별 대화 로그 DB 저장/조회 → 외부 배포** 흐름을 가진 FastAPI 웹 챗봇 Reference Complete Version을 준비합니다.

Phase A에서는 실제 AI API Key, 외부 배포 URL, 실제 팀 PR/팀원별 10+ commits, 실제 DB/Cloud Evidence를 만들었다고 간주하지 않습니다.

## Source of Truth

1. `b7-1-mission.pdf`
2. `b7-1-mission.md`

> 현재 저장소에는 별도 `b7-1-evaluation.md`가 없습니다. 따라서 Mission의 기능 요구사항·제약사항·최종 결과물·설명 목표를 검증 기준으로 사용합니다. `docs/evaluation-qa.md`는 공식 평가문항이 아니라 Mission 기반 설명 연습 자료입니다.

## Reference 설계

- FastAPI + Jinja2 SSR
- SQLite
- 회원가입/로그인/로그아웃
- Password: PBKDF2-HMAC-SHA256 + random salt
- Session: random token은 cookie에 전달하고 DB에는 hash 저장
- Chat/Logs route: 로그인 필수
- Input: 빈 입력 차단 + 1000자 제한
- AI API: server-side only, `AI_API_KEY`/`AI_API_URL`/`AI_MODEL` env
- Context: 같은 사용자 최근 대화 일부
- Conversation log: user_id, created_at, question, answer
- 사용자 기준 로그 조회
- Operational logging: request / AI call / AI response or fail / DB save result
- API failure/timeout은 server crash 없이 사용자 오류로 반환
- 협업: branch/PR + 팀원별 유의미한 commit 10회 이상은 실제 Runtime에서 증빙
- 배포: 외부 URL은 실제 Runtime에서 증빙

## Reference Complete Path

1. app/env/db 준비
2. signup/login/logout
3. protected chat + validation
4. server-side AI client
5. recent same-user context
6. conversation persistence
7. user-scoped log view
8. error/input validation/operational logging
9. local offline verify
10. two-user isolation Runtime
11. team collaboration Runtime
12. external deployment Runtime
13. docs/Evidence package
14. CLEAR

## Phase A 판정

**Reference Build: CORE READY / Mission 상태 ⬜ NOT STARTED / 실제 AI·배포·팀 Runtime 미시작 / CLEAR 아님**
