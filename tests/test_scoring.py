from mbti_cli.models import Question
from mbti_cli.scoring import score_responses


def test_simple_scoring():
    qs = [
        Question(text="q1", dimension="E"),
        Question(text="q2", dimension="I"),
        Question(text="q3", dimension="S"),
        Question(text="q4", dimension="N"),
        Question(text="q5", dimension="T"),
        Question(text="q6", dimension="F"),
        Question(text="q7", dimension="J"),
        Question(text="q8", dimension="P"),
    ]
    answers = [5, 3, 5, 1, 4, 2, 5, 1]

    res = score_responses(qs, answers)

    assert res.type in {
        "ESTJ",
        "ENTJ",
        "ESTP",
        "ENTP",
        "ESFJ",
        "ENFJ",
        "ESFP",
        "ENFP",
    }
    perc = res.percentages
    assert set(perc.keys()) == {"E/I", "S/N", "T/F", "J/P"}
