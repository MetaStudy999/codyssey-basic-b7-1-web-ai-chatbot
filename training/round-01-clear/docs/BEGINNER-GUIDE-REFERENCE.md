# B7-1 Round 01 — Beginner Guide Reference

> Phase A Reference입니다. 실제 AI API/배포/팀 협업은 Phase C에서 수행합니다.

## STEP 01 — Local App / DB
① 왜: 인증·대화·로그가 저장될 기반이 필요합니다.  
② 무엇: venv, dependencies, SQLite schema.  
③ 용어: FastAPI, SQLite, Persistence.  
④ 개념: users/sessions/conversations 3 table.  
⑤ 명령:
```bash
cd training/round-01-clear/reference
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
⑥ 주석: 실제 API Key는 아직 넣지 않아도 Home/Auth까지 확인할 수 있습니다.  
⑦ 정상: `/health` 정상, DB 생성.  
⑧ 의미: Server/DB 기반이 준비됨.  
⑨ 오류: import/dependency/port 확인.  
⑩ 완료: local server + DB.

## STEP 02 — Signup/Login/Logout
① 왜: 챗봇을 사용자별로 분리합니다.  
② 무엇: 계정 생성과 session cookie.  
③ 용어: Authentication, Session, Password Hash.  
④ 개념: PBKDF2 salted password + random session token hash.  
⑤ 실행: Browser에서 signup/login/logout.  
⑥ 주석: Plain password/session token을 DB에 그대로 저장하지 않습니다.  
⑦ 정상: 로그인 후 `/chat`, logout 후 보호 페이지 차단.  
⑧ 의미: 사용자 identity가 요청에 연결됨.  
⑨ 오류: duplicate/invalid password는 명확한 오류.  
⑩ 완료: auth flow.

## STEP 03 — Protected Chat / Input Validation
① 왜: 비로그인 사용자와 비정상 입력을 AI API 전에 차단합니다.  
② 무엇: `/chat` 접근과 1~1000자 검증.  
③ 용어: Authorization/Access Control, Validation.  
④ 개념: current session user가 없으면 `/login`.  
⑤ 실행: 비로그인/로그인, empty/normal/1000+ 질문.  
⑥ 주석: validation 실패는 API를 호출하지 않습니다.  
⑦ 정상: invalid=400, valid만 AI 단계 진입.  
⑧ 의미: 비용/보안 경계를 앞단에서 지킴.  
⑨ 오류: Form name/path 확인.  
⑩ 완료: protected/validation.

## STEP 04 — AI API Server-side
① 왜: Secret을 Browser에 노출하지 않고 AI를 호출합니다.  
② 무엇: `AI_API_URL`, `AI_API_KEY`, `AI_MODEL`.  
③ 용어: Server-side API, Secret.  
④ 개념: Browser→FastAPI→AI API→FastAPI→Browser.  
⑤ 명령:
```bash
export AI_API_URL="<runtime-endpoint>"
export AI_API_KEY="<secret-local-only>"
export AI_MODEL="<runtime-model>"
```
⑥ 주석: 실제 값은 GitHub/Evidence 금지.  
⑦ 정상: 질문에 AI answer.  
⑧ 의미: API Key는 server boundary 안에 유지됨.  
⑨ 오류: 401/403/network/timeout을 구분.  
⑩ 완료: real AI response.

## STEP 05 — Context / DB Logs
① 왜: 직전 대화 맥락과 추적 가능한 기록이 필요합니다.  
② 무엇: 같은 사용자 최근 6 Q/A → AI context, answer 저장.  
③ 용어: Context Window, Conversation Log.  
④ 개념: `WHERE user_id=?`로 사용자별 분리.  
⑤ 실행: 연결 질문 2~3개 후 `/logs`.  
⑥ 주석: 최근 context는 오래된 전체 기록을 무한 전송하지 않습니다.  
⑦ 정상: user/time/question/answer 저장.  
⑧ 의미: context와 persistence가 연결됨.  
⑨ 오류: DB path/FK/session user 확인.  
⑩ 완료: history + logs.

## STEP 06 — Two-user Isolation
① 왜: 다른 사용자의 대화가 섞이면 보안/개인정보 문제가 됩니다.  
② 무엇: A/B 두 계정으로 각각 chat/logs.  
③ 용어: Data Ownership, Isolation.  
④ 개념: route가 외부 user_id가 아니라 session user만 사용.  
⑤ 실행: A 대화→logout→B 대화→각 `/logs`.  
⑥ 주석: DB 직접 확인 시 user_id별 row도 비교.  
⑦ 정상: A 화면에 B log 없음.  
⑧ 의미: 사용자 기준 추적/분리.  
⑨ 오류: Query WHERE 조건 점검.  
⑩ 완료: isolation Evidence.

## STEP 07 — Operation Logs / Failure
① 왜: AI/DB 장애 원인을 추적해야 합니다.  
② 무엇: request/AI/DB event와 안전한 실패 처리.  
③ 용어: Operational Log, Timeout, 5xx.  
④ 개념: 실패를 catch하고 service process는 계속 살아 있음.  
⑤ 실행: 정상 호출 후 안전한 AI failure scenario.  
⑥ 주석: Key/Password/전체 민감 text는 log에 남기지 않습니다.  
⑦ 정상: event log + 사용자 오류 안내.  
⑧ 의미: 운영 가능성 확보.  
⑨ 오류: raw exception Secret 포함 여부 확인.  
⑩ 완료: failure Evidence.

## STEP 08 — Team / Deployment / CLEAR
① 왜: Term Project는 실제 협업과 외부 서비스까지 통합해야 합니다.  
② 무엇: branch/PR/10+ commits each, 외부 배포, docs package.  
③ 용어: Deployment, PR, Architecture.  
④ 개념: Reference commit ≠ 실제 team contribution.  
⑤ 실행: 실제 팀 GitHub workflow와 선택 Cloud/PaaS 배포.  
⑥ 주석: 외부 URL에서 auth→chat→logs 전체를 재검증.  
⑦ 정상: public URL + real AI + DB + collaboration Evidence.  
⑧ 의미: Linux/Web/DB/AI API/협업이 한 서비스로 통합됨.  
⑨ 오류: deployment env/DB persistence/Secret/platform logs 확인.  
⑩ 완료: 모든 Evaluation/Evidence 후에만 `✅ CLEAR`.
