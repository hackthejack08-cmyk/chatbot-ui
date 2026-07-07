# Byte-Bot Production Setup

This is the clean hosting path for the current project.

## Best Hosting Split

- Frontend: Netlify
- Backend: Render
- Database: MongoDB Atlas
- Login: email/password stored in MongoDB
- LLM: Groq through the FastAPI backend

This split is easier than forcing FastAPI into a frontend host. Netlify serves `index.html`, `chat.html`, CSS, JS, and assets. Render runs Python. MongoDB Atlas stores users and chat messages.

## What Is Real Now

- `/auth/register` creates a MongoDB user.
- `/auth/login` checks email/password with bcrypt.
- `/chat` saves messages to MongoDB when `MONGODB_URI` is set.
- `/reset/{session_id}` clears MongoDB memory for the logged-in user.
- If MongoDB is not configured, the backend still uses SQLite so local learning does not break.

## Local Setup

1. Copy `.env.example` to `.env`.
2. Add your real `GROQ_API_KEY`.
3. Add `MONGODB_URI` if you want real login and Mongo memory.
4. Install backend dependencies:

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

5. Start backend:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8010
```

6. Start frontend in a second terminal:

```powershell
python -m http.server 8028
```

Open:

```text
http://127.0.0.1:8028/index.html
```

## MongoDB Atlas Setup

1. Create a free MongoDB Atlas cluster.
2. Create a database user.
3. Copy your connection string.
4. Put it in `.env` as `MONGODB_URI`.
5. Restart FastAPI.

Your current Atlas template should become this after replacing the password:

```text
MONGODB_URI=mongodb+srv://dev07319_db_user:YOUR_REAL_PASSWORD@byte-bot.sr8eipf.mongodb.net/bytebot?retryWrites=true&w=majority
```

Keep this inactive until `YOUR_REAL_PASSWORD` is replaced. The literal `<db_password>` placeholder will not connect.

For learning, you can allow network access from `0.0.0.0/0`. For a serious project, restrict this later.

## Netlify Frontend Setup

1. Push this project to GitHub.
2. Create a new Netlify site from the repo.
3. Set publish directory to:

```text
outputs/chatbot-ui
```

If you deploy from inside the `chatbot-ui` folder, the publish directory is just:

```text
.
```

4. Edit `config.js` before deploying or in your deployed branch:

```js
window.BYTEBOT_BACKEND_URL = "https://your-bytebot-backend.onrender.com";
```

## Render Backend Setup

1. Create a new Render Web Service.
2. Use this root if your repo contains the whole Codex folder:

```text
outputs/chatbot-ui
```

3. Build command:

```text
pip install -r backend/requirements.txt
```

4. Start command:

```text
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

5. Add environment variables:

```text
GROQ_API_KEY
MONGODB_URI
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
FRONTEND_ORIGINS=https://your-site.netlify.app,http://127.0.0.1:8028,http://localhost:8028
```

## Beginner Mental Model

- `index.html` is the login screen.
- `login.js` sends register/login requests to FastAPI.
- `chat.html` is the chat screen.
- `script.js` sends chat/reset requests to FastAPI.
- `backend/app/main.py` owns the API routes.
- `backend/app/auth_routes.py` owns login/register routes.
- `backend/app/auth_service.py` owns user creation and password check.
- `backend/app/database.py` connects to MongoDB.
- `backend/app/mongo_memory.py` saves and loads chat messages from MongoDB.
- `backend/app/memory.py` is the SQLite fallback.
