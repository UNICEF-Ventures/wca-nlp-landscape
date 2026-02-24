# Benchmarking Plan — Priority Languages
*Last updated: 2026-02-24*

---

## Coverage Status

| lang | ASR | TTS | MT | LLM | Notes |
|------|:---:|:---:|:--:|:---:|-------|
| hau | ✓✓✓ | ✓ | ✓✓ | ✓✓ | Done |
| twi | ✓✓ | ✓ | ✓ | ✓✓ | Done |
| ewe | — | ✓ | ✓ | ✓✓ | ASR gap — WaxalNLP runnable |
| bam | ✓ | — | ✓ | ✓ | MADLAD MT extraction pending |
| ful | ✓ | — | — | ✓ | MADLAD MT extraction pending |
| dyu | ✓ | — | — | ✓ | MADLAD MT extraction pending |
| mos | — | — | ✓ | ✓ | ASR: no test set |
| dag | — | — | — | — | WaxalNLP + CV runnable |
| snk | — | — | — | — | CV runnable |
| gux | — | — | — | — | MMS supported, no test set |
| dts | — | — | — | — | MMS supported, no test set |
| ses | — | — | — | — | MMS supported, no test set |
| fuh | — | — | — | — | Omnilingual only (Bible-domain) |
| ffm | — | — | — | — | Omnilingual only (Bible-domain) |

---

## Paper Extraction Status

- [x] **MMS** — Table A3 CER (hau, ful, ibo, lin, wol, yor) + Table A1 WER (hau, yor). Non-FLEURS languages have no scores in paper or repo.
- [x] **NLLB** — Table 38 MAFAND-MT (hau, ibo, yor, mos, bam) + Table 39 FLORES (aka). dyu/ful not in paper or repo.
- [x] **Goldfish** — FLORES log-perplexity for aka, bam, dyu, ewe, fon, ful, hau, ibo, kau, lin, mos, wol, yor. MaLA-500 baseline for aka, bam, fon.
- [ ] **MADLAD-400** — Tables 16+17 have scores. Extract MT-10.7B BLEU/chrF++ for: dyu, bm(bam), ee(ewe), ff(ful), kri, ln(lin), wo(wol), ak(aka) + FLORES-200 en-centric pairs.
- [ ] **SAHARA** — HF Space broken, awaiting author access. Covers: hau, yor, ibo, wol, lin, twi, aka, fon, bam, ful.

---

## ML Engineer Brief (send ASAP)

Run ASR evaluations using **Omnilingual ASR** (Meta, github.com/facebookresearch/omnilingual-asr) — most inclusive ASR model for WCA languages.

| ISO | Test set | Notes |
|-----|----------|-------|
| dag | google/WaxalNLP test split | CV 9.7h also available |
| ewe | google/WaxalNLP test split | No existing ASR benchmarks |
| snk | Common Voice test split | |
| ful | google/fleurs | Baseline: MMS CER=13.8 |
| fuh | Omnilingual corpus test split | Bible-domain caveat |
| ffm | Omnilingual corpus test split | Bible-domain caveat |
| gux | Omnilingual corpus test split | Bible-domain caveat |

Report: model ID, test set, split, WER and/or CER.

