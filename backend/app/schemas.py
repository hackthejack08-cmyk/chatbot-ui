from pydantic import BaseModel, EmailStr, Field

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str

class UserPublic(BaseModel):
    id: str
    email: EmailStr
    name: str
    is_email_verified: bool
    auth_provider: str

class AuthRegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str | None = None

class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserPublic
    session_id: str

class AuthConfigResponse(BaseModel):
    mongo_enabled: bool
