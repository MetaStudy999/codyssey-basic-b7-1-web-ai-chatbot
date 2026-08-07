# Codyssey Basic B7-1 — 웹 기반 AI 챗봇 서비스 개발 프로젝트

FastAPI 기반 로그인 사용자용 AI 챗봇 MVP다. 사용자의 질문을 서버가 받아 **OpenAI-compatible AI API**에 전달하고, 최근 사용자 대화를 문맥으로 넣은 뒤 응답과 추적 정보를 SQLite에 저장한다.

## 프로젝트 개요

- **문제 정의:** 분리해서 학습한 웹/DB/AI API를 한 서비스 흐름으로 통합한다.
- **타겟 사용자:** 로그인 후 반복 질문을 하며 이전 대화 문맥이 필요한 사용자.
- **핵심 시나리오:** `회원가입 → 로그인 → 질문 → 서버 AI 호출 → 응답 → DB 저장 → 내 로그 조회`.
- **기술 스택:** Python, FastAPI, Jinja2, SQLAlchemy, SQLite, httpx.

## 빠른 실행

```bash
python -m venv .venv
source .venv/bin/activate            # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
```

`.env`에서 최소 다음 값을 실제 값으로 바꾼다.

```dotenv
SESSION_SECRET=<long-random-secret>
AI_API_KEY=<provider-api-key>
AI_MODEL=<available-chat-model>
```

실행:

```bash
uvicorn app.main:create_app --factory --reload
```

브라우저: `http://127.0.0.1:8000`

## 환경 변수

| Key | 의미 | 기본값/주의 |
|---|---|---|
| `SESSION_SECRET` | 세션 쿠키 서명 secret | **필수**, 저장소에 커밋 금지 |
| `DATABASE_URL` | SQLAlchemy DB URL | `sqlite:///./chatbot.db` |
| `AI_API_KEY` | AI provider key | 실제 AI 호출에 필수, 브라우저에 노출 금지 |
| `AI_BASE_URL` | OpenAI-compatible API base | `https://api.openai.com/v1` |
| `AI_MODEL` | provider에서 사용 가능한 chat model | 실제 AI 호출에 필수 |
| `AI_TIMEOUT_SECONDS` | AI API timeout | `20` |
| `CONTEXT_TURNS` | 현재 사용자 최근 성공 대화 context 개수 | `4` |
| `QUESTION_MAX_CHARS` | 질문 최대 길이 | `2000` |
| `SESSION_COOKIE_SECURE` | HTTPS 환경에서 secure cookie | 배포 시 `true` 권장 |

> `.env`는 `.gitignore`에 포함되어 있다. API key, DB password, session secret을 코드/문서/PR 본문에 붙여넣지 않는다.

## 기능

- 회원가입 / 로그인 / 로그아웃
- 비로그인 사용자의 챗봇 접근 차단
- 같은 화면에서 질문/AI 응답 확인
- server-side AI API 호출
- 현재 사용자 최근 N개 대화 기반 bounded context
- 질문/응답/사용자/시간/`request_id` DB 누적 저장
- `/logs` 사용자별 조회 화면
- `GET /api/me/chats` 사용자별 JSON 로그 조회
- 빈 입력/길이 제한 검증
- AI timeout/upstream 오류의 사용자 안내 및 오류 로그 저장
- 서버 이벤트 로그: request / AI call / AI result/failure / DB save success/failure
- `/health` 배포 상태 확인

## 테스트

```bash
pytest -q
```

Workcell 로컬 자동검증: **7 passed**. 자동 테스트는 fake AI adapter로 기능을 검증한다. **실제 AI API 성공과 외부 URL은 자동 테스트만으로 PASS 처리하지 않는다.**

## DB 확인

서비스에서 대화를 만든 뒤:

```bash
sqlite3 chatbot.db < scripts/check_logs.sql
```

또는 로그인 브라우저에서 `GET /api/me/chats`를 연다.

## 배포

Docker 이미지 실행 예:

```bash
docker build -t codyssey-b7-1 .
docker run --rm -p 8000:8000 --env-file .env codyssey-b7-1
```

외부 배포 환경에서는 `SESSION_COOKIE_SECURE=true`와 실제 `AI_API_KEY`, `AI_MODEL`을 secret/environment 설정으로 주입한다. SQLite 파일을 유지하려면 **영속 볼륨**이 있는 호스팅을 사용하거나 평가 환경의 DB 정책에 맞는 영속 DB URL을 설정한다.

평가 시 README의 아래 칸에 실제 값을 기록한다.

- **Deployed URL:** `NEEDS-RUNTIME`
- **Health URL:** `NEEDS-RUNTIME/health`
- **External E2E evidence:** `NEEDS-RUNTIME`

## 문서

- [시스템 아키텍처](docs/architecture.md)
- [API/Route 명세](docs/api.md)
- [DB/ERD 및 확인 가이드](docs/database.md)
- [입문자 학습 노트](docs/learning.md)
- [Mission Work Packet](MISSION-WORK-PACKET.md)

## 브랜치 / PR 협업

권장 흐름은 `main`을 안정 브랜치로 두고 `feature/*` 또는 현재 Mission 작업 브랜치에서 기능별 변경을 PR로 병합하는 것이다. 현재 Workcell은 `mission/b7-1` → `main` PR로 작업한다.

### 팀 구성원 역할 / 개인별 작업 요약

공식 Mission은 **팀원별 유의미한 커밋 10회 이상**과 실제 팀 역할/PR 기록을 요구한다. 현재 팀 구성원 정보가 제공되지 않았으므로 아래 표를 허위로 채우지 않는다.

| 팀원 | 역할 | 개인 작업 | PR/Commit evidence |
|---|---|---|---|
| `NEEDS-RUNTIME` | 실제 팀에서 확정 | 실제 팀에서 확정 | 각 팀원 10+ meaningful commits 필요 |

이 항목은 실제 팀 협업 후 Git 이력과 일치하도록 갱신해야 최종 PASS다.
