# B7-1 R01 — Evidence Guide

## 1. Offline Reference

```bash
bash training/round-01-clear/environment/verify.sh
```

실제 `Result: N PASS / 0 FAIL`을 저장합니다.

## 2. Authentication

두 사용자로 다음을 확인합니다.

- signup success
- duplicate/error
- login success/failure
- logout
- 비로그인 `/chat`, `/logs` 접근 차단

Password/Session Token 실제 값은 Evidence에 포함하지 않습니다.

## 3. AI Chat

로그인 사용자 A:

- 질문 입력
- AI 응답 표시
- 최근 context가 다음 질문에 연결
- server log에 request/AI/DB event

## 4. Input / Error

- 빈 질문 차단
- 1000자 초과 차단
- AI endpoint/network/auth failure에서 service process가 종료되지 않고 오류 UI/502

## 5. DB

최소 필드:

```text
user_id / created_at / question / answer
```

사용자 A/B를 만든 뒤 A의 `/logs`에 B 대화가 나타나지 않는지 확인합니다.

## 6. External Deployment

외부 URL에서:

```text
signup → login → chat → AI answer → my logs → logout
```

전체 흐름을 수행합니다.

## 7. Operational Logs

Secret/전체 민감 대화 대신 다음 event를 증빙합니다.

- request_received
- ai_call
- ai_response_received 또는 ai_call_failed
- db_save_success 또는 db_save_failed

## 8. Team / GitHub

실제 팀 활동:

- branch strategy
- feature branch
- PR merge
- 팀원별 유의미한 commit 10+
- 역할/개인 작업 요약

Reference commit을 팀 Evidence로 계산하지 않습니다.

## 9. Docs Package

- 프로젝트 개요
- Architecture
- API spec
- DB schema/check guide
- deployment/env
- team role summary
- Secret management

## CLEAR

Local app code만으로 CLEAR하지 않습니다. 실제 AI API, user isolation, team collaboration, 외부 배포와 Evidence까지 완료해야 합니다.
