const chatMessagesBox = document.querySelector("#messages");
const sendMessageForm = document.querySelector("#chatForm");
const messageTextInput = document.querySelector("#messageInput");
const topBotFaceText = document.querySelector("#botFace");
const topBotStatusText = document.querySelector("#botMood");
const sideBotFaceText = document.querySelector("#profileBotFace");
const sideBotStatusText = document.querySelector("#profileBotMood");
const topBotBox = document.querySelector("#computerBot");
const resetChatButton = document.querySelector("#resetChat");
const quickPromptList = document.querySelectorAll("[data-prompt]");
const chatMascotButton = document.querySelector("#chatCompanion");
const chatMascotImage = document.querySelector("#companionImage");
const sessionNameText = document.querySelector("#sessionLabel");
const welcomeText = document.querySelector("#introMessage");
const heroBotButton = document.querySelector("#heroBotButton");
const chatSection = document.querySelector("#chatSection");
const uploadToolButton = document.querySelector("#uploadToolButton");
const webSearchButton = document.querySelector("#webSearchButton");
const imageSearchButton = document.querySelector("#imageSearchButton");
const voiceToolButton = document.querySelector("#voiceToolButton");
const voiceOutputButton = document.querySelector("#voiceOutputToggle");
const voiceOutputStateText = document.querySelector("#voiceOutputState");
const knowledgeFileInput = document.querySelector("#knowledgeFileInput");
const toolStatusText = document.querySelector("#toolStatus");

const savedBackendUrl = localStorage.getItem("bytebot_api_base_url");
const savedAccessToken = localStorage.getItem("bytebot_access_token");
const isLocalFrontend =
  window.location.protocol === "file:" ||
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost";

const configuredBackendUrl = (window.BYTEBOT_BACKEND_URL || "").trim();
const defaultBackendUrl = isLocalFrontend
  ? "http://127.0.0.1:8010"
  : window.location.origin;

const backendUrl = configuredBackendUrl || savedBackendUrl || defaultBackendUrl;
const chatUrl = `${backendUrl}/chat`;
const resetUrl = `${backendUrl}/reset`;
const healthUrl = `${backendUrl}/health`;
const uploadUrl = `${backendUrl}/tools/upload`;
const transcribeUrl = `${backendUrl}/tools/transcribe`;
const googleSearchUrl = `${backendUrl}/tools/search/google`;
const imageSearchUrl = `${backendUrl}/tools/search/images`;

const currentSessionId = localStorage.getItem("bytebot_session_id") || "bytebot-guest";
const currentUserName = localStorage.getItem("bytebot_user_label") || "guest";

// Add future mascot assets here later.
const mascotImageList = [
  "assets/coding-window.gif",
  "assets/bytebuddy-team.gif"
];

const botFaceByMood = {
  idle: ["uwu", "owo", "^-^", "-w-"],
  thinking: ["o_O", "?w?", "...?", "@_@"],
  happy: [">w<", "^o^", "\\o/", "*w*"]
};

let chatHasStarted = false;
let idleFaceLoop = null;
let isVoiceOutputEnabled = localStorage.getItem("bytebot_voice_output_enabled") === "true";
let selectedSendMode = "chat";

if (chatMessagesBox && sendMessageForm && messageTextInput) {
  if (sessionNameText) {
    sessionNameText.textContent = `Local session: ${currentUserName}`;
  }

  if (welcomeText) {
    welcomeText.textContent = `Hi ${currentUserName}, I am Byte-Bot. I am ready to remember this session and chat through the backend. uwu`;
  }

  idleFaceLoop = window.setInterval(showIdleFace, 2600);

  sendMessageForm.addEventListener("submit", handleSendMessage);
  resetChatButton?.addEventListener("click", handleResetChat);
  heroBotButton?.addEventListener("click", scrollToChatSection);
  chatMascotButton?.addEventListener("click", handleMascotTap);
  uploadToolButton?.addEventListener("click", () => openFilePicker("knowledge"));
  voiceToolButton?.addEventListener("click", () => openFilePicker("voice"));
  knowledgeFileInput?.addEventListener("change", handlePickedFile);
  webSearchButton?.addEventListener("click", () => setSendMode("web"));
  imageSearchButton?.addEventListener("click", () => setSendMode("image"));
  voiceOutputButton?.addEventListener("click", handleVoiceOutputToggle);
  updateVoiceOutputButton();
  updateSendModeButtons();

  quickPromptList.forEach((quickButton) => {
    quickButton.addEventListener("click", () => {
      messageTextInput.value = quickButton.dataset.prompt;
      submitMessageForm();
    });
  });

  checkBackendHealth();
}

function scrollToChatSection() {
  chatSection?.scrollIntoView({ behavior: "smooth", block: "start" });
  window.setTimeout(() => {
    messageTextInput?.focus();
  }, 650);
}

function getAuthHeaders() {
  if (!savedAccessToken) {
    return {};
  }

  return { Authorization: `Bearer ${savedAccessToken}` };
}

function getJsonHeaders() {
  return {
    "Content-Type": "application/json",
    ...getAuthHeaders()
  };
}

async function checkBackendHealth() {
  try {
    const backendHealthResponse = await fetch(healthUrl);

    if (!backendHealthResponse.ok) {
      throw new Error(`Health check returned ${backendHealthResponse.status}`);
    }

    setBotStatus("idle and listening");
  } catch (error) {
    console.error("Byte-Bot health check error:", error);
    setBotStatus("backend offline");
  }
}

async function getReplyFromBackend(userMessageText) {
  try {
    const chatResponse = await fetch(chatUrl, {
      method: "POST",
      headers: getJsonHeaders(),
      body: JSON.stringify({
        message: userMessageText,
        session_id: currentSessionId
      })
    });

    if (!chatResponse.ok) {
      const errorData = await chatResponse.json().catch(() => ({}));
      throw new Error(errorData.detail || `Backend returned ${chatResponse.status}`);
    }

    const replyData = await chatResponse.json();
    return replyData.reply;
  } catch (error) {
    console.error("Byte-Bot backend error:", error);
    setBotStatus("backend offline");
    return `Byte-Bot could not reach the backend at ${backendUrl}. ${error.message}`;
  }
}

function openFilePicker(toolMode) {
  if (!knowledgeFileInput) {
    return;
  }

  knowledgeFileInput.dataset.toolMode = toolMode;
  knowledgeFileInput.accept = toolMode === "voice"
    ? ".mp3,.wav,.m4a,.webm,.ogg"
    : ".pdf,.csv,.txt,.md,.png,.jpg,.jpeg,.webp,.gif";
  knowledgeFileInput.value = "";
  knowledgeFileInput.click();
}

async function handlePickedFile() {
  const pickedFile = knowledgeFileInput?.files?.[0];

  if (!pickedFile) {
    return;
  }

  const toolMode = knowledgeFileInput.dataset.toolMode || "knowledge";
  const targetUrl = toolMode === "voice" ? transcribeUrl : uploadUrl;
  const formData = new FormData();
  formData.append("file", pickedFile);

  showToolStatus(`Uploading ${pickedFile.name}...`);
  showThinkingMode();

  try {
    const response = await fetch(targetUrl, {
      method: "POST",
      headers: getAuthHeaders(),
      body: formData
    });
    const responseData = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(responseData.detail || `Tool returned ${response.status}`);
    }

    if (toolMode === "voice") {
      const spokenText = responseData.text || "";
      messageTextInput.value = spokenText;
      showToolStatus("Voice converted into text. Review it, then press Send.", false, true);
      markChatAsStarted();
      addChatMessage("bot", spokenText ? `I heard: ${spokenText}` : "Voice uploaded, but no text came back.");
    } else {
      const previewText = responseData.preview ? ` Preview: ${responseData.preview}` : "";
      showToolStatus(responseData.message || "File uploaded.", false, true);
      markChatAsStarted();
      addChatMessage("bot", `${responseData.file_name} is ready. ${responseData.chunks_created || 0} chunks created.${previewText}`);
    }

    showHappyMode();
  } catch (error) {
    console.error("Byte-Bot tool upload error:", error);
    showToolStatus(error.message, true);
    markChatAsStarted();
    addChatMessage("bot", `Tool setup note: ${error.message}`);
    if (topBotBox) {
      topBotBox.dataset.state = "idle";
    }
    setBotStatus("tool needs setup");
  }
}

async function getSearchReply(searchType, queryText) {
  const searchUrl = searchType === "image" ? imageSearchUrl : googleSearchUrl;
  showToolStatus(`Searching for "${queryText}"...`);

  try {
    const response = await fetch(searchUrl, {
      method: "POST",
      headers: getJsonHeaders(),
      body: JSON.stringify({ query: queryText })
    });
    const responseData = await response.json().catch(() => ({}));

    if (!response.ok) {
      throw new Error(responseData.detail || `Search returned ${response.status}`);
    }

    showToolStatus("Search complete.", false, true);
    return makeSearchSummary(responseData, searchType);
  } catch (error) {
    console.error("Byte-Bot search tool error:", error);
    showToolStatus(error.message, true);
    setBotStatus("search needs setup");
    return `Search setup note:\n${error.message}`;
  }
}

function makeSearchSummary(searchData, searchType) {
  const results = searchData.results || [];
  const searchLabel = searchType === "image" ? "image" : "web";
  const queryText = cleanResultText(searchData.query || "your query", 90);

  if (!results.length) {
    return `I searched ${searchLabel}, but no results came back.`;
  }

  const strongestResult = results[0] || {};
  const contextTitle = cleanResultText(strongestResult.title || "the first result", 90);
  const contextSnippet = cleanResultText(strongestResult.snippet || "", 190);
  const contextLine = searchType === "image"
    ? `I searched images for "${queryText}". These are visual leads, so open the source link before trusting or using an image.`
    : `I searched the web for "${queryText}". Quick context: the strongest result I found is "${contextTitle}"${contextSnippet ? `, and it says ${contextSnippet}` : ""}. Check the source/date before treating it as final.`;

  const resultLines = results.slice(0, 4).map((result, index) => {
    const title = cleanResultText(result.title || "Untitled result", 86);
    const link = result.link || "No link available";
    const snippet = cleanResultText(result.snippet || "", 150);
    const thumbnail = result.thumbnail ? `\n   Image: ${result.thumbnail}` : "";
    const note = snippet ? `\n   Note: ${snippet}` : "";
    return `${index + 1}. ${title}\n   Link: ${link}${note}${thumbnail}`;
  });

  return `${contextLine}\n\nTop ${searchLabel} results:\n\n${resultLines.join("\n\n")}`;
}

function cleanResultText(text, maxLength) {
  const compactText = String(text)
    .replace(/Â·/g, "-")
    .replace(/â|â/g, "-")
    .replace(/â/g, "'")
    .replace(/â|â/g, '"')
    .replace(/\s+/g, " ")
    .trim();

  if (compactText.length <= maxLength) {
    return compactText;
  }

  return `${compactText.slice(0, maxLength - 3).trim()}...`;
}

function setSendMode(nextMode) {
  selectedSendMode = nextMode;
  updateSendModeButtons();

  if (nextMode === "web") {
    showToolStatus("Web search enabled for the next Send. Type a keyword, then press Send.");
    messageTextInput?.focus();
    return;
  }

  if (nextMode === "image") {
    showToolStatus("Image search enabled for the next Send. Type a keyword, then press Send.");
    messageTextInput?.focus();
    return;
  }

  showToolStatus("Tools are optional. Chat works without them.");
}

function updateSendModeButtons() {
  webSearchButton?.classList.toggle("is-active", selectedSendMode === "web");
  imageSearchButton?.classList.toggle("is-active", selectedSendMode === "image");
}

function showToolStatus(message, isError = false, isSuccess = false) {
  if (!toolStatusText) {
    return;
  }

  toolStatusText.textContent = message;
  toolStatusText.classList.toggle("is-error", isError);
  toolStatusText.classList.toggle("is-success", isSuccess);
}

async function handleSendMessage(event) {
  event.preventDefault();
  const userMessageText = messageTextInput.value.trim();

  if (!userMessageText) {
    return;
  }

  addChatMessage("user", userMessageText);
  markChatAsStarted();
  messageTextInput.value = "";
  showThinkingMode();

  const typingMessageRow = addTypingMessage();
  const sendModeForThisMessage = selectedSendMode;
  const botReplyText = sendModeForThisMessage === "web" || sendModeForThisMessage === "image"
    ? await getSearchReply(sendModeForThisMessage, userMessageText)
    : await getReplyFromBackend(userMessageText);

  typingMessageRow.remove();
  addChatMessage("bot", botReplyText);
  speakBotReply(botReplyText);
  moveMascotToBottom();
  swapMascotImage();
  showHappyMode();

  if (sendModeForThisMessage !== "chat") {
    setSendMode("chat");
  }
}

function handleVoiceOutputToggle() {
  isVoiceOutputEnabled = !isVoiceOutputEnabled;
  localStorage.setItem("bytebot_voice_output_enabled", String(isVoiceOutputEnabled));
  updateVoiceOutputButton();

  if (isVoiceOutputEnabled) {
    showToolStatus("Voice output enabled. Byte-Bot will speak new replies.", false, true);
    speakBotReply("Voice output enabled. Byte-Bot is ready to talk.");
  } else {
    window.speechSynthesis?.cancel();
    showToolStatus("Voice output disabled.");
  }
}

function updateVoiceOutputButton() {
  if (!voiceOutputButton) {
    return;
  }

  voiceOutputButton.classList.toggle("is-active", isVoiceOutputEnabled);
  voiceOutputButton.setAttribute("aria-pressed", String(isVoiceOutputEnabled));

  if (voiceOutputStateText) {
    voiceOutputStateText.textContent = isVoiceOutputEnabled ? "On" : "Off";
  }
}

function speakBotReply(replyText) {
  if (!isVoiceOutputEnabled || !("speechSynthesis" in window)) {
    return;
  }

  const cleanReply = replyText.replace(/\s+/g, " ").trim();

  if (!cleanReply) {
    return;
  }

  const spokenReply = new SpeechSynthesisUtterance(cleanReply);
  const availableVoices = window.speechSynthesis.getVoices();
  const preferredVoice = availableVoices.find((voice) =>
    /zira|samantha|female|google|english/i.test(voice.name)
  );

  spokenReply.voice = preferredVoice || availableVoices[0] || null;
  spokenReply.rate = 0.96;
  spokenReply.pitch = 1.08;
  spokenReply.volume = 1;

  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(spokenReply);
}

function addChatMessage(senderType, messageText) {
  const messageRow = document.createElement("article");
  messageRow.className = `message ${senderType}-message`;

  if (senderType === "bot") {
    const botAvatar = document.createElement("div");
    botAvatar.className = "message-avatar";
    botAvatar.textContent = "uwu";
    messageRow.append(botAvatar);
  }

  const messageBubble = document.createElement("div");
  messageBubble.className = "bubble";

  const messageParagraph = document.createElement("p");
  messageParagraph.textContent = messageText;

  messageBubble.append(messageParagraph);
  messageRow.append(messageBubble);
  chatMessagesBox.append(messageRow);
  scrollChatToBottom();
  return messageRow;
}

function addTypingMessage() {
  const typingRow = document.createElement("article");
  typingRow.className = "message bot-message";

  const botAvatar = document.createElement("div");
  botAvatar.className = "message-avatar";
  botAvatar.textContent = "owo";

  const typingBubble = document.createElement("div");
  typingBubble.className = "bubble";
  typingBubble.innerHTML = '<div class="typing-bubble" aria-label="Byte-Bot is typing"><span></span><span></span><span></span></div>';

  typingRow.append(botAvatar, typingBubble);
  chatMessagesBox.append(typingRow);
  scrollChatToBottom();
  return typingRow;
}

function showThinkingMode() {
  window.clearInterval(idleFaceLoop);

  if (topBotBox) {
    topBotBox.dataset.state = "thinking";
  }

  const thinkingFace = pickFaceForMood("thinking");
  setBotFace(thinkingFace);
  setBotStatus("thinking in pixels");
}

function showHappyMode() {
  if (topBotBox) {
    topBotBox.dataset.state = "happy";
  }

  const happyFace = pickFaceForMood("happy");
  setBotFace(happyFace);
  setBotStatus("reply delivered");

  window.setTimeout(() => {
    if (topBotBox) {
      topBotBox.dataset.state = "idle";
    }

    setBotStatus("idle and listening");
    showIdleFace();
    idleFaceLoop = window.setInterval(showIdleFace, 2600);
  }, 1300);
}

function showIdleFace() {
  const idleFace = pickFaceForMood("idle");
  setBotFace(idleFace);
}

function pickFaceForMood(moodName) {
  const moodFaceList = botFaceByMood[moodName];
  return moodFaceList[Math.floor(Math.random() * moodFaceList.length)];
}

function setBotFace(faceText) {
  if (topBotFaceText) {
    topBotFaceText.textContent = faceText;
  }

  if (sideBotFaceText) {
    sideBotFaceText.textContent = faceText;
  }
}

function setBotStatus(statusText) {
  if (topBotStatusText) {
    topBotStatusText.textContent = statusText;
  }

  if (sideBotStatusText) {
    sideBotStatusText.textContent = statusText;
  }
}

async function handleResetChat() {
  try {
    await fetch(`${resetUrl}/${currentSessionId}`, {
      method: "POST",
      headers: getAuthHeaders()
    });
  } catch (error) {
    console.error("Reset API error:", error);
  }

  chatMessagesBox.innerHTML = "";

  if (chatMascotButton) {
    chatMessagesBox.append(chatMascotButton);
  }

  chatMessagesBox.classList.add("is-empty");
  chatHasStarted = false;
  swapMascotImage();
  addChatMessage("bot", `Chat reset! I am ready for a fresh little adventure, ${currentUserName}. uwu`);

  if (topBotBox) {
    topBotBox.dataset.state = "idle";
  }

  setBotStatus("idle and listening");
  checkBackendHealth();
}

function scrollChatToBottom() {
  chatMessagesBox.scrollTop = chatMessagesBox.scrollHeight;
}

function handleMascotTap() {
  if (!chatMascotButton || !messageTextInput) {
    return;
  }

  chatMascotButton.classList.remove("is-excited");
  void chatMascotButton.offsetWidth;
  chatMascotButton.classList.add("is-excited");
  swapMascotImage();

  const nudgePromptList = [
    "Give me a tiny idea",
    "Show your happy face",
    "What do you remember about this session?"
  ];

  messageTextInput.value = nudgePromptList[Math.floor(Math.random() * nudgePromptList.length)];
  submitMessageForm();
}

function submitMessageForm() {
  if (typeof sendMessageForm.requestSubmit === "function") {
    sendMessageForm.requestSubmit();
    return;
  }

  sendMessageForm.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
}

function markChatAsStarted() {
  if (chatHasStarted) {
    return;
  }

  chatHasStarted = true;
  chatMessagesBox.classList.remove("is-empty");
}

function moveMascotToBottom() {
  if (chatMascotButton) {
    chatMessagesBox.append(chatMascotButton);
  }
}

function swapMascotImage() {
  if (!chatMascotImage) {
    return;
  }

  const randomImageIndex = Math.floor(Math.random() * mascotImageList.length);
  chatMascotImage.src = mascotImageList[randomImageIndex];
}

/*
const messages = document.querySelector("#messages");
const chatForm = document.querySelector("#chatForm");
const messageInput = document.querySelector("#messageInput");
const botFace = document.querySelector("#botFace");
const botMood = document.querySelector("#botMood");
const computerBot = document.querySelector("#computerBot");
const resetChat = document.querySelector("#resetChat");
const quickPrompts = document.querySelectorAll("[data-prompt]");
const chatCompanion = document.querySelector("#chatCompanion");
const companionImage = document.querySelector("#companionImage");
const sessionLabel = document.querySelector("#sessionLabel");
const introMessage = document.querySelector("#introMessage");

const API_BASE_URL = localStorage.getItem("bytebot_api_base_url") || "http://127.0.0.1:8000";
const API_URL = `${API_BASE_URL}/chat`;
const RESET_URL = `${API_BASE_URL}/reset`;
const SESSION_ID = localStorage.getItem("bytebot_session_id") || "bytebot-guest";
const USER_LABEL = localStorage.getItem("bytebot_user_label") || "guest";

const companionSprites = [
  "assets/coding-window.gif",
  "assets/bytebuddy-team.gif",
  "assets/bytebuddy-rocket.gif"
];

const faces = {
  idle: ["uwu", "owo", "^-^", "-w-"],
  thinking: ["o_O", "?w?", "...?", "@_@"],
  happy: [">w<", "^o^", "\\o/", "*w*"]
};

let hasStartedConversation = false;
let faceTimer = null;

if (messages && chatForm && messageInput) {
  if (sessionLabel) {
    sessionLabel.textContent = `Local session: ${USER_LABEL}`;
  }

  if (introMessage) {
    introMessage.textContent = `Hi ${USER_LABEL}, I am Byte-Bot. I am ready to remember this session and chat through the backend. uwu`;
  }

  faceTimer = window.setInterval(cycleIdleFace, 2600);

  chatForm.addEventListener("submit", handleSubmit);
  resetChat?.addEventListener("click", resetConversation);
  chatCompanion?.addEventListener("click", handleCompanionClick);

  quickPrompts.forEach((button) => {
    button.addEventListener("click", () => {
      messageInput.value = button.dataset.prompt;
      submitChatForm();
    });
  });
}

async function getBotReply(userText) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userText, session_id: SESSION_ID })
    });

    if (!response.ok) {
      throw new Error(`Backend returned ${response.status}`);
    }

    const data = await response.json();
    return data.reply;
  } catch (error) {
    console.error("Byte-Bot backend error:", error);
    return "Byte-Bot could not reach the backend right now. Check whether FastAPI is still running on the expected port.";
  }
}

async function handleSubmit(event) {
  event.preventDefault();
  const text = messageInput.value.trim();

  if (!text) {
    return;
  }

  addMessage("user", text);
  markConversationStarted();
  messageInput.value = "";
  showBotThinking();

  const typingMessage = addTypingMessage();
  const reply = await getBotReply(text);

  typingMessage.remove();
  addMessage("bot", reply);
  moveCompanionAfterLatestMessage();
  randomizeCompanionSprite();
  showBotHappy();
}

function addMessage(sender, text) {
  const message = document.createElement("article");
  message.className = `message ${sender}-message`;

  if (sender === "bot") {
    const avatar = document.createElement("div");
    avatar.className = "message-avatar";
    avatar.textContent = "uwu";
    message.append(avatar);
  }

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  const paragraph = document.createElement("p");
  paragraph.textContent = text;
  bubble.append(paragraph);
  message.append(bubble);

  messages.append(message);
  scrollToLatestMessage();
  return message;
}

function addTypingMessage() {
  const message = document.createElement("article");
  message.className = "message bot-message";
  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = "owo";
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = '<div class="typing-bubble" aria-label="Byte-Bot is typing"><span></span><span></span><span></span></div>';
  message.append(avatar, bubble);
  messages.append(message);
  scrollToLatestMessage();
  return message;
}

function showBotThinking() {
  window.clearInterval(faceTimer);
  if (computerBot) {
    computerBot.dataset.state = "thinking";
  }
  if (botFace) {
    botFace.textContent = pickFace("thinking");
  }
  if (botMood) {
    botMood.textContent = "thinking in pixels";
  }
}

function showBotHappy() {
  if (computerBot) {
    computerBot.dataset.state = "happy";
  }
  if (botFace) {
    botFace.textContent = pickFace("happy");
  }
  if (botMood) {
    botMood.textContent = "reply delivered";
  }

  window.setTimeout(() => {
    if (computerBot) {
      computerBot.dataset.state = "idle";
    }
    if (botMood) {
      botMood.textContent = "idle and listening";
    }
    faceTimer = window.setInterval(cycleIdleFace, 2600);
  }, 1300);
}

function cycleIdleFace() {
  if (botFace) {
    botFace.textContent = pickFace("idle");
  }
}

function pickFace(type) {
  const set = faces[type];
  return set[Math.floor(Math.random() * set.length)];
}

async function resetConversation() {
  try {
    await fetch(`${RESET_URL}/${SESSION_ID}`, { method: "POST" });
  } catch (error) {
    console.error("Reset API error:", error);
  }

  messages.innerHTML = "";
  if (chatCompanion) {
    messages.append(chatCompanion);
  }

  messages.classList.add("is-empty");
  hasStartedConversation = false;
  randomizeCompanionSprite();
  addMessage("bot", `Chat reset! I am ready for a fresh little adventure, ${USER_LABEL}. uwu`);

  if (computerBot) {
    computerBot.dataset.state = "idle";
  }

  if (botMood) {
    botMood.textContent = "idle and listening";
  }
}

function scrollToLatestMessage() {
  messages.scrollTop = messages.scrollHeight;
}

function handleCompanionClick() {
  if (!chatCompanion || !messageInput) {
    return;
  }

  chatCompanion.classList.remove("is-excited");
  void chatCompanion.offsetWidth;
  chatCompanion.classList.add("is-excited");
  randomizeCompanionSprite();

  const nudges = [
    "Give me a tiny idea",
    "Show your happy face",
    "What do you remember about this session?"
  ];
  messageInput.value = nudges[Math.floor(Math.random() * nudges.length)];
  submitChatForm();
}

function submitChatForm() {
  if (typeof chatForm.requestSubmit === "function") {
    chatForm.requestSubmit();
    return;
  }
  chatForm.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
}

function markConversationStarted() {
  if (hasStartedConversation) {
    return;
  }
  hasStartedConversation = true;
  messages.classList.remove("is-empty");
}

function moveCompanionAfterLatestMessage() {
  if (chatCompanion) {
    messages.append(chatCompanion);
  }
}

function randomizeCompanionSprite() {
  if (!companionImage) {
    return;
  }
  const randomIndex = Math.floor(Math.random() * companionSprites.length);
  companionImage.src = companionSprites[randomIndex];
}
*/
