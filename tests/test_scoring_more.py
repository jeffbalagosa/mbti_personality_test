from __future__ import annotations

from mbti_cli.models import Question
from mbti_cli.scoring import aggregate_totals, compute_percentages, score_responses


def test_reverse_scoring_effect():
    qs = [Question(text="q", dimension="I", reverse=True, weight=1)]
    answers = [5]
    totals = aggregate_totals(qs, answers)
    # Reverse maps 5 -> 1
    assert totals["I"] == 1


def test_weighted_scoring_effect():
    qs = [Question(text="q", dimension="T", reverse=False, weight=3)]
    answers = [4]
    totals = aggregate_totals(qs, answers)
    assert totals["T"] == 12


def test_tie_breaker_defaults_to_left_letters():
    # One item for each letter, all answered 3 -> equal totals per pair
    qs = [
        Question(text="E", dimension="E"),
        Question(text="I", dimension="I"),
        Question(text="S", dimension="S"),
        Question(text="N", dimension="N"),
        Question(text="T", dimension="T"),
        Question(text="F", dimension="F"),
        Question(text="J", dimension="J"),
        Question(text="P", dimension="P"),
    ]
    answers = [3] * len(qs)
    res = score_responses(qs, answers)
    assert res.type == "ESTJ"
    for pair, (lp, rp) in res.percentages.items():
        assert lp + rp == 100


def test_compute_percentages_requires_denominator():
    # At least one item per pair must exist in totals; simulate an empty pair error
    totals = {"E": 0, "I": 0, "S": 1, "N": 0, "T": 1, "F": 0, "J": 1, "P": 0}
    try:
        compute_percentages(totals)
    except ValueError as e:
        assert "dichotomy E/I" in str(e)
    else:
        raise AssertionError("Expected ValueError for empty E/I pair")
