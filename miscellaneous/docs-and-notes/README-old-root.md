# Byte-Bot Chat UI

Byte-Bot is a pixel-style chatbot interface with a cute computer personality, FastAPI backend, SQLite memory, reset support, and a simple place for future local RAG.

## Current Status

The UI is built, the backend runs on `8010`, and the frontend runs on `8028`. The bot can answer through Groq/LangChain when configured, and it has a local fallback path for development.

## File Structure

```text
chatbot-ui/
  frontend/      Active static frontend for local serving and hosting
  index.html     Page structure
  index.md       Explanation for index.html
  styles.css     Visual design, layout, and animations
  styles.md      Explanation for styles.css
  script.js      Demo chat behavior and bot mood states
  script.md      Explanation for script.js
  assets.md      Explanation for image, GIF, and font assets
  MERGE.md       Backend merge and scaling guide
  PROGRESS.md     Full summary of what we built so far
  ERRORS.md       Error and fix comparison notes
  FINAL_PROJECT_EXPLANATION.md  Teacher-style project explanation
  TOOLS_AND_HOSTING_ROADMAP.md  Future search, upload, voice, RAG, hosting plan
  assets/        Pixel-art scene assets copied from your downloaded files
  README.md      Project overview and setup notes
```

## How To Run

From the project folder, run everything with one command:

```bash
.\start-bytebot.ps1
```

That starts:

- backend from the project root
- frontend from `frontend/`

Open:

```text
http://127.0.0.1:8028/chat.html
```

## What The UI Includes

- Pixel-inspired hero scene based on your reference style.
- Cute computer mascot with anime-style ASCII emoticon faces.
- Idle, thinking, typing, and happy animation states.
- Clean night hero background using your supplied `github-copilots.gif`.
- Old sky, mountain, hills, and grass scene layers are kept commented in `chat.html` for rollback.
- Demo chat messages with animated message bubbles.
- Chat companion GIF that stays after the latest message and randomly changes sprites.
- Quick prompt buttons.
- Reset button.
- Responsive desktop and mobile layout.

## How The Animation Works

The active hero scene uses one clean full-screen GIF layer:

```html
<img class="scene-layer scene-night" src="assets/github-copilots.gif" alt="">
```

CSS makes this image fill the full hero with `object-fit: cover`, so it avoids horizontal cuts on different screen sizes.

The chat companion uses `#chatCompanion` and `#companionImage`. JavaScript changes the image randomly between:

```js
const companionSprites = [
  "assets/coding-window.gif",
  "assets/bytebuddy-team.gif",
  "assets/bytebuddy-rocket.gif"
];
```

The mascot animation is controlled by the `data-state` attribute on `#computerBot`.

```html
<div class="computer-bot" id="computerBot" data-state="idle">
```

CSS reads that state:

```css
.computer-bot[data-state="thinking"] {
  animation: bot-think 0.6s steps(2) infinite;
}
```

JavaScript changes the state:

```js
computerBot.dataset.state = "thinking";
```

That means the visual personality is separated from the chat logic. This makes it easier to connect your real chatbot later.

## How To Connect LangChain Later

In `script.js`, replace `getDemoReply(userText)` with a real async API call.

Example shape:

```js
async function getRealReply(userText) {
  const response = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userText })
  });

  const data = await response.json();
  return data.reply;
}
```

Then update `handleSubmit()` so it waits for your backend reply instead of using the demo reply.

## How To Change The Personality

In `script.js`, edit the `faces` object:

```js
const faces = {
  idle: ["uwu", "owo", "^-^", "-w-"],
  thinking: ["o_O", "?w?", "...?", "@_@"],
  happy: [">w<", "^o^", "\\o/", "*w*"]
};
```

You can also edit:

- `demoReplies` for fake bot responses.
- `botMood.textContent` values inside the mood functions.
- The intro message in `index.html`.

## How To Change Colors

In `styles.css`, edit the variables at the top:

```css
:root {
  --ink: #050816;
  --gold: #ffc91a;
  --blue: #1fb6ff;
  --green: #6bd66f;
  --pink: #ff7bc8;
}
```

These variables control the main color system across the whole UI.

## Beginner Notes

- `index.html` creates the page.
- `styles.css` makes it look alive.
- `script.js` makes it act like a chat.
- `assets/` stores the image files used by the hero scene.
- `MERGE.md` explains how to connect the UI to a real backend.
- `ROADMAP.md` explains what is done, what is left, and which free tools to use.
- The `.md` files explain each source file in more detail.
## Current Production Upgrade

Byte-Bot now has the beginning of a real scalable app setup:

- FastAPI backend on port `8010`
- Netlify-ready static frontend
- Render-ready backend config
- MongoDB Atlas support for users and chat memory
- Email/password registration and login
- Email/password login through MongoDB
- JWT token storage in the browser
- SQLite fallback when MongoDB is not configured
- Optional tool routes for SerpApi search, document upload, web-page loading, and Whisper transcription

Main new files:

- `frontend/` contains the active static frontend for hosting and local UI.
- `config.js` controls the backend URL used by the frontend.
- `.env.example` shows the backend secrets you need.
- `netlify.toml` prepares the static site for Netlify.
- `render.yaml` prepares the FastAPI backend for Render.
- `DEPLOYMENT_PRODUCTION.md` explains hosting step by step.
- `backend/app/auth_routes.py` contains auth API routes.
- `backend/app/auth_service.py` creates users and checks login.
- `backend/app/database.py` connects to MongoDB.
- `backend/app/mongo_memory.py` stores chat history in MongoDB.
- `backend/app/tool_routes.py` contains optional search, upload, and voice-to-text routes.
- `FINAL_PROJECT_EXPLANATION.md` explains the whole project in beginner/teacher-review language.

If MongoDB is not configured yet, the UI can still continue in local demo mode. Once you add `MONGODB_URI`, login/register becomes real.

## Current Local Run Commands

Recommended one-command startup:

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
.\start-bytebot.ps1
```

Or double-click:

```text
start-bytebot.bat
```

The starter runs the FastAPI backend from the project root and the static frontend from `frontend/`.

Manual option:

Open two terminals in:

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
```

Terminal 1, start FastAPI:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8010
```

Terminal 2, start the frontend:

```powershell
.\.venv\Scripts\python.exe -m http.server 8028 --bind 127.0.0.1
```

Then open:

```text
http://127.0.0.1:8028/chat.html
```

## Frontend Folder

The project now has a separated frontend folder:

```text
frontend/
  index.html
  chat.html
  styles.css
  script.js
  login.css
  login.js
  config.js
  assets/
```

The older root-level frontend files were kept and not deleted. The active local starter and Netlify config now use `frontend/`.

## Voice Output

The chat page has a `Voice output` button. When it is on, Byte-Bot speaks new bot replies using the browser `speechSynthesis` API.

This is different from voice input:

- Voice output: browser reads bot replies aloud.
- Voice input: user audio to text, which still needs `OPENAI_API_KEY` or another transcription provider.
