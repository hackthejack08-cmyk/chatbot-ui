# Byte-Bot Assistant Tools Roadmap

This is the separate roadmap for turning Byte-Bot from a chatbot into a central assistant with tools.

The current app should stay stable first. These files and templates are a blueprint for the next phase.

## Current Level

You are at **Level 2: working full-stack prototype**.

Current completion toward the big assistant goal: **about 45%**.

What is already working:

- Pixel frontend
- Login UI
- Chat UI
- FastAPI backend
- Groq + LangChain path
- SQLite chat memory
- Reset endpoint
- Local fallback replies
- Simple local text knowledge loader
- Hosting notes

## End Goal

Byte-Bot should become one central assistant backend that can:

- chat normally
- remember the user
- answer from PDFs, images, notes, and project files
- perform semantic search
- draft emails
- save and fetch notes
- search the web later
- talk through Discord later
- support voice input
- speak replies using TTS
- eventually run multi-step workflows with LangGraph

## Big Architecture

```text
Frontend / Discord / Voice
        |
        v
FastAPI routes
        |
        v
chat_service.py
        |
        +-- memory_service.py
        +-- router_service.py
        +-- rag_service.py
        +-- note_service.py
        +-- email_service.py
        +-- search_service.py
        +-- image_doc_service.py
        +-- voice_service.py
        +-- discord_service.py
        |
        v
Groq / LangChain / Tools
```

## Recommended File Structure

Final target structure:

```text
chatbot-ui/
  index.html
  chat.html
  styles.css
  script.js
  login.js
  assets/
  backend/
    requirements.txt
    storage/
      uploads/
      indexes/
    app/
      main.py
      schemas.py
      prompt.py
      memory.py
      rag.py
      services/
        chat_service.py
        router_service.py
        memory_service.py
        rag_service.py
        note_service.py
        email_service.py
        search_service.py
        image_doc_service.py
        voice_service.py
        discord_service.py
        langgraph_service.py
      tools/
        email_tools.py
        note_tools.py
        search_tools.py
        discord_tools.py
        image_tools.py
```

Right now, do not move everything at once. Add one module at a time.

## Phase 1: Simple Router

Goal: decide what kind of message the user sent.

Create later:

```text
backend/app/services/router_service.py
backend/app/services/chat_service.py
backend/app/services/tool_models.py
```

Start simple with keyword routing:

```python
intent = detect_intent(user_message)

if intent == "rag_question":
    answer from documents
elif intent == "note_save":
    save a note
elif intent == "email_draft":
    draft an email
else:
    normal chat
```

Do this before LangGraph. It is easier to debug.

## Phase 2: Notes Tool

Goal: let the user say:

```text
remember that my project name is Byte-Bot
```

and later:

```text
what did I ask you to remember?
```

Free tool:

- SQLite

Tables:

```sql
CREATE TABLE notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  title TEXT,
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Files:

```text
backend/app/services/note_service.py
```

## Phase 3: PDF And Text RAG

Goal: user uploads files, Byte-Bot answers from them.

Free tools:

- `pypdf`
- `sentence-transformers`
- `faiss-cpu` or `chromadb`
- SQLite for metadata

Files:

```text
backend/app/services/rag_service.py
backend/app/services/image_doc_service.py
backend/storage/uploads/
backend/storage/indexes/
```

Flow:

```text
upload PDF/text
  -> extract text
  -> split into chunks
  -> create embeddings
  -> store vectors
  -> user asks question
  -> semantic search
  -> inject top chunks into prompt
  -> answer with sources
```

Good starter embedding model:

```text
sentence-transformers/all-MiniLM-L6-v2
```

This is free and good enough for local learning.

## Phase 4: Image Understanding

Goal: user uploads an image and Byte-Bot can search/answer from it.

Start practical:

1. Use OCR first.
2. Extract visible text from the image.
3. Store OCR text like document chunks.
4. Search it the same way as PDFs.

Free tools:

- Tesseract OCR
- `pytesseract`
- `Pillow`

Later:

- CLIP embeddings for visual semantic search
- image captions
- multimodal LLM

## Phase 5: TTS

Goal: Byte-Bot speaks replies.

Beginner frontend-only option:

- Browser `speechSynthesis`

Files:

```text
script.js
```

Later backend/local option:

- Piper TTS

First frontend template:

```js
function speakReply(replyText) {
  const utterance = new SpeechSynthesisUtterance(replyText);
  utterance.rate = 1;
  utterance.pitch = 1.1;
  speechSynthesis.speak(utterance);
}
```

## Phase 6: STT

Goal: user speaks into the mic and Byte-Bot fills the chat input.

Beginner frontend-only option:

- Browser Web Speech API

Files:

```text
script.js
```

First frontend template:

```js
const recognizer = new webkitSpeechRecognition();
recognizer.lang = "en-IN";
recognizer.onresult = (event) => {
  messageTextInput.value = event.results[0][0].transcript;
};
recognizer.start();
```

Later backend/local option:

- Whisper
- faster-whisper

## Phase 7: Email Draft Tool

Goal: user asks:

```text
write a polite email to my teacher about late submission
```

Byte-Bot should draft:

- subject
- body
- recipient if known

Important: drafting is safe. Sending must require confirmation.

Free tools:

- LLM for draft
- SQLite for saved contacts

Later send options:

- Gmail SMTP
- Gmail API OAuth

## Phase 8: Discord Tool

Goal: Byte-Bot can work from Discord too.

Free tool:

- `discord.py`

Flow:

```text
Discord message
  -> same chat_service.py
  -> same memory
  -> same tools
  -> reply to Discord
```

Do not make a second brain for Discord. Discord should call the same backend logic.

## Phase 9: LangGraph

Use LangGraph when if/else routing becomes messy.

LangGraph nodes later:

```text
intent_router
load_memory
retrieve_context
choose_tool
run_tool
confirm_action
generate_reply
save_memory
```

Free tool:

- `langgraph`

Do not add it first. Add it when tool flows become multi-step.

## Phase 10: CrewAI

CrewAI is optional.

Use it only for bigger multi-agent jobs:

- research report
- blog writing
- study guide
- content planner/reviewer pipeline

Do not use CrewAI as the main Byte-Bot brain yet.

## Build Order

1. Keep current chat stable.
2. Add `services/` folder.
3. Add `router_service.py`.
4. Add `chat_service.py`.
5. Move existing chat flow from `main.py` into `chat_service.py`.
6. Add notes tool.
7. Add PDF/text RAG.
8. Add image OCR.
9. Add TTS.
10. Add STT.
11. Add email draft.
12. Add Discord.
13. Add LangGraph.
14. Add CrewAI only if needed.

## Progress Estimate

```text
Current app:             45%
Simple router/tools:     +10%
PDF/text semantic RAG:   +15%
Image OCR/search:        +8%
TTS + STT:               +10%
Email/Discord tools:     +7%
Deploy + polish:         +5%
```

After PDF/text RAG and notes, Byte-Bot will feel much closer to a real assistant.

## Template Folder

Starter files are in:

```text
blueprints/assistant_tools/
```

They are not active yet. Copy them into `backend/app/services/` when you are ready.
