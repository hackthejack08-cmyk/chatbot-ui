# Byte-Bot Production Process README

This is the simple order to turn Byte-Bot from local project into a hosted app with real login and MongoDB memory.

## What We Built In This Step

1. Real auth backend files

- `backend/app/auth_routes.py`
- `backend/app/auth_service.py`
- `backend/app/security.py`

These files add register, login, password hashing, and JWT tokens.

2. MongoDB connection files

- `backend/app/database.py`
- `backend/app/mongo_memory.py`

These files connect to MongoDB Atlas and store chat messages in the `chat_messages` collection.

3. Frontend auth flow

- `index.html`
- `login.js`
- `config.js`

The login screen now calls the backend instead of only pretending locally.

4. Hosting files

- `netlify.toml`
- `render.yaml`
- `.env.example`

These prepare the project for Netlify frontend hosting and Render backend hosting.

## Step 1: Run Locally Without MongoDB

This is the safe beginner test.

Backend:

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8010
```

Frontend:

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
python -m http.server 8028
```

Open:

```text
http://127.0.0.1:8028/index.html
```

Expected behavior:

- Backend health works.
- Chat works.
- Login page shows local demo mode if MongoDB is not configured.

## Step 2: Add MongoDB Atlas

Create a free MongoDB Atlas cluster.

Then add this to `.env`:

```text
MONGODB_URI=mongodb+srv://your_user:your_password@your_cluster.mongodb.net/bytebot
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY=make-this-long-and-random
```

Restart FastAPI.

Expected behavior:

- `/auth/config` returns `"mongo_enabled": true`
- login/register becomes real
- chat history is saved in MongoDB
- reset clears MongoDB memory

## Step 3: Host Backend On Render

Render settings:

```text
Build command:
pip install -r backend/requirements.txt

Start command:
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

Render environment variables:

```text
GROQ_API_KEY
MONGODB_URI
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
FRONTEND_ORIGINS=https://your-site.netlify.app,http://127.0.0.1:8028,http://localhost:8028
```

After deploy, Render gives you a backend URL like:

```text
https://bytebot-backend.onrender.com
```

## Step 4: Host Frontend On Netlify

In `config.js`, set:

```js
window.BYTEBOT_BACKEND_URL = "https://bytebot-backend.onrender.com";
```

Deploy the frontend folder to Netlify.

Expected behavior:

- Netlify serves the login page.
- Login calls Render.
- Render talks to MongoDB Atlas.
- Chat memory is stored in MongoDB.

## Step 6: Debug Checklist

If login does not work:

1. Open this URL:

```text
http://127.0.0.1:8010/auth/config
```

2. Check `mongo_enabled`.

If it is false:

- `MONGODB_URI` is missing or wrong.
- Restart FastAPI after editing `.env`.

If chat does not work:

1. Open this URL:

```text
http://127.0.0.1:8010/health
```

2. Check:

- `status`
- `llm_connected`
- `mongo_enabled`
- `mongo_error`

If frontend cannot reach backend:

- Check `config.js`.
- Check `FRONTEND_ORIGINS`.
- Check backend URL and port.

## What Is Still Left

These are future modules, not done yet:

- Email verification by email link using Resend, Brevo, or SendGrid.
- PDF upload and semantic search.
- Image upload and image understanding.
- TTS voice output.
- STT voice input.
- Admin dashboard.
- Production rate limiting.
- Better long-term memory.
