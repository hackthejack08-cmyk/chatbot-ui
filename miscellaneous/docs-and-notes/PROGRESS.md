# Byte-Bot Progress Log

This file is the full summary of what we have built so far.

## What We Built

- A pixel-art chatbot UI called `Byte-Bot`.
- A hero scene with layered art:
  - `landing-sky.webp`
  - `landing-mountain.webp`
  - `landing-hills.webp`
  - `landing-grass.webp`
- A cute robot mascot with animated mood states.
- A chat panel with:
  - user messages
  - bot messages
  - typing indicator
  - quick prompt buttons
  - reset button
  - companion GIF that changes randomly
- A custom pixel font using `assets/pixelgrid-squarebolds.woff`.
- Documentation files for the code and assets.
- A backend scaffold using FastAPI.

## Files In The Project

- `index.html` - page structure
- `styles.css` - layout and animation styling
- `script.js` - chat behavior and UI logic
- `backend/app/main.py` - FastAPI backend
- `backend/app/schemas.py` - request and response models
- `README.md` - overall project notes
- `MERGE.md` - how frontend and backend should connect
- `ERRORS.md` - what broke and how it was fixed
- `assets.md` - asset explanations
- `index.md` - explanation of the HTML file
- `styles.md` - explanation of the CSS file
- `script.md` - explanation of the JavaScript file

## Current Behavior

The frontend sends chat messages to:

```text
http://127.0.0.1:8000/chat
```

The backend now has two modes:

1. Real model mode, when `langchain_groq` and `GROQ_API_KEY` are available.
2. Local fallback mode, when the real model is not installed yet.

That means the bot can still answer locally while you are building the final AI stack.

## What We Already Solved

- Renamed the visible product from `ByteBuddy` to `Byte-Bot`.
- Fixed a fullscreen/layout issue in the hero and chat composition.
- Added random sprite switching in the chat companion.
- Added comments and learning notes in the code.
- Fixed the backend crash caused by a missing dependency/import path.
- Fixed the backend environment-variable check so the app can start cleanly.

## Current Workflow

1. Keep the UI stable.
2. Keep the backend runnable.
3. Use fallback replies until the real model is ready.
4. Merge in LangChain, memory, voice input, and TTS later.

## Next Steps

- Install the real backend dependencies.
- Add your GROQ API key.
- Replace fallback behavior with the final chatbot logic.
- Add memory storage.
- Add voice recognition and TTS.
- Split backend logic into cleaner files when it grows.
