# Pass 3 FE Taxonomy — Stage 2 Log

**Status:** Stage 2 in progress. Each entry source-validated against original writeup + notebook (when available).
**Branch:** `phase9/fe-taxonomy`.
**Date started:** 2026-05-28.
**Data:** updates applied directly to `stage1_data.csv` (with `pass3_source_confidence` upgrades).

This log documents Stage 1 → Stage 2 cell flips per entry. Format: read writeup + notebook → re-evaluate every Stage 1 cell → flip FALSE/null → TRUE where the MD under-summarized.

---

## Batch 1: High-priority below-range entries (notebooks available)

### s3e23 oscarm524 (n_fe 1 → 1)

**Sources:** writeup + 44-cell notebook (`ps-s3-ep23-eda-modeling-submission.ipynb`).

**Stage 2 deltas:** **0 flips.**

Notebook confirms:
- Cell 40: `X.apply(lambda x: np.log1p(x))` for ALL features in final 25-fold pipeline → col 8 ✓ (Stage 1)
- Cell 18 (PCA), cell 25 (KMeans), cell 23 (inertia) → all built but writeup-confirmed "didn't help"; not in final
- Cell 34 (hill_climbing function) + cell 36 (10-fold HC ensemble) — Pass 1

Stage 1 was correct; only log-transform was used as FE. **Confidence upgraded `notes-only` → `notebook+writeup`.**

---

### s4e10 omidbaghchehsaraei (n_fe 2 → 4)

**Sources:** writeup + 40-cell notebook (`ensemble-modeling-for-loan-approval.ipynb`).

**Stage 2 deltas:** **+2 flips.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 1 `uses_target_encoding_basic` | 0 | **1** | Notebook cells 20, 22, 26, 28: `make_pipeline(TargetEncoder(), ExtraTrees/RF/KNN/MLP)` from `category_encoders`. |
| 2 `uses_target_encoding_within_fold` | null | **1** | TargetEncoder runs inside `Pipeline` which is fit per-fold in `cross_validation()` loop (cell 12). Leak-safe by construction. |

Stage 1 (Pass 2 MD) understated: only `paddykb's all-features-as-categories` was caught (col 10). The TE pipeline was buried in cells 20/22/26/28 and not explicit in MD.

**Confidence:** `notebook+writeup`.

---

### s4e3 Moonlit (n_fe 3 → 4)

**Sources:** writeup + 37-cell notebook (`2nd-place-solution-steel-plate-defect-prediction.ipynb`).

**Stage 2 deltas:** **+1 flip.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 13 `uses_pairwise_multiplicative_interactions` | 0 | **1** | Notebook cell 11: `data['X_Range*Pixels_Areas'] = (data['X_Maximum'] - data['X_Minimum']) * data['Pixels_Areas']` — multiplicative interaction between engineered range and area. |

Other notebook FE confirms Stage 1 coding:
- `Ratio_Length_Thickness = Length_of_Conveyer / Steel_Plate_Thickness` → col 28 ✓ (steel domain ratio)
- `Normalized_Steel_Thickness` → scaling preprocessing (Pass 1, not Pass 3)
- `features_to_drop` after CV + feature importance + correlation → col 50 ✓

**Confidence:** `notebook+writeup`.

---

### s3e16 Ravi (n_fe 3 → 3)

**Sources:** writeup + 51-cell notebook (`playgrounds3e16-eda-baseline.ipynb`).

**Stage 2 deltas:** **0 flips.**

Notebook confirms:
- Cell 11 (Xformer): `PseudoBMI = Weight/Height^2`, `LenDivDiam = Length/Diameter`, `WgtDivVisWgt = Weight/VisceraWeight`, `WgtDivShellWgt = Weight/ShellWeight`, `WgtDivShckWgt = Weight/ShuckedWeight` — 5 anatomical ratios all covered by col 28
- Cell 41 confirms `mutual_info_regression` + `permutation_importance` → col 48 ✓
- Log on weight (writeup point 3, "did not help greatly") — col 8 ✓
- Cell 43 `PostProcessPred` rounds to nearest integer — postprocessing, out-of-scope

Surface Area mentioned in writeup but NOT computed in notebook's `Xformer`. Possibly in a different version of the pipeline. Conservative: don't add column.

**Confidence:** `notebook+writeup`.

---

### s5e8 mahog (n_fe 6 → 8)

**Sources:** writeup + 7-cell TabM notebook (`pg-s5e8-tabm-cv-0-976810-pb-0-97750.ipynb`).

**Stage 2 deltas:** **+2 flips.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 2 `uses_target_encoding_within_fold` | null | **1** | Notebook cell 5: cuML `TargetEncoder(n_folds=10, smooth=0, seed=42, split_method='random', stat='mean')` fit INSIDE StratifiedKFold loop, per-fold per-column. Explicit within-fold leak-safe. |
| 8 `uses_log_transform` | 0 | **1** | Notebook cell 3: `_balance_log = sign(balance) * log1p(abs(balance))` for train/test/orig. Signed-log transformation for the `balance` feature. |

Cell 3 also confirms cyclical features (`_duration_sin`, `_duration_cos`, `_balance_sin`, `_balance_cos`, `_age_sin`, `_pdays_sin`) → col 31 ✓ (Stage 1).

Note: This notebook is only the TabM single-model; the full 59-model ensemble's FE may differ. Stage 2 codes what's verifiable. Confidence `notebook+writeup` reflects this.

---

## Batch 1 summary

| Entry | Stage 1 → Stage 2 n_fe | Flips |
|---|---|---|
| s3e23 oscarm524 | 1 → 1 | 0 |
| s4e10 omidbaghchehsaraei | 2 → 4 | +2 |
| s4e3 Moonlit | 3 → 4 | +1 |
| s3e16 Ravi | 3 → 3 | 0 |
| s5e8 mahog | 6 → 8 | +2 |

**Total: 5 cells flipped FALSE/null → TRUE across 5 entries (5 / 265 cells = 1.9% flip rate).**

Higher than pilot's 0.6% (the pilot entries had unusually thorough MDs). This rate is more representative of what to expect across the remaining ~30 Stage 2 candidates.

## Key methodology observation

The flip pattern is informative: **most missed techniques cluster around TE detail (within-fold vs vanilla) and bundled-into-pipeline transformations** (log inside cell 3 setup blocks, TargetEncoder inside cross-validation loops). The Pass 2 MDs systematically miss these because the MD summarizes the writeup, and writeups themselves don't always describe what's in code-only.

This is the "generational drift" the schema's `pass3_source_confidence` column was designed to measure. Stage 2 confidence upgrades capture this rigor.

---

## Next: medium-priority Stage 2 candidates

Continuing through the corpus. Priority order:
- Heavyweight entries with notebooks: s4e12, s5e2, s5e5 (cdeotte), s6e1 (mahog), s6e2 (masaya), s6e3 (cdeotte)
- Other notebook-available entries: s3e8, s3e11, s3e23, s4e1, s4e3, s4e4, s4e9, s4e10, s5e3, s5e6 (partial), s5e7, s5e11, s6e4, etc.
- Writeup-only (no notebook): s3e7, s3e13, s3e17, s3e24, s4e7, s4e8, s5e5 (writeup-only), s5e6 (writeup-only)

Skip: Cross Sellers (proprietary), TPS Jun 2022 (buggy notebook per author).
