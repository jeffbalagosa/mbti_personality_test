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
    mbti_descriptions = {
        "INTJ": "The Architect: Imaginative and strategic thinkers, with a plan for everything.",
        "INTP": "The Logician: Innovative inventors with an unquenchable thirst for knowledge.",
        "ENTJ": "The Commander: Bold, imaginative and strong-willed leaders.",
        "ENTP": "The Debater: Smart and curious thinkers who cannot resist an intellectual challenge.",
        "INFJ": "The Advocate: Quiet and mystical, yet very inspiring and tireless idealists.",
        "INFP": "The Mediator: Poetic, kind and altruistic, always eager to help a good cause.",
        "ENFJ": "The Protagonist: Charismatic and inspiring leaders, able to mesmerize their listeners.",
        "ENFP": "The Campaigner: Enthusiastic, creative and sociable free spirits.",
        "ISTJ": "The Logistician: Practical and fact-minded individuals, whose reliability cannot be doubted.",
        "ISFJ": "The Defender: Very dedicated and warm protectors, always ready to defend their loved ones.",
        "ESTJ": "The Executive: Excellent administrators, unsurpassed at managing things or people.",
        "ESFJ": "The Consul: Extraordinarily caring, social and popular people, always eager to help.",
        "ISTP": "The Virtuoso: Bold and practical experimenters, masters of all kinds of tools.",
        "ISFP": "The Adventurer: Flexible and charming artists, always ready to explore and experience something new.",
        "ESTP": "The Entrepreneur: Smart, energetic and very perceptive people, who truly enjoy living on the edge.",
        "ESFP": "The Entertainer: Spontaneous, energetic and enthusiastic people – life is never boring around them."
    }
    desc = mbti_descriptions.get(result.type, "")
    if desc:
        print(desc)
    print("\nScores:")
    for pair, (lp, rp) in result.percentages.items():
        a, b = pair.split("/")
        print(f"{a}: {lp}%  {b}: {rp}%")

    if args.pdf:
        from .pdf_report import generate_pdf
        generate_pdf(result, args.pdf, author=args.author)
        print(f"\nSaved PDF to: {args.pdf}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
