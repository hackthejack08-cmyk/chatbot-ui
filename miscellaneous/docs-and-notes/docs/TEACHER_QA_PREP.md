# Teacher / Viva Question Prep

## What Is This Project?

Byte-Bot is a pixel-style AI chatbot web app. It has a static frontend, a FastAPI backend, MongoDB memory, Groq/LangChain AI replies, and optional tool routes for search, upload, and voice features.

## Why Did You Use FastAPI?

FastAPI is a Python web framework. It is useful here because the AI/backend code is Python-based. It gives us routes like:

```py
@app.post("/chat")
async def chat(payload: ChatRequest):
    ...
```

This means the frontend can send a JSON message to `/chat` and get a JSON reply back.

## Why Did You Use MongoDB?

MongoDB stores user accounts and chat messages in collections. It is flexible and easy to connect with Python using Motor.

## What Is Motor?

Motor is the async MongoDB driver for Python. It lets FastAPI talk to MongoDB without blocking the server.

Example:

```py
mongo_client = AsyncIOMotorClient(MONGODB_URI)
await mongo_client.admin.command("ping")
```

## What Is LangChain?

LangChain helps connect a prompt template, chat history, context, and the LLM model into a chain.

In this project:

```py
chat_chain = build_prompt() | groq_model
```

This means the prompt output is passed into the Groq model.

## What Is Groq?

Groq provides fast LLM inference. The backend uses `ChatGroq` to get AI replies.

## How Does The Frontend Talk To Backend?

The frontend uses `fetch()`.

```js
const chatResponse = await fetch(chatUrl, {
  method: "POST",
  headers: getJsonHeaders(),
  body: JSON.stringify({
    message: userMessageText,
    session_id: currentSessionId
  })
});
```

This sends the user message to FastAPI.

## How Does Reset Work?

The reset button calls:

```text
POST /reset/{session_id}
```

The backend deletes messages for that session.

## How Does Voice Output Work?

Voice output uses the browser's built-in `speechSynthesis` API:

```js
const spokenReply = new SpeechSynthesisUtterance(cleanReply);
window.speechSynthesis.speak(spokenReply);
```

This reads bot replies aloud.

## What Is The Difference Between Voice Output And Voice Input?

- Voice output means text-to-speech: bot reply becomes audio.
- Voice input means speech-to-text: user voice becomes text.

Voice output already works through the browser. Voice input is prepared but needs a transcription API like Whisper.

## Why Is There A Frontend Folder?

The frontend folder separates static website files from backend files. This makes hosting easier.

```text
frontend/
backend/
```

Vercel can host `frontend/`, while Render/Railway can host `backend/`.

## Why Are Old Files Still There?

Old root-level files were kept for rollback/reference. The active frontend is now in `frontend/`.

## What Is CORS?

CORS controls which frontend domains can call the backend. FastAPI uses `CORSMiddleware` so local and hosted frontends can access the API.

## What Is A Session ID?

A session ID identifies a chat conversation. Messages are saved using this ID so the bot can load recent chat history later.

## What Is RAG?

RAG means Retrieval-Augmented Generation. It means loading documents, splitting them into chunks, finding relevant chunks, and sending those chunks to the AI as context.

Current project has upload/chunking scaffolding. Full semantic vector search is a future step.
