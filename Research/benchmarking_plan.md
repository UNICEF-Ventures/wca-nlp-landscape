# Benchmarking Plan — Priority Languages
*Last updated: 2026-02-24*

---

## Priority Languages — Coverage Status

| lang | Language | ASR | TTS | MT | LLM | Runnable eval data |
|------|----------|:---:|:---:|:--:|:---:|-------------------|
| hau | Hausa | ✓✓✓ | ✓ | ✓ | ✓✓ | Done — don't add more |
| twi | Twi | ✓✓ | ✓ | ✓ | ✓✓ | Done |
| ewe | Ewe | — | ✓ | ✓ | ✓✓ | SIB-FLEURS, WaxalNLP — **ASR gap** |
| bam | Bambara | ✓ | — | — | ✓ | MALIBA benchmark, SIB-FLEURS. MT extractable from NLLB/MADLAD |
| ful | Fulfulde | ✓ | — | — | — | google/fleurs + SIB-FLEURS. MT extractable from NLLB. LLM via Goldfish |
| dyu | Dyula | ✓ | — | — | — | SIB-FLEURS. MT extractable from NLLB/MADLAD. LLM via Goldfish |
| mos | Mooré | — | — | — | ✓ | SIB-FLEURS. ASR extractable from MMS paper. MT extractable from NLLB |
| dag | Dagbani | — | — | — | — | google/WaxalNLP (9.7h CV also) |
| gux | Gourmantchema | — | — | — | — | MMS-ASR supported → extract WER from MMS paper |
| dts | Toro So Dogon | — | — | — | — | MMS-ASR supported → extract WER from MMS paper |
| ses | Koyraboro Senni | — | — | — | — | MMS-ASR supported → extract WER from MMS paper |
| snk | Soninke | — | — | — | — | CV active + Omnilingual corpus |
| fuh | W. Niger Fulfulde | — | — | — | — | Omnilingual corpus only |
| ffm | Maasina Fulfulde | — | — | — | — | Omnilingual ASR (domain-limited). MT extractable from MADLAD-400 |

### Notes on "covered" languages
- **bam**: ASR from MALIBA-AI bambara_asr_leaderboard.yaml (5 models). LLM pending SAHARA fix.
- **mos**: LLM pending SAHARA fix. SIB-FLEURS dataset available for LLM classification eval.
- **ewe**: No ASR benchmarks despite being priority — WaxalNLP makes this runnable.
- **gux, dts, ses**: Not zero-resource — MMS-ASR supported, WER likely in MMS paper supplementary. Extract before assigning to engineer.
- **ffm**: MADLAD-400 confirms coverage → MT (FLORES) extractable. Only priority language with MT potential not yet pulled.

---

## Work Breakdown

### A — Extract from papers / repos (no engineer needed)

**Verified against downloaded PDFs 2026-02-24.**

1. **MMS paper** (`arxiv 2305.13516`) — ⚠️ scores NOT in PDF
   - gux, dts, ses, mos, ewe are not in FLEURS-102, so no per-language table exists in the paper
   - Paper only reports regional aggregate CER for the 1,107-language eval (Africa avg ≈ 4.1)
   - Per-language scores exist but only in external repo: https://github.com/facebookresearch/fairseq/tree/main/examples/mms
   - **Action: check that repo for per-language results files for gux, dts, ses**

2. **NLLB paper** (`arxiv 2207.04672`) — ✓ partial, rest in external repo
   - **In the paper (Table 38, MAFAND-MT, spBLEU/chrF++):**
     - mos_Latn: fra→mos 5.4/27.6, mos→fra 6.1/23.5
     - bam_Latn: fra→bam 7.7/29.9, bam→fra 14.6/37.5
   - **In the paper (Table 39, FLORES-200 chrF++, partial):**
     - aka_Latn: eng→aka 35.6, aka→eng 45.6
   - **dyu, ful (fuv_Latn):** confirmed supported but no per-language table in PDF — external repo only: https://github.com/facebookresearch/fairseq/tree/nllb
   - Note: MAFAND-MT test set (news domain), different from FLORES — caveat when reporting

3. **MADLAD-400** (`arxiv 2309.04662`) — ⚠️ scores NOT in PDF
   - Paper body has only aggregate BLEU by direction. Appendix A.10 references per-language scores but is not reproduced in the 20-page PDF.
   - Per-language MT scores only in external repo: https://github.com/google-research/google-research/tree/master/madlad_400
   - **Action: check repo for dyu, bam, ffm, ful, aka, kri**

4. **Goldfish** (`arxiv 2408.10441`) — ✓ fully extractable from PDF
   - FLORES log-perplexity scores in Table 5 (appendix, in PDF). Metric: mean negative log-probability per FLORES sequence. Lower = better.
   - Confirmed in paper:
     - aka_Latn: 132.48 (Goldfish), 128.37 (MaLA-500)
     - dyu_Latn: 183.05 (Goldfish), 189.79 (MaLA-500)
     - mos_Latn: 187.64 (Goldfish), 188.11 (MaLA-500)
     - knc_Arab (Kanuri): 181.38 (Goldfish)
     - knc_Latn (Kanuri): 170.17 (Goldfish)
     - bam_Latn: 158.88 (Goldfish), 143.14 (MaLA-500)
   - sag_Latn and fuv_Latn (ful): likely in Table 5 but not captured — verify in PDF pages 15-20 or at https://github.com/tylerachang/goldfish
   - **Action: extract and add to benchmarks_manual.yaml for aka, dyu, mos, kau (knc), bam**

5. **SAHARA scores** (`arxiv 2502.19582`)
   - Blocked: HF Space broken, contacted authors
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

**Note on Omnilingual:** Facebook's model claiming 120+ language ASR. Worth running on any language it covers, but note the domain (training data is largely Bible/religious texts via CMU Wilderness). Caveat results accordingly.

### C — Documentation-only (no evaluation possible or warranted)

These languages should have a gap analysis section in the report, not a benchmark table:
- **gux, dts, ses**: After MMS extraction — characterize coverage. Bible-domain speech only, likely poor on conversational language.
- **fuh, ffm**: Thinnest coverage in the priority list. Omnilingual corpus + domain-limited. Recommend flagging for UNICEF as needing dedicated data collection if they need usable ASR.

Extended languages with **true gaps** (no known benchmark data, no obvious test set):
- **swc** (Congo Swahili), **fan** (Fang), **lir** (Liberian Kreyol), **shu** (Chadian Arabic)
- These 4 have no coverage in any noted source. Flag as genuine technology gaps.

---

## The Coverage Spectrum (for the report)

Rather than "zero-resource vs covered", frame as a spectrum:

1. **Well-benchmarked** — Multiple models, multiple independent test sets: hau, twi, yor, ibo, wol, lin, ewe (LLM+MT+TTS), bam (ASR+LLM)
2. **Partially benchmarked** — At least one evaluation, limited model variety: bam, dyu, ful, mos, gaa, aka, kau, fuf, kri, sag, pov, fon
3. **Evaluation-ready but not run** — Test sets exist, evaluations not done yet: dag (WaxalNLP), snk (CV), ewe (ASR), mos (SIB-FLEURS LLM)
4. **Extractable from papers** — MMS/NLLB/MADLAD coverage confirmed, just needs pulling: gux, dts, ses (MMS ASR); mos, dyu, ful, bam, ffm (NLLB/MADLAD MT)
5. **Low-resource, domain-limited** — Only Bible/CMU Wilderness domain coverage: fuh, ffm
6. **True gaps** — No evaluation data and no test set: swc, fan, lir, shu

---

## Next Session Checklist

- [ ] Extract MMS paper WER/CER for gux, dts, ses (and verify mos, ewe)
- [ ] Extract NLLB FLORES-200 MT scores for mos, dyu, ful, bam, aka
- [ ] Extract MADLAD-400 MT scores for ffm (and dyu, bam if not covered by NLLB)
- [ ] Extract Goldfish LLM perplexity for dyu, ful, kau, sag, aka
- [ ] Wait/follow up on SAHARA HF Space fix
- [ ] Decide scope for ML engineer engagement (Tier B above)
- [ ] Add Omnilingual model evaluation to benchmarks_manual.yaml once run
