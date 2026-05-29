from pydantic import BaseModel
from typing import List, Optional


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


class GroupStats(BaseModel):
    group_id: int
    group_name: str
    total_members: int
    total_predictions: int
    total_exact_scores: int
    top_scorer: Optional[str]
    top_scorer_points: int
    average_points: float
