from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TeamOut(BaseModel):
    id: int
    name: str
    name_en: str
    iso_code: str
    group_name: str
    flag_url: str
    confederation: str

    model_config = {"from_attributes": True}


class MatchOut(BaseModel):
    id: int
    match_number: int
    stage: str
    group_name: Optional[str] = None
    venue: str
    scheduled_at: datetime
    is_locked: bool
    is_played: bool
    home_score: Optional[int] = None
    away_score: Optional[int] = None
    match_label: Optional[str] = None
    home_team: Optional[TeamOut] = None
    away_team: Optional[TeamOut] = None

    model_config = {"from_attributes": True}
