# B7-1 R01 — Reference Status

## 판정

**Reference Build: CORE READY**  
**Runtime Mission: ⬜ NOT STARTED**  
**Runtime CLEAR: 아님**

## 공식 Source

- `b7-1-mission.pdf`
- `b7-1-mission.md`
- 별도 공식 Evaluation 파일 없음

`docs/evaluation-qa.md`는 Mission 요구사항을 바탕으로 만든 설명 연습 자료이며 공식 평가 원본으로 취급하지 않습니다.

## Phase A 준비 결과

- [x] Mission 요구사항 분석
- [x] FastAPI/Jinja2/SQLite Reference architecture
- [x] users/sessions/conversations DB schema
- [x] signup/login/logout
- [x] protected chat/log routes
- [x] PBKDF2 password hashing
- [x] hashed session token storage
- [x] server-side AI client/env Secret
- [x] recent same-user context
- [x] input validation
- [x] AI failure/timeout handling
- [x] conversation persistence
- [x] user-scoped logs
- [x] request/AI/DB operational logging
- [x] Architecture/API/DB/Deployment docs
- [x] Team collaboration Runtime template
- [x] Requirements Mapping / Q&A / Evidence Guide
- [x] Environment/offline verify
- [x] canonical `BEGINNER-GUIDE.md`
- [x] canonical `CHECKLIST.md`
- [x] Reference/Runtime 구분

## Phase C에서만 완료

- [ ] 실제 local browser flow
- [ ] 실제 AI API Key/endpoint/model
- [ ] 실제 AI answer/context
- [ ] two-user isolation
- [ ] actual server logs
- [ ] actual team feature branches/PR/10+ meaningful commits each
- [ ] actual external deployment URL
- [ ] docs/Evidence package final
- [ ] `✅ B7-1 CLEAR`

## Canonical Audit

기존 scaffold `BEGINNER-GUIDE.md`와 `CHECKLIST.md`를 상세 Reference 가이드와 동기화했고, 존재하지 않는 `b7-1-evaluation.md` 참조를 제거했습니다.
