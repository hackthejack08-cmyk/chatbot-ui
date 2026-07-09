# Local Whisper Voice Input

Byte-Bot now uses **local Whisper** for voice-to-text, so you do **not** need an `OPENAI_API_KEY` for transcription.

## What changed?

Old flow:

```text
audio file -> backend -> OpenAI Whisper API -> text
```

Problem: this needed a paid OpenAI API key.

New flow:

```text
audio file -> backend -> local faster-whisper model -> text
```

This runs on your computer/server. The first use downloads the model once.

## Files accepted by voice input

The voice input button accepts:

```text
.mp3
.wav
.m4a
.webm
.ogg
.flac
.aac
.mp4
.mpeg
.mpga
```

Most browser recordings are usually `.webm`. Phone recordings are often `.m4a`. Normal audio files are usually `.mp3` or `.wav`.

## Environment settings

These are in `.env`:

```env
LOCAL_WHISPER_MODEL=tiny
LOCAL_WHISPER_DEVICE=cpu
LOCAL_WHISPER_COMPUTE_TYPE=int8
LOCAL_WHISPER_LANGUAGE=
```

Meaning:

- `LOCAL_WHISPER_MODEL=tiny` keeps it fast and light for CPU.
- `LOCAL_WHISPER_DEVICE=cpu` means it does not need a GPU.
- `LOCAL_WHISPER_COMPUTE_TYPE=int8` makes CPU transcription lighter.
- `LOCAL_WHISPER_LANGUAGE=` blank means auto-detect language.

If you want English only later, use:

```env
LOCAL_WHISPER_LANGUAGE=en
```

## How the code works

The frontend button is in:

```text
frontend/chat.html
```

The frontend upload logic is in:

```text
frontend/script.js
```

When you click `Voice input`, JavaScript opens a file picker, sends the audio file to:

```text
POST /tools/transcribe
```

The backend route is in:

```text
backend/app/tool_routes.py
```

That route:

1. Checks if the file extension is audio.
2. Saves the uploaded file temporarily.
3. Loads the local Whisper model using `faster_whisper.WhisperModel`.
4. Calls `model.transcribe(...)`.
5. Joins the returned text segments into one transcript.
6. Deletes the temporary audio file.
7. Sends the text back to the frontend.

## Important note

Local Whisper is good for your project because it is free, but it is heavier than a normal API call. The first transcription can be slow because the model downloads and loads for the first time.
