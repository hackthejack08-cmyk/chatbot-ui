# Error and Fix Comparison

This file compares the problems we found with the corrections that were made.

## 1. Backend Did Not Reply

### My correction
- I made the backend return a local fallback reply when the real model is not available.

### The error
- The UI tried to call `http://127.0.0.1:8000/chat`.
- If FastAPI was not running, the frontend showed:
  - `Byte-Bot could not reach the backend right now. Check whether FastAPI is still running.`

### Why it happened
- The backend server was not running or was crashing before it could answer.

### Fix
- Keep FastAPI alive with a fallback `local_reply()` function.
- That gives you a real response even before the full LangChain model is installed.

## 2. Missing LangChain Groq Dependency

### My correction
- I wrapped the import in `try/except ImportError`.
- If the package is missing, the app still starts.

### The error
- `ModuleNotFoundError: No module named 'langchain_groq'`

### Why it happened
- The backend tried to import a package that was not installed.

### Fix
- Make `langchain_groq` optional.
- Only build the real chain when the package is present.

## 3. Broken Environment Variable Check

### My correction
- I changed the Groq key check to:

```python
groq_api_key = os.getenv("GROQ_API_KEY")
```

### The error
- The code used `os.getenv(GROQ_API_KEY)` instead of `os.getenv("GROQ_API_KEY")`.

### Why it happened
- `GROQ_API_KEY` without quotes is treated like a Python variable, not a string.

### Fix
- Use the quoted environment variable name.

## 4. Frontend Message Was Too Generic

### My correction
- I changed the backend reply to be a little personality-aware.

### The error
- The fallback message only said the backend was missing.

### Fix
- The local reply now gives a friendly Byte-Bot style response:
  - greeting
  - help response
  - backend explanation
  - happy-face response

## 5. My General Workflow

1. Read the code first.
2. Find the exact failing line.
3. Verify whether the issue is a path, dependency, or logic bug.
4. Fix the smallest thing that makes the app runnable again.
5. Add comments and docs so the next step is easier to understand.
6. Keep the fallback path alive until the real AI backend is ready.

## 6. What To Do Next

- Install the backend dependencies.
- Add your Groq API key.
- Restart FastAPI.
- Send a chat message again.
- Once that works, replace fallback logic with your real LangChain flow.
## Production Auth + MongoDB Upgrade

### Error / limitation

The login page looked like a real login, but it only stored the email and session id in `localStorage`.

```js
localStorage.setItem("bytebot_user_email", email);
localStorage.setItem("bytebot_session_id", sessionId);
```

That was useful for the UI prototype, but it was not real authentication. Anyone could create any session id in the browser.

### Correction

`login.js` now calls the backend:

```js
await sendAuthRequest("/auth/login", { email, password });
await sendAuthRequest("/auth/register", { email, password, name });
```

The backend stores users in MongoDB, hashes passwords with bcrypt, and returns a JWT token.

### Error / limitation

The chat memory only used SQLite.

```py
save_message(session_id, "user", user_message)
save_message(session_id, "assistant", reply)
```

SQLite is good for learning locally, but it is not the best database for a deployed multi-user chatbot.

### Correction

`main.py` now checks whether MongoDB is connected.

```py
if is_mongo_enabled():
    await save_message_mongo(session_id, "user", user_message)
else:
    save_message(session_id, "user", user_message)
```

This means:

- MongoDB Atlas is used in production.
- SQLite still works locally if MongoDB is not configured.

### Error / limitation

The frontend did not send login proof to the backend.

### Correction

`script.js` now sends the JWT token:

```js
Authorization: `Bearer ${savedAccessToken}`
```

When MongoDB is enabled, the backend uses this token to choose the correct user session.

### Error / limitation

The frontend did not know where the hosted backend would live.

### Correction

`config.js` was added:

```js
window.BYTEBOT_BACKEND_URL = "https://your-bytebot-backend.onrender.com";
```

For local development, leave it blank. For Netlify, put the Render backend URL there.

## MongoDB `SSL handshake failed`

### Error

FastAPI loaded `MONGODB_URI`, but `/health` still showed:

```json
"mongo_enabled": false
```

The backend terminal showed:

```text
SSL handshake failed ... tlsv1 alert internal error
```

### What this means

The URI is being read, but MongoDB Atlas is rejecting or interrupting the TLS connection before the app can log in.

Most common causes:

- Your current public IP is not allowed in MongoDB Atlas Network Access.
- Antivirus/firewall/VPN is interfering with MongoDB port `27017`.
- The network is routing through IPv6/NAT64 in a way Atlas does not like.

### Fix to try first

In MongoDB Atlas:

1. Go to `Network Access`.
2. Add your current IP address.
3. For quick testing only, you can add:

```text
0.0.0.0/0
```

4. Wait 1-2 minutes.
5. Restart FastAPI.
6. Open:

```text
http://127.0.0.1:8010/health
```

You want:

```json
"mongo_enabled": true
```

### Code correction added

`backend/app/database.py` now loads `.env` from the project folder directly and uses `certifi` for MongoDB TLS certificates.

## Google Auth Was Still Wired In

### Error

The app still had a Google login button, `/auth/google`, Google config fields, and a `google-auth` backend dependency even though the current project goal is simple email/password login.

### Old code shape

```py
@router.post("/google", response_model=AuthResponse)
async def google_login(payload: GoogleLoginRequest):
    user = await login_with_google(payload.credential)
    return make_auth_response(user)
```

### Correction

The app now uses only email/password auth:

```py
@router.post("/register", response_model=AuthResponse)
async def register(payload: AuthRegisterRequest):
    user = await register_user(payload.email, payload.password, payload.name)
    return make_auth_response(user)

@router.post("/login", response_model=AuthResponse)
async def login(payload: AuthLoginRequest):
    user = await login_user(payload.email, payload.password)
    return make_auth_response(user)
```

### Why this is better

The project is easier to explain:

1. Register saves user data in MongoDB.
2. Login checks email and password.
3. Backend returns a JWT token.
4. Chat uses that token for MongoDB memory.

## Tool Routes Added Without Breaking Chat

### Error risk

Search, PDF upload, image upload, and voice-to-text need extra API keys and packages. If those features are mixed directly into `/chat`, one missing key could break the whole chatbot.

### Correction

The optional tools now live in:

```text
backend/app/tool_routes.py
```

The routes are:

```text
/tools/search/google
/tools/search/twitter
/tools/search/images
/tools/upload
/tools/web-page
/tools/transcribe
```

### Why this is better

The core chat stays stable. If `SERPAPI_API_KEY` or `OPENAI_API_KEY` is missing, only that tool returns a setup message.

## MongoDB Was Enabled But Guest Chat Was Blocked

### Error

When MongoDB was connected, `/chat` required a login token every time. That made the local `chat.html` demo look broken if you opened it directly without logging in.

### Old code shape

```py
if is_mongo_enabled():
    session_id, user_name = await get_login_session(authorization)
```

### Correction

`backend/app/main.py` now uses logged-in memory when a token exists, but falls back to the simple guest session when no token exists:

```py
async def get_chat_session(payload_session_id, authorization):
    if is_mongo_enabled() and authorization and authorization.startswith("Bearer "):
        return await get_login_session(authorization)

    return get_guest_session(payload_session_id)
```

### Why this is better

- Local demo chat works immediately.
- Logged-in users still get MongoDB-backed sessions.
- The project is easier to test during development.

## Voice Output Button Added

### Need

The UI needed a button that makes Byte-Bot speak replies.

### Correction

`chat.html` now has a `Voice output` button, and `script.js` uses the browser `speechSynthesis` API. This does not expose a paid voice API key in frontend code.

### Important note

Voice input/transcription still needs `OPENAI_API_KEY` or another speech-to-text provider. Voice output works locally through the browser.

## Search Results Were Hard To Read

### Error

Web search results were rendered as one long paragraph. Long titles, snippets, and URLs ran into each other.

### Correction

`script.js` now formats each result on separate lines:

```text
1. Result title
   Link: result URL
   Note: short snippet
```

`styles.css` now keeps line breaks inside chat bubbles:

```css
.bubble p {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
```

### Why this is better

The search answer is easier to read, and long links no longer break the chat layout.

## Tool Buttons Fired Too Early

### Error

Clicking `Web search` or `Image search` immediately produced output if text was already in the message box.

### Correction

The tool buttons now enable a mode for the next Send:

```js
webSearchButton?.addEventListener("click", () => setSendMode("web"));
imageSearchButton?.addEventListener("click", () => setSendMode("image"));
```

The actual output happens inside `handleSendMessage()` after the user presses Send.
