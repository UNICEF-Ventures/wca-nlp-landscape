"""Data loading functions."""

import yaml

from .constants import LANGUAGES_DIR, ACTORS_DIR, WCA_LANGUAGES_PATH, FOCUSED_LANGUAGES_PATH


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
            'benchmarks': load_yaml(lang_dir / "benchmarks.yaml"),
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


def load_wca_languages():
    """Load all WCA languages from wca_all_languages.yaml."""
    if not WCA_LANGUAGES_PATH.exists():
        return []
    data = load_yaml(WCA_LANGUAGES_PATH)
    return data.get('languages', [])
