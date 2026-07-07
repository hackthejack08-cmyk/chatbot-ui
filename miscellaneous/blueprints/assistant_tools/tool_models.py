from enum import Enum
from pydantic import BaseModel, Field


class Intent(str, Enum):
    NORMAL_CHAT = "normal_chat"
    RAG_QUESTION = "rag_question"
    NOTE_SAVE = "note_save"
    NOTE_FETCH = "note_fetch"
    EMAIL_DRAFT = "email_draft"
    WEB_SEARCH = "web_search"
    IMAGE_SEARCH = "image_search"
    DISCORD_SEND = "discord_send"
    UNKNOWN = "unknown"


class RouterResult(BaseModel):
    intent: Intent
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    reason: str = ""


class ChatWorkRequest(BaseModel):
    message: str
    session_id: str


class ChatWorkResult(BaseModel):
    reply: str
    intent: Intent
    used_tools: list[str] = []
