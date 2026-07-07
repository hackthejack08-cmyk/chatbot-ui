from tool_models import ChatWorkRequest, ChatWorkResult, Intent
from router_service import detect_intent
from note_service import get_recent_notes, save_note
from email_service import draft_email
from search_service import search_web_placeholder


def handle_chat_work(request: ChatWorkRequest) -> ChatWorkResult:
    route = detect_intent(request.message)

    if route.intent == Intent.NOTE_SAVE:
        save_note(request.session_id, request.message)
        return ChatWorkResult(
            reply="Saved that note for this session.",
            intent=route.intent,
            used_tools=["note_service.save_note"],
        )

    if route.intent == Intent.NOTE_FETCH:
        notes = get_recent_notes(request.session_id)
        if not notes:
            reply = "I do not have saved notes for this session yet."
        else:
            reply = "\n".join(f"- {note['content']}" for note in notes)

        return ChatWorkResult(
            reply=reply,
            intent=route.intent,
            used_tools=["note_service.get_recent_notes"],
        )

    if route.intent == Intent.EMAIL_DRAFT:
        draft = draft_email(request.message)
        reply = f"Subject: {draft['subject']}\n\n{draft['body']}\nConfirm before sending."
        return ChatWorkResult(
            reply=reply,
            intent=route.intent,
            used_tools=["email_service.draft_email"],
        )

    if route.intent == Intent.WEB_SEARCH:
        result = search_web_placeholder(request.message)
        return ChatWorkResult(
            reply=result["message"],
            intent=route.intent,
            used_tools=["search_service.search_web_placeholder"],
        )

    return ChatWorkResult(
        reply="Normal chat path goes here. Call your Groq/LangChain chain from this branch.",
        intent=Intent.NORMAL_CHAT,
        used_tools=[],
    )
