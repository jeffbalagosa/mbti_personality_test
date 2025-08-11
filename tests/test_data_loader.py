from __future__ import annotations

from pathlib import Path

import pytest

from mbti_cli.data_loader import load_questions_from_yaml
from mbti_cli.models import Question


def write_yaml(tmp_path: Path, content: str) -> str:
    p = tmp_path / "q.yaml"
    p.write_text(content, encoding="utf-8")
    return str(p)


def test_load_valid_yaml_minimal(tmp_path: Path):
    # One side from each dichotomy is sufficient
    yaml_text = """
items:
  - text: "I enjoy large social gatherings"
    dimension: E
  - text: "I focus on concrete facts"
    dimension: S
  - text: "I value objective logic"
    dimension: T
  - text: "I like structure and planning"
    dimension: J
"""
    path = write_yaml(tmp_path, yaml_text)
    qs = load_questions_from_yaml(path)
    assert isinstance(qs, list) and len(qs) == 4
    assert all(isinstance(q, Question) for q in qs)


def test_invalid_yaml_missing_items(tmp_path: Path):
    path = write_yaml(tmp_path, "items: []\n")
    with pytest.raises(ValueError, match="non-empty 'items' list"):
        load_questions_from_yaml(path)


def test_invalid_item_type(tmp_path: Path):
    path = write_yaml(tmp_path, "items: [1, 2, 3]\n")
    with pytest.raises(ValueError, match="must be a mapping"):
        load_questions_from_yaml(path)


def test_invalid_dimension(tmp_path: Path):
    yaml_text = """
items:
  - text: "Invalid dimension"
    dimension: X
"""
    path = write_yaml(tmp_path, yaml_text)
    with pytest.raises(ValueError, match="'dimension' must be one of"):
        load_questions_from_yaml(path)


def test_weight_and_reverse_parsing(tmp_path: Path):
    yaml_text = """
items:
  - text: "Reversed and weighted"
    dimension: I
    reverse: true
    weight: 3
  - text: "Other pairs to satisfy sanity"
    dimension: S
  - text: "Other pairs to satisfy sanity"
    dimension: T
  - text: "Other pairs to satisfy sanity"
    dimension: J
"""
    path = write_yaml(tmp_path, yaml_text)
    qs = load_questions_from_yaml(path)
    q0 = qs[0]
    assert q0.reverse is True
    assert q0.weight == 3


def test_missing_dichotomy_pair_raises(tmp_path: Path):
    # Missing J/P entirely
    yaml_text = """
items:
  - text: "E item"
    dimension: E
  - text: "S item"
    dimension: S
  - text: "T item"
    dimension: T
"""
    path = write_yaml(tmp_path, yaml_text)
    with pytest.raises(ValueError, match=r"missing both sides of dichotomy J/P"):
        load_questions_from_yaml(path)
