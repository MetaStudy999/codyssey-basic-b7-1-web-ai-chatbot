# B7-1 Reference DB Schema

## users

| Column | Type | Rule |
|---|---|---|
| id | INTEGER | PK |
| username | TEXT | NOT NULL, UNIQUE |
| password_hash | TEXT | NOT NULL |
| password_salt | TEXT | NOT NULL |
| created_at | TEXT | NOT NULL |

## sessions

| Column | Type | Rule |
|---|---|---|
| id | INTEGER | PK |
| user_id | INTEGER | FK → users.id |
| token_hash | TEXT | NOT NULL, UNIQUE |
| created_at | TEXT | NOT NULL |

실제 session token은 cookie에만 전달하고 DB에는 SHA-256 hash만 저장합니다.

## conversations

| Column | Type | Rule |
|---|---|---|
| id | INTEGER | PK |
| user_id | INTEGER | FK → users.id |
| created_at | TEXT | NOT NULL |
| question | TEXT | NOT NULL |
| answer | TEXT | NOT NULL |

## 관계

```text
users 1 ── N sessions
users 1 ── N conversations
```

## 사용자 기준 로그 확인

```sql
SELECT id, created_at, question, answer
FROM conversations
WHERE user_id = ?
ORDER BY created_at DESC, id DESC;
```

다른 사용자의 로그를 URL parameter로 임의 조회하는 route는 Reference에 제공하지 않습니다.
