#!/usr/bin/env python3
"""Generate the benchmark coverage matrix figure for the presentation.

Shows, for each priority language × task cell:
  - "covered"  (published benchmarks exist)
  - "manual"   (we ran the evaluation ourselves)
  - "none"     (no feasible evaluation path)

Output: Event/Presentation/Images/benchmark_coverage_matrix.png
16:9 aspect ratio, horizontal layout (languages as columns).

Data from Project documents/Manual Benchmarking — UNICEF WCARO NLP Landscape(3).docx
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Event" / "Presentation" / "Images" / "benchmark_coverage_matrix.png"

# Palette
COVERED = "#2E9E6A"   # green
MANUAL = "#E76A24"    # orange (CLEAR Global brand)
NONE = "#E6E6E6"      # light gray
TEXT = "#1A1A1A"
HEADER = "#152C5B"    # deep blue
SUBTLE = "#6B6B6B"

# (Language, ISO, ASR, TTS, MT, LLM); codes: C=covered, M=manual, N=none
DATA = [
    ("Hausa",              "hau", "C", "C", "C", "C"),
    ("Twi",                "twi", "C", "C", "C", "C"),
    ("Bambara",            "bam", "C", "N", "C", "C"),
    ("Dyula",              "dyu", "C", "N", "C", "C"),
    ("Fulfulde",           "ful", "C", "N", "C", "C"),
    ("Ewe",                "ewe", "M", "C", "C", "C"),
    ("Mooré",              "mos", "M", "N", "C", "C"),
    ("Dagbani",            "dag", "M", "N", "M", "N"),
    ("Nigerian Fulfulde",  "fuv", "M", "N", "M", "C"),
    ("C-E Niger Fulfulde", "fuq", "M", "N", "N", "N"),
    ("Pulaar",             "fuc", "N", "N", "M", "N"),
    ("Soninke",            "snk", "M", "N", "N", "N"),
    ("Koyraboro Senni",    "ses", "N", "N", "N", "N"),
    ("Gourmanché",         "gux", "N", "N", "N", "N"),
    ("Escarpment Dogon",   "dts", "N", "N", "N", "N"),
    ("Maasina Fulfulde",   "ffm", "N", "N", "N", "N"),
    ("W. Niger Fulfulde",  "fuh", "N", "N", "N", "N"),
]

TASKS = ["ASR", "TTS", "MT", "LLM"]

COLOR = {"C": COVERED, "M": MANUAL, "N": NONE}
SYMBOL = {"C": "✓", "M": "✎", "N": "–"}


def main():
    n_cols = len(DATA)
    n_rows = len(TASKS)

    # 16:9 figure
    fig_w, fig_h = 16, 9
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=200)
    fig.patch.set_facecolor("white")

    # Coordinate system: width 16, height 9 (matches fig ratio)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.set_aspect("equal")
    ax.axis("off")

    # ---- Title block (top) ----
    title_y = 8.25
    ax.text(
        0.6, title_y,
        "Benchmark coverage — priority languages",
        ha="left", va="center",
        fontsize=24, fontweight="bold", color=HEADER,
    )
    ax.text(
        0.6, title_y - 0.45,
        "Where published benchmarks exist, where we filled the gaps, and where evaluation isn't feasible.",
        ha="left", va="center",
        fontsize=12, color=SUBTLE, style="italic",
    )

    # ---- Grid layout ----
    # Grid occupies bottom-middle. Leave room above for rotated language labels.
    grid_left = 2.35
    grid_right = 15.6
    grid_width = grid_right - grid_left
    gap = 0.09
    cell_w = (grid_width - (n_cols - 1) * gap) / n_cols
    cell_h = 0.62
    grid_bottom = 1.55  # leave room for legend below

    # Row (task) labels
    for ri, task in enumerate(TASKS):
        y_center = grid_bottom + (n_rows - 1 - ri) * (cell_h + gap) + cell_h / 2
        ax.text(
            grid_left - 0.25, y_center, task,
            ha="right", va="center",
            fontsize=18, fontweight="bold", color=HEADER,
        )

    # Cells
    for ri in range(n_rows):
        for ci, row in enumerate(DATA):
            code = row[2 + ri]
            x = grid_left + ci * (cell_w + gap)
            y = grid_bottom + (n_rows - 1 - ri) * (cell_h + gap)
            box = FancyBboxPatch(
                (x, y), cell_w, cell_h,
                boxstyle="round,pad=0.008,rounding_size=0.10",
                linewidth=0,
                facecolor=COLOR[code],
            )
            ax.add_patch(box)
            ax.text(
                x + cell_w / 2, y + cell_h / 2,
                SYMBOL[code],
                ha="center", va="center",
                fontsize=16, fontweight="bold",
                color="white" if code != "N" else "#8A8A8A",
            )

    # Column headers (rotated language names)
    headers_baseline = grid_bottom + n_rows * (cell_h + gap) - gap + 0.15
    for ci, row in enumerate(DATA):
        name = row[0]
        x = grid_left + ci * (cell_w + gap) + cell_w / 2
        ax.text(
            x, headers_baseline, name,
            ha="left", va="bottom",
            rotation=40, rotation_mode="anchor",
            fontsize=11.5, color=TEXT,
        )

    # ---- Legend (below grid) ----
    legend_y = 0.55
    legend_items = [
        (COVERED, "✓", "Published benchmark"),
        (MANUAL,  "✎", "Evaluated for this study"),
        (NONE,    "–", "No valid test data"),
    ]
    # Compute widths so items sit flush against each other with a fixed gap.
    # Approximate text width: ~0.145 units per char at fontsize 11.5.
    char_w = 0.145
    swatch_w = 0.45
    swatch_pad = 0.18  # space between swatch and text
    inter_gap = 1.1    # space between legend entries
    widths = [swatch_w + swatch_pad + len(lbl) * char_w for _, _, lbl in legend_items]
    total = sum(widths) + inter_gap * (len(legend_items) - 1)
    lx = grid_left + (grid_width - total) / 2  # center under the grid
    for (color, sym, label), w in zip(legend_items, widths):
        swatch = FancyBboxPatch(
            (lx, legend_y), swatch_w, swatch_w,
            boxstyle="round,pad=0.01,rounding_size=0.08",
            linewidth=0, facecolor=color,
        )
        ax.add_patch(swatch)
        ax.text(
            lx + swatch_w / 2, legend_y + swatch_w / 2, sym,
            ha="center", va="center",
            fontsize=13, fontweight="bold",
            color="white" if color != NONE else "#8A8A8A",
        )
        ax.text(
            lx + swatch_w + swatch_pad, legend_y + swatch_w / 2, label,
            ha="left", va="center",
            fontsize=11.5, color=TEXT,
        )
        lx += w + inter_gap

    OUT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUT, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
