from __future__ import annotations

import argparse
from typing import List

from .data_loader import load_questions_from_yaml
from .controller import collect_answers, prompt_intro
from .scoring import score_responses


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MBTI Personality Test (CLI)")
    p.add_argument(
        "--questions",
        default="config/mbti_questionnaire.yaml",
        help="Path to YAML questions file",
    )
    p.add_argument("--pdf", help="Path to output PDF (optional)")
    p.add_argument(
        "--author",
        default="",
        help="Author name for PDF (optional)",
    )
    return p


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    questions = load_questions_from_yaml(args.questions)

    prompt_intro()
    answers = collect_answers(questions)

    result = score_responses(questions, answers)

    print("\nYour MBTI Type:", result.type)
    print("\nScores:")
    for pair, (lp, rp) in result.percentages.items():
        a, b = pair.split("/")
        print(f"{a}: {lp}%  {b}: {rp}%")

    if args.pdf:
        # Placeholder: PDF generation not yet implemented in this scaffold.
        print(
            f"\nPDF generation not yet implemented. Would save to: {args.pdf}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
