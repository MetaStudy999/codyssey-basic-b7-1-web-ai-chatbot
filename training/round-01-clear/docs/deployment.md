# B7-1 Deployment / Environment Reference

> 실제 배포 Provider와 외부 URL은 Phase C에서 선택·기록합니다. Reference 문서에 존재하지 않는 배포 성공을 주장하지 않습니다.

## Runtime Environment Variables

```bash
export AI_API_URL="<server-side-provider-endpoint>"
export AI_API_KEY="<secret-local-or-platform-secret>"
export AI_MODEL="<runtime-model>"
```

실제 Secret은 GitHub에 commit하지 않습니다.

## Local Run

```bash
cd training/round-01-clear/reference
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

```text
http://127.0.0.1:8000
```

## Production Checkpoints

실제 배포 시 최소 확인:

- 외부 HTTPS/HTTP URL 접근
- signup
- login
- protected chat
- AI response
- user-specific logs
- AI failure handling
- input validation
- server logs
- DB persistence
- Secret이 Browser source/HTML에 없음

## Cookie

Reference local code의 cookie `secure=False`는 HTTP local development용입니다. HTTPS production 배포에서는 deployment 환경에 맞게 Secure cookie를 사용하도록 조정해야 합니다.

## DB

Reference는 SQLite로 빠른 R01 경로를 제공합니다. 실제 multi-instance Cloud 배포에서 persistent shared DB가 필요하다면 Provider의 persistent storage/managed DB로 바꿀 수 있지만, B7-1 CLEAR를 지연시키는 과도한 infrastructure 확장은 피합니다.
