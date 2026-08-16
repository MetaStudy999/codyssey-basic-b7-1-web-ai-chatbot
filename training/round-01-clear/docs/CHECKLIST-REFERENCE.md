# B7-1 R01 — Reference / Runtime Checklist

## 현재
- Mission 상태: ⬜ NOT STARTED
- Phase A: REFERENCE BUILD

## Source
- [x] Mission PDF/MD
- [x] Evaluation
- [x] Runtime/협업/배포 분리

## Web/Auth
- [x] Home
- [x] Signup
- [x] Login
- [x] Logout
- [x] protected `/chat`
- [x] protected `/logs`
- [x] salted PBKDF2 password hash
- [x] random session token + DB token hash
- [ ] 실제 browser auth flow

## AI Chat
- [x] server-side AI client
- [x] env-only API URL/Key/Model
- [x] same-user recent 6 Q/A context
- [x] 1~1000 char validation
- [x] safe 502 on AI failure
- [ ] 실제 API call
- [ ] context continuity Runtime

## DB / Logs
- [x] users/sessions/conversations schema
- [x] user_id/time/question/answer
- [x] user-scoped history/log query
- [x] request/AI/DB operation logs
- [ ] two-user isolation Runtime
- [ ] actual DB rows Evidence
- [ ] actual platform/server logs

## Docs
- [x] Architecture source
- [x] Route/API spec
- [x] DB schema/check guide
- [x] Deployment/env guide
- [x] Team runtime template
- [x] Requirements mapping
- [x] Evaluation Q&A
- [x] Evidence Guide
- [x] Beginner Reference Guide
- [x] Environment/verify

## Collaboration
- [x] branch/PR reference plan
- [ ] actual feature branches
- [ ] actual PR merges
- [ ] team member 10+ meaningful commits each
- [ ] actual role/work summary

## Deployment
- [ ] actual external URL
- [ ] signup/login/chat/logs externally
- [ ] AI failure externally
- [ ] DB persistence externally
- [ ] Secret browser exposure 없음

## Verify / Evidence
- [ ] offline verify 0 FAIL
- [ ] auth Evidence
- [ ] chat/context Evidence
- [ ] two-user isolation
- [ ] error/input validation
- [ ] operational logs
- [ ] collaboration links
- [ ] external deployment
- [ ] docs package

## CLEAR
- [ ] Mission/Evaluation 누락 없음
- [ ] actual AI Runtime
- [ ] actual team Runtime
- [ ] actual external deployment
- [ ] Evidence 완료
- [ ] 설명형 평가 가능
- [ ] **✅ B7-1 CLEAR**
