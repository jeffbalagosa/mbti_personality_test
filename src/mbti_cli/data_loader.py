from __future__ import annotations

from typing import List
import yaml

from .models import Question, MBTILetter

ALLOWED: set[MBTILetter] = {"E", "I", "S", "N", "T", "F", "J", "P"}


def load_questions_from_yaml(path: str) -> List[Question]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    items = data.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("YAML must contain non-empty 'items' list")

    questions: List[Question] = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {idx} must be a mapping")
        text = item.get("text")
        dimension = item.get("dimension")
        reverse = bool(item.get("reverse", False))
        weight = int(item.get("weight", 1))

        if not text or not isinstance(text, str):
            raise ValueError(f"Item {idx}: 'text' must be a non-empty string")
        if dimension not in ALLOWED:
            allowed = ", ".join(sorted(ALLOWED))
            raise ValueError(
                f"Item {idx}: 'dimension' must be one of [{allowed}]"
            )
        if weight <= 0:
            raise ValueError(f"Item {idx}: 'weight' must be positive")

        questions.append(
            Question(
                text=text,
                dimension=dimension,
                reverse=reverse,
                weight=weight,
            )
        )

    # Basic sanity: ensure each dichotomy has at least one item overall
    dims = {q.dimension for q in questions}
    required_pairs = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    for a, b in required_pairs:
        if a not in dims and b not in dims:
            raise ValueError(
                f"Question set missing both sides of dichotomy {a}/{b}"
            )

    return questions
