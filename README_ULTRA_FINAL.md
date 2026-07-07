# Byte-Bot Ultra Final Project Explanation

This is the main final explanation file for the Byte-Bot / ByteBuddy chatbot project.

Use this file when you need to explain the project to a teacher, interviewer, friend, or future ChatGPT chat.

## 1. Project Name

```text
Byte-Bot
```

## 2. Project Idea

Byte-Bot is a pixel-style AI chatbot web app.

The goal is not only to make a chatbot, but to make a chatbot with personality:

- cute pixel UI
- animated computer mascot
- chat interface
- FastAPI backend
- Groq/LangChain AI replies
- MongoDB memory
- login/register flow
- reset memory
- web search and image search tools
- voice output
- future PDF/image/voice RAG support

## 3. Current Folder Structure

```text
chatbot-ui/
  frontend/
    index.html
    chat.html
    styles.css
    script.js
    login.css
    login.js
    config.js
    assets/
    vercel.json

  backend/
    app/
      main.py
      prompt.py
      memory.py
      mongo_memory.py
      database.py
      auth_routes.py
      auth_service.py
      security.py
      tool_routes.py
      schemas.py
      rag.py
      knowledge/
    storage/
      uploads/
      logs/
    requirements.txt
    .venv/

  miscellaneous/
    legacy-root-frontend/
    legacy-root-assets/
    docs-and-notes/
    presentation-files/
    blueprints/

  start-bytebot.ps1
  start-bytebot.bat
  .env
  .env.example
  README.md
  README_ULTRA_FINAL.md
  DEPLOYMENT.md
  render.yaml
  netlify.toml
```

## 4. Why We Created `frontend/`

At first, the HTML, CSS, JS, backend, docs, and assets were all in one folder.

That works locally, but it becomes messy for hosting.

So we created:

```text
frontend/
```

This folder contains only the files needed by the browser:

- HTML
- CSS
- JavaScript
- images
- fonts
- frontend config

This makes it easier to host on Vercel or Netlify.

Old root-level frontend files were not deleted. They are kept as backup/reference in:

```text
miscellaneous/legacy-root-frontend/
```

Old notes, dumps, and generated files are kept in:

```text
miscellaneous/docs-and-notes/
miscellaneous/presentation-files/
miscellaneous/legacy-root-assets/
```

## 5. How To Run The Project

From:

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
```

Run:

```powershell
.\start-bytebot.ps1
```

Or double-click:

```text
start-bytebot.bat
```

This starts:

```text
Backend:  http://127.0.0.1:8010
Frontend: http://127.0.0.1:8028/chat.html
```

## 6. What `start-bytebot.ps1` Does

The file:

```text
start-bytebot.ps1
```

is a PowerShell script that starts everything.

Important variables:

```powershell
$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendRoot = Join-Path $ProjectRoot "backend"
$FrontendRoot = Join-Path $ProjectRoot "frontend"
$LogFolder = Join-Path $BackendRoot "storage\logs"
$PythonExe = Join-Path $BackendRoot ".venv\Scripts\python.exe"
$BackendPort = 8010
$FrontendPort = 8028
```

Meaning:

- `$ProjectRoot` stores the main project folder.
- `$BackendRoot` stores the `backend/` folder path.
- `$FrontendRoot` stores the `frontend/` folder path.
- `$LogFolder` stores server logs.
- `$PythonExe` points to the backend virtual environment Python.
- `$BackendPort` is the FastAPI port.
- `$FrontendPort` is the static frontend port.

The function:

```powershell
function Stop-ByteBotPort {
  param([int]$Port)
  ...
}
```

checks if a Python server is already using the port and stops it.

Then the script starts backend:

```powershell
Start-Process `
  -FilePath $PythonExe `
  -ArgumentList @("-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "$BackendPort")
```

This means:

- run Python
- use Uvicorn
- load FastAPI app from `backend.app.main:app`
- host it on `127.0.0.1`
- use port `8010`

Then it starts frontend:

```powershell
Start-Process `
  -FilePath $PythonExe `
  -ArgumentList @("-m", "http.server", "$FrontendPort", "--bind", "127.0.0.1") `
  -WorkingDirectory $FrontendRoot
```

This means:

- run Python static file server
- serve the `frontend/` folder
- use port `8028`

## 7. Frontend HTML Files

### `frontend/index.html`

This is the login/register page.

Main jobs:

- show login UI
- show register UI
- load `login.css`
- load `config.js`
- load `login.js`

### `frontend/chat.html`

This is the main chatbot page.

Important parts:

```html
<section class="pixel-stage">
```

This is the animated top scene.

```html
<section class="chat-layout" id="chatSection">
```

This is the chat area.

```html
<div class="messages is-empty" id="messages">
```

This is where JavaScript adds user and bot messages.

```html
<form class="composer" id="chatForm">
```

This is the message input and Send button.

Tool buttons:

```html
<button id="uploadToolButton">Upload docs</button>
<button id="webSearchButton">Web search</button>
<button id="imageSearchButton">Image search</button>
<button id="voiceOutputToggle">Voice output</button>
<button id="voiceToolButton">Voice input</button>
```

These buttons connect to JavaScript.

## 8. Frontend Config

File:

```text
frontend/config.js
```

Code:

```js
window.BYTEBOT_BACKEND_URL = window.BYTEBOT_BACKEND_URL || "";
```

This variable tells JavaScript where the backend is.

If blank, local frontend uses:

```text
http://127.0.0.1:8010
```

For hosting, change it to:

```js
window.BYTEBOT_BACKEND_URL = "https://your-backend-url.onrender.com";
```

## 9. CSS Overview

File:

```text
frontend/styles.css
```

CSS controls:

- colors
- fonts
- layout
- pixel scene
- mascot
- chat bubbles
- buttons
- responsiveness
- animations

### CSS Variables

At the top, the project uses CSS variables:

```css
:root {
  --ink: #050816;
  --gold: #ffc91a;
  --blue: #1fb6ff;
  --green: #6bd66f;
  --pink: #ff7bc8;
}
```

Why:

- one place controls the theme
- easier to change colors
- consistent design

### Font Loading

The custom pixel font is loaded with:

```css
@font-face {
  font-family: "PixelGrid";
  src: url("assets/pixelgrid-squarebolds.woff") format("woff");
}
```

Meaning:

- `@font-face` defines a local font.
- `font-family` gives it a name.
- `src` tells the browser where the font file is.

### Pixel Stage

The hero section uses:

```css
.pixel-stage {
  position: relative;
  min-height: 720px;
  overflow: hidden;
}
```

Meaning:

- `position: relative` lets child elements be positioned inside it.
- `min-height` gives the scene enough vertical space.
- `overflow: hidden` hides extra image parts outside the scene.

### Background Layer

The scene image uses:

```css
.scene-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}
```

Meaning:

- `position: absolute` places image over the full section.
- `inset: 0` means top/right/bottom/left are all zero.
- `object-fit: cover` makes the image cover the area without stretching weirdly.

### Chat Layout

The chat area uses CSS grid:

```css
.chat-layout {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
}
```

Meaning:

- first column is sidebar/settings
- second column is chat panel
- `minmax(0, 1fr)` prevents overflow problems

### Message Bubble Formatting

Search output uses line breaks, so we added:

```css
.bubble p {
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}
```

Meaning:

- `white-space: pre-wrap` keeps `\n` line breaks from JavaScript.
- `overflow-wrap: anywhere` lets long links wrap instead of breaking layout.

### CSS Animations

Animations are created with `@keyframes`.

Example:

```css
@keyframes mascot-hover {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
```

Meaning:

- at start/end, mascot is normal
- halfway, mascot moves up
- browser loops this to create floating effect

## 10. JavaScript Overview

File:

```text
frontend/script.js
```

JavaScript controls:

- reading form input
- sending chat to backend
- adding messages to UI
- updating mascot face/status
- reset button
- quick prompts
- web/image search mode
- file upload
- voice output

## 11. Important JavaScript Variables

DOM variables:

```js
const chatMessagesBox = document.querySelector("#messages");
const sendMessageForm = document.querySelector("#chatForm");
const messageTextInput = document.querySelector("#messageInput");
```

Meaning:

- `chatMessagesBox` is where messages appear.
- `sendMessageForm` is the chat form.
- `messageTextInput` is the text input.

Backend URL variables:

```js
const configuredBackendUrl = (window.BYTEBOT_BACKEND_URL || "").trim();
const defaultBackendUrl = isLocalFrontend
  ? "http://127.0.0.1:8010"
  : window.location.origin;
const backendUrl = configuredBackendUrl || savedBackendUrl || defaultBackendUrl;
```

Meaning:

- if `config.js` has a backend URL, use it.
- else if local, use `127.0.0.1:8010`.
- else use hosted origin.

Route variables:

```js
const chatUrl = `${backendUrl}/chat`;
const resetUrl = `${backendUrl}/reset`;
const healthUrl = `${backendUrl}/health`;
```

Meaning:

- build full backend API URLs.

Session variables:

```js
const currentSessionId = localStorage.getItem("bytebot_session_id") || "bytebot-guest";
const currentUserName = localStorage.getItem("bytebot_user_label") || "guest";
```

Meaning:

- browser remembers user/session in `localStorage`.
- if missing, use guest mode.

Mode variable:

```js
let selectedSendMode = "chat";
```

Meaning:

- default Send means normal chat.
- clicking Web Search changes mode to `web`.
- clicking Image Search changes mode to `image`.
- after Send, it returns to `chat`.

Voice variable:

```js
let isVoiceOutputEnabled = localStorage.getItem("bytebot_voice_output_enabled") === "true";
```

Meaning:

- remembers if voice output is on.

## 12. JavaScript Event Listeners

Example:

```js
sendMessageForm.addEventListener("submit", handleSendMessage);
```

Meaning:

- when user presses Send, run `handleSendMessage()`.

Tool buttons:

```js
webSearchButton?.addEventListener("click", () => setSendMode("web"));
imageSearchButton?.addEventListener("click", () => setSendMode("image"));
voiceOutputButton?.addEventListener("click", handleVoiceOutputToggle);
```

Meaning:

- Web Search button enables web-search mode.
- Image Search button enables image-search mode.
- Voice Output button toggles speech.

The `?.` is optional chaining. It prevents errors if an element does not exist.

## 13. Main Send Function

Function:

```js
async function handleSendMessage(event) {
  event.preventDefault();
  const userMessageText = messageTextInput.value.trim();
  ...
}
```

Important ideas:

- `async` means the function can use `await`.
- `event.preventDefault()` stops the browser from refreshing the page.
- `.trim()` removes extra spaces.

Then it adds user message:

```js
addChatMessage("user", userMessageText);
```

Then it chooses what Send means:

```js
const sendModeForThisMessage = selectedSendMode;
const botReplyText = sendModeForThisMessage === "web" || sendModeForThisMessage === "image"
  ? await getSearchReply(sendModeForThisMessage, userMessageText)
  : await getReplyFromBackend(userMessageText);
```

Meaning:

- if mode is `web`, run search.
- if mode is `image`, run image search.
- otherwise, run normal chatbot backend.

Then it adds bot message:

```js
addChatMessage("bot", botReplyText);
```

Then it speaks if voice output is enabled:

```js
speakBotReply(botReplyText);
```

## 14. Backend Chat Fetch

Function:

```js
async function getReplyFromBackend(userMessageText) {
  const chatResponse = await fetch(chatUrl, {
    method: "POST",
    headers: getJsonHeaders(),
    body: JSON.stringify({
      message: userMessageText,
      session_id: currentSessionId
    })
  });
}
```

Meaning:

- `fetch()` sends an HTTP request.
- `method: "POST"` sends data to backend.
- `headers` tells backend JSON is being sent.
- `JSON.stringify()` converts JavaScript object into JSON text.

## 15. Search Reply Formatting

Function:

```js
function makeSearchSummary(searchData, searchType) {
  ...
}
```

This now starts with context first:

```text
I searched the web for "...". Quick context: the strongest result I found is "...".
Check the source/date before treating it as final.
```

Then it lists links:

```text
Top web results:

1. Title
   Link: URL
   Note: snippet
```

This is better than showing only raw links.

## 16. Voice Output Function

Function:

```js
function speakBotReply(replyText) {
  if (!isVoiceOutputEnabled || !("speechSynthesis" in window)) {
    return;
  }
  ...
}
```

Meaning:

- if voice is off, do nothing.
- if browser does not support speech synthesis, do nothing.

Then:

```js
const spokenReply = new SpeechSynthesisUtterance(cleanReply);
window.speechSynthesis.speak(spokenReply);
```

Meaning:

- create a speech object from text.
- tell browser to speak it.

## 17. Backend Overview

Backend folder:

```text
backend/app/
```

Main backend file:

```text
backend/app/main.py
```

This file creates the FastAPI app and main routes.

## 18. FastAPI App

Code:

```py
app = FastAPI(title="Byte-Bot API")
```

Meaning:

- creates the backend app.
- names it Byte-Bot API.

## 19. CORS Middleware

Code:

```py
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Meaning:

- allows frontend to call backend.
- `FRONTEND_ORIGINS` controls allowed websites.
- needed when frontend is on Vercel and backend is on Render/Railway.

## 20. Environment Variables

The backend reads secrets from `.env`.

Important variables:

```env
GROQ_API_KEY=
MONGODB_URI=
MONGODB_DB_NAME=
JWT_SECRET_KEY=
SERPAPI_API_KEY=
OPENAI_API_KEY=
FRONTEND_ORIGINS=
```

Never put these in frontend JavaScript.

## 21. Backend Startup

Code:

```py
@app.on_event("startup")
async def startup():
    init_db()
    await connect_to_mongo()
```

Meaning:

- initialize SQLite fallback database.
- connect to MongoDB if configured.

## 22. Health Route

Code:

```py
@app.get("/health")
def health():
    return {
        "status": "ok",
        "llm_connected": chat_chain is not None,
        "knowledge_ready": bool(knowledge_chunks),
        "mongo_enabled": is_mongo_enabled(),
        "mongo_error": get_mongo_error(),
    }
```

Meaning:

- frontend or developer can check backend status.
- tells if LLM, knowledge, and MongoDB are working.

## 23. Chat Route

Code:

```py
@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, authorization: str | None = Header(default=None)):
```

Meaning:

- receives chat messages.
- returns a `ChatResponse`.
- optionally reads auth token from headers.

The backend extracts message:

```py
user_message = payload.message.strip()
```

Then gets session:

```py
session_id, user_name = await get_chat_session(payload.session_id, authorization)
```

This lets both guest mode and logged-in mode work.

## 24. Guest vs Logged-In Session

Function:

```py
async def get_chat_session(payload_session_id: str, authorization: str | None):
    if is_mongo_enabled() and authorization and authorization.startswith("Bearer "):
        return await get_login_session(authorization)

    return get_guest_session(payload_session_id)
```

Meaning:

- if MongoDB is enabled and token exists, use logged-in session.
- otherwise use guest session.

This fixed the problem where chat failed when MongoDB was enabled but user was not logged in.

## 25. LangChain + Groq Chain

Code:

```py
groq_model = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
return build_prompt() | groq_model
```

Meaning:

- `ChatGroq` creates the LLM model.
- `build_prompt()` creates the prompt template.
- `|` connects prompt to model.

Then:

```py
model_response = chat_chain.invoke({
    "context": context_text,
    "history": history_text,
    "question": user_message,
})
```

Meaning:

- send context, history, and user question to the AI.
- get model response.

## 26. Prompt File

File:

```text
backend/app/prompt.py
```

This controls Byte-Bot's personality.

It tells the model:

- be Byte-Bot
- be helpful
- keep replies short
- remember project facts
- mention MongoDB memory correctly
- avoid bland assistant behavior

## 27. Schemas

File:

```text
backend/app/schemas.py
```

Example:

```py
class ChatRequest(BaseModel):
    message: str
    session_id: str
```

Meaning:

- FastAPI expects JSON with `message` and `session_id`.

```py
class ChatResponse(BaseModel):
    reply: str
```

Meaning:

- backend returns JSON with `reply`.

Pydantic validates these automatically.

## 28. Memory Files

### SQLite Memory

File:

```text
backend/app/memory.py
```

Functions:

```py
init_db()
get_recent_messages()
save_message()
clear_session()
format_history()
```

Meaning:

- create local database
- load recent messages
- save messages
- clear reset
- format history for prompt

### MongoDB Memory

File:

```text
backend/app/mongo_memory.py
```

Functions:

```py
get_recent_messages_mongo()
save_message_mongo()
clear_session_mongo()
```

Meaning:

- same memory idea, but stored in MongoDB.

## 29. Auth Flow

Files:

```text
backend/app/auth_routes.py
backend/app/auth_service.py
backend/app/security.py
```

Register:

```text
POST /auth/register
```

Login:

```text
POST /auth/login
```

Config:

```text
GET /auth/config
```

Frontend login stores:

```text
bytebot_access_token
bytebot_session_id
bytebot_user_label
```

in `localStorage`.

## 30. Tool Routes

File:

```text
backend/app/tool_routes.py
```

Routes:

```text
POST /tools/search/google
POST /tools/search/images
POST /tools/upload
POST /tools/web-page
POST /tools/transcribe
```

### SerpApi Search

Code idea:

```py
client = serpapi.Client(api_key=SERPAPI_API_KEY)
return dict(client.search(params))
```

Meaning:

- use SerpApi key from backend `.env`.
- call Google/Web/Image search.
- return simplified results to frontend.

### Upload Documents

Code idea:

```py
if file_extension == ".pdf":
    loader = PyPDFLoader(str(file_path))
elif file_extension == ".csv":
    loader = CSVLoader(str(file_path))
elif file_extension in {".txt", ".md"}:
    loader = TextLoader(str(file_path), encoding="utf-8")
```

Meaning:

- choose loader based on file extension.
- PDF uses `PyPDFLoader`.
- CSV uses `CSVLoader`.
- TXT/MD uses `TextLoader`.

Then:

```py
RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
```

Meaning:

- splits big documents into smaller chunks.
- chunks are easier for future semantic search.

## 31. How Frontend And Backend Connect

Flow:

```text
User types message
  -> frontend/script.js reads input
  -> fetch() sends JSON to FastAPI /chat
  -> FastAPI validates with Pydantic schema
  -> backend loads memory
  -> backend builds prompt
  -> Groq/LangChain generates reply
  -> backend saves user and bot messages
  -> backend returns JSON reply
  -> frontend displays bot bubble
  -> optional voice output speaks reply
```

## 32. Hosting Plan

### Frontend

Use Vercel.

Host:

```text
frontend/
```

### Backend

Use Render/Railway/Fly.io.

Host:

```text
backend/
```

### Database

Use MongoDB Atlas.

### Important Hosting Variables

Backend environment variables:

```env
GROQ_API_KEY=
MONGODB_URI=
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY=
SERPAPI_API_KEY=
OPENAI_API_KEY=
FRONTEND_ORIGINS=https://your-vercel-site.vercel.app
```

Frontend config:

```js
window.BYTEBOT_BACKEND_URL = "https://your-backend-url.onrender.com";
```

## 33. About ElevenLabs

Yes, ElevenLabs can be added for better voice output.

Do not put the ElevenLabs key in frontend JS.

Correct architecture:

```text
frontend button
  -> POST /tools/tts
  -> FastAPI calls ElevenLabs using ELEVENLABS_API_KEY
  -> backend returns audio file/blob
  -> frontend plays audio
```

Why:

- API key remains private.
- frontend only receives audio output.

For now, browser `speechSynthesis` is simpler and free.

## 34. Current Completed Features

- Pixel-style frontend.
- Login/register UI.
- Chat page.
- Animated mascot.
- FastAPI backend.
- Groq/LangChain response path.
- Local fallback response path.
- MongoDB connection.
- Guest chat fallback.
- Reset route.
- Web search mode.
- Image search mode.
- Upload route for PDF, CSV, TXT, and MD files.
- Uploaded file chunks are saved into the session knowledge store so Byte-Bot can answer later questions from the file.
- CSV uploads get a simple numeric summary and IQR outlier check.
- Voice output toggle.
- Separate `frontend/` folder.
- Separate `backend/` folder with storage and virtual environment kept inside it.
- `miscellaneous/` archive for old files, drafts, generated docs, and presentation material.
- One-command startup script.
- Vercel frontend notes.
- Root `README.md`, `README_ULTRA_FINAL.md`, and `DEPLOYMENT.md` for quick explanation.

## 35. Still Left To Build

- Full PDF semantic search with embeddings/vector database.
- Real image understanding.
- Real voice input with Whisper/OpenAI or local model.
- Optional ElevenLabs high-quality TTS.
- Hosted backend deployment.
- Hosted frontend deployment.
- User-specific document storage.
- Better long-term memory summaries.
- Admin/debug dashboard.

## 36. Teacher-Friendly Summary

Byte-Bot is a full-stack AI chatbot project.

The frontend is made using HTML, CSS, and JavaScript. It provides the user interface, animations, tool buttons, and chat input.

The backend is made using FastAPI. It receives messages from the frontend, calls LangChain and Groq for AI replies, stores memory in MongoDB or SQLite, and returns responses to the frontend.

MongoDB stores user accounts and chat messages.

SerpApi is used for web and image search.

Browser `speechSynthesis` is used for voice output.

The project is organized so the frontend can be hosted on Vercel and the backend can be hosted separately.

## 37. Thank You

Thank you.

This project is now ready to explain, improve, and deploy step by step.
