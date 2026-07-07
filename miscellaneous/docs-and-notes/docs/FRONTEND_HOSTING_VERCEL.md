# Frontend Hosting With Vercel

This guide is for hosting the static Byte-Bot frontend on Vercel.

## Recommended Setup

Use Vercel for:

```text
frontend/
```

Use Render/Railway/Fly.io for:

```text
backend/
```

Reason: the frontend is static HTML/CSS/JS, but FastAPI is a long-running Python API server.

## Vercel Project Settings

When connecting your repo to Vercel:

```text
Root Directory: outputs/chatbot-ui/frontend
Framework Preset: Other
Build Command: leave empty
Output Directory: leave empty or .
Install Command: leave empty
```

If your GitHub repo starts directly inside `chatbot-ui`, then use:

```text
Root Directory: frontend
```

## Backend URL

After deploying FastAPI somewhere like Render, edit:

```text
frontend/config.js
```

Example:

```js
window.BYTEBOT_BACKEND_URL = "https://your-bytebot-backend.onrender.com";
```

For local development, keep it blank:

```js
window.BYTEBOT_BACKEND_URL = window.BYTEBOT_BACKEND_URL || "";
```

Then the frontend automatically uses:

```text
http://127.0.0.1:8010
```

## Backend CORS

Your FastAPI backend must allow your Vercel domain.

In `.env`:

```env
FRONTEND_ORIGINS=http://127.0.0.1:8028,http://localhost:8028,https://your-site.vercel.app
```

Then restart FastAPI.

## Before Deployment

Never put these in frontend files:

```text
GROQ_API_KEY
MONGODB_URI
SERPAPI_API_KEY
OPENAI_API_KEY
ELEVENLABS_API_KEY
JWT_SECRET_KEY
```

They belong only in backend `.env` or hosting environment variables.

## Simple Vercel Flow

1. Push project to GitHub.
2. Import repo into Vercel.
3. Set root directory to `frontend`.
4. Deploy frontend.
5. Deploy backend separately.
6. Put backend URL in `frontend/config.js`.
7. Put frontend Vercel URL in backend `FRONTEND_ORIGINS`.
8. Test login, chat, reset, and search.
