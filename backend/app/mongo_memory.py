from datetime import datetime, timezone

from backend.app.database import get_database


MAX_MONGO_HISTORY_MESSAGES = 40


async def get_recent_messages_mongo(session_id: str, limit: int = MAX_MONGO_HISTORY_MESSAGES):
    db = get_database()
    cursor = (
        db.chat_messages
        .find({"session_id": session_id}, {"_id": 0, "role": 1, "content": 1})
        .sort("created_at", -1)
        .limit(limit)
    )

    rows = await cursor.to_list(length=limit)
    rows.reverse()
    return rows


async def save_message_mongo(session_id: str, role: str, content: str):
    db = get_database()
    await db.chat_messages.insert_one(
        {
            "session_id": session_id,
            "role": role,
            "content": content,
            "created_at": datetime.now(timezone.utc),
        }
    )


async def clear_session_mongo(session_id: str):
    db = get_database()
    await db.chat_messages.delete_many({"session_id": session_id})
