from pydantic import BaseModel
from typing import List


class RankingEntry(BaseModel):
    position: int
    user_id: int
    username: str
    display_name: str
    avatar_emoji: str
    tier: str
    total_points: int
    exact_scores: int
    correct_winners: int

    model_config = {"from_attributes": True}


class RankingOut(BaseModel):
    group_id: int
    group_name: str
    entries: List[RankingEntry]
