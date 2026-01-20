# Project Progress

CLEAR Global consultancy for UNICEF WCARO - NLP Landscape Mapping
Duration: January - March 2026

---

## Task 1: Language and Model Mapping

Mapping of available NLP resources (ASR, TTS, MT, LLM) and key actors working on WCA languages.

### 1.1 Infrastructure
- [x] Research data and directory structure
- [x] Structuring of language database (African language grid)
- [x] Comprehensive language list
- [x] HuggingFace scraping (models + datasets)
- [ ] Lanfrica scraping (Gain wrt HF evaluated)
- [ ] MMS special check
- [x] Common Voice stats
- [x] Wikipedia info fetching
- [x] Language detail pages
- [x] Actor detail pages
- [x] HTML report generation
- [ ] Document generation
- [ ] Language specific models (related to benchmarks)
- [ ] Publish web and make it easy to pull data and render


### 1.1 Language Profiles
Automated fetching of HuggingFace models/datasets, Common Voice stats, and Wikipedia info for priority languages.

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 16   | 20?    | ████████████████░░░░ 80% |

**Completed:** Hausa, Yoruba, Bambara, Mooré, Twi, Ewe, Wolof, Fulfulde, Krio

### 1.2 Actor Directory
Profiles of organizations, research groups, and startups working on African language technology with information on focus areas, languages covered, recent projects, contact information

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 4    | 20     | ████░░░░░░░░░░░░░░░░ 20% |

**Completed:** Masakhane, GhanaNLP, RobotsMali, NCAIR

---

## Task 2: Benchmarking Study

Compile existing benchmark results (FLORES, FLEURS, Common Voice, published papers) for priority languages. Create comparative analysis where multiple models exist.

| Status | Progress |
|--------|----------|
| Not started | ░░░░░░░░░░░░░░░░░░░░ 0% |

- [ ] Compile ASR benchmarks (Whisper, MMS, etc.)
- [ ] Compile MT benchmarks (NLLB, MADLAD, etc.)
- [ ] Compile TTS benchmarks
- [ ] Compile LLM benchmarks
- [ ] Gap analysis: which languages lack benchmarks that can be done within scope
- [ ] Conducting benchmark analyses where needed and possible

### Benchmark Data

| Benchmark | URL | Type | Notes |
|-----------|-----|------|-------|
| FLORES-200 | https://github.com/facebookresearch/flores | MT | |
| FLEURS | https://huggingface.co/datasets/google/fleurs | Speech | |
| Common Voice | https://commonvoice.mozilla.org | ASR data | |
| Sahara | TBD | Text | African language benchmark |
| AfriBench | TBD | Multi | |
| Whisper paper | | ASR | Published WER by language |
| MMS paper | | ASR/TTS | Meta's Massively Multilingual Speech |
| Omnilingual ASR | | | |


---

## Task 3: Knowledge Management Assets

### 3.1 Language Factsheets
Max 3-page summaries per language covering resources, benchmarks, actors, and recommendations.

| Done | Target | Progress |
|------|--------|----------|
| 0    | 20     | ░░░░░░░░░░░░░░░░░░░░ 0% |

### 3.2 Actor Engagement Framework
5-10 page guide on identifying and engaging language technology partners.

| Status | Progress |
|--------|----------|
| Not started | ░░░░░░░░░░░░░░░░░░░░ 0% |

### 3.3 SharePoint Content
Structured documentation for UNICEF knowledge management.

| Status | Progress |
|--------|----------|
| Not started | ░░░░░░░░░░░░░░░░░░░░ 0% |

---

## Task 4: Summit Support (March 2026)

Advisory support for actor selection, agenda input, and presentation of findings.

- [ ] Actor recommendations for summit invitations
- [ ] Agenda design input
- [ ] 60-90 minute presentation session

---

## Quick Links

- **HTML Report:** `output/index.html`
- **Add language:** Edit `Research/focused_languages.yaml`, run `python scripts/populate_research.py`
- **Add actor:** Create `Research/Actors/{id}.yaml`
- **Regenerate HTML:** `python scripts/generate_html.py`
