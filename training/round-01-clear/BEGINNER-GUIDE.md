# B7-1 Round 01 — Beginner Guide

구분: **필수 Term Project (REQUIRED)**

> Phase A에서 완성한 Reference 기준 가이드입니다. 실제 AI API, 외부 배포, 팀 PR/커밋은 Phase C에서 수행합니다. 현재 저장소에는 별도 `b7-1-evaluation.md`가 없으므로 공식 검증 기준은 `b7-1-mission.pdf`와 `b7-1-mission.md`입니다.

## 프로젝트 한눈에 보기

로그인한 사용자가 웹에서 질문하면 FastAPI 서버가 서버 측에서 AI API를 호출하고, 응답을 화면에 보여 주며 사용자별 대화 로그를 SQLite에 저장합니다. Term Project이므로 실제 팀 협업 기록과 외부 배포까지 연결해야 합니다.

```text
Browser
  ↓ signup / login
FastAPI
  ↓ authenticated chat
AI API
  ↓ answer
FastAPI
  ↓ save
SQLite
  ↓
user-scoped logs
```

핵심은 **인증**, **서버 측 Secret 보호**, **사용자별 데이터 격리**, **Context 유지**, **실패 처리와 운영 로그**, **실제 협업·배포**입니다.

## STEP 01 — Local App / DB

① 왜 하는가: 인증·대화·로그가 저장될 기반이 필요합니다.  
② 무엇을 하는가: Python 가상환경, dependencies, SQLite schema, FastAPI 서버를 준비합니다.  
③ 이번 단계에서 알아야 할 용어: FastAPI, SQLite, 영속성 (Persistence).  
④ 필요한 핵심 개념: `users`, `sessions`, `conversations` 3개 테이블이 사용자·로그인 상태·대화를 연결합니다.  
⑤ 실행할 명령어:
```bash
cd training/round-01-clear/reference
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
⑥ 주석: 실제 AI API Key가 없어도 Home/Auth/Health 구조는 먼저 확인할 수 있습니다.  
⑦ 예상 정상 결과: 서버가 시작되고 `/health`가 정상 응답하며 DB가 생성됩니다.  
⑧ 의미: Web Server와 Database 기반이 준비되었습니다.  
⑨ 오류와 해결: import 오류는 가상환경/dependency, port 오류는 이미 사용 중인 프로세스를 확인합니다.  
⑩ 완료 확인: local server와 DB 구조를 설명할 수 있습니다.

## STEP 02 — Signup / Login / Logout

① 왜 하는가: 챗봇 기능과 대화 로그를 사용자별로 구분해야 합니다.  
② 무엇을 하는가: 회원가입, 로그인, 로그아웃, session cookie 흐름을 확인합니다.  
③ 용어: 인증 (Authentication), 세션 (Session), 비밀번호 해시 (Password Hash).  
④ 개념: 비밀번호는 PBKDF2 + salt로 저장하고, session token 원문 대신 DB에는 hash를 저장합니다.  
⑤ 실행: Browser에서 signup → login → logout을 순서대로 수행합니다.  
⑥ 주석: Plain password나 session token 원문을 DB/로그에 저장하지 않습니다.  
⑦ 정상 결과: 로그인 후 `/chat` 접근 가능, logout 후 보호 페이지 접근이 차단됩니다.  
⑧ 의미: 사용자 identity가 HTTP 요청과 연결되었습니다.  
⑨ 오류와 해결: 중복 계정, 잘못된 비밀번호, 만료/없는 session을 각각 확인합니다.  
⑩ 완료 확인: 인증 흐름을 사용자 관점과 서버 관점에서 설명할 수 있습니다.

## STEP 03 — Protected Chat / Input Validation

① 왜 하는가: 비로그인 사용자와 비정상 입력을 AI API 호출 전에 차단해야 합니다.  
② 무엇을 하는가: `/chat` 접근 제어와 질문 1~1000자 검증을 확인합니다.  
③ 용어: 접근 제어 (Access Control), 입력 검증 (Validation).  
④ 개념: 로그인 session user가 없으면 보호 기능을 사용할 수 없고, invalid input은 AI 비용이 발생하기 전에 종료합니다.  
⑤ 실행: 비로그인/로그인 상태에서 빈 질문, 정상 질문, 1000자 초과 질문을 각각 시도합니다.  
⑥ 주석: 외부에서 받은 `user_id`를 신뢰하지 않고 현재 session user를 기준으로 처리합니다.  
⑦ 정상 결과: invalid input은 오류 안내, 정상 입력만 AI 단계로 진행됩니다.  
⑧ 의미: 보안 경계와 비용 경계를 요청 초기에 적용했습니다.  
⑨ 오류와 해결: form field name, route, session dependency를 확인합니다.  
⑩ 완료 확인: 보호 route와 validation 이유를 설명할 수 있습니다.

## STEP 04 — AI API Server-side

① 왜 하는가: API Key를 Browser에 노출하지 않고 AI를 호출해야 합니다.  
② 무엇을 하는가: `AI_API_URL`, `AI_API_KEY`, `AI_MODEL`을 서버 환경변수로 설정합니다.  
③ 용어: 서버 측 API (Server-side API), 비밀정보 (Secret), Timeout.  
④ 개념: `Browser → FastAPI → AI API → FastAPI → Browser` 구조에서 Secret은 서버 경계 안에 둡니다.  
⑤ 실행할 명령어:
```bash
export AI_API_URL="<runtime-endpoint>"
export AI_API_KEY="<secret-local-only>"
export AI_MODEL="<runtime-model>"
```
⑥ 주석: 실제 값은 GitHub/채팅/Evidence에 기록하지 않습니다.  
⑦ 정상 결과: 로그인 사용자의 질문에 실제 AI 응답이 표시됩니다.  
⑧ 의미: Client에 Key를 노출하지 않고 AI 기능을 연결했습니다.  
⑨ 오류와 해결: 401/403, Network, Timeout, Provider 응답 형식을 구분합니다.  
⑩ 완료 확인: server-side 호출 이유와 Secret 관리 방법을 설명할 수 있습니다.

## STEP 05 — Context / DB Logs

① 왜 하는가: 직전 대화 맥락과 추적 가능한 기록이 필요합니다.  
② 무엇을 하는가: 같은 사용자 최근 대화 일부를 AI Context로 구성하고 질문/응답을 DB에 저장합니다.  
③ 용어: 문맥 창 (Context Window), 대화 로그 (Conversation Log).  
④ 개념: 최근 같은 사용자 Q/A만 사용하고, 전체 과거 기록을 무한히 전송하지 않습니다.  
⑤ 실행: 연결된 질문을 2~3번 하고 `/logs`에서 기록을 확인합니다.  
⑥ 주석: DB 조회는 현재 `user_id` 기준으로 제한합니다.  
⑦ 정상 결과: 사용자 식별, 생성 시각, 질문, 응답이 누적 저장됩니다.  
⑧ 의미: Context와 Persistence가 하나의 서비스 흐름으로 연결되었습니다.  
⑨ 오류와 해결: DB path, transaction, `WHERE user_id=?`, session user를 확인합니다.  
⑩ 완료 확인: 질문→AI→DB→로그 조회 흐름을 설명할 수 있습니다.

## STEP 06 — Two-user Isolation

① 왜 하는가: 다른 사용자의 대화가 섞이면 개인정보와 접근제어 문제가 됩니다.  
② 무엇을 하는가: A/B 두 계정으로 각각 대화와 로그를 생성합니다.  
③ 용어: 데이터 소유권 (Data Ownership), 격리 (Isolation).  
④ 개념: 사용자별 조회는 URL에서 받은 임의 user_id가 아니라 인증된 session user에 묶습니다.  
⑤ 실행: A 대화 → logout → B 대화 → 각 계정의 `/logs` 확인.  
⑥ 주석: 필요하면 SQLite에서 user_id별 row도 함께 확인합니다.  
⑦ 정상 결과: A 화면에 B 로그가 없고 B 화면에 A 로그가 없습니다.  
⑧ 의미: 사용자 기준 로그 추적과 데이터 격리가 동작합니다.  
⑨ 오류와 해결: Conversation query의 user filter를 점검합니다.  
⑩ 완료 확인: 두 사용자 격리 Evidence를 확보합니다.

## STEP 07 — Operational Logs / Failure

① 왜 하는가: AI/DB 장애가 발생했을 때 원인을 추적해야 합니다.  
② 무엇을 하는가: request, AI call, AI result/failure, DB save 이벤트와 실패 처리를 확인합니다.  
③ 용어: 운영 로그 (Operational Log), 예외 처리 (Exception Handling), 5xx.  
④ 개념: 외부 AI가 실패해도 FastAPI 프로세스 전체가 비정상 종료되면 안 됩니다.  
⑤ 실행: 정상 호출 후 안전한 AI Timeout/오류 scenario를 확인합니다.  
⑥ 주석: Key, Password, session token, 불필요한 민감 원문은 로그에 남기지 않습니다.  
⑦ 정상 결과: 서버 로그에는 핵심 event가 남고 사용자는 이해 가능한 오류 안내를 받습니다.  
⑧ 의미: 서비스가 운영·진단 가능한 상태입니다.  
⑨ 오류와 해결: raw exception에 Secret이 포함되는지 확인하고 sanitizing합니다.  
⑩ 완료 확인: 장애 후에도 서버가 계속 동작하고 로그로 원인을 설명할 수 있습니다.

## STEP 08 — Team / Deployment / CLEAR

① 왜 하는가: B7-1은 Term Project이므로 로컬 코드만으로 끝나지 않습니다.  
② 무엇을 하는가: 실제 branch/PR 협업, 팀원별 유의미한 commit 10회 이상, 외부 배포, 문서/Evidence를 완성합니다.  
③ 용어: 배포 (Deployment), Pull Request, 아키텍처 (Architecture).  
④ 개념: Reference commit은 실제 팀 기여 기록을 대신할 수 없습니다.  
⑤ 실행: 실제 팀 GitHub workflow와 선택한 Cloud/PaaS에서 배포합니다.  
⑥ 주석: 외부 URL에서 signup → login → chat → logs 전체 흐름을 다시 검증합니다.  
⑦ 정상 결과: 외부 URL, 실제 AI 응답, DB Persistence, 협업 기록이 서로 연결됩니다.  
⑧ 의미: Linux/Web/DB/AI API/협업 학습이 하나의 서비스로 통합되었습니다.  
⑨ 오류와 해결: deployment env, DB persistence, Secret 설정, platform log를 순서대로 확인합니다.  
⑩ 완료 확인: Mission 요구사항과 Evidence가 모두 연결된 뒤에만 `✅ CLEAR`입니다.

## CLEAR 전에 반드시 확인

- Signup/Login/Logout 실제 브라우저 동작
- 로그인 사용자만 Chat 사용 가능
- AI API Key가 Browser/Repository에 노출되지 않음
- 실제 AI 응답과 최근 대화 Context 유지
- 사용자별 Conversation DB 누적 및 조회
- 두 사용자 데이터 격리
- 요청/AI/DB 운영 로그
- AI Timeout/실패 시 서버 생존 + 사용자 오류 안내
- 실제 feature branch/PR merge 기록
- 팀원별 유의미한 commit 10회 이상
- 실제 외부 접속 URL
- README/Architecture/API/DB/Deployment/Team 문서
- Runtime Evidence와 자기 말 설명

Reference 구현이나 문서가 존재한다는 이유만으로 `✅ CLEAR`로 변경하지 않습니다.
