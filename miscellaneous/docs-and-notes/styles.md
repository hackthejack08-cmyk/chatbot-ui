# styles.css Explanation

`styles.css` controls the full visual design: colors, layout, pixel scene, chat bubbles, responsive behavior, and animations.

## Color Variables

```css
:root {
  --ink: #050816;
  --panel: #10182a;
  --gold: #ffc91a;
}
```

The `:root` block stores reusable colors and values. If you want to change the whole theme, start here.

## Reset Styles

```css
* {
  box-sizing: border-box;
}
```

This makes element sizing easier because padding and borders are included inside the element's width.

```css
body {
  min-height: 100vh;
  margin: 0;
}
```

This removes the browser's default page margin and makes the page fill the screen height.

## App Shell

```css
.app-shell {
  min-height: 100vh;
  overflow: hidden;
}
```

This is the full-page wrapper. It keeps the design contained and gives the whole app its dark base.

## Pixel Stage

```css
.pixel-stage {
  position: relative;
  min-height: 420px;
  overflow: hidden;
}
```

The top scene uses `position: relative` so clouds, mountains, flowers, and the bot can be positioned inside it.

## CSS-Drawn Scene

The current version uses image files in `assets/` for the main scenery.

Example:

```css
.scene-sky {
  top: 0;
  height: 64%;
  object-fit: cover;
}
```

This places the sky image at the back of the hero scene.

## Asset Scene

```css
.asset-scene {
  position: absolute;
  inset: 0;
  z-index: 0;
}
```

`.asset-scene` fills the whole hero area. All background images sit inside it.

```css
.scene-layer {
  position: absolute;
  left: 0;
  width: 100%;
  image-rendering: pixelated;
}
```

`.scene-layer` is shared by the sky, mountain, hills, and grass images.

## Chat Companion

```css
.chat-companion {
  position: sticky;
  image-rendering: pixelated;
}
```

This displays the animated companion inside the chat panel. It stays after the latest messages and can switch between different GIFs from JavaScript.

```css
.messages.is-empty .chat-companion {
  position: relative;
  width: clamp(220px, 32vw, 340px);
}
```

Before the first user prompt, the companion is centered in the message area.

## Old Scene Code

```css
.pixel-stage::before,
.pixel-stage::after {
  display: none;
}
```

The previous handmade pseudo-element overlays are disabled so they do not cover the supplied artwork. The older CSS blocks are still in the file for learning/reference.

## Hero Text

```css
h1 {
  font-family: "Press Start 2P", monospace;
  text-shadow: 5px 5px 0 var(--shadow);
}
```

This gives the heading a retro pixel-game style.

## Computer Bot

```css
.computer-bot {
  width: 144px;
  height: 156px;
  animation: bot-idle 2.4s ease-in-out infinite;
}
```

The mascot is built from small blocks: antenna, monitor, screen, neck, and base.

Small pseudo-elements add extra pixel details:

```css
.monitor::before {
  background: #dbe6f8;
}
```

This adds tiny highlights to the top of the monitor.

The default animation is `bot-idle`, which makes the computer float gently.

## State-Based Animations

```css
.computer-bot[data-state="thinking"] {
  animation: bot-think 0.6s steps(2) infinite;
}
```

JavaScript changes `data-state`. CSS reacts by switching animation.

Available states:

- `idle`
- `thinking`
- `happy`

## Chat Layout

```css
.chat-layout {
  display: grid;
  grid-template-columns: minmax(210px, 300px) minmax(0, 820px);
}
```

This creates two columns: a profile/settings panel and a main chat panel.

## Chat Panel

```css
.chat-panel {
  display: grid;
  grid-template-rows: auto minmax(300px, 52vh) auto auto;
}
```

This stacks the chat header, message area, quick prompt buttons, and input form.

## Message Bubbles

```css
.message {
  display: flex;
  animation: message-enter 260ms ease-out both;
}
```

Every new message fades and slides in because of the `message-enter` animation.

Bot and user messages have different styles:

```css
.user-message .bubble {
  background: var(--gold);
}
```

This makes user messages yellow while bot messages stay dark blue.

## Typing Indicator

```css
.typing-bubble span {
  animation: typing-dot 0.82s ease-in-out infinite;
}
```

The typing indicator is three small blocks. Each one animates with a small delay so it looks like the bot is thinking.

## Buttons And Inputs

Buttons use hover and active effects:

```css
.composer button:active {
  box-shadow: 0 2px 0 var(--gold-dark);
  transform: translateY(3px);
}
```

This makes the send button feel like a physical pixel button.

## Keyframes

`@keyframes` blocks define animations.

Example:

```css
@keyframes bot-idle {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
```

This moves the bot up and down forever. Other keyframes move the sky, mountain, hills, grass, companion, and rocket accent.

## Responsive Design

```css
@media (max-width: 850px) {
  .chat-layout {
    grid-template-columns: 1fr;
  }
}
```

On smaller screens, the sidebar and chat panel become a single column so the layout fits mobile.
