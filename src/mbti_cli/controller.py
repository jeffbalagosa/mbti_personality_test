from __future__ import annotations

from typing import List

from .models import Likert, Question


def prompt_intro() -> None:
    print("MBTI Personality Test")
    print(
        "Please answer each statement on a scale of 1 (Strongly Disagree) "
        "to 5 (Strongly Agree)."
    )
    print(
        "Commands: 1-5 to answer, 'z' to undo last, 'done' to finish when all "
        "answered.\n"
    )


def prompt_question(idx: int, total: int, text: str) -> None:
    print(f"[{idx+1}/{total}] {text}")


def collect_answers(questions: List[Question], input_fn=input) -> List[Likert]:
    answers: List[Likert] = []
    total = len(questions)
    while len(answers) < total:
        q = questions[len(answers)]
        prompt_question(len(answers), total, q.text)
        raw = input_fn("> ").strip().lower()
        if raw == "z":
            if answers:
                answers.pop()
                print("Undid last answer.\n")
            else:
                print("Nothing to undo.\n")
            continue
        if raw == "done":
            if len(answers) == total:
                break
            print("You must answer all questions before finishing.\n")
            continue
        try:
            val = int(raw)
        except ValueError:
            print("Enter 1-5, 'z' to undo, or 'done' to finish.\n")
            continue
        if val < 1 or val > 5:
            print("Value must be between 1 and 5.\n")
            continue
        answers.append(val)  # type: ignore[arg-type]
        print()
    return answers
