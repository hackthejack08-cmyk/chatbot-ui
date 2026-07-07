# Byte-Bot Deployment Guide

Recommended deployment:

```text
Frontend: Vercel
Backend: Render
Database: MongoDB Atlas
LLM: Groq
Search: SerpApi
```

## 1. Prepare Secrets

Never put these in frontend files:

```text
GROQ_API_KEY
MONGODB_URI
SERPAPI_API_KEY
OPENAI_API_KEY
ELEVENLABS_API_KEY
JWT_SECRET_KEY
```

Put them only in `.env` locally or in the hosting service environment variables.

Before real deployment, rotate any keys that were pasted in chat or screenshots.

## 2. Deploy Backend On Render

Render project settings:

```text
Root Directory: outputs/chatbot-ui
Build Command: pip install -r backend/requirements.txt
Start Command: uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

If your GitHub repo starts directly inside `chatbot-ui`, leave root directory empty.

Render environment variables:

```text
GROQ_API_KEY=your_groq_key
MONGODB_URI=your_mongodb_atlas_connection_string
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY=make_this_long_random_and_private
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
SERPAPI_API_KEY=your_serpapi_key
FRONTEND_ORIGINS=http://127.0.0.1:8028,http://localhost:8028,https://your-vercel-site.vercel.app
```

After Render deploys, test:

```text
https://your-render-service.onrender.com/health
```

## 3. Deploy Frontend On Vercel

Vercel project settings:

```text
Root Directory: outputs/chatbot-ui/frontend
Framework Preset: Other
Build Command: leave empty
Output Directory: .
Install Command: leave empty
```

If your GitHub repo starts directly inside `chatbot-ui`, use:

```text
Root Directory: frontend
```

Edit:

```text
frontend/config.js
```

Set the backend URL:

```js
window.BYTEBOT_BACKEND_URL = "https://your-render-service.onrender.com";
```

## 4. Update CORS

After Vercel gives you the final frontend URL, put it into Render:

```text
FRONTEND_ORIGINS=https://your-vercel-site.vercel.app,http://127.0.0.1:8028,http://localhost:8028
```

Then restart the Render backend.

## 5. Final Test Order

1. Open Vercel frontend.
2. Register a new account.
3. Login.
4. Send a normal chat message.
5. Try reset.
6. Try web search.
7. Try image search.
8. Check Render logs if a backend call fails.

## 6. Current Local Start Command

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
.\start-bytebot.ps1
```

This starts:

```text
Backend:  http://127.0.0.1:8010
Frontend: http://127.0.0.1:8028/chat.html
```
