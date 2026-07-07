# Byte-Bot Hosting Notes

These are the easy notes for future hosting.

## 1. Local run

Backend:

```bash
uvicorn backend.app.main:app --reload --port 8010
```

Frontend:

```bash
python -m http.server 8028
```

Then open:

- `http://127.0.0.1:8028/index.html`

## 2. How the frontend finds the backend

`login.js` stores the backend URL in browser storage.

- If you open the project locally, it uses:
  - `http://127.0.0.1:8010`
- If you host the frontend on a normal website, it uses:
  - `window.location.origin`

That means:

- local testing works with FastAPI on port `8010`
- same-domain hosting works later without changing the main chat script

## 3. If frontend and backend are on different domains later

Change the saved backend URL in `login.js` or in browser storage.

Example:

```js
localStorage.setItem("bytebot_api_base_url", "https://your-backend-url.com");
```

## 4. Add more mascot assets later

Open `script.js` and edit:

```js
const mascotImageList = [
  "assets/coding-window.gif",
  "assets/bytebuddy-team.gif"
];
```

Add new image paths there.

## 5. Backend files that matter

- `backend/app/main.py`: FastAPI routes
- `backend/app/memory.py`: SQLite chat memory
- `backend/app/prompt.py`: Byte-Bot prompt template
- `backend/app/rag.py`: simple local knowledge loading

## 6. If the bot says backend offline

Check these in order:

1. Is FastAPI running on port `8010`?
2. Does `/health` open in the browser?
3. Is `GROQ_API_KEY` set?
4. If Groq is missing, does fallback mode still answer?

## 7. Good next step

After this, the best next step is:

1. verify the backend starts cleanly
2. test `/chat`
3. test `/reset/{session_id}`
4. then continue UI polishing only after chat is stable
