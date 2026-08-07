-- SQLite verification script for B7-1.
.headers on
.mode column
SELECT
  id,
  user_id,
  request_id,
  created_at,
  status,
  error_code,
  substr(question, 1, 60) AS question,
  substr(answer, 1, 80) AS answer
FROM chat_logs
ORDER BY created_at DESC, id DESC
LIMIT 20;
