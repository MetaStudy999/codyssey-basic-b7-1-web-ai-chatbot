# B7-1 R01 — Requirement / Implementation / Verification / Evidence

| ID | Requirement | Reference Implementation | Runtime Verification | Evidence |
|---|---|---|---|---|
| R01 | Web question UI | `templates/chat.html` | browser | screenshot |
| R02 | response same service flow | POST→save→GET chat history | browser | Q/A screen |
| R03 | signup/login/logout | auth routes | browser | auth flow |
| R04 | unauthenticated access control | `/chat`, `/logs` redirect | browser/test | redirect |
| R05 | server-side AI API | `AIClient` in FastAPI | real API | server log/Q&A |
| R06 | API Key not exposed | env server only | source/browser inspect | secret check |
| R07 | context strategy | recent 6 same-user Q/A | code/runtime | conversation continuity |
| R08 | Q/A DB persistence | conversations table | sqlite/runtime | DB rows |
| R09 | user/time/question/answer tracking | DB schema | query | DB Evidence |
| R10 | user-based log lookup | `/logs` current user only | two-user scenario | access Evidence |
| R11 | request/AI/DB operation logs | Python logging | terminal/platform logs | log excerpt |
| R12 | AI failure/timeout safe handling | `AIServiceError` → 502 | failure scenario | error UI/log |
| R13 | input validation | 1~1000 chars | invalid form | 400/UI |
| R14 | external deployment | Phase C | external browser | deployed URL |
| R15 | project overview/docs | docs/reference | review | repository docs |
| R16 | architecture | `architecture.mmd` source | final diagram | architecture artifact |
| R17 | API spec | `api-spec.md` | review/runtime | document |
| R18 | DB schema/check guide | `db-schema.md` | SQLite query | document/output |
| R19 | deployment/env docs | `deployment.md` | external Runtime | document |
| R20 | team role/work summary | `team-runtime.md` template | actual team history | commit/PR links |
| R21 | branch/PR/10+ commits each | Phase C real team | GitHub history | links |
| R22 | Secret management | env + no key in repo | scan | verify result |
| R23 | evaluation explanations | `evaluation-qa.md` | user explanation | evaluator check |

## Runtime 필수

Reference app이 존재한다는 이유로 AI/API/팀/배포를 PASS 처리하지 않습니다. 최소 두 사용자를 만들어 user-specific log isolation도 실제 확인합니다.
