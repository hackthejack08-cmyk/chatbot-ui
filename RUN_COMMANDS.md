# Byte-Bot Run Commands

Open PowerShell in this folder:

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui"
```

## Start frontend and backend together

```powershell
.\start-bytebot.ps1
```

If PowerShell blocks the script:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-bytebot.ps1
```

Then open:

```text
http://127.0.0.1:8028/chat.html
```

Backend health check:

```text
http://127.0.0.1:8010/health
```

## Manual backend command

```powershell
.\backend\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8010
```

## Install / repair local Whisper voice input

Voice input now uses free local Whisper through `faster-whisper`.

```powershell
.\backend\.venv\Scripts\python.exe -m pip install faster-whisper
```

The first voice transcription downloads the tiny model once. Accepted voice files:

```text
.mp3, .wav, .m4a, .webm, .ogg, .flac, .aac, .mp4, .mpeg, .mpga
```

## Manual frontend command

Open another PowerShell terminal:

```powershell
cd "C:\Users\HARSH TIWARI\Documents\Codex\2026-07-02\h\outputs\chatbot-ui\frontend"
..\backend\.venv\Scripts\python.exe -m http.server 8028 --bind 127.0.0.1
```
