import os
from pathlib import Path

import certifi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import PyMongoError


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "bytebot")

mongo_client: AsyncIOMotorClient | None = None
mongo_db = None
mongo_connection_error: str | None = None


async def connect_to_mongo():
    global mongo_client, mongo_db, mongo_connection_error

    if not MONGODB_URI:
        return

    try:
        mongo_client = AsyncIOMotorClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            tls=True,
            tlsCAFile=certifi.where(),
        )
        await mongo_client.admin.command("ping")
        mongo_db = mongo_client[MONGODB_DB_NAME]
        await ensure_indexes()
        mongo_connection_error = None
    except PyMongoError as error:
        mongo_client = None
        mongo_db = None
        mongo_connection_error = str(error)
        print(f"Byte-Bot MongoDB connection failed: {error}")


async def close_mongo():
    if mongo_client is not None:
        mongo_client.close()


def is_mongo_enabled() -> bool:
    return mongo_db is not None


def get_mongo_error() -> str | None:
    return mongo_connection_error


def get_database():
    if mongo_db is None:
        raise RuntimeError("MongoDB is not connected. Set MONGODB_URI in .env.")

    return mongo_db


async def ensure_indexes():
    if mongo_db is None:
        return

    await mongo_db.users.create_index("email", unique=True)
    await mongo_db.chat_messages.create_index([("session_id", 1), ("created_at", -1)])
