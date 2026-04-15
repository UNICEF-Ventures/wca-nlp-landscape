"""Benchmark coverage tab — reads Research/benchmark_coverage.md produced by populate_research.py."""

from pathlib import Path
import re
import yaml

_RESEARCH_DIR = Path(__file__).resolve().parent.parent.parent / "Research"
_COVERAGE_MD   = _RESEARCH_DIR / "benchmark_coverage.md"
_FOCUSED_YAML  = _RESEARCH_DIR / "focused_languages.yaml"

_TASKS = ["ASR", "TTS", "MT", "LLM"]

_COLORS = {
    "C": ("#2E9E6A", "white",   "✓", "Published benchmark"),
    "M": ("#E76A24", "white",   "✎", "Evaluated for this study"),
    "N": ("#E6E6E6", "#8A8A8A", "–", "No valid test data"),
}

_BENCHMARKING_REPO = "https://github.com/translatorswb/Manual-Benchmarking-WCARO-NLP-Landscape"


def _load_coverage() -> dict[str, list[str]]:
    """Parse benchmark_coverage.md and return {iso: [ASR, TTS, MT, LLM]}."""
    text = _COVERAGE_MD.read_text(encoding="utf-8")
    coverage = {}
    for line in text.splitlines():
        # Data rows look like: | iso | C | N | M | C | Language name |
        if not line.startswith("|") or line.startswith("|---") or "ISO" in line or "Total" in line:
            continue
        parts = [p.strip() for p in line.strip().strip("|").split("|")]
        if len(parts) < 5:
            continue
        iso = parts[0]
        cells = parts[1:5]  # ASR, TTS, MT, LLM
        if re.match(r'^[a-z]{2,3}$', iso):
            coverage[iso] = cells
    return coverage


def _load_focused() -> tuple[list[str], list[str]]:
    data = yaml.safe_load(_FOCUSED_YAML.read_text(encoding="utf-8"))
    return data.get("priority", []), data.get("extended", [])


def _lang_name(iso: str) -> str:
    info_path = _RESEARCH_DIR / "Languages" / iso / "info.yaml"
    if info_path.exists():
        info = yaml.safe_load(info_path.read_text(encoding="utf-8")) or {}
        return info.get("name", iso)
    return iso


def _cell(code: str) -> str:
    code = code if code in _COLORS else "N"
    bg, fg, sym, _ = _COLORS[code]
    return (
        f'<td style="text-align:center; padding:0.3rem; border:none; background:none;">'
        f'<div style="background:{bg}; color:{fg}; border-radius:6px; '
        f'width:32px; height:28px; display:flex; align-items:center; '
        f'justify-content:center; font-size:1rem; font-weight:700; margin:auto;">'
        f'{sym}</div></td>'
    )


def _header_row(isos: list[str]) -> str:
    cells = '<th style="border:none; background:none;"></th>'
    for iso in isos:
        name = _lang_name(iso)
        cells += (
            f'<th style="writing-mode:vertical-rl; transform:rotate(180deg); '
            f'padding:0.4rem 0.3rem; font-size:0.82rem; font-weight:600; '
            f'color:#1A1A1A; white-space:nowrap; vertical-align:bottom; '
            f'border:none; background:none; min-width:28px;">'
            f'<a href="lang/{iso}.html" style="color:#1A1A1A; text-decoration:none;"'
            f' onmouseover="this.style.color=\'#E76A24\'" onmouseout="this.style.color=\'#1A1A1A\'">'
            f'{name}</a></th>'
        )
    return f'<tr>{cells}</tr>'


def _data_rows(isos: list[str], coverage: dict) -> str:
    html = ""
    for ti, task in enumerate(_TASKS):
        cells = (
            f'<td style="padding:0.35rem 0.7rem 0.35rem 0; font-size:0.95rem; '
            f'font-weight:700; color:#152C5B; white-space:nowrap; '
            f'border:none; background:none;">{task}</td>'
        )
        for iso in isos:
            codes = coverage.get(iso, ["N", "N", "N", "N"])
            cells += _cell(codes[ti])
        html += f'<tr>{cells}</tr>\n'
    return html


def _table(isos: list[str], coverage: dict, caption: str) -> str:
    return f"""
<div style="margin-bottom:2rem;">
    <h3 style="color:#152C5B; margin-bottom:0.75rem; font-size:1rem;
               text-transform:uppercase; letter-spacing:0.05em;">{caption}</h3>
    <div style="overflow-x:auto;">
        <table style="border-collapse:separate; border-spacing:4px; background:none;">
            <thead>{_header_row(isos)}</thead>
            <tbody>{_data_rows(isos, coverage)}</tbody>
        </table>
    </div>
</div>"""


def _legend() -> str:
    items = ""
    for code, (bg, fg, sym, label) in _COLORS.items():
        items += (
            f'<span style="display:inline-flex; align-items:center; gap:0.4rem; margin-right:1.2rem;">'
            f'<span style="background:{bg}; color:{fg}; border-radius:5px; '
            f'width:26px; height:22px; display:inline-flex; align-items:center; '
            f'justify-content:center; font-size:0.85rem; font-weight:700;">{sym}</span>'
            f'<span style="font-size:0.88rem; color:#444;">{label}</span>'
            f'</span>'
        )
    return f'<div style="margin-top:1.2rem; display:flex; flex-wrap:wrap; gap:0.2rem;">{items}</div>'


def generate_benchmark_coverage_tab() -> str:
    """Return HTML for the Benchmark Coverage tab."""
    priority_isos, extended_isos = _load_focused()
    coverage = _load_coverage()

    return f"""
<div style="padding:1.5rem 0; max-width:1200px;">

    <h2 style="color:#152C5B; margin-bottom:0.5rem;">Benchmark coverage — focus languages</h2>
    <p style="margin:0 0 0.7rem 0; color:#1A1A1A; max-width:760px;">
        <strong>What is benchmarking?</strong>
        Benchmarking measures how well an NLP model performs on a standardised test set,
        producing scores like Word Error Rate (WER) for speech or BLEU for translation.
        Comparable scores across models and languages make it possible to identify gaps
        and prioritise where new tools are needed.
    </p>
    <p style="margin:0 0 2rem 0; color:#1A1A1A; max-width:760px;">
        For this study we compiled <strong>over 1,600 publicly reported benchmark results</strong>
        from model papers, leaderboards and evaluation campaigns. Detailed results for each language
        are available on the individual language pages. For languages where no published evaluation
        existed, we <strong>manually ran 28 additional evaluations</strong> using held-out test data.
        For more information on our methodology and detailed results check
        <a href="{_BENCHMARKING_REPO}" target="_blank" style="color:#E76A24; font-weight:600;"
        >CLEAR Global's Github repository</a>.
    </p>

    <p style="margin:0 0 1.5rem 0; color:#1A1A1A; max-width:760px;">
        The tables below give an overview of which languages have benchmark results for each NLP task
        (ASR, TTS, MT, LLM), and which ones we ran manually as part of this study where no published
        evaluation existed. Click any language name to see the detailed results.
    </p>

    {_table(priority_isos, coverage, f"Priority languages ({len(priority_isos)})")}

    <hr style="border:none; border-top:2px solid #dee2e6; margin:0.5rem 0 1.5rem 0;">

    {_table(extended_isos, coverage, f"Extended languages ({len(extended_isos)})")}

    {_legend()}
</div>
"""
