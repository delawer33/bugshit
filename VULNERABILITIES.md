# TaskFlow — Known Vulnerabilities

Internal reference for security review and pentester evaluation. **Not for production deployment.**

---

## Critical

| ID | Type | Location | Description |
|----|------|----------|-------------|
| C1 | SQL injection | `GET /api/tasks/search?q=` → `services/tasks.py` `search_tasks_raw` | User input interpolated into raw SQL via f-string. |
| C2 | Broken authentication | `DELETE /api/tasks/{id}` → `routes/tasks.py` | No auth required to delete any task. |
| C3 | Remote code execution | `GET /api/tasks/calc?expr=` → `routes/tasks.py` | Server calls `eval()` on user-supplied expression. |
| C4 | Command injection | `POST /api/tasks/export` (body.filter) → `services/export.py` | Filter passed to `shell=True` grep pipeline. |
| C5 | Command injection | `POST /api/admin/export-shell` → `services/export.py` | Arbitrary shell command appended to echo pipeline. |
| C6 | Insecure deserialization | `POST /api/admin/import-state` → `routes/admin.py` | Uploaded bytes deserialized with `pickle.loads()`. |
| C7 | Path traversal | `GET /api/files/download/{id}?name=` → `services/files.py` | `requested_name` joined to storage path without sanitization. |
| C8 | Privilege / balance escalation | `PATCH /api/users/me` → `schemas.py`, `routes/users.py` | Client can set `is_admin` and `wallet_balance`. |

---

## High

| ID | Type | Location | Description |
|----|------|----------|-------------|
| H1 | Hardcoded secret | `config.py` `jwt_secret` | JWT signing key committed in source. |
| H2 | Authentication bypass | `config.py` `support_master_password` + `auth.authenticate_user` | Password `admin123` authenticates as any existing username. |
| H3 | JWT misconfiguration | `auth.decode_token` | Accepts `none` algorithm; `verify_exp: False`. |
| H4 | Weak cryptography | `auth.hash_password` | Passwords hashed with MD5. |
| H5 | Sensitive data exposure | `auth.authenticate_user` | Login logs username and password in plaintext. |
| H6 | IDOR | `GET /api/users/{user_id}` | Any authenticated user can read any profile. |
| H7 | Broken access control | `GET /api/tasks/{id}` | Optional auth; unauthenticated access to tasks by ID. |
| H8 | Business logic | `POST /api/wallet/deposit` | Unlimited balance credit without payment verification. |
| H9 | Race condition | `services/wallet.py` `transfer_funds` | Read-modify-write without locking; concurrent transfers can corrupt balances. |
| H10 | SSRF | `POST /api/webhooks/deliver` → `services/webhooks.py` | Server POSTs to user-controlled URL; TLS verification disabled. |
| H11 | CORS misconfiguration | `main.py` | `allow_origins=["*"]` with `allow_credentials=True`. |
| H12 | Stored XSS | Comments API + `CommentThread.tsx` | HTML stored and rendered via `innerHTML`. |
| H13 | DOM XSS | `SearchPage.tsx` | Export output rendered with `dangerouslySetInnerHTML`. |
| H14 | Token storage | `api/client.ts` | JWT stored in `localStorage` (stealable via XSS). |

---

## Medium

| ID | Type | Location | Description |
|----|------|----------|-------------|
| M1 | Memory leak | `database.py` `_query_cache` | Unbounded in-process query cache. |
| M2 | Memory leak | `auth.py` `_active_sessions` | Session map never pruned. |
| M3 | Memory leak | `services/wallet.py` `_transfer_ledger` | Append-only transfer log. |
| M4 | Resource leak | `services/export.py` `_open_export_files` | Audit log file handles kept open. |
| M5 | Timing attack | `auth.verify_password` | Non-constant-time password comparison. |
| M6 | Reflected XSS | `GET /errors?msg=` → `main.py` | User input echoed in HTML response. |
| M7 | Information disclosure | `POST /api/tasks/export` errors | Returns HTTP 200 with error details reflecting input. |
| M8 | Rate-limit state | `middleware/rate_limit.py` | Per-IP hit lists grow (middleware present but not wired). |
| M9 | Client memory leak | `hooks/usePolling.ts` | `focus` listener not removed; `window.__activityLog` unbounded. |
| M10 | Client memory leak | `utils/analytics.ts` | Event buffer never capped or flushed. |
| M11 | Weak sanitization | `utils/validators.ts` `sanitizeHtml` | Only strips `<script>` tags. |

---

## Low

| ID | Type | Location | Description |
|----|------|----------|-------------|
| L1 | Weak password policy | `schemas.py` `UserCreate` | Minimum password length of 1. |
| L2 | Information disclosure | `main.py` access middleware | Full request URL logged (may include tokens in query). |
| L3 | Client bug | `hooks/useKeyboardShortcuts.ts` | Stale handlers due to empty effect deps. |
| L4 | User enumeration | `routes/auth.py` login | Same error for unknown user vs bad password (minor). |
| L5 | Unsafe file upload | `services/files.py` `save_upload` | Uses client-provided filename as storage path. |

---

## Quick test hints

- **SQLi:** `GET /api/tasks/search?q=' OR '1'='1`
- **Unauth delete:** `DELETE /api/tasks/1` (no `Authorization` header)
- **RCE:** `GET /api/tasks/calc?expr=__import__('os').system('id')`
- **Escalation:** `PATCH /api/users/me` with `{"is_admin": true, "wallet_balance": 99999}`
- **Master password:** login any user with password `admin123`
- **IDOR:** `GET /api/users/2` as another authenticated user

---

## Seed credentials

| User  | Password     |
|-------|--------------|
| admin | admin        |
| alice | password123  |
| bob   | password123  |
