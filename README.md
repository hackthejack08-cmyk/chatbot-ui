# Byte-Bot Project

This is the cleaned project root for Byte-Bot.

The active project is organized into three main folders:

```text
chatbot-ui/
  frontend/        active HTML, CSS, JS, assets, and Vercel config
  backend/         FastAPI backend, Python modules, requirements, local venv, storage
  miscellaneous/   old UI copies, old notes, generated files, presentation files, dumps
```

Important root files:

```text
README_ULTRA_FINAL.md   full teacher/interview/project explanation
DEPLOYMENT.md           deployment steps for frontend, backend, MongoDB, and env vars
start-bytebot.ps1       one-command local starter for backend + frontend
start-bytebot.bat       double-click Windows starter
render.yaml             Render backend blueprint
netlify.toml            optional Netlify frontend config
.env.example            example backend environment file
```

## Run Locally

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
.\start-bytebot.ps1
```

If PowerShell blocks scripts:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-bytebot.ps1
```

Open:

```text
http://127.0.0.1:8028/chat.html
```

Backend health:

```text
http://127.0.0.1:8010/health
```

## Why There Is A Miscellaneous Folder

Nothing useful was deleted. Old root UI files, older explanations, generated presentation files, and previous drafts were moved into `miscellaneous/` so the main project is easier to understand.

The app uses `frontend/` and `backend/` now.

## Notes

If `Byte-Bot_Project_Presentation.pptx` is still visible in the root, it means PowerPoint is currently holding that file open. Close PowerPoint and move it to:

```text
miscellaneous/presentation-files/
```
