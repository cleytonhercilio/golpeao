from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PredictionCreate(BaseModel):
    match_id: int
    bolao_group_id: int
    home_score: int
    away_score: int
    predicted_winner_id: Optional[int] = None


class PredictionOut(BaseModel):
    id: int
    match_id: int
    bolao_group_id: int
    home_score: int
    away_score: int
    predicted_winner_id: Optional[int] = None
    points_earned: int
    is_exact: bool
    is_winner_correct: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
