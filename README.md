# UNICEF WCARO NLP Landscape

Mapping of NLP/language technology resources for West and Central Africa.

**Status:** Work in progress. Not yet open for external contributions.

**Live site:** https://translatorswb.github.io/wca-nlp-landscape/

---

## About

This project maps available language technology (ASR, TTS, MT, LLM) for languages spoken in UNICEF's West and Central Africa region. It aggregates data from HuggingFace, Common Voice, Wikipedia, and other sources to provide an overview of available models, datasets, and actors working on these languages.

Developed by [CLEAR Global](https://clearglobal.org) for UNICEF WCARO.

## Setup

```bash
pip install -r scripts/requirements.txt
```

## Populating Language Data

`populate_research.py` fetches data from multiple sources and saves it per language under `Research/Languages/{iso}/`. Languages to process are listed in `Research/focused_languages.yaml` (ISO 639-3 codes).

For each language, the script:

1. **[African Language Grid](https://github.com/other/african-language-grid)** ([Kamusi Project](https://kamusi.org/)) — Looks up the language in `Source data/African-language-grid/` and writes basic metadata (countries, population, endangerment, alternate names) to `info.yaml`
2. **Wikipedia** — Scrapes the language's Wikipedia page for family, speaker counts (L1/L2), writing system. Appended to `info.yaml` under `wikipedia:`
3. **[MMS](https://ai.meta.com/research/publications/scaling-speech-technology-to-1000-languages/)** (Meta) — Checks `Source data/mms_language_coverage.yaml` for ASR/TTS/LID support. Added to `info.yaml` under `tech_resources:`
4. **[HuggingFace](https://huggingface.co/)** models — Queries the API for models tagged with the language code, grouped by task (ASR, TTS, translation, LLM). Top models by downloads saved to `models.yaml` with total counts
5. **HuggingFace** datasets — Same approach, saved to `datasets.yaml`
6. **[Mozilla Common Voice](https://commonvoice.mozilla.org/)** — Extracts corpus statistics (hours, clips, gender breakdown) from the local Common Voice JSON file. Saved to `benchmarks.yaml` under `common_voice:`
7. **Published evaluations** — Distributes benchmark results from `Source data/Evaluations/*.yaml` (Whisper, NLLB, etc.) to each language's `benchmarks.yaml` under `evaluations:`

```bash
# Fetch data for all focus languages
python scripts/populate_research.py

# Fetch single language
python scripts/populate_research.py --lang hau

# Force re-fetch (overwrites existing models.yaml, datasets.yaml)
python scripts/populate_research.py --force
```

Without `--force`, existing `models.yaml` and `datasets.yaml` are skipped. Other files (`info.yaml`, `benchmarks.yaml`) are always rebuilt. Manual files `benchmarks_manual.yaml`, `notes.md` are created in first run and never overwritten in subsequent runs.

## Adding Benchmark / Evaluation Data

There are two ways to add benchmark results. Both render identically on language pages.

**Bulk: paper with results for many languages**

Add a YAML file in `Source data/Evaluations/`. When `populate_research.py` runs, results are distributed to each language's `benchmarks.yaml`.

```yaml
# Source data/Evaluations/whisper_fleurs.yaml
model: openai/whisper-large-v3
model_url: https://huggingface.co/openai/whisper-large-v3
task: asr
results:
  hau:
    - test_set: FLEURS
      source: reported
      source_url: https://github.com/openai/whisper/blob/main/model-card.md
      metrics:
        - name: WER
          value: 15.0
  yor:
    - test_set: FLEURS
      source: reported
      source_url: https://github.com/openai/whisper/blob/main/model-card.md
      metrics:
        - name: WER
          value: 26.8
```

For files with multiple models, use the `models:` list format (see `Source data/Evaluations/CG_TWB_voice.yaml` for an example).

After adding, run `python scripts/populate_research.py` to distribute.

**One-off: single result for a single language**

Edit `Research/Languages/{iso}/benchmarks_manual.yaml` directly. This file is never overwritten by scripts. If the same model + test set exists in both files, the manual entry wins.

```yaml
evaluations:
  asr:
    - model: some-org/model-name
      model_url: https://huggingface.co/some-org/model-name
      results:
        - test_set: Common Voice 17
          source: reported
          source_url: https://arxiv.org/abs/...
          metrics:
            - name: WER
              value: 12.5
```

Metric names are arbitrary -- whatever you write under `metrics` becomes a column in the rendered table (WER, CER, BLEU, chrF++, etc.).

## Generating Output

**HTML report** (deployed automatically via GitHub Actions on push):
```bash
python scripts/generate_html.py
# Output: output/index.html + output/lang/*.html + output/actor/*.html
```

**DOCX documents** (run locally):
```bash
# Generate both Languages and Actors documents
python scripts/generate_docs.py
# Output: output/WCA_NLP_Languages.docx, output/WCA_NLP_Actors.docx

# Generate only one
python scripts/generate_docs.py --languages
python scripts/generate_docs.py --actors
```

## Adding a Language

1. Add ISO 639-3 code to `Research/focused_languages.yaml`
2. Run `python scripts/populate_research.py`
3. Commit and push (HTML updates automatically), or run `generate_html.py` / `generate_docs.py` locally

## Adding an Actor

Create `Research/Actors/{id}.yaml`. See existing files for the full schema (type, countries, languages, projects, publications, etc.). Languages listed in the actor's `languages` field will automatically appear on those language pages.

## Structure

```
Research/
├── focused_languages.yaml    # [manual] ISO 639-3 codes to process
├── Languages/{iso}/
│   ├── info.yaml             # [auto] Language metadata from African Grid + Wikipedia + MMS
│   ├── models.yaml           # [auto] HuggingFace models by task
│   ├── datasets.yaml         # [auto] HuggingFace datasets by task
│   ├── benchmarks.yaml       # [auto] Common Voice stats + evaluations from Source data/
│   ├── benchmarks_manual.yaml # [manual] Hand-entered benchmarks (never overwritten)
│   └── notes.md              # [manual] Additional observations
└── Actors/{id}.yaml          # [manual] Organization profiles

Source data/
├── Evaluations/              # Benchmark YAML files (distributed to languages by script)
├── African-language-grid/    # Language metadata spreadsheets
├── mms_language_coverage.yaml
└── cv-corpus-*.json          # Common Voice statistics

output/                       # Generated (not in repo)
├── index.html                # Browsable HTML report
├── WCA_NLP_Languages.docx    # Language profiles document
└── WCA_NLP_Actors.docx       # Actor profiles document
```

**Auto-generated** `[auto]`: Fetched by scripts from external sources. Re-running overwrites these files.

**Manual** `[manual]`: Curated by researchers. Never overwritten by scripts.

## License

Data is aggregated from public sources. See individual sources for their respective licenses.
