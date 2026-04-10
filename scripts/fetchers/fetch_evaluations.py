"""Fetch evaluation data from Source data/Evaluations/ and distribute to languages."""

from pathlib import Path

import yaml


EVALUATIONS_DIR = Path(__file__).parent.parent.parent / "Source data" / "Evaluations"


_CASCADE_FIELDS = ('source', 'source_url')


def _resolve_cascaded_fields(test_result, model_defaults, file_defaults):
    """Cascade source/source_url from file → model → result levels.

    Most-specific wins: if the result already has a value for a field, keep it;
    otherwise inherit from model-level; otherwise from file-level. Each field
    cascades independently.
    """
    out = dict(test_result)
    for key in _CASCADE_FIELDS:
        if out.get(key) is None:
            if model_defaults.get(key) is not None:
                out[key] = model_defaults[key]
            elif file_defaults.get(key) is not None:
                out[key] = file_defaults[key]
    return out


def _process_model_entry(model_entry, by_language, file_defaults):
    """Process a single model entry and add results to by_language dict."""
    model = model_entry.get('model', '')
    model_url = model_entry.get('model_url', '')
    task = model_entry.get('task', '')
    results = model_entry.get('results', {})

    if not task or not results:
        return

    model_defaults = {k: model_entry[k] for k in _CASCADE_FIELDS if k in model_entry}

    for iso_code, test_results in results.items():
        iso_code = str(iso_code)
        if iso_code not in by_language:
            by_language[iso_code] = {}
        if task not in by_language[iso_code]:
            by_language[iso_code][task] = []

        resolved_results = [
            _resolve_cascaded_fields(tr, model_defaults, file_defaults)
            for tr in test_results
        ]

        entry = {
            'model': model,
            'model_url': model_url,
            'results': resolved_results,
        }
        by_language[iso_code][task].append(entry)


def load_evaluation_sources():
    """Load all evaluation YAML files from Source data/Evaluations/.

    Supports two formats (single or multi-model), and a cascade for
    source / source_url at file, model, and result levels:

        # File-level defaults (apply to all results unless overridden)
        source: reported
        source_url: https://arxiv.org/abs/...

        models:
          - model: model-name
            model_url: https://...
            task: asr
            # Model-level override (optional)
            source_url: https://different-paper
            results:
              {iso_code}:
                - test_set: ...
                  # Result-level override (optional)
                  source_url: https://yet-another
                  metrics: [...]

    Most-specific wins. Each cascaded field is resolved independently.

    Returns a dict: {iso_code: {task: [entries]}}
    """
    by_language = {}

    if not EVALUATIONS_DIR.exists():
        return by_language

    for eval_file in sorted(EVALUATIONS_DIR.glob("*.yaml")):
        with open(eval_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        if not data:
            continue

        file_defaults = {k: data[k] for k in _CASCADE_FIELDS if k in data}

        if 'models' in data:
            for model_entry in data['models']:
                _process_model_entry(model_entry, by_language, file_defaults)
        else:
            _process_model_entry(data, by_language, file_defaults)

    return by_language


def get_evaluations_for_language(iso_code, all_evaluations):
    """Get evaluation entries for a specific language.

    Returns dict like:
        {
            'asr': [
                {
                    'model': 'openai/whisper-large-v3',
                    'model_url': '...',
                    'results': [
                        {'test_set': 'FLEURS', 'source': 'reported', ...}
                    ]
                }
            ]
        }
    """
    return all_evaluations.get(iso_code, {})
