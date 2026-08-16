#!/usr/bin/env bash
# B7-1 R01 offline verification helper. Does not call AI API or deploy.

set -u

PASS=0
FAIL=0
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
ROUND_DIR=$(cd "$SCRIPT_DIR/.." && pwd)
REF="$ROUND_DIR/reference"

pass() { echo "[PASS] $1"; PASS=$((PASS + 1)); }
fail() { echo "[FAIL] $1"; FAIL=$((FAIL + 1)); }

if command -v python3 >/dev/null 2>&1; then PYTHON=python3; elif command -v python >/dev/null 2>&1; then PYTHON=python; else
  echo "[FAIL] Python not found"; echo "Result: 0 PASS / 1 FAIL"; exit 1
fi

$PYTHON -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)' && pass "Python >= 3.10" || fail "Python >= 3.10"

for file in \
  "$REF/requirements.txt" \
  "$REF/app/db.py" \
  "$REF/app/auth.py" \
  "$REF/app/ai_client.py" \
  "$REF/app/main.py" \
  "$REF/templates/home.html" \
  "$REF/templates/signup.html" \
  "$REF/templates/login.html" \
  "$REF/templates/chat.html" \
  "$REF/templates/logs.html"; do
  [ -f "$file" ] && pass "file exists: ${file#$ROUND_DIR/}" || fail "file missing: ${file#$ROUND_DIR/}"
done

if $PYTHON -m compileall -q "$REF/app"; then pass "Python syntax compile"; else fail "Python syntax compile"; fi

if PYTHONPATH="$REF" $PYTHON - <<'PY'
from pathlib import Path
import tempfile
import app.db as db

with tempfile.TemporaryDirectory() as tmp:
    db.DB_PATH = Path(tmp) / "test.db"
    db.init_db()
    with db.db_connection() as c:
        tables = {row[0] for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    raise SystemExit(0 if {'users','sessions','conversations'} <= tables else 1)
PY
then pass "SQLite schema creates users/sessions/conversations"; else fail "SQLite schema"; fi

for route in '/signup' '/login' '/logout' '/chat' '/logs' '/health'; do
  grep -Fq "\"$route\"" "$REF/app/main.py" && pass "route present: $route" || fail "route missing: $route"
done

for keyword in request_received ai_call ai_response_received ai_call_failed db_save_success db_save_failed; do
  grep -Fq "$keyword" "$REF/app/main.py" && pass "operation log event: $keyword" || fail "operation log event missing: $keyword"
done

if grep -RInE '(sk-[A-Za-z0-9_-]{12,}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|AI_API_KEY[[:space:]]*=[[:space:]]*[A-Za-z0-9_-]{12,})' "$ROUND_DIR" --exclude='verify.sh' >/tmp/b7-1-secret-scan.out 2>/dev/null; then
  fail "possible credential-like value detected"
else
  pass "no obvious credential-like value in Round files"
fi

if grep -Fq 'PBKDF2' "$REF/app/auth.py" && grep -Fq 'token_hash' "$REF/app/auth.py"; then
  pass "password/session credential protection code present"
else
  fail "password/session credential protection code"
fi

if grep -Fq 'WHERE user_id = ?' "$REF/app/main.py"; then pass "user-scoped conversation queries present"; else fail "user-scoped query"; fi

if grep -Fq 'len(text) > 1000' "$REF/app/main.py"; then pass "chat input length validation"; else fail "chat input validation"; fi

echo
printf 'Result: %d PASS / %d FAIL\n' "$PASS" "$FAIL"
[ "$FAIL" -eq 0 ]
