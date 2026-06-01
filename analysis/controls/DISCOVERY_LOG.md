# Phase 1 Pilot — Discovery Log

**Pilot status:** Discovery complete (5/5 target).
**Started:** 2026-06-01.

## Discovery results

| # | Competition | Control rank | Author | Content type | Local files | Winner (coded) | Winner's paradigm | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | playground-series-s6e4 | 19 | ? | ? | ? | kirill0212 r1 | community-template | |
| 2 | playground-series-s6e3 | 16 | mhamza0810 | writeup + NB | `16th Place Solution - Ridge Ensembling _ Kaggle.txt`, `16th_Place_ps-s6e3-pytabkit-ensemble-baseline.ipynb` | cdeotte r1 | heavyweight | **Coded.** n_fe_tech=9. Rich FE module: freq enc, digits, deviations, round-flags, n-gram combos, rowwise counts, domain ratios, cyclical embeddings, ORIG_proba. **DVAE WAS AVAILABLE but explicitly dropped** (cell 5 cols_to_drop). No other Group G. Highest control n_fe_tech yet. |
| 3 | playground-series-s6e2 | 15 | emreduman05 | writeup + 2 NBs | `15th Place Solution _ Kaggle.txt`, `15th_heart-disease-basic-eda.ipynb`, `15th_predicting_heart_disease_s6e2.ipynb` | masaya r1 | heavyweight | **Coded.** n_fe_tech=4 (TE basic, TE within-fold, freq enc, pairwise mult). Adopted cdeotte's nested K-fold. Stark contrast to masaya's 10 techniques — no Group G, no original-derived stats. |
| 4 | playground-series-s5e10 | 14 | metamodels | writeup + meta-only NB | `S5E10 _ 14th place solution _ Kaggle.txt`, `14th-place-simple-average-oof-ensemble.ipynb` | Tilii r1 | heavyweight | **Coded.** n_fe_tech=2 (TE basic, residual). Notebook is just meta-averager loading external OOFs. Base-model FE for 100+ pooled models is UNENUMERATED in writeup. Source confidence: writeup-only. Caveat: actual FE diversity probably higher than 2. |
| 5 | playground-series-s5e8 | 15 | ? | ? | ? | mahog r2 | ensemble-standard | |

(Author handle / content type / filenames to be filled in as we process each entry.)

## Paradigm coverage

- **Heavyweight:** 3 controls (s5e10, s6e2, s6e3) — directly tests the audit-flagged heavyweight finding
- **Community-template:** 1 control (s6e4)
- **Ensemble-standard:** 1 control (s5e8)
- **Single-model-heavy / lookup / problem-fit / minimal:** 0 controls (pilot didn't target these)

## Era coverage

- **s5 era (2025):** 2 controls (s5e8, s5e10)
- **s6 era (2026):** 3 controls (s6e2, s6e3, s6e4)
- **s3/s4 era:** 0 controls

This concentration is fine for the pilot — it matches where heavyweight as a paradigm is observed in our corpus. Phase 2 would need to broaden to s3/s4 if we want era-stable claims.

## Rank distribution

- Ranks: 14, 15, 15, 16, 19. Median 15.
- All five are clearly outside top 3. **True non-winning controls.**
- Median rank 15 satisfies the "≥8" pilot success criterion.

## Next steps for Phase 1

1. Save each control's content to `data/writeups/<slug>/control_<author>_rank<N>.{txt,ipynb}`
2. Code Pass 3 booleans for each (writes to `analysis/pass3-fe-taxonomy/controls_data.csv`)
3. Write `analysis/controls/PILOT_RESULTS.md` decision memo
4. Decide: scale to Phase 2 (target 25-30 controls) OR finalize comparison from pilot data alone

## Time tracking

| Step | Estimated | Actual |
|---|---|---|
| Discovery | 5 hr | (TBD) |
| Save content locally | 1 hr | (TBD) |
| Pass 3 coding × 5 entries | 3.5 hr | (TBD) |
| Decision memo | 1 hr | (TBD) |
| **Total** | 10.5 hr | (TBD) |
