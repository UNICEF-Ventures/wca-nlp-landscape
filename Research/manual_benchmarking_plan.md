# Manual Benchmarking Plan — UNICEF WCARO NLP Landscape

**Prepared by:** CLEAR Global | **Date:** 2026-03-04 | **Status:** DRAFT — for UNICEF review

## Benchmark Coverage Overview

Through the landscape mapping, we compiled published evaluation results from 14 major benchmark sources for all 15 priority languages. The table below shows the current state and what we propose to evaluate manually.

**Legend:** ✅ = covered by published benchmarks | 🔧 = proposed manual evaluation | ➖ = not feasible (no models or test data)

| Language | ISO | ASR | TTS | MT | LLM | Notes |
|----------|-----|-----|-----|-----|-----|-------|
| Hausa | hau | ✅ | ✅ | ✅ | ✅ | |
| Bambara | bam | ✅ | ➖ | ✅ | ✅ | |
| Twi | twi | ✅ | ✅ | ✅ | ✅ | |
| Fon | fon | ✅ | ➖ | ✅ | ✅ | |
| Dyula | dyu | ✅ | ➖ | ✅ | ✅ | LLM coverage shallow |
| Fulfulde | ful | ✅ | ➖ | ✅ | ✅ | LLM coverage shallow |
| Ewe | ewe | 🔧 | ✅ | ✅ | ✅ | ASR: Omnilingual + MMS + HF models on SimbaBench/CV |
| Mooré | mos | 🔧 | ➖ | ✅ | ✅ | ASR: Omnilingual + MMS on SimbaBench |
| Dagbani | dag | 🔧 | ➖ | 🔧 | ➖ | ASR: Omnilingual on Common Voice (25h). MT: OPUS-MT on parallel datasets |
| Nigerian Fulfulde | fuv | 🔧 | ➖ | 🔧 | ✅ | ASR: Omnilingual on corpus test + FLEURS. MT: NLLB on FLORES-200. *Confirm if fuv is a distinct priority or covered under ful.* |
| Soninke | snk | 🔧 | ➖ | ➖ | ➖ | ASR: Omnilingual on corpus test split |
| W. Niger Fulfulde | fuh | 🔧 | ➖ | ➖ | ➖ | ASR: Feasibility check — corpus exists but model support unconfirmed |
| Koyraboro Senni | ses | ➖ | ➖ | 🔧 | ➖ | MT: OPUS-MT on parallel datasets (no standard test set) |
| Gourmanché | gux | ➖ | ➖ | ➖ | ➖ | Only Bible audio exists — not valid for real-world eval |
| Maasina Fulfulde | ffm | ➖ | ➖ | ➖ | ➖ | No model support, no test data |
| Toro So Dogon | dts | ➖ | ➖ | ➖ | ➖ | MMS-ASR exists but no evaluation data |

## What This Means

- **10 languages** are already well-covered by published benchmarks — no action needed.
- **7 languages** can be manually evaluated (8 ASR evals + 3 MT evals).
- **3 languages** (gux, ffm, dts) have no feasible evaluation path — this itself is a finding we'll document.
- We skip **TTS** (requires a linguist) and **LLM** (no evaluation datasets exist for uncovered languages).

## Scope

~15-20 model evaluations across 7 languages. Requires GPU compute and 2-3 weeks of engineering time. Results integrate directly into the landscape site.

## Decision Points for next call with UNICEF

1. **Nigerian Fulfulde (fuv):** Distinct priority, or covered under Fulfulde (ful)?
2. **Non-standard MT test sets** (dag, ses): No FLORES-200 coverage, so we'd use Bible/parallel text — less comparable. Proceed?
3. **Anything to add or remove?**
