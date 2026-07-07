# Merge Guide

This file explains how to merge the static ByteBuddy UI with your real chatbot backend later.

## Current Frontend Flow

The frontend is static right now.

```text
User types message
script.js catches form submit
addMessage("user", text) renders user bubble
addTypingMessage() renders typing dots
getDemoReply(text) returns fake reply
addMessage("bot", reply) renders bot bubble
```

The function to replace is:

```js
function getDemoReply(userText) {
```

## Recommended Backend Shape

Use a small backend endpoint:

```text
POST /chat
```

Request:

```json
{
  "message": "hello",
  "sessionId": "local-demo"
}
```

Response:

```json
{
  "reply": "Hi, I am ByteBuddy uwu"
}
```

## Frontend Merge Step

Add this function in `script.js`:

```js
async function getBackendReply(userText) {
  const response = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      message: userText,
      sessionId: "local-demo"
    })
  });

  const data = await response.json();
  return data.reply;
}
```

Then change the submit flow from:

```js
addMessage("bot", getDemoReply(text));
```

To:

```js
const reply = await getBackendReply(text);
addMessage("bot", reply);
```

Because that uses `await`, the callback around it must become `async`.

## Scalable File Direction

When the project grows, split `script.js` into smaller files:

```text
scripts/
  chat.js        message rendering and form submit
  api.js         backend calls
  companion.js   sprite switching and animation state
  config.js      URLs, session id, feature flags
```

Keep these responsibilities separate:

- UI rendering: message bubbles, typing indicator, reset.
- Backend API: `fetch()` calls only.
- Personality: backend system prompt, not hardcoded frontend text.
- Memory: backend database, not browser-only storage.
- Companion visuals: frontend-only animation state.

## Suggested Backend Stack

For your LangChain chatbot:

```text
Python + FastAPI
LangChain chatbot code
SQLite first, PostgreSQL later
Frontend fetch() to /chat
```

## Minimal FastAPI Contract

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    sessionId: str | None = None

@app.post("/chat")
async def chat(request: ChatRequest):
    reply = "Replace this with your LangChain response"
    return {"reply": reply}
```

## Things To Add Later

- Streaming replies.
- Real memory per user/session.
- Voice input.
- Text-to-speech.
- Real auth if users save history.
- Error messages when backend is offline.
