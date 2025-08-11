from __future__ import annotations

from typing import Callable, List

from mbti_cli.controller import collect_answers
from mbti_cli.models import Question


def make_input_fn(responses: List[str]) -> Callable[[str], str]:
    it = iter(responses)

    def _inp(_: str = "> ") -> str:
        return next(it)

    return _inp


def test_collect_answers_happy_path():
    qs = [
        Question(text="q1", dimension="E"),
        Question(text="q2", dimension="S"),
        Question(text="q3", dimension="T"),
    ]
    inputs = ["1", "2", "5"]
    out = collect_answers(qs, input_fn=make_input_fn(inputs))
    assert out == [1, 2, 5]


def test_collect_answers_undo():
    qs = [
        Question(text="q1", dimension="E"),
        Question(text="q2", dimension="S"),
        Question(text="q3", dimension="T"),
    ]
    # 1, 2, undo, 3, 4 -> final should be [1,3,4]
    inputs = ["1", "2", "z", "3", "4"]
    out = collect_answers(qs, input_fn=make_input_fn(inputs))
    assert out == [1, 3, 4]


def test_collect_answers_done_gate():
    qs = [
        Question(text="q1", dimension="E"),
        Question(text="q2", dimension="S"),
        Question(text="q3", dimension="T"),
    ]
    # Try to finish early; then complete the rest
    inputs = ["1", "done", "2", "3"]
    out = collect_answers(qs, input_fn=make_input_fn(inputs))
    assert out == [1, 2, 3]


def test_collect_answers_invalid_entries_are_ignored():
    qs = [
        Question(text="q1", dimension="E"),
        Question(text="q2", dimension="S"),
        Question(text="q3", dimension="T"),
    ]
    # invalid: letter, 0, 6 -> then valid 3,3,3
    inputs = ["x", "0", "6", "3", "3", "3"]
    out = collect_answers(qs, input_fn=make_input_fn(inputs))
    assert out == [3, 3, 3]
