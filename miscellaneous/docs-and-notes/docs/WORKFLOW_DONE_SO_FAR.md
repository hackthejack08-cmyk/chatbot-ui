# Byte-Bot Workflow Done So Far

## 1. Started With UI

We first built a pixel-style chatbot interface inspired by a coding adventure style:

- login/register page
- animated hero background
- Byte-Bot mascot
- chat section
- quick prompt buttons
- reset button
- tool buttons

## 2. Added Personality

Byte-Bot was designed as:

- cute
- curious
- helpful
- pixel/anime-style
- short and friendly in replies

This personality lives mostly in:

```text
backend/app/prompt.py
```

## 3. Connected Backend

We added FastAPI in:

```text
backend/app/main.py
```

Main routes:

```text
GET  /health
POST /chat
POST /reset/{session_id}
```

The frontend sends messages with `fetch()` from:

```text
frontend/script.js
```

## 4. Added Memory

Memory works in two modes:

- MongoDB when enabled
- SQLite fallback for local/simple mode

MongoDB files:

```text
backend/app/database.py
backend/app/mongo_memory.py
```

SQLite fallback file:

```text
backend/app/memory.py
```

## 5. Added Login/Register

Auth files:

```text
backend/app/auth_routes.py
backend/app/auth_service.py
backend/app/security.py
```

Frontend login files:

```text
frontend/index.html
frontend/login.js
frontend/login.css
```

## 6. Added Tools

Tool routes live in:

```text
backend/app/tool_routes.py
```

Current tool routes:

```text
/tools/search/google
/tools/search/images
/tools/upload
/tools/web-page
/tools/transcribe
```

## 7. Added Voice Output

Voice output uses the browser:

```js
speechSynthesis.speak(spokenReply);
```

This means bot replies can be read aloud without using paid backend TTS yet.

## 8. Organized Frontend

We created:

```text
frontend/
```

The active frontend now lives there. Old root files were kept.

## 9. Added One-Command Startup

Run:

```powershell
.\start-bytebot.ps1
```

This starts:

- backend on `http://127.0.0.1:8010`
- frontend on `http://127.0.0.1:8028/chat.html`

## 10. Current Status

Byte-Bot now has:

- working frontend
- working backend
- Groq/LangChain chat path
- MongoDB connection
- guest fallback chat
- reset route
- web search route
- image search route
- upload route scaffold
- voice output button
- frontend folder for hosting
- Vercel-ready frontend notes
