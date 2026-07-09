import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

from backend.app.auth_routes import router as auth_router
from backend.app.auth_service import get_user_by_id
from backend.app.database import close_mongo, connect_to_mongo, get_mongo_error, is_mongo_enabled
from backend.app.memory import (
    MAX_HISTORY_MESSAGES,
    clear_session,
    format_history,
    get_recent_messages,
    init_db,
    save_message,
)
from backend.app.mongo_memory import clear_session_mongo, get_recent_messages_mongo, save_message_mongo
from backend.app.rag import build_retriever, clear_uploaded_knowledge, get_context
from backend.app.schemas import ChatRequest, ChatResponse
from backend.app.security import decode_access_token
from backend.app.tool_routes import router as tool_router

try:
    from backend.app.prompt import build_prompt
except ImportError:
    build_prompt = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
FRONTEND_ORIGINS = [
    origin.strip()
    for origin in os.getenv(
        "FRONTEND_ORIGINS",
        "http://127.0.0.1:8028,http://localhost:8028,null",
    ).split(",")
    if origin.strip()
]

app = FastAPI(title="Byte-Bot API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(tool_router)

knowledge_chunks = build_retriever()


def build_chain():
    if ChatGroq is None or build_prompt is None or not GROQ_API_KEY:
        return None

    groq_model = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY)
    return build_prompt() | groq_model


chat_chain = build_chain()


@app.on_event("startup")
async def startup():
    init_db()
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown():
    await close_mongo()


async def get_login_session(authorization: str | None) -> tuple[str, str]:
    """Return the safe Mongo-backed session id for the logged-in user."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please login before chatting with the MongoDB backend.",
        )

    token = authorization.replace("Bearer ", "", 1)
    token_payload = decode_access_token(token)
    user_doc = await get_user_by_id(token_payload["sub"])

    if not user_doc:
        raise HTTPException(status_code=401, detail="User no longer exists.")

    session_id = f"bytebot-{str(user_doc['_id'])}"
    user_name = user_doc.get("name") or user_doc["email"].split("@")[0]
    return session_id, user_name


def get_guest_session(payload_session_id: str) -> tuple[str, str]:
    """Return a simple local/demo session when the user is not logged in."""
    session_id = payload_session_id.strip() or "bytebot-guest"
    user_name = session_id.replace("bytebot-", "").strip() or "guest"
    return session_id, user_name


async def get_chat_session(payload_session_id: str, authorization: str | None) -> tuple[str, str]:
    """Use login memory when a token exists, otherwise allow the guest demo to work."""
    if is_mongo_enabled() and authorization and authorization.startswith("Bearer "):
        return await get_login_session(authorization)

    return get_guest_session(payload_session_id)


def local_reply(user_message: str, user_name: str) -> str:
    lower_message = user_message.lower()

    if "hello" in lower_message or "hi" in lower_message:
        return f"Hi {user_name}, Byte-Bot is awake and listening uwu"

    if "memory" in lower_message:
        return "I am in fallback mode right now, so I can still save your session history even if the live Groq chain is offline."

    if "backend" in lower_message or "fastapi" in lower_message:
        return "The FastAPI backend is alive. If you want live model replies, make sure GROQ_API_KEY is set and langchain-groq is installed."

    if "happy" in lower_message or "face" in lower_message:
        return "Happy mode engaged >w<"

    return f"Byte-Bot heard you, {user_name}: {user_message}"


def split_local_reply(reply: str, chunk_size: int = 18):
    """Split fallback replies so the frontend still gets stream-like chunks."""
    for start_index in range(0, len(reply), chunk_size):
        yield reply[start_index:start_index + chunk_size]


async def save_chat_message(session_id: str, role: str, content: str):
    """Save one chat message to MongoDB when enabled, otherwise SQLite."""
    if is_mongo_enabled():
        await save_message_mongo(session_id, role, content)
    else:
        save_message(session_id, role, content)


async def stream_assistant_reply(user_message: str, user_name: str, session_id: str, history_text: str, context_text: str):
    """Yield assistant text chunks and save the final full reply once."""
    full_reply_parts = []

    try:
        if chat_chain is None:
            reply = local_reply(user_message, user_name)
            for reply_chunk in split_local_reply(reply):
                full_reply_parts.append(reply_chunk)
                yield reply_chunk
                await asyncio.sleep(0.025)
        else:
            async for model_chunk in chat_chain.astream(
                {
                    "context": context_text,
                    "history": history_text,
                    "question": user_message,
                }
            ):
                reply_chunk = getattr(model_chunk, "content", str(model_chunk))
                if not reply_chunk:
                    continue

                full_reply_parts.append(reply_chunk)
                yield reply_chunk
    except Exception as error:
        error_reply = f"Byte-Bot backend error: {str(error)}"
        full_reply_parts.append(error_reply)
        yield error_reply

        full_reply = "".join(full_reply_parts).strip()
    if full_reply:
        await save_chat_message(session_id, "assistant", full_reply)


@app.get("/")
def home():
    return {
        "message": "Byte-Bot backend is running",
        "llm_connected": chat_chain is not None,
        "knowledge_ready": bool(knowledge_chunks),
        "mongo_enabled": is_mongo_enabled(),
        "mongo_error": get_mongo_error(),
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
        "llm_connected": chat_chain is not None,
        "knowledge_ready": bool(knowledge_chunks),
        "mongo_enabled": is_mongo_enabled(),
        "mongo_error": get_mongo_error(),
    }


@app.post("/reset/{session_id}")
async def reset_session(session_id: str, authorization: str | None = Header(default=None)):
    if is_mongo_enabled():
        if authorization and authorization.startswith("Bearer "):
            session_id, _ = await get_login_session(authorization)
        await clear_session_mongo(session_id)
    else:
        clear_session(session_id)

    clear_uploaded_knowledge(session_id)
    return {"message": f"Session {session_id} cleared"}


@app.post("/chat/stream")
async def chat_stream(payload: ChatRequest, authorization: str | None = Header(default=None)):
    user_message = payload.message.strip()
    session_id, user_name = await get_chat_session(payload.session_id, authorization)

    if not user_message:
        return StreamingResponse(iter(["Please type something."]), media_type="text/plain")

    if is_mongo_enabled():
        recent_messages = await get_recent_messages_mongo(session_id, MAX_HISTORY_MESSAGES)
    else:
        recent_messages = get_recent_messages(session_id, MAX_HISTORY_MESSAGES)

    history_text = format_history(recent_messages)
    context_text = get_context(knowledge_chunks, user_message, session_id=session_id)

    await save_chat_message(session_id, "user", user_message)

    return StreamingResponse(
        stream_assistant_reply(user_message, user_name, session_id, history_text, context_text),
        media_type="text/plain",
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(payload: ChatRequest, authorization: str | None = Header(default=None)):
    user_message = payload.message.strip()
    session_id, user_name = await get_chat_session(payload.session_id, authorization)

    if not user_message:
        return ChatResponse(reply="Please type something.")

    if is_mongo_enabled():
        recent_messages = await get_recent_messages_mongo(session_id, MAX_HISTORY_MESSAGES)
    else:
        recent_messages = get_recent_messages(session_id, MAX_HISTORY_MESSAGES)

    history_text = format_history(recent_messages)
    context_text = get_context(knowledge_chunks, user_message, session_id=session_id)

    try:
        if chat_chain is None:
            reply = local_reply(user_message, user_name)
        else:
            model_response = chat_chain.invoke(
                {
                    "context": context_text,
                    "history": history_text,
                    "question": user_message,
                }
            )
            reply = model_response.content.strip()

        if is_mongo_enabled():
            await save_message_mongo(session_id, "user", user_message)
            await save_message_mongo(session_id, "assistant", reply)
        else:
            save_message(session_id, "user", user_message)
            save_message(session_id, "assistant", reply)

        return ChatResponse(reply=reply)
    except Exception as error:
        return ChatResponse(reply=f"Byte-Bot backend error: {str(error)}")
