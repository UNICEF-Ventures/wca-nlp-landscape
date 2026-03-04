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
- [x] List language support for MMS, AfriNLLB, Omnilingual, WaxalNLP, SimbaBench
- [x] Benchmark infrastructure (evaluations in benchmarks.yaml + benchmarks_manual.yaml, Source data/Evaluations/ with fetcher)
- [x] Unbenchmarked models support (`unbenchmarked_models` in benchmarks_manual.yaml — lists noteworthy models without scores)
- [ ] Crisis index information for languages (pending approval from CLEAR to add)
- [x] Document generation (DOCX: Languages + Actors)


### 1.2 Language Profiles
Automated fetching of HuggingFace models/datasets, Common Voice stats, and Wikipedia info for priority languages.

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 34   | 20     | ████████████████████ 170% |

**Focus languages (34):**

*Focus 1 — UNICEF country office survey (10):*
- Hausa (hau), Mende (men), Bambara (bam), Ewe (ewe), Fang (fan), Liberian Koloqua (lir), Shuwa Arabic (shu), Mooré (mos), Fon (fon), Guinea-Bissau Creole (pov)

*Focus 2 — UNICEF additions 17.2 (5):*
- Dyula (dyu), Gourmantchéma (gux), Soninke (snk), Twi (twi), Dagbani (dag)

*Focus 3 — CLEAR additional selection (14):*
- Yoruba (yor), Igbo (ibo), Wolof (wol), Fulfulde (ful), Krio (kri), Temne (tem), Ga (gaa), Kanuri (kau), Congo Swahili (swc), Lingala (lin), Sango (sag), Mandinka (mnk), Akan (aka), Pular (fuf)

*Focus 4 — Additional Fulfulde variants and Niger/Mali languages (4):*
- Fulfulde Maasina (ffm), Fulfulde Adamawa (fub), , Nigerian Fulfulde (fuv), Koyraboro Senni (ses), Toro So Dogon (dts)

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
24. UBC Deep Learning & NLP Lab - Canada, SAHARA/Toucan/AfroLID (517 African languages)
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
- [x] Validate criteria with UNICEF (3 Feb meeting)
- [x] Finalize ranked list

---

## Task 2: Benchmarking Study

Compile existing benchmark results and run manual evaluations for priority languages. Create comparative analysis where multiple models exist.

### 2.1 Infrastructure

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 3    | 3      | ████████████████████ 100% |

- [x] Benchmark data infrastructure (two-file system, Source data/Evaluations/, rendering on language pages)
- [x] Unbenchmarked models support (`unbenchmarked_models` in benchmarks_manual.yaml)
- [x] **Webpage feature:** "Sources" tab on website — unified sortable table of all data and benchmark sources with type badges, focus languages, and status (`Research/sources.yaml`)

### 2.2 Collect Benchmark Sources
Identify and track published benchmark papers, leaderboards, and evaluation datasets relevant to WCA languages.

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 14   | 16     | █████████████████░░░ 88%  |
- [x] Whisper FLEURS WER (6 focus langs)
- [x] CLEAR Global TWB Voice ASR + TTS (Hausa, Kanuri)
- [x] PazaBench ASR (52 models, 7 focus langs: ful, hau, ibo, lin, twi, wol, yor)
- [x] SimbaBench ASR + TTS (12 ASR models, 11 focus langs for ASR, 6 for TTS)
- [x] AfroBench-Lite LLM (24 models, 5 focus langs: hau, ibo, lin, wol, yor)
- [x] IrokoBench LLM (4 models, 7 focus langs: ewe, hau, ibo, lin, twi, wol, yor)
- [x] AfriqueLLM (5 models, 7 focus langs, LLM + MT tasks)
- [x] SAHARA LLM (24 models, 10 focus langs: hau, yor, ibo, wol, lin, fon, bam, mos, ewe, twi)
- [x] AfriNLLB + NLLB-600M MT (FLORES-200 BLEU/chrF, 4 focus langs: hau, yor, lin, wol)
- [x] NLLB/FLORES MT (hau, ibo, yor, mos, bam, aka)
- [x] MAFAND-MT (9 focus langs)
- [x] MADLAD-400 MT (14 langs, 3 test sets, 6 models, fully verified)
- [x] Bambara ASR leaderboard (MALIBA-AI, 5 models)
- [x] Goldfish monolingual LMs (FLORES perplexity, multiple langs)
- [ ] Seamless MT (not yet investigated)
- [ ] Additional TTS benchmarks (beyond SimbaBench + TWB Voice)

### 2.3 Save Benchmark Results
Extract scores from collected sources into `Source data/Evaluations/` YAML files and distribute to language profiles via `populate_research.py`.

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 3    | 3      | ████████████████████ 100% |
- [x] All sources listed in 2.2 extracted and saved
- [x] Manual entries in `benchmarks_manual.yaml` for one-off results (Goldfish, MMS FLEURS, Kreyol-MT, Bloom Speech, MAFAND Masakhane)
- [x] `Research/sources.yaml` status tracking (included/placeholder/noted)

### 2.4 Plan Manual Benchmarking
Gap analysis and feasibility assessment for languages missing benchmarks.

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 3    | 3      | ████████████████████ 100% |
- [x] Gap analysis completed (`Research/manual_benchmarking_plan.md`)
- [x] Identified 10 languages feasible for ASR evaluation, 3-4 for MT
- [x] Identified languages with no feasible path (fuh, ffm, shu, swc, lir, pov — no test data)

### 2.5 Execute Manual Benchmarking
Run model evaluations where public test data exists but no published scores are available.

| Done | Target | Progress                 |
|------|--------|--------------------------|
| 0    | 6      | ░░░░░░░░░░░░░░░░░░░░ 0%  |
- [ ] Quick wins: extract missing SimbaBench ASR scores for mos, sag, ewe
- [ ] Quick wins: run NLLB-200 on FLORES-200 for fuv, sag
- [ ] ASR evals: ewe, mos, dag, fan, sag, kri (on SimbaBench/Common Voice test splits)
- [ ] ASR evals (Bible-domain, lower priority): gux, ses, dts on CMU Wilderness
- [ ] MT evals: fuv, sag, kri, dag (NLLB/MADLAD on FLORES-200 or available test sets)
- [ ] Hire engineer for manual benchmark execution (pending decision)

---

## Task 3: Knowledge Management Assets

### 3.1 Language Factsheets (Deliverable 3.1)
Curated factsheets per language with resources, benchmarks, and assessment. Max 3 pages each.

| Status | Progress |
|--------|----------|
| Done — generated via `generate_docs.py` | ████████████████████ 100% |

Language profiles are auto-generated from YAML data into DOCX (`WCA_NLP_Languages.docx`) and HTML (live site). Content maintained through data pipeline.

### 3.2 Actor Engagement Framework (Deliverable 3.2)
Brief framework: criteria for identifying actors, key discovery resources, engagement best practices. Builds on Task 1 actor mapping.

| Status | Progress |
|--------|----------|
| Not started | ░░░░░░░░░░░░░░░░░░░░ 0% |

### 3.3 SharePoint Content (Deliverable 3.3)
Structured content for UNICEF SharePoint. CLEAR provides content/docs; UNICEF handles SharePoint setup and maintenance.

| Status | Progress |
|--------|----------|
| Content ready (docs + site), UNICEF to set up SharePoint | ████████████████████ 100% |

---

## Task 4: Summit Support (March 2026)

Advisory support for actor selection, agenda input, and presentation of findings.

- [x] Actor recommendations for summit invitations (prioritization framework + ranked list delivered)
- [ ] Agenda design input (up to 2 review cycles)
- [ ] 60-90 minute presentation session (virtual delivery, presenting findings + presentation materials)

---

## Recent Updates

### 2026-03-04
- **Translation datasets added to HuggingFace fetching:** Dataset scraping previously only covered ASR and TTS task categories. Added `translation` task category to `populate_research.py`, `htmlgen/pages.py` (language detail pages), and `generate_docs.py` (DOCX output). All focus languages now have MT datasets populated.
- **MADLAD-400 fully parsed and verified:** All 4 tables extracted from PDF — Table 16 (GATONES), Table 17 (FLORES-200), Table 18 (Flores-200 direct, skipped — subset of Table 17), Table 19 (NTREX). Fixed 6 wrong NTL baseline values Gemini had confused between models. 14 focus languages (bam, dyu, ewe, ful, twi, kri, fon, hau, ibo, yor, wol, lin, sag, mos), 6 models (MT-3B, MT-7.2B, MT-10.7B, LM-8B, NTL-1.6B, NTL-6.4B), up to 3 test sets per language. BLEU + chrF in both directions.

### 2026-03-03
- **Sahara LLM benchmarks fully extracted:** Scores populated in `Source data/Evaluations/sahara_llm.yaml` from PDF paper tables. 10 focus languages (hau, yor, ibo, wol, lin, fon, bam, mos, ewe, twi), 24 models, 16 NLP tasks across 4 clusters.
- **MADLAD-400 MT benchmarks initial extraction:** `Source data/Evaluations/madlad.yaml` created (via Gemini, with errors — corrected on 2026-03-04).
- Both sources marked as `included` in `Research/sources.yaml`.
- **PROGRESS.md benchmark table overhauled** to match actual `sources.yaml` state. Several sources (Bambara ASR, NLLB/FLORES, MMS, Goldfish, MAFAND-MT) were already included but incorrectly listed as "noted" or "not yet investigated".
- **URLs corrected:** Repo and live site URLs updated from translatorswb → UNICEF-Ventures across CLAUDE.md and PROGRESS.md.

### 2026-02-24
- **WaxalNLP and SimbaBench added** as multilingual dataset coverage files (`Source data/Multilingual-models-datasets/`). Both now appear in the NLP & Tech Resources section for covered focus languages.
- **Renamed** `Source data/Multilingual-models/` → `Source data/Multilingual-models-datasets/` to reflect that the directory holds both models and datasets.
- **Sources page overhauled:** Merged `data_sources` and `benchmark_sources` into a single unified `sources` list in `Research/sources.yaml`. Single sortable table with consistent type badges (Reference, Model Hub, Dataset, Model, Benchmark). Multi-type support for dual-nature sources (e.g. Kreyol-MT, NLLB/FLORES, SimbaBench, AfriNLLB are `[model, benchmark]` or `[benchmark, dataset]`). Status column renamed to "Benchmarks". Default sort by name; clickable sort on Source and Type columns.
- **Focus language columns populated** for Common Voice (7 langs), WaxalNLP (11), Omnilingual ASR (25), BibleMMS-TTS (1) in sources.yaml.
- **HuggingFace data refetched** for all focus languages (models.yaml + datasets.yaml updated).

### 2026-02-23
- **IrokoBench included:** `Source data/Evaluations/irokobench.yaml` — all 3 tasks, 4 models (GPT-4o, LLaMA 3.1 70B, Gemma 2 27B, Aya-101), 7 focus languages (ewe, hau, ibo, lin, twi, wol, yor). AfriMMMLU (5 subject metrics), AfriMGSM (math exact match), AfriXNLI (NLI accuracy). In-language setting throughout.
- **AfriqueLLM benchmarks included:** `Source data/Evaluations/AfriqueLLM.yaml` — 5 models (AfriqueQwen-14B, Qwen3-14B, AfriqueGemma-12B, Gemma3-12B, AfriqueLlama-8B) across 7 focus languages (ewe, hau, ibo, lin, twi, wol, yor). LLM tasks: Intent + Topic classification (AfroBench). MT tasks: chrF++ en↔xx on FLORES-200. Source: [arxiv 2601.06395](https://arxiv.org/abs/2601.06395).
- **SAHARA LLM benchmark:** Confirmed language coverage from paper (Table D2 + Figure E3). 10 focus languages covered: hau, yor, ibo, wol, lin, fon, bam, mos, ewe (multiple clusters), twi (token tasks only). Placeholder file created at `Source data/Evaluations/sahara_llm.yaml` — values are null pending leaderboard fix. Contacted authors to restore broken HF Space.
- **Bug fix:** `generate_html.py` crashed on `value: null` (or missing `value` key) in benchmark metrics YAML. Fixed `htmlgen/utils.py` to use `m.get('value')` instead of `m['value']`.
- **Focus language list restructured:** `focused_languages.yaml` now has two tiers — `priority` (14 languages: UNICEF confirmed + most critical) and `extended` (19 languages: broader coverage). Both tiers are processed and displayed, but the distinction enables prioritization for manual benchmarking and factsheet work.

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
- Downloaded 4 new papers: AfriqueLLM, Sahara, SimbaBench, IrokoBench
- New benchmark sources identified from notes:
  - Sahara (UBC-NLP): 517 languages, 16 NLP tasks, ACL 2025
  - SimbaBench (UBC-NLP): 61 languages, ASR/TTS/SLID, EMNLP 2025
  - AfriqueLLM (McGill-NLP): 20 African language LLMs, AfroBench-Lite eval
  - IrokoBench: 16 African languages, LLM benchmark (AfriXNLI, AfriMGSM, AfriMMLU)
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

- **Live site:** https://unicef-ventures.github.io/wca-nlp-landscape/
- **GitHub repo:** https://github.com/UNICEF-Ventures/wca-nlp-landscape
- **HTML Report (local):** `output/index.html`
- **Add language:** Edit `Research/focused_languages.yaml`, run `python scripts/populate_research.py`
- **Add actor:** Create `Research/Actors/{id}.yaml`
- **Regenerate HTML:** `python scripts/generate_html.py`
- **Generate DOCX:** `python scripts/generate_docs.py` (or `--languages` / `--actors`)
