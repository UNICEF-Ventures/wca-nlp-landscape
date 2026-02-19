#!/usr/bin/env python3
"""
Parse SimbaBench API data into evaluation YAML for populate_research.py.

Usage:
    # Fetch fresh data from API and generate YAML:
    python scripts/parse_simbabench.py

    # Use previously saved JSON:
    python scripts/parse_simbabench.py --json "Source data aux/simbabench_api.json"

API endpoint: https://ubc-nlp-simbabench.hf.space/api/data
Paper: https://arxiv.org/abs/2505.18436 (EMNLP 2025)
Space: https://huggingface.co/spaces/UBC-NLP/SimbaBench
"""

import argparse
import json
import urllib.request
import yaml
import io
from pathlib import Path

API_URL = "https://ubc-nlp-simbabench.hf.space/api/data"
SPACE_URL = "https://huggingface.co/spaces/UBC-NLP/SimbaBench"
OUTPUT_PATH = "Source data/Evaluations/simbabench.yaml"
JSON_CACHE_PATH = "Source data aux/simbabench_api.json"

# Language name in SimbaBench -> (ISO 639-3, test_set label)
# Multiple names can map to the same ISO (e.g. Twi + Asante-twi -> twi)
# All become separate test_set results under that ISO.
# Each name maps to a LIST of (ISO, test_set_label) tuples.
# This allows one SimbaBench language to appear on multiple ISO pages
# (e.g. Akuapim-twi appears on both aka and twi pages).
LANG_MAP = {
    "Hausa": [("hau", "Common Voice 19")],
    "Yoruba": [("yor", "Yoruba Voice")],
    "Igbo": [("ibo", "Common Voice 19")],
    "Akuapim-twi": [("aka", "FinancialSpeech, Akuapem Twi"), ("twi", "FinancialSpeech, Akuapem Twi")],
    "Asante-twi": [("twi", "FinancialSpeech, Asante Twi")],
    "Twi": [("twi", "FLEURS, Twi")],
    "Ga": [("gaa", "FinancialSpeech")],
    "Wolof": [("wol", "Kallaama")],
    "Pulaar": [("fuc", "Kallaama, Pulaar")],
    "Pular": [("fuf", "Nicolingua-WA, Pular")],
    "Fon": [("fon", "ALFFA")],
    "Dyula": [("dyu", "Common Voice 19")],
    "Ewe": [("ewe", "bibleTTS")],
    "Lingala": [("lin", "bibleTTS")],
}

TTS_LANG_MAP = {
    "Ewe": [("ewe", "bibleTTS, Ewe")],
    "Yoruba": [("yor", "bibleTTS, Yoruba")],
    "Hausa": [("hau", "bibleTTS, Hausa")],
    "Lingala": [("lin", "bibleTTS, Lingala")],
    "Asante-twi": [("twi", "bibleTTS, Asante Twi")],
    "Akuapim-twi": [("aka", "bibleTTS, Akuapem Twi"), ("twi", "bibleTTS, Akuapem Twi")],
}

# ASR models to include (short name -> (HF model ID, HF URL))
ASR_MODELS = {
    "mms-1b-all": ("facebook/mms-1b-all", "https://huggingface.co/facebook/mms-1b-all"),
    "whisper-large-v3": ("openai/whisper-large-v3", "https://huggingface.co/openai/whisper-large-v3"),
    "whisper-large-v3-turbo": ("openai/whisper-large-v3-turbo", "https://huggingface.co/openai/whisper-large-v3-turbo"),
    "seamless-m4t-v2-large": ("facebook/seamless-m4t-v2-large", "https://huggingface.co/facebook/seamless-m4t-v2-large"),
    "Simba-S": ("UBC-NLP/Simba-S", "https://huggingface.co/UBC-NLP/Simba-S"),
    "Simba-M": ("UBC-NLP/Simba-M", "https://huggingface.co/UBC-NLP/Simba-M"),
    "omniASR_LLM_7B_v2": ("UBC-NLP/omniASR_LLM_7B_v2", "https://huggingface.co/UBC-NLP/omniASR_LLM_7B_v2"),
    "omniASR_LLM_1B_v2": ("UBC-NLP/omniASR_LLM_1B_v2", "https://huggingface.co/UBC-NLP/omniASR_LLM_1B_v2"),
    "omniASR_LLM_300M_v2": ("UBC-NLP/omniASR_LLM_300M_v2", "https://huggingface.co/UBC-NLP/omniASR_LLM_300M_v2"),
    "omniASR_CTC_7B_v2": ("UBC-NLP/omniASR_CTC_7B_v2", "https://huggingface.co/UBC-NLP/omniASR_CTC_7B_v2"),
    "omniASR_CTC_3B_v2": ("UBC-NLP/omniASR_CTC_3B_v2", "https://huggingface.co/UBC-NLP/omniASR_CTC_3B_v2"),
    "omniASR_CTC_1B_v2": ("UBC-NLP/omniASR_CTC_1B_v2", "https://huggingface.co/UBC-NLP/omniASR_CTC_1B_v2"),
}

# TTS models
TTS_MODELS = {
    "MMS-TTS": ("facebook/mms-tts", "https://huggingface.co/facebook/mms-tts"),
    "Simba-TTS": ("UBC-NLP/Simba-TTS", "https://huggingface.co/UBC-NLP/Simba-TTS"),
}


def fetch_api_data():
    """Fetch data from SimbaBench Space API."""
    print(f"Fetching from {API_URL} ...")
    req = urllib.request.Request(API_URL)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode())


def extract_asr(data, model_short):
    """Extract ASR results for focus languages from one model."""
    hf_name, hf_url = ASR_MODELS[model_short]
    entry = {"model": hf_name, "model_url": hf_url, "task": "asr", "results": {}}

    for family, fdata in data["asr"]["by_family"].items():
        for row in fdata["data"]:
            if row["Model"] != model_short:
                continue
            for key, val in row.items():
                if not key.startswith("WER_"):
                    continue
                lang_name = key[4:]
                if lang_name not in LANG_MAP:
                    continue
                cer = row.get(f"CER_{lang_name}")
                for iso, test_label in LANG_MAP[lang_name]:
                    metrics = [{"name": "WER", "value": round(val, 2)}]
                    if cer is not None:
                        metrics.append({"name": "CER", "value": round(cer, 2)})
                    result = {
                        "test_set": f"SimbaBench ({test_label})",
                        "source": "reported",
                        "source_url": SPACE_URL,
                        "metrics": metrics,
                    }
                    if iso not in entry["results"]:
                        entry["results"][iso] = []
                    entry["results"][iso].append(result)
    return entry


def extract_tts(data, tts_model_name):
    """Extract TTS results for focus languages."""
    hf_name, hf_url = TTS_MODELS[tts_model_name]
    entry = {"model": hf_name, "model_url": hf_url, "task": "tts", "results": {}}

    for row in data["tts"][tts_model_name]:
        lang_name = row["language"]
        if lang_name not in TTS_LANG_MAP:
            continue
        for iso, test_label in TTS_LANG_MAP[lang_name]:
            result = {
                "test_set": f"SimbaBench ({test_label})",
                "source": "reported",
                "source_url": SPACE_URL,
                "metrics": [
                    {"name": "WER", "value": row["wer"]},
                    {"name": "UTMOS", "value": row["utmos"]},
                    {"name": "PESQ", "value": row["pesq"]},
                ],
            }
            if iso not in entry["results"]:
                entry["results"][iso] = []
            entry["results"][iso].append(result)
    return entry


def main():
    parser = argparse.ArgumentParser(description="Parse SimbaBench API data into evaluation YAML")
    parser.add_argument("--json", help="Path to cached JSON file (skip API fetch)")
    args = parser.parse_args()

    if args.json:
        print(f"Loading from {args.json} ...")
        with open(args.json) as f:
            data = json.load(f)
    else:
        data = fetch_api_data()
        # Save cache
        cache_path = Path(JSON_CACHE_PATH)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Cached API response to {JSON_CACHE_PATH}")

    # Build model entries
    models_list = []

    for model_short in ASR_MODELS:
        entry = extract_asr(data, model_short)
        if entry["results"]:
            models_list.append(entry)
            print(f"  ASR {entry['model']}: {len(entry['results'])} languages")

    for tts_name in TTS_MODELS:
        entry = extract_tts(data, tts_name)
        if entry["results"]:
            models_list.append(entry)
            print(f"  TTS {entry['model']}: {len(entry['results'])} languages")

    # Write YAML with header
    header = f"""\
# SimbaBench: Voice of a Continent — ASR + TTS benchmark results
# API: {API_URL}
# Space: {SPACE_URL}
# Paper: https://arxiv.org/abs/2505.18436 (EMNLP 2025)
# Authors: UBC-NLP
#
# Generated by: scripts/parse_simbabench.py
# Raw JSON cached at: {JSON_CACHE_PATH}
#
# ASR models: {len(ASR_MODELS)} ({', '.join(ASR_MODELS.keys())})
# TTS models: {len(TTS_MODELS)} ({', '.join(TTS_MODELS.keys())})
# Metrics — ASR: WER/CER (lower=better), TTS: WER (lower=better), UTMOS/PESQ (higher=better)

"""
    yaml_str = yaml.dump(
        {"models": models_list},
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
        width=200,
    )

    output_path = Path(OUTPUT_PATH)
    with open(output_path, "w") as f:
        f.write(header + yaml_str)

    print(f"\nWritten {output_path} ({len(models_list)} model entries)")


if __name__ == "__main__":
    main()
