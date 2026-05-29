from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class GroupCreate(BaseModel):
    name: str


class MemberOut(BaseModel):
    user_id: int
    username: str
    display_name: str
    avatar_emoji: str
    tier: str
    total_points: int
    joined_at: datetime

    model_config = {"from_attributes": True}


class GroupOut(BaseModel):
    id: int
    name: str
    invite_code: str
    owner_id: int
    is_active: bool
    created_at: datetime
    member_count: int = 0

    model_config = {"from_attributes": True}


class GroupDetail(GroupOut):
    members: List[MemberOut] = []
