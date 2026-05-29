SCORING_RULES = {
    "exact_score": 10,
    "exact_score_draw": 12,
    "correct_winner": 3,
    "correct_draw": 4,
    "correct_goal_diff": 2,
    "ko_exact_score": 15,
    "ko_correct_winner": 5,
    "ko_correct_winner_extra": 8,
    "champion_correct": 50,
    "top_scorer_correct": 20,
    "finalist_correct": 15,
}

TIERS = [
    {"name": "Bronze",  "min_points": 0,   "icon": "🥉", "color": "#CD7F32"},
    {"name": "Prata",   "min_points": 50,  "icon": "🥈", "color": "#C0C0C0"},
    {"name": "Ouro",    "min_points": 150, "icon": "🥇", "color": "#FFD700"},
    {"name": "Platina", "min_points": 300, "icon": "💎", "color": "#E5E4E2"},
    {"name": "Lenda",   "min_points": 500, "icon": "👑", "color": "#FF6B35"},
]


def get_tier(points: int) -> dict:
    for tier in reversed(TIERS):
        if points >= tier["min_points"]:
            return tier
    return TIERS[0]


def calculate_points(prediction, match) -> dict:
    """
    Calculates points for a prediction against a real match result.

    Returns a dict with:
    - points: int total points earned
    - breakdown: list of (rule_name, points, description) tuples
    - is_exact: bool — True if the exact score was predicted
    - is_winner_correct: bool — True if the correct winner (or draw) was predicted
    """
    points = 0
    breakdown = []

    pred_home = prediction.home_score
    pred_away = prediction.away_score
    real_home = match.home_score
    real_away = match.away_score
    is_group = match.stage == "group"

    # 1. Placar exato
    if pred_home == real_home and pred_away == real_away:
        if pred_home == pred_away and is_group:
            rule = "exact_score_draw"
        else:
            rule = "exact_score" if is_group else "ko_exact_score"
        pts = SCORING_RULES[rule]
        points += pts
        breakdown.append((rule, pts, "Placar exato! 🎯"))
        return {
            "points": points,
            "breakdown": breakdown,
            "is_exact": True,
            "is_winner_correct": True,
        }

    # 2. Determinar resultado previsto vs real
    pred_result = "H" if pred_home > pred_away else ("A" if pred_away > pred_home else "D")
    real_result = "H" if real_home > real_away else ("A" if real_away > real_home else "D")

    if pred_result == real_result:
        if real_result == "D" and is_group:
            pts = SCORING_RULES["correct_draw"]
            breakdown.append(("correct_draw", pts, "Acertou o empate 🤝"))
            points += pts
            # Nota: bônus de diferença de gols NÃO se aplica a empates,
            # pois a diferença é sempre 0 e não distingue o placar exato.
        else:
            rule = "correct_winner" if is_group else "ko_correct_winner"
            pts = SCORING_RULES[rule]
            breakdown.append((rule, pts, "Acertou o vencedor ⚽"))
            points += pts

            # Bônus: diferença de gols correta (apenas quando há vencedor)
            if abs(pred_home - pred_away) == abs(real_home - real_away):
                pts_diff = SCORING_RULES["correct_goal_diff"]
                points += pts_diff
                breakdown.append(("correct_goal_diff", pts_diff, "Diferença de gols exata 📐"))

    return {
        "points": points,
        "breakdown": breakdown,
        "is_exact": False,
        "is_winner_correct": pred_result == real_result,
    }
