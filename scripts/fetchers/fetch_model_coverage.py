"""Generic multilingual model coverage loader.

Scans Source data/Multilingual-models/*.yaml and extracts tech_resources
labels for each supported language.

Each YAML file must have:
  - tech_resources_label: Label to show in NLP & Tech Resources (e.g. "AfriNLLB")
  - languages: dict keyed by ISO 639-3 code

Optional:
  - multitask: true  — instead of one label, adds {label}-{TASK} for each
    boolean field that is true (e.g. MMS with asr/tts/lid → MMS-ASR, MMS-TTS, MMS-LID)

Languages with role: pivot (e.g. English, French) are skipped.

To add a new model: create a YAML file in Source data/Multilingual-models/,
include a tech_resources_label and list supported languages under languages:.
"""

from pathlib import Path

import yaml


MODELS_DIR = Path(__file__).parent.parent.parent / "Source data" / "Multilingual-models"

# Fields in a language entry that are metadata, not tasks
_META_FIELDS = {'name', 'role'}


def load_model_coverage():
    """Load all multilingual model coverage files.

    Returns:
        dict: {iso_639_3: [label1, label2, ...]}
    """
    by_language = {}

    if not MODELS_DIR.exists():
        return by_language

    for coverage_file in sorted(MODELS_DIR.glob("*.yaml")):
        with open(coverage_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            continue

        label = data.get('tech_resources_label')
        if not label:
            continue

        multitask = data.get('multitask', False)
        languages = data.get('languages', {})

        for iso_code, info in languages.items():
            if not isinstance(info, dict):
                continue
            if info.get('role') == 'pivot':
                continue

            if multitask:
                for field, value in info.items():
                    if field in _META_FIELDS:
                        continue
                    if value is True:
                        by_language.setdefault(iso_code, []).append(f"{label}-{field.upper()}")
            else:
                by_language.setdefault(iso_code, []).append(label)

    return by_language
