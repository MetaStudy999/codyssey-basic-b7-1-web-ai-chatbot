# B7-1 R01 Environment

## Golden Path

- Python 3.10+
- FastAPI
- Uvicorn
- Jinja2
- python-multipart
- SQLite
- 실제 AI API는 Phase C에서 server-side environment로 연결

## Local Setup

```bash
cd training/round-01-clear/reference
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Runtime Secret:

```bash
export AI_API_URL="<runtime-endpoint>"
export AI_API_KEY="<secret-local-only>"
export AI_MODEL="<runtime-model>"
```

Run:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Secret

실제 API Key/Token/Password는 Repository/Evidence에 저장하지 않습니다. User password는 DB에 plain text가 아니라 salted PBKDF2 hash로 저장하도록 Reference를 구성했습니다.

## Verify

```bash
bash training/round-01-clear/environment/verify.sh
```

Offline verify는 Python source compile, DB schema, Secret-like pattern, required route/log keyword를 확인합니다. 실제 FastAPI browser flow, AI API, two-user isolation, deployment/team collaboration은 Phase C에서 별도 검증합니다.
