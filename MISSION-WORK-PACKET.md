# B7-1 Mission Work Packet — Web AI Chatbot

## 1. Identity
- Mission ID: `B7-1`
- Mission Title: 웹 기반 AI 챗봇 서비스 개발 프로젝트
- Mission Repository: `MetaStudy999/codyssey-basic-b7-1-web-ai-chatbot`
- Workcell: Chat 14
- Started At: `2026-08-08T04:40:00+09:00`

## 2. Control Tower Baseline
- Repository: `MetaStudy999/codyssey-basic`
- Frozen Baseline SHA: `0d1581b3e82366988f57e1d76da311c028b8e15e`
- Active Wave: `20260808-01`
- Rule: Control Tower READ ONLY.

## 3. Read / Write Boundary
- READ: frozen Control Tower, B7-1 repository, B7-1 official source/attachments.
- WRITE: B7-1 repository only.
- DO NOT WRITE: Control Tower or other mission repositories.

## 4. Source Inventory
| Source Candidate | Type | State | Location | Notes |
|---|---|---|---|---|
| Mission | PDF | VALID | `b7-1-mission.pdf` + provided official attachment | rendered PDF has 5 pages; functional requirements verified |
| Mission | Markdown | DUPLICATE | `b7-1-mission.md` | requirements substantively match PDF; metadata says 6 pages |
| Evaluation | PDF/MD | MISSING | repo root/docs/search + File Library search | no B7-1 evaluation source found |
| Official operation | PDF | VALID/PARTIAL | 2026 orientation, Basic Term Project row | B7-1 Project A is required Term Project; Mission details remain governed by Mission PDF |

- Source Mode: `MISSION-LED`
- Source Confidence: `MEDIUM`
- Source Gaps:
  - 공식 Evaluation/평가문항을 발견하지 못했다. Evaluation을 추정하지 않는다.
  - 팀 구성원 identity/실제 분업 증빙은 Source가 요구하지만 현재 Repository에 없다.
  - Mission Markdown의 `6쪽` 메타데이터와 현재 렌더링된 PDF의 5페이지가 다르지만 확인된 요구사항 내용에는 충돌이 없다.

## 5. Mission Contract
### Goal
로그인 사용자가 웹에서 질문하면 FastAPI 서버가 server-side AI API를 호출하고, 사용자별 최근 문맥을 적용해 응답을 반환하며, 질문/응답을 DB에 누적 저장·조회·추적하고 외부 URL로 배포 가능한 서비스를 완성한다.

### Required Deliverables
- [x] FastAPI web chatbot implementation
- [x] GitHub repository source
- [x] README/architecture/API/DB/deploy/secret-management docs
- [x] DB inspection guide (`GET /api/me/chats`, `scripts/check_logs.sql`)
- [ ] externally reachable runtime URL (`NEEDS-RUNTIME`)
- [ ] team collaboration evidence and each member's 10+ meaningful commits (`NEEDS-RUNTIME`)

### Required Functions / Behaviors
- [x] signup/login/logout and protected chatbot
- [x] web question input + response on chat screen
- [x] server-side AI API call
- [x] bounded same-user context strategy
- [x] DB persistence with user/time/question/answer plus request trace fields
- [x] user-based log UI/API
- [x] request/AI/DB success-failure logging
- [x] AI timeout/failure safe UX
- [x] input validation
- [x] environment-based secrets + `.gitignore`

### Constraints
Python/FastAPI. SQLite is used for the default evaluation-friendly local profile. AI key/database secrets are never committed. AI call timeout is mandatory.

### Explicit Non-scope
B7-2 board CRUD, multi-tenant admin console, RAG/vector DB, streaming tokens, OAuth/social login, distributed queue.

## 6. Requirement Traceability
| ID | Requirement | Source | Location | Implementation | Test/Evidence | Status |
|---|---|---|---|---|---|---|
| REQ-B7-1-001 | Login user can input question and see AI answer in web UI | Mission PDF | pp.1-3 | `/chat` | pytest + browser runtime | TESTED |
| REQ-B7-1-002 | Signup/login/access control | Mission PDF | p.3 | auth routes + sessions | `test_auth_*` | TESTED |
| REQ-B7-1-003 | AI API is called server-side | Mission PDF | p.3 | `app/ai.py` | fake-adapter integration test; real key pending | NEEDS-RUNTIME |
| REQ-B7-1-004 | Minimum context strategy | Mission PDF | p.3 | recent N successful same-user turns | context isolation test | TESTED |
| REQ-B7-1-005 | Persist user/time/question/answer and user-based trace | Mission PDF | p.3 | `ChatLog`, `/logs`, `/api/me/chats` | pytest + SQL guide | TESTED |
| REQ-B7-1-006 | Request/AI/DB success/failure logs | Mission PDF | pp.3-4 | structured log messages + request_id | logger-enabled regression test; runtime capture pending | NEEDS-RUNTIME |
| REQ-B7-1-007 | Timeout/failure does not terminate service | Mission PDF | pp.3-4 | typed AI errors + saved error chat | timeout test | TESTED |
| REQ-B7-1-008 | Input validation | Mission PDF | p.3 | blank/length limit | validation test | TESTED |
| REQ-B7-1-009 | External URL at evaluation time | Mission PDF | pp.1,3 | Docker-ready | external browser evidence | NEEDS-RUNTIME |
| REQ-B7-1-010 | Branch/feature/PR history, each member 10+ commits | Mission PDF | p.4 | draft Mission PR prepared | GitHub team evidence | NEEDS-RUNTIME |
| REQ-B7-1-011 | README docs incl team/secret/env/deploy/API/DB | Mission PDF | pp.2,4 | README + docs | doc/code review | IMPLEMENTED |

## 7. Evaluation Mapping
Official Evaluation source: `MISSING`. No evaluation criteria are invented. If a source is provided before final PASS, it must be mapped here and the implementation rechecked.

## 8. Repository Baseline
- Default Branch: `main`
- Baseline Commit: `16d902072afc212b24fa8b68a68a89204d099cab`
- Work Branch: `mission/b7-1`
- Baseline files: `README.md`, `b7-1-mission.md`, `b7-1-mission.pdf`
- Existing app/tests/docs/deploy: none

## 9. Mission-specific TOC
```text
Source/Evaluation Discovery
→ FastAPI App Factory
→ Session Auth
→ Chat UI
→ AI Adapter
→ Bounded User Context
→ Conversation DB + Traceability
→ Error/Timeout/Logging
→ DB Inspection
→ Automated Tests
→ Documentation/Learning
→ External Runtime
→ Team Evidence
→ Handoff
```

## 10. Engineering Plan
- Prompt: implement only confirmed Mission requirements; stop at runtime/team gaps.
- Context: Mission PDF/MD + frozen Governance + current repo.
- Harness: `pytest -q`, GitHub Actions, secrets only through env.
- Loop: self review once; independent review once for BLOCKER/MAJOR.
- Fusion order: Source → Test → Runtime → Evidence.

## 11. Agent Routing
- Orchestrator/Integrator: ChatGPT
- Primary Builder: ChatGPT (current tool environment)
- Independent Reviewer: pending until a distinct reviewer is available; no fake independent audit is recorded.
- Specialist agents: OFF unless BLOCKER/MAJOR ambiguity appears
- Runtime Authority: Human

## 12. Dependency / Drift Check
- Upstream Dependency: `RECOMMENDED`, not official reuse requirement.
- Related Missions: B5/B6 concepts.
- Actual prerequisite required before G2: `NONE` — B7-1 PDF requires integrated capabilities but does not require importing prior repositories/artifacts.
- Control Tower Drift: NONE against frozen baseline.
- Source Drift: requirements are substantively aligned; Markdown metadata says the PDF is 6 pages while the currently rendered PDF has 5 pages. This does not change any confirmed requirement.
- Action: CONTINUE.

## 13. Test Plan
| Test | Requirement | Method | Actual | Status |
|---|---|---|---|---|
| auth/access | 002 | pytest | passed | TESTED |
| input validation | 008 | pytest | passed | TESTED |
| success chat persistence | 001/005 | pytest | passed | TESTED |
| context bound/isolation | 004 | pytest | passed | TESTED |
| timeout error persistence | 007 | pytest | passed | TESTED |
| unauthenticated log API | 005 | pytest | passed | TESTED |
| required INFO lifecycle logs enabled | 006 | pytest | passed | TESTED |
| real AI API | 003 | actual credential | not run | NEEDS-RUNTIME |
| external URL E2E | 009 | external browser | not run | NEEDS-RUNTIME |

Local harness result: `7 passed`.

## 14. Runtime Plan
- Real AI provider key/model call: Human secret required.
- Browser signup/login/chat/context/log verification: Human acceptance required for final evidence.
- External hosting URL: Human/cloud account required.
- Team member/PR/10+ commit evidence: Human team workflow required.

## 15. Evidence Plan
- GitHub Actions/pytest result.
- Browser screenshots: login, chat answer/context, logs.
- Server log excerpt for request/AI/DB chain.
- `GET /api/me/chats` or SQLite query output.
- External URL and `/health`.
- Team PR and commit links.

## 16. Review Record
- Self-review finding `MAJOR`: required INFO lifecycle log messages existed but the named logger inherited WARNING level, so INFO events could be suppressed in some runtimes.
- Action: fixed in commit `8cff561e8637d8a6e77e3c13d982504ad14a3b75` by enabling the application logger and added a regression test.
- Self-review after fix: BLOCKER=0, MAJOR=0.
- Independent reviewer: pending; G4 remains TODO until a distinct review is actually completed.

## 17. Completion Gates
| Gate | Exit Condition | Status |
|---|---|---|
| G1 SOURCE | Source state/mode/gap/provenance fixed | PASS |
| G2 BUILD | required implementation exists | IMPLEMENTED |
| G3 TEST | automated tests pass | TESTED |
| G4 REVIEW | BLOCKER=0, MAJOR=0 under independent review | TODO |
| G5 RUNTIME | actual AI/browser/cloud checks | NEEDS-RUNTIME |
| G6 EVIDENCE | required external/team evidence | NEEDS-RUNTIME |
| G7 LEARN | beginner learning material | IMPLEMENTED |
| G8 MERGE | PR/merge after gates | TODO |

## 18. STOP Rule
Stop mission-completion work only after confirmed Mission requirements, any later Evaluation mapping, BLOCKER=0, MAJOR=0, tests, runtime, evidence, and G8 merge are complete. Runtime/team gaps must not be falsely marked PASS.

## 19. Handoff Contract
At final completion update `HANDOFF.md` and `mission-result.yaml`. Control Tower remains unchanged by this Workcell.
