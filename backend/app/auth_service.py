from datetime import datetime, timezone

from bson import ObjectId
from fastapi import HTTPException, status

from backend.app.database import get_database, is_mongo_enabled
from backend.app.security import create_access_token, hash_password, verify_password


def serialize_user(user_doc: dict) -> dict:
    return {
        "id": str(user_doc["_id"]),
        "email": user_doc["email"],
        "name": user_doc.get("name") or user_doc["email"].split("@")[0],
        "is_email_verified": bool(user_doc.get("is_email_verified", False)),
        "auth_provider": user_doc.get("auth_provider", "password"),
    }


def require_mongo_auth():
    if not is_mongo_enabled():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="MongoDB is not connected. Set MONGODB_URI before using real login.",
        )


async def register_user(email: str, password: str, name: str | None = None) -> dict:
    require_mongo_auth()
    clean_email = email.strip().lower()

    if "@" not in clean_email:
        raise HTTPException(status_code=400, detail="Please enter a valid email.")

    if len(password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters.")

    db = get_database()
    existing_user = await db.users.find_one({"email": clean_email})

    if existing_user:
        raise HTTPException(status_code=409, detail="This email is already registered.")

    # Never store the real password. Store only a bcrypt hash in MongoDB.
    user_doc = {
        "email": clean_email,
        "name": name or clean_email.split("@")[0],
        "password_hash": hash_password(password),
        "auth_provider": "password",
        "is_email_verified": False,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc),
    }
    result = await db.users.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id
    return user_doc


async def login_user(email: str, password: str) -> dict:
    require_mongo_auth()
    clean_email = email.strip().lower()
    db = get_database()
    user_doc = await db.users.find_one({"email": clean_email})

    # First check whether this email exists and has a password login.
    if not user_doc or not user_doc.get("password_hash"):
        raise HTTPException(status_code=401, detail="Wrong email or password.")

    # Then compare the typed password with the stored bcrypt hash.
    if not verify_password(password, user_doc["password_hash"]):
        raise HTTPException(status_code=401, detail="Wrong email or password.")

    return user_doc


async def get_user_by_id(user_id: str) -> dict | None:
    require_mongo_auth()
    db = get_database()

    if not ObjectId.is_valid(user_id):
        return None

    return await db.users.find_one({"_id": ObjectId(user_id)})


def make_auth_response(user_doc: dict) -> dict:
    public_user = serialize_user(user_doc)
    token = create_access_token(public_user["id"], public_user["email"])
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": public_user,
        "session_id": f"bytebot-{public_user['id']}",
    }
