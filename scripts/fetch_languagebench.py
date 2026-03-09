#!/usr/bin/env python3
"""
Fetch LanguageBench results and generate evaluation YAML.

Pulls data from fair-forward/evals-for-every-language-results on HuggingFace
and generates Source data/Evaluations/languagebench.yaml with top N models
per task per language.

Usage:
    python scripts/fetch_languagebench.py                  # defaults: top 3, output to Source data/Evaluations/languagebench.yaml
    python scripts/fetch_languagebench.py --top 5          # top 5 models per task
    python scripts/fetch_languagebench.py -o output.yaml   # custom output path
    python scripts/fetch_languagebench.py --top 3 -o out.yaml
"""

import argparse
import sys
from datetime import date
from pathlib import Path

import yaml

# BCP-47 to our ISO 639-3 mapping for focus languages in languagebench
BCP_TO_ISO = {
    'ak': 'aka', 'bm': 'bam', 'dyu': 'dyu', 'ee': 'ewe', 'fon': 'fon',
    'fuv': 'fuv', 'ha': 'hau', 'ig': 'ibo', 'ln': 'lin', 'mos': 'mos',
    'sg': 'sag', 'wo': 'wol', 'yo': 'yor'
}

# Languages with existing MMLU/MGSM from IrokoBench (full test sets, much better than 10-sample)
HAS_EXISTING_MMLU = {'hau', 'yor', 'ibo', 'ewe', 'wol', 'lin'}

# Task key -> (test_set_human, test_set_machine)
TASK_TEST_SETS = {
    'translation_from': ('FLORES+ 10-sample', 'FLORES+ Synthetic 10-sample'),
    'translation_to':   ('FLORES+ 10-sample', 'FLORES+ Synthetic 10-sample'),
    'classification':   ('SIB-200 10-sample', 'SIB-200 Synthetic 10-sample'),
    'mmlu':             ('MMLU 10-sample', 'MMLU Synthetic 10-sample'),
    'arc':              ('ARC 10-sample', 'ARC Synthetic 10-sample'),
    'mgsm':             ('MGSM 10-sample', 'MGSM Synthetic 10-sample'),
}

SOURCE_URL = "https://huggingface.co/spaces/fair-forward/languagebench"


def fetch_results():
    """Load results dataset from HuggingFace."""
    from datasets import load_dataset
    ds = load_dataset('fair-forward/evals-for-every-language-results', split='train')
    return ds.to_pandas()


def make_model_url(model_name):
    """Generate URL for a model."""
    if '/' in model_name:
        provider = model_name.split('/')[0]
        if provider == 'google' and 'translate' in model_name:
            return 'https://cloud.google.com/translate'
    return f'https://openrouter.ai/{model_name}'


def build_metrics(task_key, iso, all_metrics_for_model):
    """Build metrics list for a given task/language/model."""
    metrics = []
    if task_key == 'translation_from':
        bleu = all_metrics_for_model[all_metrics_for_model['metric'] == 'bleu']
        chrf = all_metrics_for_model[all_metrics_for_model['metric'] == 'chrf']
        if len(bleu) > 0:
            metrics.append({'name': f'SpBLEU {iso}\u2192en', 'value': float(round(float(bleu.iloc[0]['score']) * 100, 1))})
        if len(chrf) > 0:
            metrics.append({'name': f'ChrF {iso}\u2192en', 'value': float(round(float(chrf.iloc[0]['score']) * 100, 1))})
    elif task_key == 'translation_to':
        bleu = all_metrics_for_model[all_metrics_for_model['metric'] == 'bleu']
        chrf = all_metrics_for_model[all_metrics_for_model['metric'] == 'chrf']
        if len(bleu) > 0:
            metrics.append({'name': f'SpBLEU en\u2192{iso}', 'value': float(round(float(bleu.iloc[0]['score']) * 100, 1))})
        if len(chrf) > 0:
            metrics.append({'name': f'ChrF en\u2192{iso}', 'value': float(round(float(chrf.iloc[0]['score']) * 100, 1))})
    elif task_key == 'classification':
        acc = all_metrics_for_model[all_metrics_for_model['metric'] == 'accuracy']
        if len(acc) > 0:
            metrics.append({'name': 'Classification Acc.', 'value': float(round(float(acc.iloc[0]['score']) * 100, 1))})
    elif task_key == 'mmlu':
        acc = all_metrics_for_model[all_metrics_for_model['metric'] == 'accuracy']
        if len(acc) > 0:
            metrics.append({'name': 'MMLU Acc.', 'value': float(round(float(acc.iloc[0]['score']) * 100, 1))})
    elif task_key == 'arc':
        acc = all_metrics_for_model[all_metrics_for_model['metric'] == 'accuracy']
        if len(acc) > 0:
            metrics.append({'name': 'ARC Acc.', 'value': float(round(float(acc.iloc[0]['score']) * 100, 1))})
    elif task_key == 'mgsm':
        acc = all_metrics_for_model[all_metrics_for_model['metric'] == 'accuracy']
        if len(acc) > 0:
            metrics.append({'name': 'MGSM Acc.', 'value': float(round(float(acc.iloc[0]['score']) * 100, 1))})
    return metrics


def generate_yaml(df, top_n):
    """Generate the evaluation YAML structure from results dataframe."""
    our_results = df[df['bcp_47'].isin(BCP_TO_ISO.keys())].copy()

    # model_name -> {iso: {test_set: [metrics]}}
    model_results = {}

    # First pass: collect top N models per task per language
    # For translation, track which models were selected so we can backfill the other direction
    # translation_selected[iso] = set of model names that made top N in either direction
    translation_selected = {}

    for bcp, iso in BCP_TO_ISO.items():
        lang_data = our_results[our_results['bcp_47'] == bcp]

        for task_key, (human_ts, machine_ts) in TASK_TEST_SETS.items():
            if task_key in ('mmlu', 'mgsm', 'arc') and iso in HAS_EXISTING_MMLU:
                continue

            task_data = lang_data[lang_data['task'] == task_key]
            if len(task_data) == 0:
                continue

            sort_metric = 'chrf' if task_key.startswith('translation') else 'accuracy'
            metric_data = task_data[task_data['metric'] == sort_metric].sort_values('score', ascending=False)
            top = metric_data.head(top_n)

            for _, row in top.iterrows():
                model_name = row['model']
                origin = row['origin']
                test_set = human_ts if origin == 'human' else machine_ts

                all_metrics = task_data[task_data['model'] == model_name]
                metrics = build_metrics(task_key, iso, all_metrics)

                if model_name not in model_results:
                    model_results[model_name] = {}
                if iso not in model_results[model_name]:
                    model_results[model_name][iso] = {}
                if test_set not in model_results[model_name][iso]:
                    model_results[model_name][iso][test_set] = []
                model_results[model_name][iso][test_set].extend(metrics)

                # Track translation models for backfill
                if task_key.startswith('translation'):
                    if iso not in translation_selected:
                        translation_selected[iso] = set()
                    translation_selected[iso].add(model_name)

    # Second pass: for any model selected in one translation direction, backfill the other
    for bcp, iso in BCP_TO_ISO.items():
        if iso not in translation_selected:
            continue
        lang_data = our_results[our_results['bcp_47'] == bcp]

        for task_key in ('translation_from', 'translation_to'):
            human_ts, machine_ts = TASK_TEST_SETS[task_key]
            task_data = lang_data[lang_data['task'] == task_key]
            if len(task_data) == 0:
                continue

            for model_name in translation_selected[iso]:
                all_metrics = task_data[task_data['model'] == model_name]
                if len(all_metrics) == 0:
                    continue

                origin = all_metrics.iloc[0]['origin']
                test_set = human_ts if origin == 'human' else machine_ts
                metrics = build_metrics(task_key, iso, all_metrics)

                if iso not in model_results.get(model_name, {}):
                    continue
                if test_set not in model_results[model_name][iso]:
                    model_results[model_name][iso][test_set] = []
                # Only add if this direction's metrics aren't already present
                existing_names = {m['name'] for m in model_results[model_name][iso][test_set]}
                for m in metrics:
                    if m['name'] not in existing_names:
                        model_results[model_name][iso][test_set].append(m)

    # Build final structure
    models_list = []
    for model_name in sorted(model_results.keys()):
        results_by_lang = {}
        for iso in sorted(model_results[model_name].keys()):
            entries = []
            for test_set, metrics in sorted(model_results[model_name][iso].items()):
                entries.append({
                    'test_set': test_set,
                    'source': 'reported',
                    'source_url': SOURCE_URL,
                    'metrics': metrics
                })
            results_by_lang[iso] = entries

        models_list.append({
            'model': model_name,
            'model_url': make_model_url(model_name),
            'task': 'llm',
            'results': results_by_lang
        })

    return {'models': models_list}, len(model_results)


def write_yaml(data, output_path, top_n):
    """Write YAML with header comments."""
    today = date.today().isoformat()

    with open(output_path, 'w') as f:
        f.write("# LanguageBench / AI Language Proficiency Monitor\n")
        f.write("# Source: https://huggingface.co/spaces/fair-forward/languagebench\n")
        f.write("# Paper: arXiv:2507.08538 (Pomerenke, Nothnagel, Ostermann 2025)\n")
        f.write("# GitHub: https://github.com/datenlabor-bmz/evals-for-every-language\n")
        f.write(f"# Data pulled: {today} from fair-forward/evals-for-every-language-results\n")
        f.write("#\n")
        f.write("# IMPORTANT CAVEATS:\n")
        f.write("# - All results based on n=10 sentences per language/task \u2014 treat with caution\n")
        f.write("# - \"Synthetic\" test sets were machine-translated (Google Translate) from English\n")
        f.write("# - Human-translated test sets use original FLORES+, SIB-200, AfriMMLU, etc.\n")
        f.write(f"# - Top {top_n} models per task per language shown (out of ~37 evaluated)\n")
        f.write("# - MMLU/ARC/MGSM omitted for hau, yor, ibo, ewe, wol, lin (better data in irokobench.yaml)\n")
        f.write("#\n")
        f.write("# Datasets: FLORES+ (translation), SIB-200 (classification), MMLU, ARC, MGSM\n")
        f.write(f"# Metric naming: direction in metric name (e.g. SpBLEU hau\u2192en, ChrF en\u2192hau)\n")
        f.write("\n")
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=120)


def main():
    parser = argparse.ArgumentParser(description="Fetch LanguageBench results and generate evaluation YAML")
    parser.add_argument('--top', type=int, default=3, help='Number of top models per task per language (default: 3)')
    parser.add_argument('-o', '--output', type=str, default=None,
                        help='Output YAML path (default: Source data/Evaluations/languagebench.yaml)')
    args = parser.parse_args()

    if args.output is None:
        repo_root = Path(__file__).resolve().parent.parent
        args.output = repo_root / 'Source data' / 'Evaluations' / 'languagebench.yaml'

    print(f"Fetching results from HuggingFace...")
    df = fetch_results()
    print(f"  {len(df)} result rows loaded")

    print(f"Generating YAML (top {args.top} models per task)...")
    data, n_models = generate_yaml(df, args.top)
    n_langs = len(set(iso for m in data['models'] for iso in m['results']))
    print(f"  {n_models} models, {n_langs} languages")

    write_yaml(data, args.output, args.top)
    print(f"Written to {args.output}")


if __name__ == '__main__':
    main()
