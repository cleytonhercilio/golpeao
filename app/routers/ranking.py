from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.group import BolaoGroup, GroupMember
from app.models.prediction import Prediction
from app.schemas.ranking import RankingOut, RankingEntry

router = APIRouter(prefix="/ranking", tags=["ranking"])


@router.get("/{group_id}", response_model=RankingOut)
def get_ranking(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    group = db.query(BolaoGroup).filter(BolaoGroup.id == group_id).first()
    if not group:
        raise HTTPException(404, "Bolão não encontrado")

    members = db.query(GroupMember).filter(GroupMember.group_id == group_id).all()
    entries = []

    for m in members:
        user = db.query(User).filter(User.id == m.user_id).first()
        if not user:
            continue
        preds = db.query(Prediction).filter(
            Prediction.user_id == m.user_id,
            Prediction.bolao_group_id == group_id,
        ).all()
        total_points = sum(p.points_earned for p in preds)
        exact_scores = sum(1 for p in preds if p.is_exact)
        correct_winners = sum(1 for p in preds if p.is_winner_correct)

        entries.append(RankingEntry(
            position=0,
            user_id=user.id,
            username=user.username,
            display_name=user.display_name,
            avatar_emoji=user.avatar_emoji,
            tier=user.tier,
            total_points=total_points,
            exact_scores=exact_scores,
            correct_winners=correct_winners,
        ))

    entries.sort(key=lambda x: (-x.total_points, -x.exact_scores, -x.correct_winners))
    for i, e in enumerate(entries):
        e.position = i + 1

    return RankingOut(group_id=group_id, group_name=group.name, entries=entries)
