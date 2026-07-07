# assets/ Explanation

The `assets/` folder stores images, GIFs, and the local pixel font used by the frontend.

## Font

```text
pixelgrid-squarebolds.woff
```

This is loaded in `styles.css` with `@font-face` and used for pixel-style headings, buttons, labels, and avatars.

## Hero Background

```text
landing-sky.webp
landing-mountain.webp
landing-hills.webp
landing-grass.webp
```

These files create the layered pixel-art hero background. CSS stacks them in `.asset-scene`.

## Chat Companion GIFs

```text
coding-window.gif
bytebuddy-team.gif
bytebuddy-rocket.gif
```

These are the animated companion sprites used inside the chat panel. `script.js` randomly switches between them with `randomizeCompanionSprite()`.

## Side Accent

```text
bytebuddy-rocket.gif
```

The rocket GIF also appears in the settings panel as a decorative accent.

## Tool Icon

```text
upload-toolkit.png
```

This is the upload/document icon used by the chat tool dock. It represents PDF, CSV, text, image, and voice upload features.

## `web-search-tool.png`

This is the pixel-art image used by the `Web search` tool button in `chat.html`.

## `voice-output-tool.png`

This is the pixel-art image used by the `Voice output` toggle. The button turns browser text-to-speech on or off.

## `voice-search-tool.png`

This is the pixel-art image used by the `Voice input` tile. That tile is for future speech-to-text / Whisper input.

## Unused / Optional Assets

```text
landing-mascot.webp
landing-title.gif
```

These are kept in the folder for experimentation, but they are not required by the current active UI.
