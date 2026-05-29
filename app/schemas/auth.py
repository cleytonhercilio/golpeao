from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    display_name: str
    avatar_emoji: str = "⚽"


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    email: str
    display_name: str
    avatar_emoji: str
    tier: str
    total_points: int
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}
