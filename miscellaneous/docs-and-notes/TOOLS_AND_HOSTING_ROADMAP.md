# Byte-Bot Tools And Hosting Roadmap

This roadmap is separate from the UI files. Use it when you want to continue toward search, uploads, semantic search, voice input, TTS, and deployment.

## Level 1: Stable Chat

Status: mostly done.

Files:

```text
backend/app/main.py
backend/app/prompt.py
backend/app/memory.py
backend/app/mongo_memory.py
script.js
```

Goal:

- User sends message.
- FastAPI receives message.
- Groq/LangChain creates reply.
- UI displays reply.
- Memory is saved.

## Level 2: Login And MongoDB

Status: in progress, code ready, Mongo network/config must be confirmed.

Files:

```text
backend/app/auth_routes.py
backend/app/auth_service.py
backend/app/security.py
backend/app/database.py
index.html
login.js
```

Goal:

- Register with email/password.
- Store user in MongoDB.
- Login checks MongoDB.
- JWT token is saved in browser storage.
- Chat uses the token for memory.

## Level 3: Web Search Tool

Status: scaffold added.

Files:

```text
backend/app/tool_routes.py
script.js
chat.html
```

Environment variable:

```text
SERPAPI_API_KEY=your_serpapi_key_here
```

Routes:

```text
POST /tools/search/google
POST /tools/search/twitter
POST /tools/search/images
```

Frontend behavior:

- Type a keyword in the message box.
- Click Web search or Image search.
- Frontend sends the keyword to FastAPI.
- FastAPI calls SerpApi.
- Results appear in chat.

## Level 4: Document Upload

Status: scaffold added.

Files:

```text
backend/app/tool_routes.py
chat.html
script.js
assets/upload-toolkit.png
```

Supported files now:

```text
.pdf
.csv
.txt
.md
.png
.jpg
.jpeg
.webp
.gif
.mp3
.wav
.m4a
.webm
.ogg
```

Current behavior:

- PDF/CSV/TXT/MD files are loaded.
- Text is split into chunks.
- A preview comes back to the UI.

Next upgrade:

- Add embeddings.
- Store chunks in a vector database.
- Retrieve matching chunks during chat.

Beginner vector options:

- Chroma for local testing.
- FAISS for local testing.
- MongoDB Atlas Vector Search later.

## Level 5: Semantic Search / RAG

Status: future.

Recommended files to create:

```text
backend/app/document_store.py
backend/app/vector_search.py
backend/app/rag_routes.py
```

Simple template:

```py
def add_chunks_to_vector_store(chunks):
    # Convert chunks into embeddings.
    # Save embeddings and metadata.
    pass


def search_similar_chunks(question):
    # Convert question into an embedding.
    # Return closest chunks.
    pass
```

Goal:

- User uploads a PDF.
- Backend chunks the PDF.
- Backend creates embeddings.
- User asks a question.
- Backend retrieves matching chunks.
- Groq answers using those chunks.

## Level 6: Voice Input

Status: route scaffold added.

Environment variable:

```text
OPENAI_API_KEY=your_openai_key_here
```

Route:

```text
POST /tools/transcribe
```

Current behavior:

- Upload an audio file.
- Backend sends it to Whisper.
- Text comes back to the frontend.

Beginner free option before paid APIs:

- Browser Web Speech API.

More reliable option:

- OpenAI Whisper API.

## Level 7: Text To Speech

Status: future.

Beginner browser-only template:

```js
function speakText(text) {
  const voiceMessage = new SpeechSynthesisUtterance(text);
  voiceMessage.rate = 1;
  voiceMessage.pitch = 1.1;
  speechSynthesis.speak(voiceMessage);
}
```

Where to call it:

```js
addChatMessage("bot", botReplyText);
speakText(botReplyText);
```

## Level 8: Hosting

Recommended simple split:

```text
Frontend: Vercel or Netlify
Backend: Render
Database: MongoDB Atlas
```

Frontend environment:

```js
window.BYTEBOT_BACKEND_URL = "https://your-backend.onrender.com";
```

Backend environment:

```text
GROQ_API_KEY=
MONGODB_URI=
MONGODB_DB_NAME=bytebot
JWT_SECRET_KEY=
SERPAPI_API_KEY=
OPENAI_API_KEY=
FRONTEND_ORIGINS=https://your-site.vercel.app
```

## Final Target

Byte-Bot should become:

- A real chatbot.
- A logged-in app.
- A memory-based assistant.
- A document Q&A assistant.
- A search assistant.
- A voice-enabled companion.
- A deployable project.
