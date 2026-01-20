# UNICEF WCARO NLP Landscape

Mapping of NLP/language technology resources for West and Central Africa.

**Status:** Work in progress. Not yet open for external contributions.

**Live site:** https://translatorswb.github.io/wca-nlp-landscape/

---

## About

This project maps available language technology (ASR, TTS, MT, LLM) for languages spoken in UNICEF's West and Central Africa region. It aggregates data from HuggingFace, Common Voice, Wikipedia, and other sources to provide an overview of available models, datasets, and actors working on these languages.

Developed by [CLEAR Global](https://clearglobal.org) for UNICEF WCARO.

## Data Sources

- **[African Language Grid](https://github.com/other/african-language-grid)** by [Kamusi Project](https://kamusi.org/) - Primary source for language metadata
- **HuggingFace** - Models and datasets
- **Mozilla Common Voice** - Speech corpus statistics
- **Wikipedia** - Language background info

## Scripts

**Populate language data:**
```bash
# Install dependencies
pip install requests beautifulsoup4 pyyaml

# Fetch data for all focus languages
python scripts/populate_research.py

# Fetch single language by ISO 639-3 code
python scripts/populate_research.py --lang hau

# Force re-fetch (overwrites existing data)
python scripts/populate_research.py --force
```

**Generate HTML report:**
```bash
python scripts/generate_html.py
# Output: output/index.html
```

**Add a new language:**
1. Add ISO 639-3 code to `Research/focused_languages.yaml`
2. Run `python scripts/populate_research.py`
3. Run `python scripts/generate_html.py`

## Structure

```
Research/
├── focused_languages.yaml    # [manual] Languages to process
├── Languages/{iso}/
│   ├── info.yaml             # [auto] Language metadata from African Grid + Wikipedia
│   ├── models.yaml           # [auto] HuggingFace models
│   ├── datasets.yaml         # [auto] HuggingFace datasets
│   ├── benchmarks.yaml       # [auto] Common Voice stats
│   └── notes.md              # [manual] Additional observations
└── Actors/{id}.yaml          # [manual] Organization profiles
```

**Auto-generated:** Fetched by scripts from external sources. Re-running scripts will overwrite.

**Manual:** Curated by researchers. Not overwritten by scripts.

## License

Data is aggregated from public sources. See individual sources for their respective licenses.
