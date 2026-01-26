"""Fetch evaluation data from Source data/Evaluations/ and distribute to languages."""

from pathlib import Path

import yaml


EVALUATIONS_DIR = Path(__file__).parent.parent.parent / "Source data" / "Evaluations"


def _process_model_entry(model_entry, by_language):
    """Process a single model entry and add results to by_language dict."""
    model = model_entry.get('model', '')
    model_url = model_entry.get('model_url', '')
    task = model_entry.get('task', '')
    results = model_entry.get('results', {})

    if not task or not results:
        return

    for iso_code, test_results in results.items():
        iso_code = str(iso_code)
        if iso_code not in by_language:
            by_language[iso_code] = {}
        if task not in by_language[iso_code]:
            by_language[iso_code][task] = []

        entry = {
            'model': model,
            'model_url': model_url,
            'results': test_results,
        }
        by_language[iso_code][task].append(entry)


def load_evaluation_sources():
    """Load all evaluation YAML files from Source data/Evaluations/.

    Supports two formats:

    Single model:
        model: model-name
        model_url: https://...
        task: asr
        results:
          {iso_code}:
            - test_set: ...
              metrics: [...]

    Multiple models:
        models:
          - model: model-name
            model_url: https://...
            task: asr
            results:
              {iso_code}:
                - test_set: ...
                  metrics: [...]

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

        if 'models' in data:
            for model_entry in data['models']:
                _process_model_entry(model_entry, by_language)
        else:
            _process_model_entry(data, by_language)

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
