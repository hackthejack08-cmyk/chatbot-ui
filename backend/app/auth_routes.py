from fastapi import APIRouter, Depends, Header, HTTPException

from backend.app.auth_service import (
    get_user_by_id,
    login_user,
    make_auth_response,
    register_user,
    serialize_user,
)
from backend.app.database import is_mongo_enabled
from backend.app.schemas import (
    AuthConfigResponse,
    AuthLoginRequest,
    AuthResponse,
    AuthRegisterRequest,
    UserPublic,
)
from backend.app.security import decode_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


async def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token.")

    token = authorization.replace("Bearer ", "", 1)
    payload = decode_access_token(token)
    user = await get_user_by_id(payload["sub"])

    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists.")

    return user


@router.get("/config", response_model=AuthConfigResponse)
def auth_config():
    return AuthConfigResponse(
        mongo_enabled=is_mongo_enabled(),
    )


@router.post("/register", response_model=AuthResponse)
async def register(payload: AuthRegisterRequest):
    user = await register_user(payload.email, payload.password, payload.name)
    return make_auth_response(user)


@router.post("/login", response_model=AuthResponse)
async def login(payload: AuthLoginRequest):
    user = await login_user(payload.email, payload.password)
    return make_auth_response(user)


@router.get("/me", response_model=UserPublic)
async def me(user=Depends(get_current_user)):
    return serialize_user(user)
