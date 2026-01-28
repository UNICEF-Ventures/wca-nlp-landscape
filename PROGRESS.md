# Project Progress

CLEAR Global consultancy for UNICEF WCARO - NLP Landscape Mapping
Duration: January - March 2026

---

## Task 1: Language and Model Mapping

Mapping of available NLP resources (ASR, TTS, MT, LLM) and key actors working on WCA languages.

### 1.1 Infrastructure
- [x] Research data and directory 
- [x] Structuring of language database (African language grid)
- [x] Comprehensive language list (wca_all_languages.yaml)
- [x] HuggingFace scraping (models + datasets)
- [x] Common Voice stats integration
- [x] Wikipedia info fetching
- [x] Language detail pages
- [x] Actor detail pages
- [x] HTML report generation with tabs
- [x] Countries tab with LUDP integration
- [x] GitHub Pages auto-deployment
- [x] Search filtering on Focus Languages and Actors tabs
- [x] LUDP panel for languages
- [x] Multilingual model coverage check logic
- [x] List language support for MMS, AfriNLLB, Omnilingual
- [x] Benchmark infrastructure (evaluations in benchmarks.yaml + benchmarks_manual.yaml, Source data/Evaluations/ with fetcher)
- [x] Unbenchmarked models support (`unbenchmarked_models` in benchmarks_manual.yaml — lists noteworthy models without scores)
- [ ] Crisis index information for languages (pending approval from CLEAR to add)
- [x] Document generation (DOCX: Languages + Actors)


### 1.2 Language Profiles
Automated fetching of HuggingFace models/datasets, Common Voice stats, and Wikipedia info for priority languages.

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 24   | 24     | ████████████████████ 100% |

**Focus languages (24):**
- Nigeria: Hausa (hau), Yoruba (yor), Igbo (ibo)
- Ghana: Twi (twi), Akan (aka), Ewe (ewe), Dagbani (dag), Ga (gaa)
- Mali: Bambara (bam)
- Burkina Faso: Mooré (mos)
- Senegal/Gambia: Wolof (wol), Mandinka (mnk)
- Guinea: Pular (fuf)
- Sierra Leone: Krio (kri), Mende (men), Temne (tem)
- Benin: Fon (fon)
- CAR: Sango (sag)
- Chad: Shuwa Arabic (shu), Kanuri (kau)
- Gabon/Eq. Guinea: Fang (fan)
- DRC: Lingala (lin), Swahili Congo (swc)
- Widespread: Fulfulde (ful)

### 1.3 Actor Directory
Profiles of organizations, research groups, and startups working on African language technology.

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 26   | 24     | ████████████████████ 108% |

**Completed actors:**
1. Masakhane - Pan-African NLP research community
2. GhanaNLP / Khaya AI - Ghana, translation + speech
3. RobotsMali - Mali, Bambara chatbot
4. NCAIR - Nigeria, government AI research
5. Maliba AI - Mali, Bambara NLP
6. Sunbird AI - Uganda, speech tech
7. DSN (Data Science Nigeria) - Nigeria, AI training
8. GoAI - Burkina Faso, Mooré NLP (UNICEF partner)
9. Farmerline / Darli AI - Ghana/multi-country, 20+ languages, agtech
10. HCI Lab, University of Ghana - Ghana, 5000-hour speech corpus
11. IMSP Benin - Benin, Fon NLP (FFSTC corpus, 61hrs)
12. LAfricaMobile - Senegal, Wolof/Fulfulde/Hausa/Ewe ASR/TTS
13. Baamtu - Senegal, Wolof (consulting, closed)
14. GalsenAI - Senegal, Wolof NLP community
15. Chad AI Network - Chad, Chadian Arabic NLP
16. NaijaVoices - Nigeria, 1800hrs speech dataset (Hausa/Igbo/Yoruba)
17. BurkimbIA - Burkina Faso, open-source Moore models (complement to GoAI)
18. Awarri - Nigeria, N-ATLAS government-backed LLM
19. HausaNLP - Nigeria/distributed, Hausa NLP research community
20. Jokalante - Senegal, KALLAAMA speech dataset + NAFOORE chatbot
21. CONCREE - Senegal, Wolof TTS (Adia suite)
22. Lanfrica - Pan-African, language resource discovery platform
23. Intron Voice AI - Nigeria, Sahara ASR models, healthcare focus
24. UBC Deep Learning & NLP Lab - Canada, SERENGETI/Toucan/AfroLID (517 African languages)
25. Digital Umuganda - Rwanda, AfriVoice dataset (Lingala/Fulfulde/Wolof), 2200hrs Kinyarwanda Common Voice (CLEAR Global contact)
26. CLEAR Global - Global, TWB Voice (Hausa/Kanuri/Shuwa Arabic), Gamayun, LT4CR, 55 HF models (conducting this consultancy)

Languages missing dedicated actors
Sierra Leone: Krio, Mende, Temne - no dedicated actors
DRC/Congo: Lingala, Congo Swahili - no dedicated actors (partially covered by CLEAR Global LT4CR + Gamayun)
CAR: Sango - no dedicated actors
Gabon/Equatorial Guinea: Fang - no dedicated actors

---

## Task 2: Benchmarking Study

Compile existing benchmark results (FLORES, FLEURS, Common Voice, published papers) for priority languages. Create comparative analysis where multiple models exist.

| Status | Progress |
|--------|----------|
| Infrastructure done, data collection started | ██░░░░░░░░░░░░░░░░░░ 10% |

- [x] Benchmark data infrastructure (two-file system, Source data/Evaluations/, rendering on language pages)
- [x] Initial ASR data: Whisper FLEURS WER, CLEAR Global TWB Voice (Hausa, Kanuri)
- [x] Initial TTS data: CLEAR Global TWB Voice TTS (Hausa, Kanuri) — scores entered
- [ ] Compile ASR benchmarks (more Whisper variants, MMS, wav2vec2, etc.)
- [ ] Compile MT benchmarks (NLLB, MADLAD, AfriNLLB etc.)
- [ ] Compile TTS benchmarks (more models)
- [ ] Compile LLM benchmarks (AfriqueLLM, Goldfish, Aya, Serengeti)
- [ ] Gap analysis: which languages lack benchmarks
- [ ] Conducting benchmark analyses where needed and possible

### Benchmark Data Sources

| Benchmark | URL | Type | Notes |
|-----------|-----|------|-------|
| FLORES-200 | https://github.com/facebookresearch/flores | MT | 200 languages |
| FLEURS | https://huggingface.co/datasets/google/fleurs | Speech | |
| Common Voice | https://commonvoice.mozilla.org | ASR data | |
| Whisper paper | OpenAI | ASR | Published WER by language |
| MMS paper | Meta | ASR/TTS | Massively Multilingual Speech |
| AfriSpeech | | ASR | African-focused |
| Sahara | | Text | African language benchmark |
| AfriBench | | Multi | |

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

## Recent Updates (January 2026)

### 2026-01-27
- Added DOCX document generation (`scripts/generate_docs.py`)
  - Two documents: `WCA_NLP_Languages.docx` and `WCA_NLP_Actors.docx`
  - Summary matrix at the top of each doc with key stats (languages: speakers, HF models, benchmark coverage; actors: type, countries, openness, maturity, engagement)
  - Clickable hyperlinks throughout: internal bookmarks (summary → entry), HuggingFace model/dataset search links, actor websites, benchmark source URLs, resource links, publications
  - CLI: `--languages` / `--actors` flags, or both by default
  - Uses `python-docx`, added to `scripts/requirements.txt`
- Added `unbenchmarked_models` support in `benchmarks_manual.yaml` for listing noteworthy models without benchmark scores
  - Renders as "Noteworthy models without benchmark" table (Model / Task / Notes columns) on language detail pages
  - Placed after the Benchmarks section
  - Also made benchmark tables robust to entries without results (shows row with dashes)
  - Updated `benchmarks_manual.yaml` template with example

### 2026-01-26 (night)
- Built benchmark/evaluation infrastructure:
  - Two-file system: `benchmarks.yaml` (auto-generated) + `benchmarks_manual.yaml` (hand-entered, never overwritten)
  - `Source data/Evaluations/` directory with structured YAML files that distribute to languages via `fetch_evaluations.py`
  - Supports single-model and multi-model file formats
  - Benchmark section renders on language detail pages with per-task tables (ASR, TTS, MT, LLM)
  - Metric names are arbitrary (WER, CER, BLEU, Pronunciation accuracy, etc.)
  - "reported" source text links to source URL
- Added initial benchmark data
- Added MMS (Meta) language coverage as flat entries (MMS-ASR, MMS-TTS, MMS-LID) in tech_resources
- Fixed language detail page section ordering: General Info → Language Use → Actors → NLP & Tech → Common Voice → Benchmarks → Models → Datasets

### 2026-01-26 (evening)
- Added Digital Umuganda: Rwanda, AfriVoice dataset (Lingala 517hrs, Fulfulde 527hrs, Wolof 531hrs), OD4A (17 languages, 4500hrs), 2200hrs Kinyarwanda Common Voice, MT Rwanda with CLEAR Global
- Added CLEAR Global: TWB Voice (Hausa/Kanuri/Shuwa Arabic), Gamayun, LT4CR, SynVoices, OpenSLR/Coqui TTS (Hausa/Yoruba/Ewe/Lingala/Twi), NLU chatbot data, 55 models + 14 datasets on HuggingFace
- Kanuri now covered by CLEAR Global TWB Voice; Lingala/Congo Swahili partially covered by CLEAR Global LT4CR + Gamayun
- Actor count: 26/24 (108%)

### 2026-01-26 (later)
- Refactored `generate_html.py` (2,083 lines) into `scripts/htmlgen/` package (7 modules: constants, data, utils, styles, pages, tabs)
- Moved `fetch_*.py` scripts into `scripts/fetchers/` package, updated imports in `populate_research.py`
- Added text search to Focus Languages tab and Actors tab (search by name, ISO code, country, description, etc.)
- Entry point (`scripts/generate_html.py`) unchanged — GitHub Actions deployment unaffected

### 2026-01-26
- Added 8 new actors + UBC-NLP (24 total, 100% of target)
  - NaijaVoices: Nigeria, 1800hrs speech dataset, Interspeech 2025, Chris Emezue
  - BurkimbIA: Burkina Faso, open-source Moore models (ASR/TTS/MT), complement to GoAI
  - Awarri: Nigeria, N-ATLAS government-backed LLM (Llama-3 8B), UNGA80 launch
  - HausaNLP: Hausa NLP research community, AfriSenti, multiple ACL/EMNLP best papers
  - Jokalante: Senegal, KALLAAMA 125hrs speech (Wolof/Pulaar/Sereer), NAFOORE chatbot
  - CONCREE: Senegal, Wolof TTS (Adia suite), entrepreneurship platform
  - Lanfrica: Pan-African language resource catalog (2,199 languages), Bengio advisor
  - Intron Voice AI: Nigeria, Sahara ASR (300+ African accents), healthcare deployment
- Research report at Research/potential-new-actors.md
- Languages now without actors reduced to: Krio, Mende, Temne, Lingala, Congo Swahili, Sango, Fang, Kanuri
- Pular/Fulfulde now partially covered by Jokalante (KALLAAMA dataset) and LAfricaMobile
- Mandinka partially covered by Jokalante (NAFOORE chatbot languages)
- Note: BurkimbIA ASR leaderboard (huggingface.co/spaces/burkimbia/leaderboard-asr) useful for benchmarking task

### 2026-01-23
- Added 5 new actors (15 total, 75% of target)
- **TODO:** Check people from K4All Fongbe project: https://k4all.org/project/database-fongbe/
  - Kevin Degila (ML Research Engineer, Konta)
  - Momboladji Balogoun (Data Analyst, Gozem; co-founder Takwimu Lab)
  - Godson Kalipe (Data Engineer, Takwimu Lab)
  - Jamiil Toure (Design engineer, Masakhane contributor)
  - All affiliated with Takwimu Lab (West African francophone data science org)
  - IMSP Benin: Fon language research, FFSTC corpus (61hrs), D. Fortuné Kponou
  - LAfricaMobile: Senegal telecom, ASR/TTS for Wolof, Fulfulde, Hausa, Ewe
  - Baamtu: Senegal consulting firm, Wolof chatbots (closed/commercial)
  - GalsenAI: Senegal community, 18 models + 8 datasets for Wolof
  - Chad AI Network: Chad community, Kalam-na project for 123 Chadian languages
- Updated Masakhane with Bonaventure Dossou and FFR (Fon-French) project
- Updated RobotsMali with Yacouba Diarra LinkedIn
- Senegal now well-covered with 3 actors for Wolof

### 2026-01-22
- Added HCI Lab, University of Ghana actor with comprehensive research
  - Discovered UGSpeechData: 5,000-hour speech corpus (largest for Ghana)
  - Added key faculty: Prof. Isaac Wiafe, Prof. Jamal-Deen Abdulai
  - Documented Tɛkyerɛma Pa project (impaired speech ASR, Google collaboration)
- Added Farmerline / Darli AI actor
  - 33+ models, 21+ datasets on HuggingFace
  - Voice-first agtech for 60+ countries, 27+ languages
- Added favicon to generated HTML pages
- Updated CLAUDE.md and PROGRESS.md

### 2026-01-20
- Added Countries tab with CLEAR Global LUDP integration
- Added new languages: fon, sag, shu, fan, mnk, aka, fuf
- Total focus languages: 24

### 2026-01-19
- Added actors: Maliba AI, Sunbird AI, DSN, GoAI
- GitHub Pages deployment configured
- Actor-language linking implemented

---

## Quick Links

- **Live site:** https://translatorswb.github.io/wca-nlp-landscape/
- **GitHub repo:** https://github.com/translatorswb/wca-nlp-landscape
- **HTML Report (local):** `output/index.html`
- **Add language:** Edit `Research/focused_languages.yaml`, run `python scripts/populate_research.py`
- **Add actor:** Create `Research/Actors/{id}.yaml`
- **Regenerate HTML:** `python scripts/generate_html.py`
- **Generate DOCX:** `python scripts/generate_docs.py` (or `--languages` / `--actors`)
