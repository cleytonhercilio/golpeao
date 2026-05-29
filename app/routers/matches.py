from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.dependencies import get_db
from app.models.match import Match
from app.schemas.match import MatchOut

router = APIRouter(prefix="/matches", tags=["matches"])


@router.get("/upcoming", response_model=List[MatchOut])
def upcoming_matches(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    return (
        db.query(Match)
        .filter(Match.scheduled_at >= now, Match.is_played == False)
        .order_by(Match.scheduled_at)
        .limit(5)
        .all()
    )


@router.get("/", response_model=List[MatchOut])
def list_matches(
    stage: Optional[str] = None,
    group: Optional[str] = None,
    group_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    query = db.query(Match)
    if stage:
        query = query.filter(Match.stage == stage)
    grp = group or group_name
    if grp:
        query = query.filter(Match.group_name == grp)
    return query.order_by(Match.scheduled_at).all()


@router.get("/{match_id}", response_model=MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(404, "Jogo não encontrado")
    return match
