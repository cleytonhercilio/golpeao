import pytest
from unittest.mock import MagicMock
from app.services.scoring import calculate_points, get_tier, SCORING_RULES


def make_match(home_score, away_score, stage="group"):
    m = MagicMock()
    m.home_score = home_score
    m.away_score = away_score
    m.stage = stage
    return m


def make_prediction(home_score, away_score, predicted_winner_id=None):
    p = MagicMock()
    p.home_score = home_score
    p.away_score = away_score
    p.predicted_winner_id = predicted_winner_id
    return p


def test_exact_score_group():
    result = calculate_points(make_prediction(2, 1), make_match(2, 1, "group"))
    assert result["points"] == SCORING_RULES["exact_score"]
    assert result["is_exact"] is True
    assert result["is_winner_correct"] is True


def test_exact_draw_group():
    result = calculate_points(make_prediction(1, 1), make_match(1, 1, "group"))
    assert result["points"] == SCORING_RULES["exact_score_draw"]
    assert result["is_exact"] is True


def test_correct_winner_group():
    result = calculate_points(make_prediction(3, 0), make_match(2, 0, "group"))
    assert result["points"] == SCORING_RULES["correct_winner"]
    assert result["is_winner_correct"] is True
    assert result["is_exact"] is False


def test_correct_winner_with_goal_diff():
    result = calculate_points(make_prediction(3, 1), make_match(2, 0, "group"))
    assert result["points"] == SCORING_RULES["correct_winner"] + SCORING_RULES["correct_goal_diff"]


def test_correct_draw_group():
    result = calculate_points(make_prediction(0, 0), make_match(1, 1, "group"))
    assert result["points"] == SCORING_RULES["correct_draw"]


def test_wrong_prediction():
    result = calculate_points(make_prediction(2, 0), make_match(0, 1, "group"))
    assert result["points"] == 0
    assert result["is_exact"] is False
    assert result["is_winner_correct"] is False


def test_exact_score_knockout():
    result = calculate_points(make_prediction(1, 0), make_match(1, 0, "qf"))
    assert result["points"] == SCORING_RULES["ko_exact_score"]
    assert result["is_exact"] is True


def test_correct_winner_knockout():
    result = calculate_points(make_prediction(2, 0), make_match(1, 0, "sf"))
    assert result["points"] == SCORING_RULES["ko_correct_winner"]


def test_get_tier_bronze():
    assert get_tier(0)["name"] == "Bronze"


def test_get_tier_silver():
    assert get_tier(50)["name"] == "Prata"


def test_get_tier_gold():
    assert get_tier(150)["name"] == "Ouro"


def test_get_tier_platinum():
    assert get_tier(300)["name"] == "Platina"


def test_get_tier_legend():
    assert get_tier(500)["name"] == "Lenda"


def test_get_tier_boundary():
    # 149 pts = Prata, 150 pts = Ouro
    assert get_tier(149)["name"] == "Prata"
    assert get_tier(150)["name"] == "Ouro"


def test_breakdown_has_entries_on_hit():
    result = calculate_points(make_prediction(2, 1), make_match(2, 1, "group"))
    assert len(result["breakdown"]) > 0


def test_breakdown_empty_on_miss():
    result = calculate_points(make_prediction(2, 0), make_match(0, 1, "group"))
    assert result["breakdown"] == []
