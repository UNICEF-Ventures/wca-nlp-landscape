#!/usr/bin/env python3
"""Collect numbers for the presentation slides.

Prints stats on focus languages, actors, models, datasets, benchmark
sources, tasks, and benchmark result counts (reported vs. evaluated).
"""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "Research"
LANGUAGES = RESEARCH / "Languages"
ACTORS = RESEARCH / "Actors"
EVAL_SOURCES = ROOT / "Source data" / "Evaluations"
FOCUSED = RESEARCH / "focused_languages.yaml"

CLEAR_MANUAL_SOURCE = "CLEAR_manual_benchmarking.yaml"


def load_yaml(path: Path):
    if not path.exists():
        return None
    with path.open() as f:
        return yaml.safe_load(f)


def count_focus_languages():
    data = load_yaml(FOCUSED) or {}
    return len(data.get("priority", [])), len(data.get("extended", []))


def count_actors():
    return sum(
        1 for p in ACTORS.glob("*.yaml")
        if p.name not in {"actor-template.yaml"}
    )


def count_eval_sources():
    return sum(1 for p in EVAL_SOURCES.glob("*.yaml"))


def iter_language_dirs():
    for d in sorted(LANGUAGES.iterdir()):
        if d.is_dir():
            yield d


def collect_model_dataset_stats():
    total_models = 0
    total_datasets = 0
    unique_models = set()
    unique_datasets = set()
    tasks = set()
    for d in iter_language_dirs():
        models = load_yaml(d / "models.yaml") or {}
        datasets = load_yaml(d / "datasets.yaml") or {}
        for task, block in models.items():
            if isinstance(block, dict) and "items" in block:
                tasks.add(task)
                items = block["items"] or []
                total_models += len(items)
                for item in items:
                    unique_models.add(item.get("name"))
        for task, block in datasets.items():
            if isinstance(block, dict) and "items" in block:
                tasks.add(task)
                items = block["items"] or []
                total_datasets += len(items)
                for item in items:
                    unique_datasets.add(item.get("name"))
    return total_models, total_datasets, len(unique_models), len(unique_datasets), tasks


def collect_benchmark_stats():
    """Count benchmark results across all languages.

    A 'result' = one (model, test_set, language) tuple.
    Split by whether the result came from a paper/reported source or from
    CLEAR Global's own manual benchmarking runs.
    """
    reported = 0
    evaluated_clear = 0
    evaluated_other = 0
    benchmark_tasks = set()

    for d in iter_language_dirs():
        lang = d.name
        for fname in ("benchmarks.yaml", "benchmarks_manual.yaml"):
            data = load_yaml(d / fname) or {}
            evals = data.get("evaluations") or {}
            for task, models in evals.items():
                if not isinstance(models, list):
                    continue
                benchmark_tasks.add(task)
                for entry in models:
                    results = entry.get("results") or []
                    for r in results:
                        source = (r.get("source") or "").lower()
                        source_url = r.get("source_url") or ""
                        if source == "evaluated":
                            if "Manual-Benchmarking-WCARO" in source_url or \
                               "translatorswb/Manual-Benchmarking" in source_url:
                                evaluated_clear += 1
                            else:
                                evaluated_other += 1
                        else:
                            reported += 1
    return reported, evaluated_clear, evaluated_other, benchmark_tasks


def main():
    priority, extended = count_focus_languages()
    actors = count_actors()
    eval_sources = count_eval_sources()
    total_models, total_datasets, unique_models, unique_datasets, model_tasks = collect_model_dataset_stats()
    reported, evaluated_clear, evaluated_other, bench_tasks = collect_benchmark_stats()

    print("=" * 60)
    print("WCA NLP Landscape — slide stats")
    print("=" * 60)
    print(f"Priority languages:          {priority}")
    print(f"Extended focus languages:    {extended}")
    print(f"Total focus languages:       {priority + extended}")
    print()
    print(f"Actors profiled:             {actors}")
    print()
    print(f"Evaluation source files:     {eval_sources}")
    print(f"  (in Source data/Evaluations/)")
    print()
    print(f"Models (total across langs): {total_models}")
    print(f"Models (unique):             {unique_models}")
    print(f"Datasets (total across langs): {total_datasets}")
    print(f"Datasets (unique):           {unique_datasets}")
    print(f"NLP tasks covered (models):  {sorted(model_tasks)}")
    print()
    print(f"Benchmark tasks covered:     {sorted(bench_tasks)}")
    print(f"Benchmark results (reported from papers/projects):")
    print(f"  {reported}")
    print(f"Benchmark results (run by CLEAR Global for this project):")
    print(f"  {evaluated_clear}")
    if evaluated_other:
        print(f"Benchmark results (other 'evaluated'):   {evaluated_other}")
    print()
    print("=" * 60)


if __name__ == "__main__":
    main()
