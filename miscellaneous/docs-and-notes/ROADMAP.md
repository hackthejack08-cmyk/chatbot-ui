# Byte-Bot Roadmap

This file is the simple project map: what is done, what is left, and which free tools are useful.

Roadmap image:

![Byte-Bot Progress Roadmap](assets/bytebot-progress-roadmap.svg)

## Current Level

You are at **Level 2: working full-stack prototype**.

Level 1 was only a frontend demo.
Level 2 means the UI can talk to a real FastAPI backend, use memory, and reset sessions.

## Done So Far

- Pixel login page.
- Pixel chat page.
- Clean night hero scene using `github-copilots.gif`.
- Old scene layers are kept as comments in `chat.html`.
- Cute computer mascot with idle/thinking/happy faces.
- Sidebar mini computer with status bar.
- FastAPI backend.
- `/chat` endpoint.
- `/health` endpoint.
- `/reset/{session_id}` endpoint.
- SQLite memory with `session_id`.
- Groq + LangChain path when `GROQ_API_KEY` is set.
- Local fallback reply when Groq is not available.
- Simple local knowledge loader in `rag.py`.
- Hosting notes for local and future deploy.

## Left To Build

1. Real login/auth
   - Right now login is local browser storage only.
   - Later use Clerk, Supabase Auth, or Firebase Auth.

2. Better long-term memory
   - Current memory stores chat messages.
   - Later add user profile memory, facts, preferences, and summaries.

3. Stronger RAG
   - Current RAG reads simple local text/markdown chunks.
   - Later add PDF upload, chunking, embeddings, and vector search.

4. Voice input
   - Add microphone speech-to-text.
   - Start with browser Web Speech API.

5. Text-to-speech
   - Add spoken Byte-Bot replies.
   - Start with browser `speechSynthesis`.

6. Better response control
   - Limit answer length.
   - Tune personality.
   - Add safe refusal behavior.

7. Testing
   - Backend endpoint tests.
   - Frontend manual test checklist.

8. Deployment
   - Frontend on Netlify or Vercel.
   - Backend on Render, Railway, Fly.io, or a VPS.

## Free Tools To Use

### Backend

- FastAPI: Python API server.
- Uvicorn: runs FastAPI locally.
- SQLite: free local memory database.
- Python dotenv: loads secret keys from `.env`.

### AI / LLM

- Groq free tier: fast hosted LLM calls.
- LangChain: prompt and chain structure.

### RAG / Knowledge

- Local `.txt` and `.md` files: easiest starting point.
- pypdf: read PDF files.
- FAISS: free vector search.
- ChromaDB: free local vector database.
- SentenceTransformers: free local embeddings.

### Voice

- Browser Web Speech API: free speech recognition in supported browsers.
- Browser `speechSynthesis`: free basic text-to-speech.
- Piper TTS: free local TTS later.
- whisper.cpp or faster-whisper: free local speech-to-text later.

### Frontend Hosting

- Netlify free tier.
- Vercel free tier.
- GitHub Pages for static frontend only.

### Backend Hosting

- Render free/low-cost tier.
- Railway trial/free credits.
- Fly.io free/low-cost tier.
- A small VPS later when you want more control.

## Best Next Step

Keep the app stable first:

1. Make sure the frontend always talks to `http://127.0.0.1:8010` locally.
2. Test `/chat`.
3. Test `/reset/{session_id}`.
4. Add simple PDF/text RAG after chat stays stable.
5. Add voice input and TTS after RAG.

## End Goal

Byte-Bot should become a real personal AI companion:

- cute pixel UI
- real chat backend
- memory
- local documents / PDF knowledge
- voice input
- text-to-speech
- deployable frontend and backend
- beginner-readable code structure
