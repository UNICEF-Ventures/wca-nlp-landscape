"""Data loading functions."""

import yaml

from .constants import LANGUAGES_DIR, ACTORS_DIR, WCA_LANGUAGES_PATH, FOCUSED_LANGUAGES_PATH, SOURCES_PATH


def load_yaml(path):
    """Load YAML file, return empty dict if not found."""
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def load_markdown(path):
    """Load markdown file, return empty string if not found."""
    if not path.exists():
        return ""
    with open(path, 'r') as f:
        return f.read()


def load_focused_languages():
    """Load focused languages list (ISO codes)."""
    if not FOCUSED_LANGUAGES_PATH.exists():
        return []
    data = load_yaml(FOCUSED_LANGUAGES_PATH)
    if isinstance(data, list):
        return data
    return []


def merge_evaluations(auto_evals, manual_evals):
    """Merge evaluation entries from auto and manual benchmark files.

    For each task (asr, translation, llm, etc.), combines entries.
    If the same model + test_set appears in both, manual wins.
    """
    if not auto_evals and not manual_evals:
        return {}
    if not auto_evals:
        return manual_evals
    if not manual_evals:
        return auto_evals

    merged = {}
    all_tasks = set(list(auto_evals.keys()) + list(manual_evals.keys()))

    for task in all_tasks:
        auto_entries = auto_evals.get(task, [])
        manual_entries = manual_evals.get(task, [])

        # Index manual entries by (model, test_set) for override detection
        manual_keys = set()
        for entry in manual_entries:
            for result in entry.get('results', []):
                manual_keys.add((entry.get('model', ''), result.get('test_set', '')))

        # Add auto entries, skipping any overridden by manual
        combined = list(manual_entries)
        for entry in auto_entries:
            model = entry.get('model', '')
            filtered_results = [
                r for r in entry.get('results', [])
                if (model, r.get('test_set', '')) not in manual_keys
            ]
            if filtered_results:
                combined.append({**entry, 'results': filtered_results})

        merged[task] = combined

    return merged


def load_benchmarks(lang_dir):
    """Load and merge benchmarks.yaml and benchmarks_manual.yaml."""
    auto = load_yaml(lang_dir / "benchmarks.yaml")
    manual = load_yaml(lang_dir / "benchmarks_manual.yaml")

    # Start with auto data (common_voice etc.)
    merged = dict(auto)

    # Merge evaluations from both files
    auto_evals = auto.get('evaluations', {})
    manual_evals = manual.get('evaluations', {})
    combined_evals = merge_evaluations(auto_evals, manual_evals)
    if combined_evals:
        merged['evaluations'] = combined_evals

    # Merge unbenchmarked_models (concatenate both lists)
    auto_unbenched = auto.get('unbenchmarked_models', [])
    manual_unbenched = manual.get('unbenchmarked_models', [])
    combined_unbenched = auto_unbenched + manual_unbenched
    if combined_unbenched:
        merged['unbenchmarked_models'] = combined_unbenched

    return merged


def load_all_languages():
    """Load all language data from Research/Languages/."""
    languages = {}

    if not LANGUAGES_DIR.exists():
        return languages

    for lang_dir in sorted(LANGUAGES_DIR.iterdir()):
        if not lang_dir.is_dir() or lang_dir.name.startswith('.'):
            continue

        iso_code = lang_dir.name
        languages[iso_code] = {
            'info': load_yaml(lang_dir / "info.yaml"),
            'models': load_yaml(lang_dir / "models.yaml"),
            'datasets': load_yaml(lang_dir / "datasets.yaml"),
            'benchmarks': load_benchmarks(lang_dir),
            'notes': load_markdown(lang_dir / "notes.md"),
        }

    return languages


def load_all_actors():
    """Load all actor data from Research/Actors/."""
    actors = {}

    if not ACTORS_DIR.exists():
        return actors

    for actor_file in sorted(ACTORS_DIR.glob("*.yaml")):
        actor_key = actor_file.stem
        actors[actor_key] = load_yaml(actor_file)

    return actors


def load_sources():
    """Load sources data from Source data/sources.yaml."""
    data = load_yaml(SOURCES_PATH)
    return {
        'data_sources': data.get('data_sources', []),
        'benchmark_sources': data.get('benchmark_sources', []),
    }


def load_wca_languages():
    """Load all WCA languages from wca_all_languages.yaml."""
    if not WCA_LANGUAGES_PATH.exists():
        return []
    data = load_yaml(WCA_LANGUAGES_PATH)
    return data.get('languages', [])
