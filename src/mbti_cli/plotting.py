from __future__ import annotations
import io
from typing import Dict, Tuple
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")


def render_percentages_bar(percentages: Dict[str, Tuple[int, int]]) -> bytes:
    pairs = list(percentages.keys())
    left = [percentages[p][0] for p in pairs]
    right = [percentages[p][1] for p in pairs]

    fig, ax = plt.subplots(figsize=(6, 3))
    x = range(len(pairs))
    width = 0.35
    ax.bar([i - width / 2 for i in x], left, width, label="Left")
    ax.bar([i + width / 2 for i in x], right, width, label="Right")
    ax.set_ylim(0, 100)
    ax.set_xticks(list(x))
    ax.set_xticklabels(pairs)
    ax.set_ylabel("Percent")
    ax.legend(frameon=False)
    for i, v in enumerate(left):
        ax.text(i - width / 2, v + 1, f"{v}%", ha="center", va="bottom", fontsize=8)
    for i, v in enumerate(right):
        ax.text(i + width / 2, v + 1, f"{v}%", ha="center", va="bottom", fontsize=8)
    buf = io.BytesIO()
    fig.tight_layout()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf.getvalue()
