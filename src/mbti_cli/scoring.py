from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

from .models import Question, Likert, MBTILetter

PAIRS: List[Tuple[MBTILetter, MBTILetter]] = [
    ("E", "I"),
    ("S", "N"),
    ("T", "F"),
    ("J", "P"),
]


@dataclass(frozen=True)
class ScoreResult:
    totals: Dict[MBTILetter, int]
    percentages: Dict[str, Tuple[int, int]]  # key "E/I" -> (E%, I%)
    type: str


def _effective_value(value: Likert, reverse: bool, weight: int) -> int:
    v: int = 6 - value if reverse else value
    return v * weight


def aggregate_totals(
    questions: List[Question],
    answers: List[Likert],
) -> Dict[MBTILetter, int]:
    if len(questions) != len(answers):
        raise ValueError("Questions and answers length mismatch")
    totals: Dict[MBTILetter, int] = {
        "E": 0,
        "I": 0,
        "S": 0,
        "N": 0,
        "T": 0,
        "F": 0,
        "J": 0,
        "P": 0,
    }
    for q, a in zip(questions, answers):
        totals[q.dimension] += _effective_value(a, q.reverse, q.weight)
    return totals


def compute_percentages(
    totals: Dict[MBTILetter, int]
) -> Dict[str, Tuple[int, int]]:
    percentages: Dict[str, Tuple[int, int]] = {}
    for a, b in PAIRS:
        left = totals.get(a, 0)
        right = totals.get(b, 0)
        denom = left + right
        if denom <= 0:
            raise ValueError(f"No items contributing to dichotomy {a}/{b}")
        lp = round(left / denom * 100)
        rp = 100 - lp
        percentages[f"{a}/{b}"] = (lp, rp)
    return percentages


def derive_type(totals: Dict[MBTILetter, int]) -> str:
    letters: List[str] = []
    for a, b in PAIRS:
        if totals.get(a, 0) > totals.get(b, 0):
            letters.append(a)
        elif totals.get(b, 0) > totals.get(a, 0):
            letters.append(b)
        else:
            # tie-breaker: default to first of pair for MVP
            letters.append(a)
    return "".join(letters)


def score_responses(
    questions: List[Question],
    answers: List[Likert],
) -> ScoreResult:
    totals = aggregate_totals(questions, answers)
    percentages = compute_percentages(totals)
    mbti_type = derive_type(totals)
    return ScoreResult(totals=totals, percentages=percentages, type=mbti_type)
