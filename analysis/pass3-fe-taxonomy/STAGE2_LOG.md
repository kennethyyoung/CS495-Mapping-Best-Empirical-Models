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

---

## Batch 2: Heavyweight + below-range entries (notebooks available)

### s4e12 cdeotte (n_fe 8 → 8)

**Sources:** writeup + 21-cell notebook (`first-place-single-model-cv-1-016-lb-1-016.ipynb`).

**Stage 2 deltas:** **0 flips.** All 8 Stage 1 columns confirmed by notebook code:
- Cell 4-5: Policy Start Date decomposition (year/month/day/dow/seconds) → col 30 ✓
- Cell 7: `factorize` + HIGH_CARDINALITY detection — numerics-as-cats setup
- Cell 9: 20 surviving combinations (the brute-force-145K survivors) → col 16 ✓ (selection step kept) + col 17 ✓ (2-6 way combos)
- Cell 11: `target_encode` function with kfold splits, 5 aggregations (mean/median/min/max/nunique) → col 1, 2, 3 ✓
- Cell 14: Count encoding for high-cardinality + combo features → col 5 ✓; numerics-as-cats TE/CE → col 18 ✓

Stage 1 was thorough for cdeotte heavyweights.

### s5e2 cdeotte (n_fe 16 → 16)

**Sources:** writeup + 36-cell notebook (`first-place-single-model-lb-38-81.ipynb`).

**Stage 2 deltas:** **0 flips.** All 16 Stage 1 columns confirmed (with v3.1 col 17 flip). Notebook is the simplified 138-feature version; the actual 500-feature production code shares the same techniques.

Confirmed mappings: cell 12 NaN-base-2 (col 7) + per-column-NaN-with-WC; cell 13 multi-precision rounding (col 12); cell 14-15 original price merge by WC and rounded WC (col 32); cell 16 digits 1-9 (col 11); cell 17 digit pairs + cell 18 cat pairs (col 17); cell 23 STATS = mean/std/count/nunique/median/min/max/skew (cols 19/20/24); cell 24 QUANTILES + histogram bins (cols 21/22); cell 25 nested-fold TE (col 2).

### s6e2 masayakawamata (n_fe 10 → 10)

**Sources:** writeup + 21-cell RealMLP single-OOF notebook (`s6e2-single-realmlp.ipynb`).

**Stage 2 deltas:** **0 flips.** This notebook is only 1 of ~150 OOFs the ensemble used. What's verifiable:
- Cell 10: digit extraction (integer + decimal positions) → col 11 ✓
- Cell 12: multi-strategy binning (qcut q=4/5/10/20 + cut bins=5/10 + custom domain rounds Age/5, BP/10, Cholesterol/50, Max HR/10) → col 10 ✓
- Cell 14: ALL_CATS (treat all base as categorical strings) → col 18 ✓
- Cell 19: cuML TargetEncoder + StratifiedKFold pattern → col 2 ✓

Cols 32, 33, 38, 41 (original-target stats, DVAE, gplearn) are writeup-attested but live in other OOFs not in this single-model notebook.

### s3e6 viktortaran (n_fe 1 → 1)

**Sources:** writeup + 148-cell notebook (`ps-s-3-e-6.ipynb`).

**Stage 2 deltas:** **0 flips.** Notebook is large (148 cells, mostly EDA + per-model experiments). Cell 11 confirms `PermutationImportance` (eli5) → col 48 ✓. Did not exhaustively scan all 148 cells; final pipeline appears to match MD's "light FE" characterization. Conservative no-flip.

### s3e9 ambrosm (n_fe 1 → 5) — **BIG FLIP**

**Sources:** writeup + 20-cell notebook (`pss3e9-winning-model.ipynb`).

**Stage 2 deltas:** **+4 flips.** Stage 1 from MD massively under-counted. Cell 4 reveals 9 engineered features the MD didn't enumerate:

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 2 `uses_target_encoding_within_fold` | null | **1** | Cell 5: custom `TargetEncoder(BaseEstimator, TransformerMixin)` class for AgeInDays, fit per-fold in `make_pipeline(TargetEncoder(), ...)` (cell 8). |
| 13 `uses_pairwise_multiplicative_interactions` | 0 | **1** | Cell 4: `youngCementComponent = CementComponent * (AgeInDays < 40)` and `youngSuperplasticizerComponent = SuperplasticizerComponent * (AgeInDays < 10)` — threshold-conditional multiplicative interactions. |
| 27 `uses_domain_binary_flags` | 0 | **1** | Cell 4: `hasBlastFurnaceSlag = BlastFurnaceSlag != 0`, `hasFlyAshComponent = FlyAshComponent != 0`, `hasSuperplasticizerComponent = SuperplasticizerComponent != 0` — 3 domain-meaningful component-presence flags for concrete strength prediction. |
| 28 `uses_domain_ratios` | 0 | **1** | Cell 4: `Age_Water = AgeInDays / WaterComponent`, `Age_Cement = AgeInDays / CementComponent`, `Coarse_Fine = CoarseAggregateComponent / FineAggregateComponent` — 3 domain-meaningful concrete-mixture ratios. |

ambrosm's MD describes his approach as "PDP-derived nonlinear features for Ridge" — the notebook reveals these are the concrete-domain interactions, ratios, and threshold flags. The MD's anti-Optuna and trust-CV framing dominated the narrative; the actual FE was substantial.

### s3e11 ambrosm (n_fe 1 → 4) — **BIG FLIP**

**Sources:** writeup + 58-cell notebook (`pss3e11-zoo-of-models.ipynb`).

**Stage 2 deltas:** **+3 flips.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 2 `uses_target_encoding_within_fold` | null | **1** | Cell 26: `make_pipeline(TargetEncoder(cols=['store_sqft']), RandomForestRegressor(...))` — fit per-fold. |
| 13 `uses_pairwise_multiplicative_interactions` | 0 | **1** | Cell 21-22: `PolynomialFeatures(3, interaction_only=True)` and `PolynomialFeatures(4, interaction_only=True)` create explicit a*b, a*b*c, a*b*c*d products of features. |
| 14 `uses_pairwise_additive_interactions` | 0 | **1** | Cell 4: `salad = (salad_bar + prepared_food) / 2` — pairwise additive interaction (average of two features). |

ambrosm's "Zoo of Models" included explicit polynomial-interaction-Ridge variants (cells 21, 22), captured as multiplicative interactions. The MD focused on the dendrogram and zoo structure; the FE inside each branch was glossed.

---

## Batch 2 summary

| Entry | Stage 1 → 2 n_fe | Flips |
|---|---|---|
| s4e12 cdeotte | 8 → 8 | 0 |
| s5e2 cdeotte | 16 → 16 | 0 |
| s6e2 masayakawamata | 10 → 10 | 0 |
| s3e6 viktortaran | 1 → 1 | 0 |
| s3e9 ambrosm | 1 → **5** | +4 |
| s3e11 ambrosm | 1 → **4** | +3 |

**Total: 7 cells flipped across 6 entries.**

**Pattern:** ambrosm entries massively under-counted in Stage 1. His MDs emphasized methodology (anti-Optuna, trust-CV, zoo structure) over per-feature FE detail. Heavyweight cdeotte entries were already thoroughly captured.

**Cumulative Stage 2 deltas so far (11 entries):**
- Batch 1: 5 flips (s4e10 +2, s4e3 +1, s5e8 +2)
- Batch 2: 7 flips (s3e9 +4, s3e11 +3)
- **Total: 12 cell flips / 11 × 53 = 583 cells × 2% flip rate**

Higher than batch 1 alone (1.9%). The ambrosm entries are large drivers. Other ensemble-standard entries with notebooks may have similar under-counting.

---

---

## Batch 3: Fork-based and pipeline-bundled FE entries (6 entries)

### s3e1 Kirderf (n_fe 1 → 3) — **BIG FLIP**

**Sources:** writeup + 41-cell dmitryuarov notebook (`ps-s3e1-coordinates-key-to-victory.ipynb`).

**Stage 2 deltas:** **+2 flips.**

The forked notebook is heavy on geographic FE that Stage 1 (col 53 only) didn't capture:

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 31 `uses_cyclical_encoding` | 0 | **1** | Cell 8: sin/cos lat/lon embeddings at multiple frequencies (`emb_size=20, precision=1e6`). `latlon[..., 0::2] = np.cos(...)`, `latlon[..., 1::2] = np.sin(...)` — produces 40 sinusoidal features (exp_latlon1, exp_latlon2). |
| 39 `uses_pca_svd_components` | 0 | **1** | Cell 12: `PCA().fit(coordinates)` → pca_lat, pca_lon features. |

**Schema gaps surfaced** (not flipped — singletons):
- KMeans clustering features (cell 10: 20 cluster centers + haversine distance-to-cluster features)
- UMAP manifold projection (cell 12: umap_lat, umap_lon)
- Coordinate rotation features (cell 15: rot_15_x/y, rot_30_x/y, rot_45_x/y, rot_52, rot_60, rot_75)

Kirderf is the case for relaxing col 53 (single-fork-doing-all-FE), and now we see WHAT the dmitryuarov notebook actually produces.

### s3e4 Ollie Kemp (n_fe 1 → 1)

**Sources:** notebook only (`3rd-place-solution-ensemble-catboost.ipynb`, no writeup).

**Stage 2 deltas:** **0 flips.** Cell 5 `create_features` confirms 8 rowwise stats: V_sum, V_min, V_max, V_avg, V_std, V_pos (count>0), V_neg (count<0), V_range — all covered by col 26. Cell 3 CatTune class and cell 14 random_jump pseudo-ensemble are modeling (out-of-scope).

### s4e4 stopwhispering (n_fe 5 → 6)

**Sources:** writeup + 41-cell FE preprocessor notebook + 2 supporting notebooks.

**Stage 2 deltas:** **+1 flip.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 9 `uses_power_or_polynomial_transform` | 0 | **1** | Cell 21: `preprocessing.PolynomialFeatures(degree=2)` — creates squared features + pairwise products of metric_cols. Cell 24 FeatureUnion incorporates polynomials into the pipeline. |

Cell 13 `RatioFeaturesGenerator` confirms pairwise anatomical ratios → col 28 ✓. Cell 17 `LogTransformer` confirms log1p → col 8 ✓. OpenFE-generated features (from MD) not visible in this notebook — likely upstream.

### s4e5 adaubas (n_fe 5 → 5)

**Sources:** writeup + 35-cell ENSEMBLE notebook (`pss4e05-1st-place-solution-ensemble-with-ridge.ipynb`).

**Stage 2 deltas:** **0 flips.** This notebook is the Ridge meta-learner over 30+ pre-trained GBM OOFs. The base-model FE (row stats, count thresholds, sorted features) is upstream and NOT in this notebook. Cell 9 confirms permutation importance class → col 48 ✓.

Confidence: `writeup+notes` (downgrade from `notebook+writeup` because the notebook doesn't cover the base-model FE — writeup is the canonical source for those techniques).

### s4e9 Mart Preusse (n_fe 5 → 5)

**Sources:** writeup + 150-cell notebook (`ps4e9-cat-svr-lgbm-nn-py.ipynb`).

**Stage 2 deltas:** **0 flips.** Scanned cells 4-76. Cell 11 regex digit extraction confirms col 43. Cell 72 milage//10000 binning confirms col 10. Notebook is too large to exhaustively scan (encoding error past cell 80). Stage 1 likely covers the headline FE.

### s6e4 kirill0212 (n_fe 7 → 7)

**Sources:** writeup + 59-cell notebook (`ps6e4-ensemble-cv-0-98155.ipynb`).

**Stage 2 deltas:** **0 flips.** Cell 1 FE function confirms multi-position digits + magnitude-scaled rounding (col 11 + col 12). Cell 3 frequency-based mapping (col 6). Cell 4 explicit 2-way categorical combinations via `combinations(columns, r=[2])` with string concatenation + factorize → col 17 (2+ way per v3.1). All 7 Stage 1 cols confirmed.

---

## Batch 3 summary

| Entry | Stage 1 → 2 n_fe | Flips |
|---|---|---|
| s3e1 Kirderf | 1 → **3** | +2 (geographic FE) |
| s3e4 Ollie Kemp | 1 → 1 | 0 |
| s4e4 stopwhispering | 5 → **6** | +1 (polynomial) |
| s4e5 adaubas | 5 → 5 | 0 |
| s4e9 Mart Preusse | 5 → 5 | 0 |
| s6e4 kirill0212 | 7 → 7 | 0 |

**Total: 3 cells flipped across 6 entries.**

**Pattern:** s3e1 was the biggest under-counter — its forked notebook is heavy on geographic FE that the MD only labeled as "geographic FE uncatalogued (col 53)". Other entries had thorough Stage 1 coverage; mid-range entries (5-7 n_fe) tend to be already well-captured.

**Schema gaps surfaced (Stage 2 cumulative):**
- 2-way categorical combos (FIXED in v3.1)
- Single-fork forked FE (FIXED in v3.1)
- Geographic FE family (KMeans-haversine, UMAP, coordinate rotations) — singleton, defer
- Sorted-features (siukeitin technique) — appears at adaubas s4e5 and others; defer

**Cumulative Stage 2 deltas so far (17 entries):**
- Batch 1: 5 flips
- Batch 2: 7 flips
- Batch 3: 3 flips
- **Total: 15 cell flips / 17 × 53 = 901 cells × 1.7% flip rate**

---

## Next batch candidates

Remaining notebook-available:
- s3e8 Craig Thomas (EDA-only notebook per MD)
- s4e1 Iqbal (full 53-cell pipeline)
- s5e3 cdeotte (starter only)
- s5e4 greysky (training notebook)
- s5e7 Irfan
- s5e11 mahog (XGB-only)
- s6e1 mahog (Ridge meta)
- s6e3 cdeotte (L4 meta-learner)
- ICR room722
- TPS Feb 2022 ambrosm
- TPS May 2022 ambrosm

Writeup-only (no notebook → max confidence is `writeup+notes`):
- s3e7 Hardy Xu, s3e13 Umar, s3e17 ISoft, s3e24 Ravi, s4e7 Cross Sellers, s4e8 Optimistix, s5e5 cdeotte, s5e6 cdeotte

Skip: TPS Jun 2022 (buggy notebook).
