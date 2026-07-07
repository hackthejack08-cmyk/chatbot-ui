# index.html Explanation

`index.html` is the main webpage. It contains the chatbot layout, links the CSS file, and loads the JavaScript file.

## Document Setup

```html
<!DOCTYPE html>
<html lang="en">
```

This tells the browser that the file is modern HTML and that the page language is English.

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0">
```

This makes the page scale correctly on phones, tablets, and desktop screens.

## Fonts And CSS

```html
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
```

The first line loads the pixel font and normal UI font. The second line connects the page to `styles.css`.

## Main App Shell

```html
<main class="app-shell">
```

Everything visible on the page lives inside this main wrapper.

## Pixel Stage

```html
<section class="pixel-stage" aria-label="Animated chatbot scene">
```

This is the top animated scene. It contains clouds, mountains, flowers, the title text, and the computer mascot.

The current version uses your supplied image assets:

```html
<div class="asset-scene" aria-hidden="true">
  <img class="scene-layer scene-sky" src="assets/landing-sky.webp" alt="">
  <img class="scene-layer scene-mountain" src="assets/landing-mountain.webp" alt="">
  <img class="scene-layer scene-hills" src="assets/landing-hills.webp" alt="">
  <img class="scene-layer scene-grass" src="assets/landing-grass.webp" alt="">
</div>
```

These images stack like layers in a game background: sky at the back, mountains behind, hills in the middle, and grass in front.

The previous handmade CSS scene is still kept as a comment:

```html
<!--
  OLD HANDMADE CSS SCENE
  Kept here for learning and easy rollback.
-->
```

It is commented out, so the browser ignores it, but you can still read it and learn from it.

The chat section has an interactive companion button:

```html
<button class="chat-companion" id="chatCompanion" type="button">
  <img id="companionImage" src="assets/coding-window.gif" alt="">
</button>
```

JavaScript randomly changes `#companionImage` after replies and companion clicks.

## Hero Copy

```html
<div class="hero-copy">
  <p class="eyebrow">local frontend only</p>
  <h1>ByteBuddy</h1>
  <p>A tiny computer friend with big emoticon energy.</p>
</div>
```

This is the main title area. You can rename the bot by changing `ByteBuddy`.

## Computer Mascot

```html
<div class="computer-bot" id="computerBot" data-state="idle">
```

This is the animated computer chatbot. The `id` lets JavaScript find it. The `data-state` controls which animation is active.

The face is here:

```html
<span id="botFace">uwu</span>
```

JavaScript changes this text to random anime-style ASCII emoticons.

## Status Panel

```html
<p id="botMood">idle and listening</p>
```

This small label shows the bot's current mood. JavaScript updates it when the bot is thinking or happy.

## Chat Layout

```html
<section class="chat-layout" aria-label="Chatbot demo">
```

This holds the lower part of the interface: the settings card and the chat panel.

## Profile Panel

```html
<aside class="profile-panel">
```

This sidebar explains the fixed personality. It is visual only and has no backend logic.

## Chat Panel

```html
<section class="chat-panel">
```

This is the actual chat UI. It contains the header, messages, quick prompt buttons, and message form.

## Messages Area

```html
<div class="messages" id="messages" aria-live="polite">
```

JavaScript adds new chat messages inside this container. `aria-live="polite"` helps screen readers notice updates without interrupting the user.

## Quick Prompts

```html
<button type="button" data-prompt="What can you do?">What can you do?</button>
```

Each quick prompt has a `data-prompt` value. JavaScript reads that value and sends it like a normal message.

## Composer Form

```html
<form class="composer" id="chatForm">
```

This is the input area. When the user submits it, JavaScript catches the event and adds the message to the UI.

## JavaScript Link

```html
<script src="script.js"></script>
```

This loads the chat behavior after the page markup is ready.
