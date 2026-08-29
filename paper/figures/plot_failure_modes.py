"""Generate two symmetric vertical failure-mode bar charts."""

from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

OUT_DIR = Path(__file__).resolve().parent

PANELS = [
    {
        "title": "(a) Attack-derived  ·  n = 717",
        "rows": [
            ("Criterion\nrules", 349, 48.7, "primary"),
            ("Salience\nallocation", 248, 34.6, "primary"),
            ("Refusal–\nsubstance", 65, 9.1, "primary"),
            ("Rep. /\nreasoning", 55, 7.7, "primary"),
            ("Incoherent\nverdict†", 112, 27.5, "cross"),
            ("Hallucinated\nevidence", 41, 5.7, "cross"),
        ],
    },
    {
        "title": "(b) TVD-Conflict  ·  n = 1,681",
        "rows": [
            ("Criterion\nrules", 649, 38.6, "primary"),
            ("Salience\nallocation", 506, 30.1, "primary"),
            ("Refusal–\nsubstance", 405, 24.1, "primary"),
            ("Rep. /\nreasoning", 121, 7.2, "primary"),
            ("Incoherent\nverdict†", 107, 13.9, "cross"),
            ("Hallucinated\nevidence", 99, 5.9, "cross"),
        ],
    },
]

PRIMARY = "#3C5488"
CROSS = "#E69F00"


def draw_panel(ax, panel, show_ylabel):
    x = np.arange(6)
    labels = [row[0] for row in panel["rows"]]
    counts = [row[1] for row in panel["rows"]]
    shares = [row[2] for row in panel["rows"]]
    colors = [PRIMARY if row[3] == "primary" else CROSS for row in panel["rows"]]
    bars = ax.bar(x, counts, width=0.68, color=colors,
                  edgecolor="white", linewidth=0.5)
    ax.set_ylim(0, 735)
    ax.set_yticks([0, 100, 200, 300, 400, 500, 600, 700])
    ax.set_xticks(x, labels)
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.5)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="both", length=0)
    ax.tick_params(axis="x", pad=5, labelsize=6.35)
    ax.tick_params(axis="y", labelleft=show_ylabel)
    ax.set_title(panel["title"], fontsize=9.3, fontweight="semibold", pad=8)
    if show_ylabel:
        ax.set_ylabel("Number of conflicts")

    for bar, count, share in zip(bars, counts, shares):
        ax.text(bar.get_x() + bar.get_width() / 2, count + 10,
                f"{count:,}\n{share:.1f}%", ha="center", va="bottom",
                fontsize=6.8, color="#222222", linespacing=0.9)


def main():
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 8,
        "xtick.color": "#333333",
        "ytick.color": "#555555",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.95), sharey=True,
                             gridspec_kw={"wspace": 0.12})
    draw_panel(axes[0], PANELS[0], True)
    draw_panel(axes[1], PANELS[1], False)

    fig.text(0.36, 0.985, "■", color=PRIMARY, ha="right", va="top", fontsize=9)
    fig.text(0.365, 0.985, "Primary", color="#333333", ha="left", va="top", fontsize=7.5)
    fig.text(0.49, 0.985, "■", color=CROSS, ha="right", va="top", fontsize=9)
    fig.text(0.495, 0.985, "Cross-cutting", color="#333333", ha="left", va="top", fontsize=7.5)
    fig.text(0.64, 0.985, "† Binary conflicts only", color="#666666",
             ha="left", va="top", fontsize=7.3)

    fig.subplots_adjust(left=0.075, right=0.995, bottom=0.25, top=0.81)
    for suffix in ("pdf", "svg", "png"):
        kwargs = {"bbox_inches": "tight", "pad_inches": 0.02}
        if suffix == "png":
            kwargs["dpi"] = 300
        fig.savefig(OUT_DIR / f"failure_modes.{suffix}", **kwargs)
    plt.close(fig)


if __name__ == "__main__":
    main()
