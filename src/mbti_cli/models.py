from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MBTILetter = Literal["E", "I", "S", "N", "T", "F", "J", "P"]
Likert = Literal[1, 2, 3, 4, 5]


@dataclass(frozen=True)
class Question:
    text: str
    dimension: MBTILetter
    reverse: bool = False
    weight: int = 1


@dataclass(frozen=True)
class Response:
    question_idx: int
    value: Likert
