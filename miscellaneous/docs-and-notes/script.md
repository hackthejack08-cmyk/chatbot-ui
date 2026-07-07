# script.js Explanation

`script.js` makes the UI behave like a chatbot demo. It does not call a real backend yet.

## Selecting HTML Elements

```js
const messages = document.querySelector("#messages");
const chatForm = document.querySelector("#chatForm");
const messageInput = document.querySelector("#messageInput");
```

These lines find important elements from `index.html` so JavaScript can read or change them.

## Bot Faces

```js
const faces = {
  idle: ["uwu", "owo", "^-^", "-w-"],
  thinking: ["o_O", "?w?", "...?", "@_@"],
  happy: [">w<", "^o^", "\\o/", "*w*"]
};
```

This object stores anime-style ASCII emoticon faces for each mood. Change these arrays to change the computer's personality.

## Demo Replies

```js
const demoReplies = [
  "I am a frontend-only demo right now..."
];
```

These are fake replies. They make the interface feel alive before you connect the real LangChain chatbot. The wording also matches the cute personality.

## Event Listeners

```js
chatForm.addEventListener("submit", handleSubmit);
resetChat.addEventListener("click", resetConversation);
```

Event listeners tell JavaScript what to do when the user submits the form or clicks reset.

## Quick Prompt Buttons

```js
quickPrompts.forEach((button) => {
  button.addEventListener("click", () => {
    messageInput.value = button.dataset.prompt;
    submitChatForm();
  });
});
```

Each quick prompt button copies its `data-prompt` value into the input, then submits the form.

`submitChatForm()` supports browsers that do not have `requestSubmit()`.

## Form Submit Flow

```js
function handleSubmit(event) {
  event.preventDefault();
  const text = messageInput.value.trim();
}
```

`event.preventDefault()` stops the page from refreshing. `trim()` removes empty space from the start and end of the message.

The full flow is:

1. Read the user text.
2. Add the user message.
3. Clear the input.
4. Put the bot into thinking mode.
5. Show a typing indicator.
6. Wait briefly.
7. Remove typing indicator.
8. Add a bot reply.
9. Move the companion after the latest message.
10. Randomly switch the companion GIF.
11. Show the happy animation.

## Adding Messages

```js
function addMessage(sender, text) {
  const message = document.createElement("article");
  message.className = `message ${sender}-message`;
}
```

This function creates new message HTML with JavaScript. The `sender` decides whether it looks like a user message or bot message.

```js
paragraph.textContent = text;
```

`textContent` is used instead of `innerHTML` for normal messages. That is safer because the browser treats the text as text, not code.

## Typing Indicator

```js
function addTypingMessage() {
  const message = document.createElement("article");
}
```

This creates a temporary bot message that contains three animated dots. It gets removed before the final bot reply appears.

## Demo Reply Logic

```js
function getDemoReply(userText) {
  const lowerText = userText.toLowerCase();
}
```

This function checks the user's message and returns a fake response. For example, if the user mentions LangChain, it returns a connection hint.

This is the main function to replace when you connect a real backend.

## Bot Mood Functions

```js
function showBotThinking() {
  computerBot.dataset.state = "thinking";
  botFace.textContent = pickFace("thinking");
}
```

This changes the bot's CSS state and face. The CSS file sees `data-state="thinking"` and runs the thinking animation.

```js
function showBotHappy() {
  computerBot.dataset.state = "happy";
}
```

This starts the happy animation after a reply is shown.

## Random Face Picker

```js
function pickFace(type) {
  const set = faces[type];
  return set[Math.floor(Math.random() * set.length)];
}
```

This picks one random face from the correct mood list. That randomness helps the fixed personality feel less static.

## Companion Sprites

```js
const companionSprites = [
  "assets/coding-window.gif",
  "assets/bytebuddy-team.gif",
  "assets/bytebuddy-rocket.gif"
];
```

This list controls which animated computer/character GIFs can appear in the chat panel.

```js
function randomizeCompanionSprite() {
  const randomIndex = Math.floor(Math.random() * companionSprites.length);
  companionImage.src = companionSprites[randomIndex];
}
```

This picks one GIF and updates the visible companion image.

## Reset Conversation

```js
function resetConversation() {
  messages.innerHTML = "";
  messages.append(chatCompanion);
  messages.classList.add("is-empty");
  addMessage("bot", "Chat reset! I am ready for a fresh little adventure. uwu");
}
```

This clears the chat and adds a fresh starting message.

## Auto Scroll

```js
function scrollToLatestMessage() {
  messages.scrollTop = messages.scrollHeight;
}
```

This keeps the newest message visible after messages are added.
