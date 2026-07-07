# Auth And Database Notes

This file explains the production login and MongoDB upgrade in beginner language.

## Frontend Flow

### `config.js`

```js
window.BYTEBOT_BACKEND_URL = window.BYTEBOT_BACKEND_URL || "";
```

This variable tells the frontend where the FastAPI backend is.

- Empty locally: frontend uses `http://127.0.0.1:8010`.
- Filled when hosted: frontend uses your Render backend URL.

### `login.js`

Important variables:

- `backendUrl`: the backend address.
- `currentAuthMode`: either `login` or `register`.
- `backendAuthConfig`: stores whether MongoDB login is enabled.

Important functions:

- `checkBackendAuthConfig()` calls `/auth/config`.
- `handleAuthSubmit()` runs when the user submits the login/register form.
- `sendAuthRequest()` sends data to `/auth/login` or `/auth/register`.
- `saveFrontendSession()` saves the JWT token and session id in `localStorage`.

Why `localStorage` is still used:

The browser needs to remember the login token between pages. The actual user account is in MongoDB, not only in the browser.

### `script.js`

Important variables:

- `savedAccessToken`: the JWT token from login.
- `currentSessionId`: the chat session id.
- `backendUrl`: the FastAPI backend address.

Important functions:

- `getAuthHeaders()` creates the `Authorization: Bearer ...` header.
- `getReplyFromBackend()` sends chat messages to `/chat`.
- `handleResetChat()` calls `/reset/{session_id}`.

Why the token matters:

When MongoDB is enabled, the backend uses the token to find the real logged-in user. The browser cannot just pretend to be someone else by changing `session_id`.

## Backend Flow

### `backend/app/database.py`

Important library:

- `motor`: async MongoDB driver for Python.

Important variables:

- `MONGODB_URI`: your MongoDB Atlas connection string.
- `MONGODB_DB_NAME`: database name, usually `bytebot`.
- `mongo_db`: the connected database object.

Important functions:

- `connect_to_mongo()` connects FastAPI to MongoDB.
- `close_mongo()` closes the connection on shutdown.
- `is_mongo_enabled()` tells the app whether MongoDB is active.
- `ensure_indexes()` makes MongoDB faster and prevents duplicate emails.

### `backend/app/auth_service.py`

Important libraries:

- `bcrypt`: hashes and checks passwords.
- `bson.ObjectId`: reads MongoDB user ids.

Important functions:

- `register_user()` creates a new user in MongoDB.
- `login_user()` checks email and password.
- `make_auth_response()` creates the response sent back to the frontend.

### `backend/app/security.py`

Important libraries:

- `bcrypt`: password safety.
- `jwt` from `PyJWT`: creates login tokens.

Important functions:

- `hash_password()` turns a password into a safe hash.
- `verify_password()` checks a login password against the hash.
- `create_access_token()` creates the JWT token.
- `decode_access_token()` reads and verifies the JWT token.

### `backend/app/mongo_memory.py`

Important collection:

- `chat_messages`: stores each user and bot message.

Important functions:

- `get_recent_messages_mongo()` loads recent memory.
- `save_message_mongo()` saves a user or assistant message.
- `clear_session_mongo()` clears memory for reset.

### `backend/app/main.py`

Important routes:

- `GET /health`: checks backend status.
- `POST /chat`: receives user messages and returns Byte-Bot replies.
- `POST /reset/{session_id}`: clears chat memory.

Important behavior:

```py
if is_mongo_enabled():
    use MongoDB memory
else:
    use SQLite memory
```

This keeps your project beginner-safe:

- local testing still works without MongoDB
- production uses MongoDB once configured

## What Is Still Future Work

- Email/password verification email through Resend, Brevo, or SendGrid.
- Upload PDFs/images and run semantic search over them.
- TTS voice output.
- STT voice input.
- Admin dashboard for users and sessions.

## Simple Auth Summary

The main auth flow is intentionally simple:

1. Register stores user data in MongoDB.
2. The password is hashed with bcrypt before saving.
3. Login searches MongoDB by email.
4. Login checks the typed password against `password_hash`.
5. If it matches, backend returns a JWT token.
6. If it does not match, backend returns `401 Wrong email or password`.

The current app uses email/password login only. Social login was removed to keep the project simple.
