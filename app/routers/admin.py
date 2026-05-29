from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.dependencies import get_db, get_admin_user
from app.models.user import User
from app.models.match import Match
from app.models.prediction import Prediction
from app.services.scoring import calculate_points, get_tier
from app.services.achievements import check_and_unlock
from app.services.notifications import add_event, get_feed

router = APIRouter(prefix="/admin", tags=["admin"])


class MatchResult(BaseModel):
    home_score: int
    away_score: int
    winner_team_id: int = None


@router.post("/matches/{match_id}/result")
def set_match_result(
    match_id: int,
    result: MatchResult,
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(404, "Jogo não encontrado")

    match.home_score = result.home_score
    match.away_score = result.away_score
    match.winner_team_id = result.winner_team_id
    match.is_played = True
    match.is_locked = True

    preds = db.query(Prediction).filter(Prediction.match_id == match_id).all()
    updated = 0

    # Recalculate points for each prediction
    for pred in preds:
        calc = calculate_points(pred, match)
        pred.points_earned = calc["points"]
        pred.is_exact = calc["is_exact"]
        pred.is_winner_correct = calc["is_winner_correct"]
        updated += 1

    # Commit prediction updates first
    db.commit()

    # Now recalculate user totals
    affected_user_ids = {p.user_id for p in preds}
    for user_id in affected_user_ids:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            all_pts = sum(
                p.points_earned
                for p in db.query(Prediction).filter(Prediction.user_id == user_id).all()
            )
            user.total_points = all_pts
            user.tier = get_tier(all_pts)["name"].lower()
    db.commit()

    # Check achievements for affected users
    user_group_pairs = {(p.user_id, p.bolao_group_id) for p in preds}
    for user_id, group_id in user_group_pairs:
        newly_unlocked = check_and_unlock(db, user_id, group_id)
        for ach in newly_unlocked:
            user = db.query(User).filter(User.id == user_id).first()
            display = user.display_name if user else "Alguém"
            add_event("achievement", f"{display} desbloqueou {ach.name}!", display, ach.icon)

    home_name = match.home_team.name if match.home_team else "Time A"
    away_name = match.away_team.name if match.away_team else "Time B"
    add_event(
        "result",
        f"Resultado: {home_name} {result.home_score} × {result.away_score} {away_name}",
        icon="⚽",
    )

    return {"message": f"Resultado registrado. {updated} palpites recalculados."}


@router.get("/matches/pending-results")
def pending_results(
    db: Session = Depends(get_db),
    admin: User = Depends(get_admin_user),
):
    matches = (
        db.query(Match)
        .filter(Match.is_played == False, Match.is_locked == True)
        .order_by(Match.scheduled_at)
        .all()
    )
    return [
        {
            "id": m.id,
            "match_number": m.match_number,
            "stage": m.stage,
            "scheduled_at": m.scheduled_at.isoformat(),
            "match_label": m.match_label,
            "home_team": m.home_team.name if m.home_team else None,
            "away_team": m.away_team.name if m.away_team else None,
        }
        for m in matches
    ]


@router.get("/feed")
def activity_feed(
    limit: int = 20,
    admin: User = Depends(get_admin_user),
):
    return get_feed(limit)
