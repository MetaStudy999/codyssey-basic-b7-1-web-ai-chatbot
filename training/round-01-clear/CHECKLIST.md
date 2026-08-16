# B7-1 Round 01 — Project Clear Checklist

## 현재 상태

- Reference Build: **CORE READY**
- Runtime Mission: ⬜ NOT STARTED
- 별도 `b7-1-evaluation.md`: **없음** — 공식 Mission 요구사항을 검증 기준으로 사용

## Source / Learn

- [x] `b7-1-mission.pdf` 확인
- [x] `b7-1-mission.md` 확인
- [x] 기능/협업/배포/Runtime 요구사항 분리
- [x] 인증/AI/DB/로그/배포 핵심 개념 준비
- [x] 상세 canonical Beginner Guide 준비

## Web / Auth

- [x] Home
- [x] Signup
- [x] Login
- [x] Logout
- [x] protected `/chat`
- [x] protected `/logs`
- [x] PBKDF2 salted password hash
- [x] random session token + DB token hash
- [ ] 실제 Browser auth flow

## AI Chat

- [x] server-side AI client
- [x] env-only API URL/Key/Model
- [x] same-user recent context
- [x] 1~1000자 input validation
- [x] AI failure/timeout safe handling
- [ ] 실제 AI API call
- [ ] 실제 context continuity

## DB / Logs

- [x] users/sessions/conversations schema
- [x] user_id / created_at / question / answer
- [x] user-scoped history/log query
- [x] request/AI/DB operational logging
- [ ] two-user isolation Runtime
- [ ] 실제 DB row Evidence
- [ ] 실제 server/platform log Evidence

## Docs

- [x] Architecture source
- [x] API spec
- [x] DB schema/verification guide
- [x] Deployment/env guide
- [x] Team Runtime template
- [x] Requirements Mapping
- [x] Mission-based Q&A Reference
- [x] Evidence Guide
- [x] Environment/offline verify
- [x] canonical Beginner Guide / Checklist

## Collaboration

- [x] branch/PR reference plan
- [ ] actual feature branches
- [ ] actual PR merges
- [ ] 팀원별 유의미한 commit 10회 이상
- [ ] 실제 역할/개인별 작업 요약과 Git 이력 일치

## Deployment

- [ ] 실제 외부 접속 URL
- [ ] 외부에서 signup/login/chat/logs 확인
- [ ] 실제 AI failure path 확인
- [ ] DB persistence 확인
- [ ] Browser/Repository에 Secret 노출 없음

## Verify / Evidence

- [ ] offline `verify.sh` 실제 0 FAIL
- [ ] auth Evidence
- [ ] chat/context Evidence
- [ ] two-user isolation Evidence
- [ ] error/input validation Evidence
- [ ] operational log Evidence
- [ ] collaboration links
- [ ] external deployment Evidence
- [ ] docs package 최종 확인

## CLEAR Gate

- [ ] 공식 Mission 필수 요구사항 누락 없음
- [ ] actual AI Runtime
- [ ] actual team Runtime
- [ ] actual external deployment
- [ ] Evidence 완료
- [ ] 사용자가 인증→AI→DB→로그→배포 흐름을 자기 말로 설명
- [ ] Secret 노출 없음
- [ ] **✅ B7-1 CLEAR**

Reference 구현이나 문서가 존재한다는 이유만으로 CLEAR하지 않습니다.
