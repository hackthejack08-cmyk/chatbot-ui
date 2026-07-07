# Byte-Bot Frontend

This folder contains the static frontend files for Byte-Bot.

## Files

- `index.html` - login/register page.
- `chat.html` - main chatbot page.
- `styles.css` - shared visual styling.
- `script.js` - chat, tool buttons, mascot animation, and voice output.
- `login.js` - login/register frontend logic.
- `config.js` - backend URL configuration.
- `assets/` - pixel images, gifs, fonts, and mascot files.

## Backend Address

The frontend reads the backend URL from `config.js`.

For local development, leave it blank:

```js
window.BYTEBOT_BACKEND_URL = window.BYTEBOT_BACKEND_URL || "";
```

The frontend will use:

```text
http://127.0.0.1:8010
```

## How To Run

Use the root starter:

```powershell
.\start-bytebot.ps1
```

Or double-click:

```text
start-bytebot.bat
```
