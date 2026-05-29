from sqlalchemy.orm import Session
from app.models.achievement import Achievement, UserAchievement
from app.models.prediction import Prediction
from app.models.match import Match
from app.models.user import User
from app.services.scoring import get_tier


ACHIEVEMENT_CHECKS = [
    {"slug": "primeiro_gol",    "check": lambda s: s["total_predictions"] >= 1},
    {"slug": "em_chamas",       "check": lambda s: s["consecutive_winner_hits"] >= 3},
    {"slug": "craque_do_bolao", "check": lambda s: s["exact_scores"] >= 5},
    {"slug": "polvo",           "check": lambda s: s.get("perfect_round") is True},
    {"slug": "aguia",           "check": lambda s: s.get("upset_predicted") is True},
    {"slug": "lenda",           "check": lambda s: s.get("exact_draw_score") is True},
    {"slug": "sortudo",         "check": lambda s: s.get("opening_match_exact") is True},
    {"slug": "fantasma",        "check": lambda s: s["missed_predictions"] >= 5},
    {"slug": "rei",             "check": lambda s: s.get("champion_correct") is True},
    {"slug": "100pts",          "check": lambda s: s["total_points"] >= 100},
]


def _build_stats(db: Session, user_id: int, bolao_group_id: int) -> dict:
    preds = (
        db.query(Prediction)
        .filter(Prediction.user_id == user_id, Prediction.bolao_group_id == bolao_group_id)
        .order_by(Prediction.created_at)
        .all()
    )

    total_points = sum(p.points_earned for p in preds)
    exact_scores = sum(1 for p in preds if p.is_exact)
    total_predictions = len(preds)

    # Consecutive winner hits
    max_consec = current = 0
    for p in preds:
        if p.is_winner_correct:
            current += 1
            max_consec = max(max_consec, current)
        else:
            current = 0

    # Exact draw and opening match exact
    exact_draw = False
    opening_exact = False
    for p in preds:
        if p.is_exact:
            match = db.query(Match).filter(Match.id == p.match_id).first()
            if match:
                if match.home_score is not None and match.home_score == match.away_score:
                    exact_draw = True
                if match.match_number == 1:
                    opening_exact = True

    return {
        "total_predictions": total_predictions,
        "total_points": total_points,
        "exact_scores": exact_scores,
        "consecutive_winner_hits": max_consec,
        "missed_predictions": 0,
        "perfect_round": False,
        "upset_predicted": False,
        "exact_draw_score": exact_draw,
        "opening_match_exact": opening_exact,
        "champion_correct": False,
    }


def check_and_unlock(db: Session, user_id: int, bolao_group_id: int) -> list[Achievement]:
    stats = _build_stats(db, user_id, bolao_group_id)
    unlocked = []

    for ach_def in ACHIEVEMENT_CHECKS:
        if not ach_def["check"](stats):
            continue
        ach = db.query(Achievement).filter(Achievement.slug == ach_def["slug"]).first()
        if not ach:
            continue
        already = db.query(UserAchievement).filter(
            UserAchievement.user_id == user_id,
            UserAchievement.achievement_id == ach.id,
            UserAchievement.bolao_group_id == bolao_group_id,
        ).first()
        if already:
            continue
        db.add(UserAchievement(user_id=user_id, achievement_id=ach.id, bolao_group_id=bolao_group_id))
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.total_points += ach.points_bonus
            user.tier = get_tier(user.total_points)["name"].lower()
        unlocked.append(ach)

    if unlocked:
        db.commit()
    return unlocked
