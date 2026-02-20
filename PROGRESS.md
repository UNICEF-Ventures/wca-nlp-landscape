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
| 33   | 20     | ████████████████████ 165% |

**Focus languages (33):**

*Focus 1 — UNICEF country office survey (10):*
- Hausa (hau), Mende (men), Bambara (bam), Ewe (ewe), Fang (fan), Liberian Koloqua (lir), Shuwa Arabic (shu), Mooré (mos), Fon (fon), Guinea-Bissau Creole (pov)

*Focus 2 — UNICEF additions 17.2 (5):*
- Dyula (dyu), Gourmantchéma (gux), Soninke (snk), Twi (twi), Dagbani (dag)

*Focus 3 — CLEAR additional selection (14):*
- Yoruba (yor), Igbo (ibo), Wolof (wol), Fulfulde (ful), Krio (kri), Temne (tem), Ga (gaa), Kanuri (kau), Congo Swahili (swc), Lingala (lin), Sango (sag), Mandinka (mnk), Akan (aka), Pular (fuf)

*Focus 4 — Additional Fulfulde variants and Niger/Mali languages (4):*
- Fulfulde Maasina (ffm), Fulfulde Adamawa (fub), Koyraboro Senni (ses), Toro So Dogon (dts)

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

Languages missing dedicated actors:
- Sierra Leone: Mende (men), Temne (tem) - no dedicated actors
- Liberia: Liberian Koloqua (lir) - no dedicated actors
- Guinea-Bissau: Guinea-Bissau Creole (pov) - no dedicated actors
- Guinea: Pular (fuf) - no dedicated actors (Fulfulde/ful partially covered by Jokalante, LAfricaMobile, Digital Umuganda)
- CAR: Sango (sag) - no dedicated actors
- Gabon/Eq. Guinea: Fang (fan) - no dedicated actors
- Burkina Faso: Gourmantchéma (gux) - no dedicated actors
- DRC/Congo: Lingala (lin), Congo Swahili (swc) - partially covered by CLEAR Global (LT4CR, Gamayun)
- Note: Krio (kri) now partially covered by Farmerline; Soninke (snk) covered by MALIBA-AI and RobotsMali; Dyula (dyu) covered by Farmerline

### 1.4 Actor Prioritization (for Summit Invitations)

Scoring framework for prioritizing 26 actors for March 2026 summit in Senegal.

**Scoring dimensions (0-3 points each, max 18):**
1. **WCA Regional Relevance** - HQ in WCA + primary work in WCA
2. **Priority Language Coverage** - Overlap with UNICEF survey Focus 1 languages
3. **Technical Maturity** - established/emerging/early
4. **Openness & Sustainability** - open/partial/closed (from `openness` field in YAML)
5. **UNICEF Alignment** - active partner/high relevance/moderate/low
6. **Summit Readiness** - presentable outputs, location/travel considerations

**Tier classification:**
- Tier 1 (14-18): Summit invitation priority
- Tier 2 (10-13): Strong candidates for summit or follow-up
- Tier 3 (6-9): Include in landscape report, lower priority
- Tier 4 (0-5): Low priority for WCA focus

Full scoring framework: `Event/actor_prioritization_methodology.md` (not in repo)

**Status:**
- [x] Openness field populated for all 26 actors
- [x] Draft scoring framework applied to all actors
- [ ] Validate criteria with UNICEF (3 Feb meeting)
- [ ] Finalize ranked list (end of week)

---

## Task 2: Benchmarking Study

Compile existing benchmark results (FLORES, FLEURS, Common Voice, published papers) for priority languages. Create comparative analysis where multiple models exist.

| Status | Progress |
|--------|----------|
| Infrastructure done, data collection in progress | ████████░░░░░░░░░░░░ 40% |

- [x] Benchmark data infrastructure (two-file system, Source data/Evaluations/, rendering on language pages)
- [x] Initial ASR data: Whisper FLEURS WER, CLEAR Global TWB Voice (Hausa, Kanuri)
- [x] Initial TTS data: CLEAR Global TWB Voice TTS (Hausa, Kanuri) — scores entered
- [x] PazaBench ASR results compiled (52 models, 39 African languages, CER+WER) — 7 focus languages covered: ful, hau, ibo, lin, twi, wol, yor
- [x] Compile LLM benchmarks: AfroBench-Lite scores (24 models, 5 focus languages: hau, ibo, lin, wol, yor)
- [ ] Compile ASR benchmarks (more Whisper variants, MMS, wav2vec2, etc.)
- [x] Compile MT benchmarks: AfriNLLB + NLLB-600M baseline (FLORES-200 BLEU/chrF, 4 focus langs: hau, yor, lin, wol)
- [ ] Compile MT benchmarks (more: NLLB full, MADLAD, Seamless etc.)
- [ ] Compile TTS benchmarks (more models)
- [ ] Gap analysis: which languages lack benchmarks
- [ ] Conducting benchmark analyses where needed and possible
- [x] **Webpage feature:** "Sources" tab on website listing all data sources and benchmark sources with status, languages, and links (`Source data/sources.yaml`)

### Benchmark Data Sources — Tracking

**Status key:** INCLUDED = scores extracted and in the system | PLACEHOLDER = file exists but values are "?" | NOTED = identified, not yet extracted | PAPER = paper downloaded to `Project documents/`

#### Already included (scores in the system)

| # | Benchmark / Source | Paper/URL | Type | Focus langs covered | Status |
|---|-------------------|-----------|------|-------------------|--------|
| 1 | **Whisper** (FLEURS WER) | [arxiv 2212.04356](https://arxiv.org/abs/2212.04356) | ASR | hau, yor, lin (6 model sizes; large-v3 = "?") | INCLUDED |
| 2 | **PazaBench** (Microsoft) | [HF Space](https://huggingface.co/spaces/microsoft/paza-bench) | ASR | dyu, ful, hau, ibo, lin, twi, wol, yor (52 models, CER+WER) | INCLUDED |
| 3 | **AfroBench-Lite** (McGill-NLP) | [HF Space](https://huggingface.co/spaces/McGill-NLP/AfroBench) / [arxiv 2311.07978](https://arxiv.org/abs/2311.07978) | LLM | hau, ibo, lin, wol, yor (24 models, 15 NLP tasks aggregate) | INCLUDED |
| 4 | **CLEAR Global TWB Voice** | HuggingFace model cards | ASR+TTS | hau, kau (Whisper & w2v-bert fine-tunes + TTS) | INCLUDED |
| 5 | **Kreyol-MT** | [arxiv 2405.05376](https://arxiv.org/abs/2405.05376) | MT | kri, pov, sag (bible-based BLEU, caution on generalization) | INCLUDED |
| 6 | **AfriNLLB** (FLORES-200) | [HF Collection](https://huggingface.co/collections/AfriNLP/afrinllb) | MT | hau, yor, lin, wol (AfriNLLB 548M + NLLB-600M baseline) | INCLUDED |

#### To be extracted (papers downloaded, need to pull scores)

| # | Benchmark / Source | Paper/URL | Type | Potential focus langs | Status |
|---|-------------------|-----------|------|----------------------|--------|
| 7 | **Sahara** (UBC-NLP) | [arxiv 2502.19582](https://arxiv.org/abs/2502.19582) / [HF Space](https://huggingface.co/spaces/UBC-NLP/sahara) (broken) | LLM | 517 languages, 16 tasks (4 clusters: classification, generation, MCCR, tokens). 10 focus langs covered: hau, yor, ibo, wol, ful, lin, twi, aka, fon, bam. 24 models evaluated. **Scores in private dataset** (`UBC-NLP/sahara_leaderboard_results_private`). HF Space broken. Ask authors for access or score export. | BLOCKED — need author help |
| 8 | **SimbaBench** (UBC-NLP) | [arxiv 2505.18436](https://arxiv.org/abs/2505.18436) / [EMNLP 2025](https://aclanthology.org/2025.emnlp-main.559/) / [HF Space](https://huggingface.co/spaces/UBC-NLP/SimbaBench) | ASR+TTS | 12 ASR models + 2 TTS models. 11 focus langs ASR (aka, dyu, fon, fuc, fuf, gaa, hau, ibo, twi, wol, yor), 6 TTS (aka, ewe, hau, lin, twi, yor). Data pulled from Space API. Parser: `scripts/parse_simbabench.py`. | INCLUDED ✓ verified |
| 9 | **AfriqueLLM** (McGill-NLP) | [arxiv 2601.06395](https://arxiv.org/abs/2601.06395) / [HF Collection](https://huggingface.co/collections/McGill-NLP/afriquellm) | LLM | 20 African languages CPT. Training: hau, ibo, yor + 17 more. Eval on AfroBench-Lite. 5 base models (Llama 3.1, Gemma 3, Qwen 3). | PAPER |
| 10 | **IrokoBench** | [arxiv 2406.03368](https://arxiv.org/abs/2406.03368) | LLM | 16 African languages: hau, ibo, yor, wol + more. AfriXNLI, AfriMGSM, AfriMMLU. 10 open + 4 proprietary LLMs. | PAPER |
| 11 | **SERENGETI** (UBC-NLP) | [arxiv 2212.10785](https://arxiv.org/abs/2212.10785) | NLU (encoder) | 517 African languages, 8 NLU tasks, 20 datasets. Encoder model (not generative). 82.27 avg F1. | PAPER |
| 12 | **Bambara ASR Leaderboard** (MALIBA-AI) | [HF Space](https://huggingface.co/spaces/MALIBA-AI/bambara-asr-leaderboard) | ASR | bam only. Multiple models compared. Need browser agent to scrape scores. | NOTED |

#### Identified but not yet investigated

| # | Benchmark / Source | Paper/URL | Type | Notes |
|---|-------------------|-----------|------|-------|
| 13 | **NLLB** (Meta) | [arxiv 2207.04672](https://arxiv.org/abs/2207.04672) | MT | FLORES-200 BLEU scores for 200 languages. Many WCA langs. High priority to extract. |
| 14 | **MMS** (Meta) | [arxiv 2305.13516](https://arxiv.org/abs/2305.13516) | ASR+TTS+LID | Massively Multilingual Speech. 1100+ languages. Has published WER/CER. |
| 15 | **Seamless** (Meta) | [arxiv 2312.05187](https://arxiv.org/abs/2312.05187) | ASR+MT+TTS | SeamlessM4T. Multimodal translation. |
| 16 | **MADLAD-400** | [arxiv 2309.04662](https://arxiv.org/abs/2309.04662) | MT | 400+ languages. Translation model. |
| 17 | **BLOOM/BLOOMZ** | [arxiv 2211.01786](https://arxiv.org/abs/2211.01786) / [HF evals](https://huggingface.co/datasets/bigscience/evaluation-results) | LLM | 176B multilingual model. Has eval results dataset on HF. |
| 18 | **LLaMAX** | [HF](https://huggingface.co/LLaMAX/LLaMAX3-8B-Alpaca) | LLM | Multilingual LLaMA extension. |
| 19 | **Goldfish** | [arxiv 2408.10441](https://arxiv.org/abs/2408.10441) / [HF](https://huggingface.co/goldfish-models) | LLM | Low-resource language models. |
| 20 | **FLORES-200** | [github](https://github.com/facebookresearch/flores) | MT test set | Standard MT evaluation dataset. 200 languages. |
| 21 | **FLEURS** | [HF](https://huggingface.co/datasets/google/fleurs) | Speech test set | Standard speech evaluation dataset. |
| 22 | **Common Voice** | [commonvoice.mozilla.org](https://commonvoice.mozilla.org) | ASR data | Community speech dataset. Stats already integrated. |
| 23 | **AfriSpeech** | | ASR | African-focused speech benchmark. |

### Papers downloaded (in `Project documents/`, not in repo)

- `afriquellm.pdf` — AfriqueLLM (McGill-NLP, 2026)
- `sahara.pdf` — Sahara benchmark (UBC-NLP, ACL 2025)
- `simbabench.pdf` — SimbaBench / Voice of a Continent (UBC-NLP, EMNLP 2025)
- `serengeti.pdf` — SERENGETI (UBC-NLP, 2022)
- `irokobench.pdf` — IrokoBench (Adelani et al., 2024)
- `afrobench.pdf` — AfroBench (McGill-NLP)
- `afrimcqa.pdf` — AfriMCQA
- `afrimteb_e5.pdf` — AfriMTEB
- `waxal-paper.pdf` — WAXAL
- `kreyolMT.pdf` — Kreyol-MT
- `omnilingual-paper.pdf` — Omnilingual

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

## Recent Updates

### 2026-02-20
- Added 4 new focus languages (33 total): Fulfulde Maasina (ffm), Fulfulde Adamawa (fub), Koyraboro Senni (ses), Toro So Dogon (dts)
- **AfriNLLB MT benchmarks included:** FLORES-200 BLEU/chrF scores for AfriNLLB 548M and NLLB-600M baseline across hau, yor, lin, wol. Source: AfriNLP HuggingFace collection.
- Moved `sources.yaml` from `Source data/` to `Research/` (now tracked in repo)
- **Bug fix:** MT evaluation data (`task: mt`) was not rendering in HTML benchmarks — the rendering code expected `translation` instead of `mt`. Fixed in `htmlgen/utils.py`, `htmlgen/tabs.py`, and `generate_docs.py`.

### 2026-02-19
- Added **Sources tab** to website with two sections: Data Sources (7 general sources) and Benchmark Sources (22 tracked). Each benchmark shows type, focus languages covered, and color-coded status badge (INCLUDED/PLACEHOLDER/TO_EXTRACT/NOTED/BLOCKED). Source metadata lives in `Source data/sources.yaml`.
- SimbaBench scores extracted and included (12 ASR + 2 TTS models, 11 focus languages for ASR, 6 for TTS)

### 2026-02-18
- Discovered **EQUATE Index** — Language AI Readiness Index from Cambridge University ([equate-index.ai](https://www.equate-index.ai/en), [arxiv 2602.12018](https://arxiv.org/abs/2602.12018)). Covers 6003 languages across 3 dimensions: AI resources, digital infrastructure, socioeconomics. CSV data downloaded to `Source data/equate_index_data.csv`. Useful as contextual framing for the landscape report (not a model benchmark).
- Meeting with Nico: all outputs approved, continue benchmark work. Will hire engineer for manual benchmark evaluations.
- Focus language tiers clarified: Group 1 (UNICEF survey, 10 langs) + Group 2 (UNICEF additions, 5 langs) = priority for manual benchmarks. Group 3 (CLEAR selection, 14 langs) = important but lower priority for manual work.
- Comprehensive benchmark source tracking added to PROGRESS.md (23 sources tracked: 6 included, 6 to extract, 11 to investigate)
- Downloaded 5 new papers: AfriqueLLM, Sahara, SimbaBench, SERENGETI, IrokoBench
- New benchmark sources identified from notes:
  - Sahara (UBC-NLP): 517 languages, 16 NLP tasks, ACL 2025
  - SimbaBench (UBC-NLP): 61 languages, ASR/TTS/SLID, EMNLP 2025
  - AfriqueLLM (McGill-NLP): 20 African language LLMs, AfroBench-Lite eval
  - IrokoBench: 16 African languages, LLM benchmark (AfriXNLI, AfriMGSM, AfriMMLU)
  - SERENGETI: 517 languages, encoder NLU model
  - Bambara ASR Leaderboard (MALIBA-AI): bam ASR models
- TODO: Extract scores from newly identified papers (priority: SimbaBench for ASR/TTS, Sahara for LLM, NLLB for MT)

### 2026-02-06
- Compiled AfroBench-Lite LLM benchmark scores into `Source data/Evaluations/afrobench_lite.yaml`
  - McGill-NLP AfroBench: aggregate scores across 15 NLP tasks, 22 datasets for African languages
  - Source: https://huggingface.co/spaces/McGill-NLP/AfroBench
  - 24 models evaluated: open-weight (Aya-101, Gemma family, LLaMA family, LLaMAX, AfroLLaMa, Lugha-Llama) and proprietary (GPT-4o, GPT-4.1, GPT-5, Gemini family, Claude family)
  - 5 focus languages covered: Hausa (hau), Igbo (ibo), Lingala (lin), Wolof (wol), Yoruba (yor)
  - Top performers: GPT-5, Claude 4.5 Sonnet, Gemini 2.5 Pro consistently score highest (65-83 range)
  - Wolof notably lower across all models (e.g. Claude 4.5 Sonnet: 43.9 vs 75.2 for Hausa)
- Downloaded papers for review (in `Project documents/`, not in repo):
  - `afrobench.pdf` — AfroBench paper (McGill-NLP, 15 tasks, 64 African languages)
  - `afrimteb_e5.pdf` — AfriMTEB (African Massive Text Embedding Benchmark)
  - `afrimcqa.pdf` — AfriMCQA (African Multiple-Choice QA benchmark)
  - `waxal-paper.pdf` — WAXAL (downloaded earlier)
- Compiled PazaBench ASR benchmark results into `Source data/Evaluations/pazabench.yaml`
  - Microsoft's PazaBench: 52 ASR models evaluated on 39 African languages (CER + WER)
  - Source: https://huggingface.co/spaces/microsoft/paza-bench
  - 7 focus languages covered: Fulfulde (ful), Hausa (hau), Igbo (ibo), Lingala (lin), Twi (twi), Wolof (wol), Yoruba (yor)
  - Notable gap: 19 of 26 focus languages not in PazaBench (Bambara, Ewe, Fon, Mooré, Krio, etc.)

### 2026-02-02
- Added 2 new languages from UNICEF country office survey (Focus 1 priorities):
  - Liberian Koloqua (lir) - Liberia
  - Guinea-Bissau Creole (pov) - Guinea-Bissau
- Focus languages now at 26 (was 24)
- Created actor prioritization scoring framework and draft ranking of all 26 actors
  - 6 dimensions: WCA relevance, language coverage, maturity, openness, UNICEF alignment, summit readiness
  - Draft tiers pending validation at 3 Feb meeting
  - Notes added for distributed communities (Masakhane, HausaNLP, etc.) on who to invite
- Added `openness` field display to actor detail pages in HTML (color-coded: green=open, yellow=partial, red=closed)
- Created `Event/` folder (gitignored) for summit planning documents
  - `actor_prioritization_methodology.md` - scoring framework
  - `actor_prioritization_report.md` - full rankings with justifications
  - `actor_rankings.yaml` - machine-readable scores
- Added `scripts/md_to_docx.py` - converts markdown to docx using pandoc
- Draft ready for 3 Feb UNICEF meeting; finalize by end of week

### 2026-01-28
- Fixed HuggingFace dataset links in both HTML and DOCX outputs to show both ISO-2 and ISO-3 language codes
  - Dataset pages don't include `numTotalItems` in HTML like model pages do
  - Implemented fallback counting mechanism: tracks items found per language code during scraping
  - Now displays multiple clickable links (e.g., "bm: 21 | bam: 3") matching the model listing behavior
  - Both HTML and DOCX generation updated to support `counts_by_code` for datasets
- Added multilingual model support auto-detection for three large models
  - Omnilingual: Speech-to-text model supporting 120+ languages
  - AfriNLLB: Machine translation model (African languages extension of NLLB)
  - Displays as flat entries in tech_resources section alongside MMS
- Verified and corrected Whisper FLEURS evaluation scores in benchmark data
- Fixed Lingala coding (Lingala-Bangala) when calling language LUDP

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
