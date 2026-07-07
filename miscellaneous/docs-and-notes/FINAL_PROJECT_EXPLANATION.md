# Byte-Bot Final Project Explanation

This file explains the project in beginner language, including UI logic, backend flow, login, MongoDB, search tools, upload tools, and voice-to-text planning.

## Current Goal

Byte-Bot is a pixel-style AI chatbot project.

Current working goal:

1. User opens the login page.
2. User registers or logs in with email and password.
3. FastAPI checks MongoDB.
4. User opens the chat page.
5. The chat page sends messages to FastAPI.
6. FastAPI uses Groq/LangChain when available.
7. Memory is saved in MongoDB when MongoDB is connected.
8. Reset clears the chat memory.
9. Optional tools can upload documents, search the web, search images, and later transcribe voice.

## Main File Structure

```text
chatbot-ui/
  index.html
  login.css
  login.js
  chat.html
  styles.css
  script.js
  config.js
  backend/
    app/
      main.py
      auth_routes.py
      auth_service.py
      database.py
      mongo_memory.py
      memory.py
      prompt.py
      rag.py
      schemas.py
      security.py
      tool_routes.py
```

## Frontend Files

### `index.html`

This is the login/register page.

Important parts:

- The form has email and password fields.
- The register tab also shows the name field.
- The page loads `config.js` first, then `login.js`.
- There is no social login in the current version.

The password input is:

```html
<input id="password" type="password">
```

This only hides the text on screen. The real password safety happens in FastAPI with bcrypt.

### `login.css`

This styles the pixel login page.

Important ideas:

- `position: absolute` layers the night scene images behind the login card.
- `image-rendering: pixelated` keeps the pixel art crisp.
- The login card stays centered with CSS grid.
- Button states use hover/focus styles for a proper website feel.

### `login.js`

This file makes login/register actually work.

Important variables:

- `backendUrl`: where FastAPI is running.
- `currentAuthMode`: either `login` or `register`.
- `backendAuthConfig`: tells the page whether MongoDB login is enabled.

Important functions:

- `checkBackendAuthConfig()` calls `GET /auth/config`.
- `handleAuthSubmit()` runs when the login form submits.
- `sendAuthRequest()` sends the email/password to FastAPI.
- `saveFrontendSession()` saves the JWT token, email, user label, and session id in browser localStorage.

Simple flow:

```text
User clicks login/register
        ↓
login.js reads email and password
        ↓
fetch() sends JSON to FastAPI
        ↓
FastAPI returns token + user
        ↓
login.js stores token in localStorage
        ↓
browser opens chat.html
```

## Chat UI Files

### `chat.html`

This is the main chatbot page.

Important visible sections:

- Hero pixel scene
- Clickable computer mascot
- Companion settings panel
- Chat panel
- Quick prompt buttons
- Tool dock for upload/search/voice
- Message input form

The hero mascot button uses:

```html
<button id="heroBotButton">
```

When clicked, JavaScript scrolls the page down to the chat section.

### `styles.css`

This file controls the complete pixel UI.

Important animation ideas:

- `@keyframes bot-idle` makes the mascot gently move.
- `@keyframes bot-think` makes the mascot look busy.
- `@keyframes message-enter` animates new messages.
- `@keyframes typing-dot` animates the typing indicator.
- The hero background uses a GIF layer with `object-fit: cover`.

Important CSS pattern:

```css
.computer-bot[data-state="thinking"] {
  animation: bot-think 0.6s steps(2) infinite;
}
```

This means JavaScript only changes `data-state`. CSS handles the animation.

### `script.js`

This file controls the chat page.

Important variables:

- `backendUrl`: FastAPI URL.
- `chatUrl`: `/chat` endpoint.
- `resetUrl`: `/reset/{session_id}` endpoint.
- `currentSessionId`: local session id.
- `savedAccessToken`: login token.
- `messageTextInput`: the message input box.
- `chatMessagesBox`: the message area.

Important functions:

- `getAuthHeaders()` adds the JWT token to requests.
- `getJsonHeaders()` adds JSON and auth headers.
- `handleSendMessage()` sends the typed message.
- `getReplyFromBackend()` calls FastAPI `/chat`.
- `addChatMessage()` creates a message bubble in HTML.
- `handleResetChat()` calls backend reset and clears the UI.
- `handlePickedFile()` sends uploaded files to `/tools/upload` or `/tools/transcribe`.
- `handleSearchTool()` sends search keywords to SerpApi endpoints.

Main chat flow:

```text
User types message
        ↓
handleSendMessage()
        ↓
add user bubble
        ↓
show thinking animation
        ↓
fetch("/chat")
        ↓
backend returns reply
        ↓
add bot bubble
        ↓
show happy animation
```

Loop examples:

```js
quickPromptList.forEach((quickButton) => {
  quickButton.addEventListener("click", () => {
    messageTextInput.value = quickButton.dataset.prompt;
    submitMessageForm();
  });
});
```

This loop adds the same click behavior to every quick prompt button.

Condition example:

```js
if (!userMessageText) {
  return;
}
```

This stops empty messages from being sent.

Try/catch example:

```js
try {
  const response = await fetch(chatUrl, options);
} catch (error) {
  setBotStatus("backend offline");
}
```

This prevents the whole page from breaking if the backend is offline.

## Backend Files

### `backend/app/main.py`

This is the FastAPI entry point.

Important routes:

- `GET /health`
- `POST /chat`
- `POST /reset/{session_id}`

Important behavior:

```py
if is_mongo_enabled():
    use MongoDB memory
else:
    use SQLite fallback memory
```

This keeps local development working even when MongoDB is not configured.

### `backend/app/auth_routes.py`

This owns auth endpoints:

- `GET /auth/config`
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

Current auth is email/password only.

### `backend/app/auth_service.py`

This owns user logic.

Important functions:

- `register_user()` creates a new MongoDB user.
- `login_user()` finds a user and checks the password.
- `make_auth_response()` creates the JWT response.

Important safety note:

The code stores `password_hash`, not the raw password. This keeps the project safe enough for deployment and does not affect the UI.

### `backend/app/security.py`

This owns password hashing and JWT tokens.

Important functions:

- `hash_password(password)`
- `verify_password(password, hashed_password)`
- `create_access_token(user_id, email)`
- `decode_access_token(token)`

Teacher answer:

Hashing means the real password is converted into a protected string before saving. Login checks the typed password against the stored hash.

### `backend/app/database.py`

This connects to MongoDB Atlas.

Important variables:

- `MONGODB_URI`
- `MONGODB_DB_NAME`
- `mongo_db`

Important functions:

- `connect_to_mongo()`
- `close_mongo()`
- `is_mongo_enabled()`
- `get_database()`
- `ensure_indexes()`

The users collection has a unique email index so the same email cannot register twice.

### `backend/app/mongo_memory.py`

This stores chat memory in MongoDB.

Important functions:

- `save_message_mongo()`
- `get_recent_messages_mongo()`
- `clear_session_mongo()`

### `backend/app/tool_routes.py`

This is the new optional tools module.

Routes:

- `POST /tools/search/google`
- `POST /tools/search/twitter`
- `POST /tools/search/images`
- `POST /tools/upload`
- `POST /tools/web-page`
- `POST /tools/transcribe`

What each tool does:

- Search routes use `SERPAPI_API_KEY`.
- Upload route accepts PDF, CSV, TXT, MD, images, and audio.
- PDF/CSV/TXT/MD files are loaded with LangChain document loaders.
- Documents are split into chunks using `RecursiveCharacterTextSplitter`.
- Transcribe route uses `OPENAI_API_KEY` and `whisper-1`.

The upload route uses conditions:

```py
if file_extension == ".pdf":
    loader = PyPDFLoader(...)
elif file_extension == ".csv":
    loader = CSVLoader(...)
elif file_extension in {".txt", ".md"}:
    loader = TextLoader(...)
else:
    raise HTTPException(...)
```

That is the beginner-readable if/elif structure you wanted.

## Data Flow From Frontend To Backend

Chat request:

```text
script.js
  fetch("http://127.0.0.1:8010/chat")
        ↓
FastAPI /chat route
        ↓
Pydantic checks request body
        ↓
Mongo/SQLite loads recent memory
        ↓
LangChain + Groq creates reply
        ↓
Mongo/SQLite saves user and assistant messages
        ↓
FastAPI returns JSON
        ↓
script.js adds bot bubble
```

Login request:

```text
login.js
  fetch("/auth/login")
        ↓
auth_routes.py
        ↓
auth_service.py
        ↓
MongoDB users collection
        ↓
security.py checks password hash
        ↓
JWT token returned
```

## Environment Variables

Use `.env` locally and hosting environment variables in production.

```text
GROQ_API_KEY=
MONGODB_URI=
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY=
SERPAPI_API_KEY=
OPENAI_API_KEY=
FRONTEND_ORIGINS=
```

Do not put real keys in GitHub.

## What Is Done

- Pixel login page
- Pixel chat page
- Clickable mascot scrolls to chat
- Email/password auth
- MongoDB connection support
- MongoDB chat memory support
- SQLite fallback memory
- Groq/LangChain chat
- Reset endpoint
- Tool route scaffold
- Upload UI
- Search UI
- Voice UI placeholder
- Beginner docs

## What Is Left

- Confirm MongoDB Atlas connection on your network.
- Add `SERPAPI_API_KEY` to enable live search.
- Add `OPENAI_API_KEY` to enable Whisper voice-to-text.
- Add embeddings and vector database for real semantic search.
- Add PDF summary with LLM after upload.
- Deploy frontend to Vercel or Netlify.
- Deploy backend to Render, Railway, or Fly.io.

## Free/Beginner-Friendly Tools

- Frontend hosting: Vercel or Netlify.
- Backend hosting: Render free tier, Railway trial, or Fly.io.
- Database: MongoDB Atlas free cluster.
- LLM: Groq developer free tier while available.
- Web search: SerpApi free trial/limited plan, or later Tavily/Brave Search API.
- Vector database: Chroma locally, FAISS locally, or MongoDB Atlas Vector Search later.
- Speech-to-text: browser Web Speech API for free local experiments, or OpenAI Whisper API later.
- Text-to-speech: browser `speechSynthesis` first, paid voice APIs later.

## Teacher Questions You Can Answer

Q: How is frontend connected to backend?

A: JavaScript uses `fetch()` to send HTTP requests to FastAPI routes like `/chat`, `/auth/login`, and `/tools/upload`.

Q: How does MongoDB connect?

A: `database.py` reads `MONGODB_URI` from `.env`, creates an async Motor client, pings MongoDB, and stores the database object in `mongo_db`.

Q: How is login checked?

A: Register saves a user by email. Login searches the users collection by email and checks the typed password against the stored password hash.

Q: How is memory saved?

A: Every message is saved with `session_id`, `role`, `content`, and `created_at`. Later the backend loads recent messages and gives them to the prompt.

Q: Why use try/catch in JavaScript?

A: It catches backend/network errors so the page can show a friendly message instead of breaking.

Q: Why use Pydantic schemas?

A: They validate the request and response shape, so FastAPI knows what data should arrive and what data should be returned.
