from tool_models import Intent, RouterResult


def detect_intent(user_message: str) -> RouterResult:
    message = user_message.lower()

    if any(word in message for word in ["remember this", "save note", "save this"]):
        return RouterResult(intent=Intent.NOTE_SAVE, confidence=0.8, reason="User wants to save information.")

    if any(word in message for word in ["what did i save", "my notes", "remember about me"]):
        return RouterResult(intent=Intent.NOTE_FETCH, confidence=0.8, reason="User wants saved information.")

    if any(word in message for word in ["pdf", "document", "file", "according to"]):
        return RouterResult(intent=Intent.RAG_QUESTION, confidence=0.7, reason="User may need document knowledge.")

    if any(word in message for word in ["email", "mail", "teacher", "subject line"]):
        return RouterResult(intent=Intent.EMAIL_DRAFT, confidence=0.75, reason="User wants an email drafted.")

    if any(word in message for word in ["latest", "today", "news", "search web", "internet"]):
        return RouterResult(intent=Intent.WEB_SEARCH, confidence=0.7, reason="User wants current information.")

    if any(word in message for word in ["image", "photo", "screenshot", "ocr"]):
        return RouterResult(intent=Intent.IMAGE_SEARCH, confidence=0.65, reason="User mentions image knowledge.")

    if "discord" in message:
        return RouterResult(intent=Intent.DISCORD_SEND, confidence=0.7, reason="User mentions Discord.")

    return RouterResult(intent=Intent.NORMAL_CHAT, confidence=0.55, reason="Default chat path.")
