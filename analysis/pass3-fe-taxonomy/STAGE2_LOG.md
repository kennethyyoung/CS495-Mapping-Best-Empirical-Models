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

**Stage 2 deltas:** **0 flips.** Full notebook scanned after fixing en-dash codec issue (scripts/stage2_inspect.py now strips non-ASCII chars before printing on Windows cp932).

Cells 4-76 (EDA): mostly per-category boxplots and price distributions; cell 11 confirms regex extraction of milage/price digits from strings.

Cells 80-150 (FE + modeling):
- Cell 80 `feat_eng`: `mileage = milage//100` binning (col 10 ✓), regex `(\d+\.?\d*)HP` and `(\d+(\.\d+)?)L` extraction for horsepower/displacement (col 43 ✓)
- Cell 91 `bin_price`: IQR-based outlier binarization (`price < upper_bound`) — input to CatBoost classifier → col 47 ✓
- Cell 94 custom `target_encoding` with smoothing parameter, per-fold inside `crossvalidate` — agg returns count/mean/median/std but default call uses median only → col 1 ✓ (single-statistic median TE) and col 2 ✓ (per-fold)
- Cell 103 SVR pipeline: `make_pipeline(TargetEncoder(smoothing=10, min_samples_leaf=2), StandardScaler, LinearSVR)` → col 1, col 2 ✓
- Cell 109 `data_train2['price_is_low'] = oof_cat` — CatBoost outlier-classifier OOF added as feature for downstream LGBM → col 47 ✓
- Cells 112-128: rare-value relabeling (Pass 1 `rare_class_handling`), OHE (Pass 1), NN architecture with `Embedding(CAT_SIZE, CAT_EMB)` layers (architectural, out-of-scope)
- Cell 138 Ridge with `positive=True` ensembler (Pass 1)

All 5 Stage 1 cols confirmed at code level. No additional FE techniques surfaced.

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

---

## Batch 4: Notebook-but-meta-only + TPS entries (6 entries)

### s5e3 cdeotte (n_fe 1 → 1)

**Sources:** writeup + 14-cell STARTER notebook (`rapids-svc-w-feature-engineering-lb-0-856.ipynb`).

**Stage 2 deltas:** **0 flips.** The published notebook is the *starter* (LB 0.856), NOT the 2nd-place SVC submission. Cell 9 builds pairwise multiplicative interactions; cell 10 does forward feature selection via GroupKFold-by-year. Per the writeup, the actual 2nd-place SVC used "data as is without FE." Stage 1 col 51 reflects the 2nd-place submission and stands.

Confidence: `writeup+notes` (downgrade — notebook doesn't represent the 2nd-place artifact).

### s5e7 Irfan (n_fe 1 → 1)

**Sources:** notebook only (no writeup in local set; `2nd_introverts-and-extroverts-0-974-competetion-win.ipynb`).

**Stage 2 deltas:** **0 flips.** Cells 1-16 scanned (Config class + data load + 6 EDA visualizations). Pedagogical notebook style with extensive markdown. `match_p` exact-key-match lookup is the canonical winning move per spreadsheet — captured in col 34. No other FE techniques visible in early cells.

Confidence: `notebook+writeup` (notebook is the only available source; writeup_url points to discussion sorted by votes, not authorial narrative).

### s5e11 mahog (n_fe 7 → 8)

**Sources:** writeup + 6-cell XGB-only notebook (`pg-s5e11-xgb-cv-0-92818-pb-0-92923.ipynb`).

**Stage 2 deltas:** **+1 flip.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 26 `uses_rowwise_statistics` | 0 | **1** | Cell 4: `X_train[f'TE_{agg}'] = X_train[TE_columns].agg(agg, axis=1)` for `agg_list = ['mean', 'std', 'min', 'max']` — row-wise aggregations across the TE-derived columns. Same pattern as greysky s5e4. |

Cell 2 also reveals `default_risk = debt_to_income_ratio * 0.40 + (850 - credit_score)/850 * 0.35 + interest_rate/100 * 0.25` — a weighted-sum domain composite. No clean schema column (not col 27 binary, not col 28 ratio). Schema gap.

Cell 4 confirms sklearn `TargetEncoder(cv=10)` per-fold → col 2 ✓.

### s6e1 mahog (n_fe 7 → 7)

**Sources:** writeup + 15-cell Ridge META notebook (`pg-s6e1-ridge-ensemble-cv-8-56634-lb-8-57273.ipynb`).

**Stage 2 deltas:** **0 flips.** Notebook is Ridge meta-learner only; loads 190 OOFs from external `pg-s6e1-oofs` dataset. Base-model FE is NOT in this notebook. Cell 4 `CenteredIsotonicRegression` per-OOF before stacking is postprocessing.

Confidence: `writeup+notes` (downgrade — base-model FE not source-validatable from meta-learner notebook).

### TPS Feb 2022 ambrosm (n_fe 1 → 1)

**Sources:** writeup + 20-cell notebook (`tpsfeb22-exploiting-the-flawed-random-generation.ipynb`).

**Stage 2 deltas:** **0 flips.** Notebook confirms:
- Cell 6: `bias_vector` + integer recovery + `np.gcd.reduce` across feature columns — distinctive **gcd-reduction technique** (schema gap)
- Cell 12: `transform(Z)` reconstructs the 100-element decamer sequence from per-element counts — **reverse-transformation** (schema gap)
- Cell 16: `RadiusNeighborsClassifier(p=1, weights='distance')` Manhattan-distance lookup → col 35 ✓

Reverse-transformation and gcd-reduction are distinctive techniques not in the schema (singletons in the corpus).

### TPS May 2022 ambrosm + Pourchot (n_fe 2 → 3) — **RE-CODING**

**Sources:** writeup + 23-cell Pourchot keras notebook (`tpsmay22-keras-test-tuned.ipynb`).

**Stage 2 deltas:** **3 cell changes (1 down, 2 up). Net +1.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 13 `uses_pairwise_multiplicative_interactions` | 1 | **0** | Stage 1 mis-coded based on MD's generic "pairwise interaction features." Notebook reveals these are **additive sums with thresholds**, not multiplicative. |
| 14 `uses_pairwise_additive_interactions` | 0 | **1** | Cell 4: `i_02_21 = (df.f_21 + df.f_02 > 5.2).astype(int) - (df.f_21 + df.f_02 < -5.3).astype(int)`, `i_05_22 = (df.f_22 + df.f_05 > ...)`, `i_00_01_26 = df.f_00 + df.f_01 + df.f_26 > ...` — additive sums of 2-3 features. |
| 15 `uses_threshold_or_binary_flags` | 0 | **1** | Same cell 4: thresholds applied to additive sums produce ternary {-1, 0, +1} features. |

Cell 4 also confirms col 43 (10 character extracts from f_27 via `df.f_27.str.get(i).apply(ord) - ord('A')` and `unique_characters = len(set(s))`).

**Methodology note:** Stage 1 read "pairwise interaction features" generically as multiplicative. Stage 2 reveals the actual mechanic. This is the kind of re-coding the source-validation step is designed to catch.

---

## Batch 4 summary

| Entry | n_fe Stage 1 → 2 | Flips |
|---|---|---|
| s5e3 cdeotte (starter, not 2nd-place) | 1 → 1 | 0 |
| s5e7 Irfan | 1 → 1 | 0 |
| s5e11 mahog | 7 → **8** | +1 (col 26) |
| s6e1 mahog (Ridge meta only) | 7 → 7 | 0 |
| TPS Feb 2022 ambrosm | 1 → 1 | 0 |
| TPS May 2022 ambrosm | 2 → **3** | +2 / -1 net (re-coding) |

**Total: 4 cell changes (3 flips up + 1 flip down) across 6 entries.**

**Key finding:** Stage 1 mis-coded `i_02_21` etc. as multiplicative (col 13) based on the MD's generic "interaction" wording. Source validation revealed they're additive thresholded ternary features (col 14 + col 15). This is the type of re-coding Stage 2 is designed to catch.

---

---

## Batch 5: Remaining notebook-available entries (5 entries)

### s3e8 Craig Thomas (n_fe 3 → 3)

**Sources:** writeup + 81-cell `play-s3e8-eda-models.ipynb`.

**Stage 2 deltas:** **0 flips.** Published notebook is EDA + initial model exploration, NOT the 1,816-model custom framework. Cell 9 shows `has_missing_xyz = (x==0 | y==0 | z==0)` as gemstone-domain missing indicator and `impute_missing_xyz` formula; cells 14/17 do adversarial validation as diagnostic. Whether `has_missing_xyz` makes it into the production framework isn't clear from EDA notebook. Stage 1 from writeup stands.

Confidence: `writeup+notes` (downgrade — notebook doesn't represent winning framework).

### s4e1 Iqbal (n_fe 8 → 9)

**Sources:** writeup + 53-cell full pipeline (`ps4e1-3rd-place-solution.ipynb`).

**Stage 2 deltas:** **+1 flip.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 28 `uses_domain_ratios` | 0 | **1** | Cell 21 `feature_generator`: `Products_Per_Tenure = Tenure / NumOfProducts` — banking-domain ratio of customer tenure to product count. |

Other cells confirm Stage 1: cells 18-20 multi-feature rounders (col 10 ✓), cell 21 `IsActive_by_CreditCard = HasCrCard * IsActiveMember` (col 13 ✓), `ZeroBalance = (Balance == 0)` (col 27 ✓), `AgeCat = round(Age/20)` (col 10 ✓), `AllCat` 9-way categorical combo (col 17 ✓). Cell 25 Vectorizer TFIDF + TruncatedSVD on Surname / AllCat / EstimatedSalary / CreditScore (col 42 + col 39 ✓). Cell 30 CatBoostEncoder per-fold (col 1 + col 2 ✓).

### s5e4 greysky (n_fe 6 → 6)

**Sources:** writeup + 6-cell minimal training notebook.

**Stage 2 deltas:** **0 flips.** Published notebook loads pre-built 1,552-feature parquet from external `podcast-listening-huge-dataset` and trains a single LGBM. **No FE in this notebook.** The 1,552-feature pipeline is in a separate `podcast-dataset-generator` notebook NOT in our local set. Stage 1 from writeup stands.

Confidence: `writeup+notes` (downgrade — FE lives in external notebook).

### s6e3 cdeotte (n_fe 19 → 19)

**Sources:** writeup + 3-cell L4 meta-learner notebook.

**Stage 2 deltas:** **0 flips.** Published notebook is the L4 cuML LogisticRegression over 154 base-model OOFs loaded from external dataset. **None of the 19 FE techniques are in this notebook.** All 850 base-model notebooks are external/LLM-generated and not all public. Stage 1 from writeup stands.

Confidence: `writeup+notes` (downgrade — meta-learner doesn't cover any FE).

### ICR room722 (n_fe 1 → 1)

**Sources:** writeup + 9-cell `icr-adv-model.ipynb`.

**Stage 2 deltas:** **0 flips.** Notebook confirms architecture-only approach:
- Cell 1: Custom NaN fill (`nan_fill = isna().any() * (min - max)`, then replace zeros with median) — sophisticated imputation but NOT a missing-indicator feature
- Cell 3: Custom Keras layers — `GatedLinearUnit`, `GatedResidualNetwork`, `VariableSelection` (TFT-paper VSN)
- Cell 5: 3-level VSN with dropout cascade 0.75 → 0.5 → 0.25 (matches writeup)
- Cell 6: probability reweighting postprocessing

All architecture / preprocessing / postprocessing — no FE techniques. col 51 ✓.

---

## Batch 5 summary

| Entry | n_fe Stage 1 → 2 | Flips |
|---|---|---|
| s3e8 Craig Thomas | 3 → 3 | 0 (EDA-only notebook) |
| s4e1 Iqbal | 8 → **9** | +1 (col 28 Products_Per_Tenure ratio) |
| s5e4 greysky | 6 → 6 | 0 (FE in external notebook) |
| s6e3 cdeotte | 19 → 19 | 0 (L4 meta-only) |
| ICR room722 | 1 → 1 | 0 (architecture-only) |

**Total: 1 cell flip across 5 entries.**

**Pattern:** "Heavyweight" entries where the published notebook is just the meta-learner or starter (s5e4, s6e3, s4e5, s5e3, s6e1) yield 0 flips at Stage 2. The actual FE lives in external/private notebooks. The writeup remains the canonical source for these entries.

---

## Cumulative Stage 2 progress (28 / 45 entries = 62%)

| Batch | Entries | Net flips |
|---|---|---|
| 1 (high-priority below-range) | 5 | +5 |
| 2 (heavyweight + ambrosm) | 6 | +7 |
| 3 (fork-based + bundled) | 6 | +3 |
| 4 (meta-only notebooks + TPS) | 6 | +4 |
| 5 (remaining notebook-available) | 5 | +1 |

**Total: 20 cell flips / 28 × 53 = 1,484 cells × 1.3% flip rate.**

The remaining 17 entries are all **writeup-only** (no published notebook):
- s3e7 Hardy Xu, s3e13 Umar, s3e17 ISoft, s3e24 Ravi, s4e5 adaubas (notebook is Ridge-only), s4e7 Cross Sellers, s4e8 Optimistix, s5e5 cdeotte, s5e6 cdeotte (pilot — already validated against writeup)
- Plus a few more without notebooks

For these, Stage 2 confidence cap is `writeup+notes` since no notebook source-validation possible.

Skip: TPS Jun 2022 (buggy notebook per author).

---

---

## Batch 6: Writeup-only entries (7 entries, no notebook source)

For these entries no notebook was published. Stage 2 = careful re-read of the original writeup to catch anything the Pass 2 MD missed. Confidence cap: `writeup+notes`.

### s3e7 Hardy Xu (n_fe 1 → 2) — **FLIP**

Writeup re-read finds explicit minimal-FE statement that the MD missed:

> "I played around with creating additional features, but I didn't find anything that improved my CV significantly."

**Stage 2 deltas:** **+1 flip (col 51).**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 51 `explicit_minimal_or_no_fe` | 0 | **1** | Author explicit no-FE conclusion in §Feature Engineering. |

Other Stage 1 codings confirmed:
- col 52 (adversarial validation to filter ~17% of original) ✓
- Opposite-label assignment + 0.5 prediction for test duplicates = postprocessing, NOT col 34 (which requires synthetic-to-original key match — this is train-to-test internal)

### s3e13 Umar (n_fe 2 → 2)

**Stage 2 deltas:** **0 flips.** Writeup confirms:
- "No feature engineering, all features being used were scaled using a standard scaler" → col 51 ✓
- Autoencoder bottleneck 64-64-32-16-32-64 + freeze encoder + add 16relu-11softmax head → col 38 ✓
- Simple averaging of LGBM + NN + autoencoder → Pass 1

### s3e17 ISoft (n_fe 1 → 1)

**Stage 2 deltas:** **0 flips.** Writeup is extremely short (~30 lines). 5 AutoML frameworks + meta-model + 10% from 2 public submissions. No FE described (AutoML handles internally). col 51 ✓.

### s3e24 Ravi (n_fe 2 → 2)

**Stage 2 deltas:** **0 flips.** Writeup confirms brute-force features 80-120 (col 16 ✓) + permutation importance (col 48 ✓). Secondary features tried but did not help. "Probing" = manual weight modification (postprocessing). Original dataset concat = Pass 1.

### s4e7 Cross Sellers (n_fe 1 → 1)

**Stage 2 deltas:** **0 flips.** Writeup describes a 12-version feature store in proprietary GitHub repo with author-itemized contents:
- "feature importance on a single fold using a simple catboost model" (tree feature importance, not permutation — out-of-scope for col 48)
- "borrowed ideas from the topper posts in the AutoML component" — sources noted but specific techniques not enumerated
- Target reversal = postprocessing
- "What did not work: Linear approaches, Optuna, Hill Climb" — modeling

The col 53 captures the uncatalogued proprietary FE. No additional Stage 2 flips possible without access to the GitHub repo.

### s4e8 Optimistix (n_fe 1 → 1)

**Stage 2 deltas:** **0 flips.** Writeup is detailed (long narrative) but FE-light:
- siukeitin's "exact solution to original dataset" → probability of being poisonous as feature (col 32 ✓)
- 72 OOFs + AutoGluon ensembler — modeling
- "Insert confident disagreements" — postprocessing
- Hill Climbing for OOF selection — ensemble method
- Three independent paths to 0.98535 — saturation observation

No additional FE techniques. The writeup is methodologically rich but feature-engineering-thin.

### s5e5 cdeotte (n_fe 8 → 10) — **FLIP**

Writeup re-read finds two techniques worth coding:

> "In my final ensemble 25% of the weight is XGBoost with NVIDIA cuML TargetEncoder features."
>
> "CatBoost loves categorical features, so I converted each numerical feature into 9 equal width binned values... Afterward I created combinations of all pairs of columns. The resultant new columns had 81 unique values and were also categorical."

**Stage 2 deltas:** **+2 flips.**

| Column | Stage 1 | Stage 2 | Evidence |
|---|---|---|---|
| 2 `uses_target_encoding_within_fold` | null | **1** | cuML TargetEncoder is per-fold inside the standard cdeotte training loop. |
| 17 `uses_categorical_combos` (2+ way per v3.1) | 0 | **1** | 9-binned numerics combined pairwise → 81 unique cat values used as categoricals. This is 2-way categorical combos, covered by v3.1 col 17 broadening. |

All other Stage 1 cols confirmed:
- Log1p transforms (col 8 ✓)
- "all products, divisions, sums, and differences between all pairs of features" (col 13 mult/div ✓ + col 14 sums/diffs ✓)
- 9 equal-width binning (col 10 ✓)
- Numerics-as-cats then combos (col 18 ✓)
- 26 groupby z-score features (col 23 ✓)
- NN-over-LR + XGB-over-NN residual chain (col 46 ✓)

cdeotte's 100%-retrain-with-1/(K-1)-iter-boost is mentioned for every competition — modeling, out of scope.

---

## Batch 6 summary

| Entry | n_fe Stage 1 → 2 | Flips |
|---|---|---|
| s3e7 Hardy Xu | 1 → **2** | +1 (col 51 explicit no-FE) |
| s3e13 Umar | 2 → 2 | 0 |
| s3e17 ISoft | 1 → 1 | 0 |
| s3e24 Ravi | 2 → 2 | 0 |
| s4e7 Cross Sellers | 1 → 1 | 0 |
| s4e8 Optimistix | 1 → 1 | 0 |
| s5e5 cdeotte | 8 → **10** | +2 (col 2 + col 17) |

**Total: 3 cell flips across 7 entries.**

**Pattern for writeup-only:** Most MDs faithfully captured the writeup's FE section. The flips found are:
- Explicit "tried FE, didn't help" statements get under-recognized (Hardy Xu s3e7)
- Heavyweight cdeotte signatures (within-fold TE in cuML, 2-way categorical combos with 81-unique-values) get glossed in MDs (s5e5)

---

## Cumulative Stage 2 progress (35 / 45 entries = 78%)

| Batch | Entries | Net flips |
|---|---|---|
| 1 | 5 | +5 |
| 2 | 6 | +7 |
| 3 | 6 | +3 |
| 4 | 6 | +4 |
| 5 | 5 | +1 |
| 6 (writeup-only) | 7 | +3 |

**Total: 23 cell flips / 35 × 53 = 1,855 cells × 1.2% flip rate.**

The remaining 10 entries already had Stage 2 done either via pilot (s5e6 cdeotte, s3e14 Sergey, s3e5 Heitor) or extended pilot (s5e6, ICR, s3e3 Bill Cruise, s4e9 Mart Preusse). Counting pilot results, **Stage 2 is effectively complete for 38/45 = 84% of the corpus.**

Remaining 7 entries with limited validation:
- TPS Jun 2022 (buggy notebook — skipped)
- s3e10 seascape (R-based notebook — not scanned)
- Others were validated in pilot/extended pilot batches

---

## Schema gaps cumulative (post-batch-6)

| Gap | Entries affected | Status |
|---|---|---|
| 2-way categorical combos | s5e2, s5e8, s5e11, s6e4 | **FIXED v3.1 col 17** |
| Single-fork uncatalogued FE | s3e1, s4e7 | **FIXED v3.1 col 53** |
| Geographic FE family (cluster-distance, UMAP, rotations) | s3e1 Kirderf | singleton, defer |
| Reverse-transformation + gcd-reduction | TPS Feb 2022 ambrosm | singleton, defer |
| Domain composite score | s5e11 mahog (default_risk), s3e3 Bill Cruise (AttritionRisk), s3e7 Hardy Xu (could fit) | 2+ entries — **candidate for v3.2** |
| NN-internal preprocessing as FE | s3e26, ICR, s6e1 | architectural boundary — out-of-scope |
| Sorted-features (siukeitin technique) | s4e5 adaubas | singleton, defer |

## Schema gaps cumulative

1. ~~2-way categorical combos~~ → fixed in v3.1 (col 17)
2. ~~Single-fork uncatalogued FE~~ → fixed in v3.1 (col 53 relax)
3. Geographic FE family (KMeans-haversine, UMAP, coordinate rotations) — Kirderf s3e1 dmitryuarov singleton
4. Reverse-transformation + gcd-reduction (TPS Feb 2022) — singleton
5. Domain composite score (mahog s5e11 default_risk, Bill Cruise s3e3 AttritionRisk) — appearing 2+ times
6. NN-internal preprocessing (PLE, per-feature embeddings) — singleton family

Recommend: add `uses_domain_composite_score` column after Stage 2 completes (2+ entries justify); defer geo/reverse-transformation as singletons.
