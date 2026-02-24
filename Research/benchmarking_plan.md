# Benchmarking Plan — Priority Languages
*Last updated: 2026-02-24*

---

## Priority Languages — Coverage Status

| lang | Language | ASR | TTS | MT | LLM | Runnable eval data |
|------|----------|:---:|:---:|:--:|:---:|-------------------|
| hau | Hausa | ✓✓✓ | ✓ | ✓✓ | ✓✓ | Done — don't add more |
| twi | Twi | ✓✓ | ✓ | ✓ | ✓✓ | Done |
| ewe | Ewe | — | ✓ | ✓ | ✓✓ | WaxalNLP — **ASR gap** |
| bam | Bambara | ✓ | — | ✓ | ✓ | MALIBA benchmark. MADLAD MT still pending (external repo) |
| ful | Fulfulde | ✓ | — | — | ✓ | google/fleurs. MT pending NLLB/MADLAD external repo |
| dyu | Dyula | ✓ | — | — | ✓ | SIB-FLEURS. MT pending NLLB/MADLAD external repo |
| mos | Mooré | — | — | ✓ | ✓ | SIB-FLEURS. ASR pending MMS external repo |
| dag | Dagbani | — | — | — | — | google/WaxalNLP (9.7h CV also) |
| gux | Gourmantchema | — | — | — | — | MMS-ASR supported → pending MMS external repo |
| dts | Toro So Dogon | — | — | — | — | MMS-ASR supported → pending MMS external repo |
| ses | Koyraboro Senni | — | — | — | — | MMS-ASR supported → pending MMS external repo |
| snk | Soninke | — | — | — | — | CV active + Omnilingual corpus |
| fuh | W. Niger Fulfulde | — | — | — | — | Omnilingual corpus only |
| ffm | Maasina Fulfulde | — | — | — | — | Omnilingual ASR (domain-limited). MT pending MADLAD external repo |

### Notes
- **bam, mos**: MT entered from NLLB Table 38 (MAFAND-MT news domain, fra pairs).
- **hau, ibo, yor**: MAFAND-MT entered from NLLB Table 38 (eng pairs) + Masakhane M2M-100 models.
- **ful, dyu**: Goldfish LLM perplexity entered. MT still needs NLLB/MADLAD external repos.
- **ewe**: No ASR benchmarks despite being priority — WaxalNLP makes this runnable.
- **gux, dts, ses**: MMS coverage confirmed but scores only in external repo (not in PDF).
- **ffm**: MADLAD-400 MT potential — only priority language still fully zero-benchmark.

---

## Work Breakdown

### A — Extract from papers / repos (no engineer needed)

**Verified against downloaded PDFs 2026-02-24.**

1. **MMS paper** (`arxiv 2305.13516`) — ❌ no per-language data available
   - gux, dts, ses, mos, ewe not in FLEURS-102 — no per-language table in PDF
   - GitHub repo (examples/mms) contains only model checkpoints, no results files
   - **Dead end** — only option is to run MMS model directly on a test set (→ Tier B)

2. **NLLB paper** (`arxiv 2207.04672`) — ✅ done (PDF portion)
   - Extracted Table 38 (MAFAND-MT): hau, ibo, yor (eng pairs); mos, bam (fra pairs)
   - Extracted Table 39 (FLORES-200 chrF++): aka
   - dyu, ful (fuv_Latn) not in PDF — GitHub repo also contains no results files (dead end)

3. **MADLAD-400** (`arxiv 2309.04662`) — ❌ no per-language data available
   - GitHub repo contains only model checkpoints and vocabulary files, no evaluation results
   - **Dead end** — dyu, bam, ffm, ful, aka, kri MT scores not retrievable without running the model

4. **Goldfish** (`arxiv 2408.10441`) — ✅ done
   - Entered FLORES log-perplexity for: aka, bam, dyu, ewe, fon, ful (fuv), hau, ibo,
     kau (knc_arab + knc_latn), lin, mos, wol, yor
   - MaLA-500-10B-v2 baseline also entered for: aka, bam, fon
   - sag, wol scores confirmed from user; fuv confirmed in table

5. **SAHARA scores** (`arxiv 2502.19582`) — ⚠️ blocked
   - HF Space broken, contacted authors
   - Covers: bam, mos, ewe, fon, hau, yor, ibo, wol, lin, twi (once fixed)

### B — ML engineer: run evaluations on existing test sets

**Priority:**
| Language | Test set | Models to run | Task |
|----------|----------|---------------|------|
| dag | google/WaxalNLP + Omnilingual test split | Whisper variants, MMS, Omnilingual | ASR → WER/CER |
| ewe | google/WaxalNLP + Omnilingual test split | Whisper variants, Omnilingual | ASR → WER/CER |
| snk | Common Voice test split + Omnilingual test split | Whisper, MMS, Omnilingual | ASR → WER/CER |
| ful | google/fleurs + Omnilingual test split | Omnilingual + additional Whisper variants | ASR → WER/CER |

**Secondary:**
| Language | Test set | Models | Task |
|----------|----------|--------|------|
| mos | SIB-FLEURS | Llama 3.1, Aya-101, GPT-4o (zero-shot) | LLM classification |
| bam | SIB-FLEURS | Same as above | LLM classification |
| fuh | Omnilingual corpus test split | Omnilingual model | ASR → WER/CER (Bible-domain, caveat) |
| ffm | Omnilingual corpus test split | Omnilingual model | ASR → WER/CER (Bible-domain, caveat) |

**Note on Omnilingual:** Training data is largely Bible/CMU Wilderness domain — caveat results accordingly.

### C — Documentation-only (no evaluation possible or warranted)

- **gux, dts, ses**: After MMS extraction — characterize coverage. Bible-domain speech only.
- **fuh, ffm**: Thinnest coverage in priority list. Flag to UNICEF as needing dedicated data collection.
- **True gaps** (no data, no test set): swc, fan, lir, shu

---

## The Coverage Spectrum (for the report)

1. **Well-benchmarked** — Multiple models, multiple test sets: hau, twi, yor, ibo, wol, lin
2. **Good coverage** — 3+ task types: ewe (MT+LLM+TTS), bam (ASR+MT+LLM), mos (MT+LLM), aka (ASR+MT+LLM)
3. **Partial** — 1–2 task types: dyu (ASR+LLM), ful (ASR+LLM), kau (ASR+TTS+LLM), gaa (ASR), fuf (ASR), kri (MT), sag (MT), pov (MT), fon (ASR+LLM)
4. **Evaluation-ready but not run**: dag (WaxalNLP), snk (CV), ewe ASR (WaxalNLP)
5. **Extractable pending repos**: gux, dts, ses (MMS ASR); dyu, ful, ffm (NLLB/MADLAD MT)
6. **Domain-limited only**: fuh, ffm (Omnilingual/Bible domain)
7. **True gaps**: swc, fan, lir, shu

---

## Next Session Checklist

- [ ] MMS: no results in repo — move gux, dts, ses to Tier B (run MMS model on test set)
- [ ] MADLAD: no results in repo — dyu, ffm, ful MT scores only obtainable by running model
- [ ] NLLB: no results in repo — dyu, ful FLORES-200 scores only obtainable by running model
- [ ] Wait/follow up on SAHARA HF Space fix
- [ ] Decide scope for ML engineer engagement (Tier B above)
- [ ] Add Omnilingual model evaluation to benchmarks_manual.yaml once run
