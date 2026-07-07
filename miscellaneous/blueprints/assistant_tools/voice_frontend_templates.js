function speakReply(replyText) {
  if (!("speechSynthesis" in window)) {
    return;
  }

  const utterance = new SpeechSynthesisUtterance(replyText);
  utterance.rate = 1;
  utterance.pitch = 1.1;
  speechSynthesis.speak(utterance);
}

function startVoiceInput(messageTextInput) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    alert("Speech recognition is not supported in this browser.");
    return;
  }

  const recognizer = new SpeechRecognition();
  recognizer.lang = "en-IN";
  recognizer.interimResults = false;

  recognizer.onresult = (event) => {
    messageTextInput.value = event.results[0][0].transcript;
  };

  recognizer.start();
}
