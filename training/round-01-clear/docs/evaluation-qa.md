# B7-1 R01 — Evaluation Q&A Reference

## 1. 전체 요청 흐름은?

```text
Browser form
→ FastAPI route
→ session user 확인
→ input validation
→ same-user 최근 대화 조회
→ server-side AI API
→ answer 수신
→ DB 저장
→ HTML에서 Q/A 확인
```

AI Key는 Browser로 보내지 않습니다.

## 2. 인증과 접근 제어를 왜 분리해서 생각해야 하는가?

인증은 사용자가 누구인지 확인하는 과정이고 접근 제어는 그 인증 상태/사용자에 따라 어떤 기능을 허용할지 결정하는 과정입니다. Reference에서는 session cookie로 사용자를 찾고 `/chat`, `/logs`에서 로그인하지 않은 사용자를 `/login`으로 보냅니다.

## 3. Password를 어떻게 저장하는가?

Plain password를 저장하지 않고 random salt + PBKDF2-HMAC-SHA256으로 만든 hash를 저장합니다. 로그인 시 입력 password를 같은 salt/iteration으로 hash해 constant-time compare합니다.

## 4. Session token을 DB에 그대로 저장하지 않는 이유는?

DB가 유출되었을 때 active token 자체가 노출되는 위험을 줄이기 위해 Browser에는 random token을 주고 DB에는 SHA-256 token hash만 저장합니다. 요청 시 cookie token을 hash해 DB와 비교합니다.

## 5. Context 유지 전략은?

같은 `user_id`의 최근 6개 Q/A를 시간순으로 복원해 현재 질문과 함께 AI API에 전달합니다. 모든 과거 대화를 무한히 넣지 않아 context 크기와 비용을 제한하면서 직전 대화 맥락을 유지합니다.

## 6. 다른 사용자 대화가 섞이지 않는 이유는?

대화 Query는 항상 현재 session의 `user.id`를 조건으로 사용합니다. `/logs`도 외부 user_id를 입력받지 않고 session user만 조회합니다.

## 7. 왜 AI API 호출을 서버에서 하는가?

Browser JavaScript에 API Key를 넣으면 사용자에게 Secret이 공개됩니다. Server environment에서 Key를 읽고 결과만 HTML 응답으로 돌려줍니다.

## 8. AI API 실패/timeout에서 왜 service가 죽지 않는가?

AI client가 HTTP/network/timeout/response format 오류를 `AIServiceError`로 바꾸고 route가 이를 잡아 502 + 사용자 안내를 반환합니다. Process 전체를 종료하지 않습니다.

## 9. 어떤 운영 로그를 남기는가?

Reference는 최소 다음 event를 구조화된 text로 남깁니다.

- request received
- AI call
- AI response received 또는 AI call failed
- DB save success 또는 DB save failed

질문/답변 전체나 API Key를 운영 로그에 남기지 않고 user id와 길이 등 필요한 metadata 중심으로 기록합니다.

## 10. 입력 검증은?

질문을 trim한 뒤 비어 있거나 1000자를 넘으면 AI API를 호출하지 않고 400으로 안내합니다. API 비용과 비정상 입력을 서버 진입 초기에 차단합니다.

## 11. DB 로그에서 최소 추적 필드는?

`user_id`, `created_at`, `question`, `answer`입니다. 이 정보로 어떤 사용자가 언제 어떤 질문을 하고 어떤 답을 받았는지 추적할 수 있습니다.

## 12. SQLite를 선택한 이유와 한계는?

R01에서 설치가 단순하고 SQL/관계/영속성을 명확히 확인할 수 있어 Reference Golden Path로 적합합니다. multi-instance production에서는 shared persistent DB가 필요할 수 있으므로 managed DB로 확장할 수 있습니다.

## 13. 협업 기록은 왜 Reference 코드로 대체할 수 없는가?

Branch/PR/team member commit 기준은 실제 협업 행동의 Evidence입니다. AI가 미리 작성한 코드나 문서 commit 수를 팀원별 작업으로 환산하면 평가 의미가 사라집니다. Phase C에서 실제 팀 활동으로 채웁니다.

## 14. 외부 배포에서 확인해야 할 것은?

URL이 열리는 것만 아니라 signup→login→chat→AI answer→log view가 외부 환경에서 끝까지 동작해야 합니다. Secret 설정, DB persistence, platform logs도 함께 확인합니다.
