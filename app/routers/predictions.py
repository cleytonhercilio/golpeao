from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.match import Match
from app.models.prediction import Prediction
from app.models.group import GroupMember
from app.schemas.prediction import PredictionCreate, PredictionOut

router = APIRouter(prefix="/predictions", tags=["predictions"])


def _assert_match_open(match: Match):
    if match.is_locked:
        raise HTTPException(400, "Palpites fechados para este jogo")
    if match.is_played:
        raise HTTPException(400, "Jogo já realizado")


@router.post("/", response_model=PredictionOut, status_code=201)
def create_prediction(
    data: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    match = db.query(Match).filter(Match.id == data.match_id).first()
    if not match:
        raise HTTPException(404, "Jogo não encontrado")
    _assert_match_open(match)

    member = db.query(GroupMember).filter(
        GroupMember.group_id == data.bolao_group_id,
        GroupMember.user_id == current_user.id,
    ).first()
    if not member:
        raise HTTPException(403, "Você não é membro deste bolão")

    existing = db.query(Prediction).filter(
        Prediction.user_id == current_user.id,
        Prediction.match_id == data.match_id,
        Prediction.bolao_group_id == data.bolao_group_id,
    ).first()
    if existing:
        raise HTTPException(400, "Palpite já registrado. Use PUT para atualizar.")

    pred = Prediction(
        user_id=current_user.id,
        match_id=data.match_id,
        bolao_group_id=data.bolao_group_id,
        home_score=data.home_score,
        away_score=data.away_score,
        predicted_winner_id=data.predicted_winner_id,
    )
    db.add(pred)
    db.commit()
    db.refresh(pred)
    return pred


@router.get("/", response_model=List[PredictionOut])
def list_predictions(
    bolao_group_id: Optional[int] = None,
    match_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Prediction).filter(Prediction.user_id == current_user.id)
    if bolao_group_id:
        query = query.filter(Prediction.bolao_group_id == bolao_group_id)
    if match_id:
        query = query.filter(Prediction.match_id == match_id)
    return query.all()


@router.put("/{prediction_id}", response_model=PredictionOut)
def update_prediction(
    prediction_id: int,
    data: PredictionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    pred = db.query(Prediction).filter(
        Prediction.id == prediction_id,
        Prediction.user_id == current_user.id,
    ).first()
    if not pred:
        raise HTTPException(404, "Palpite não encontrado")

    match = db.query(Match).filter(Match.id == pred.match_id).first()
    _assert_match_open(match)

    pred.home_score = data.home_score
    pred.away_score = data.away_score
    pred.predicted_winner_id = data.predicted_winner_id
    pred.updated_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(pred)
    return pred
