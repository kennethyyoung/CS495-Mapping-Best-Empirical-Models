# Pass 3 FE Taxonomy — Schema (v3, post-pilot)

**Status:** Locked after 3-entry pilot.
**Branch:** `phase9/fe-taxonomy`.
**Author:** Kenneth Young.
**Date:** 2026-05-28.

This document defines the structured-coding schema for Pass 3 — the FE taxonomy that unlocks "what feature engineering do winners use?" as a queryable question. **v2 leaned toward more granular columns because aggregating up is easy and disaggregating after the fact is expensive.** A second coder revisiting `uses_target_encoding = TRUE` cannot tell whether it was vanilla TE or within-fold TE without re-reading the writeup. v2 separated these at the source.

**v3 changes from v2 (after pilot, see `PILOT.md`):**

1. Added column 53 `uses_forked_base_model_fe_uncatalogued` — flag fork-heavy entries where base-model FE isn't documented in the winner's writeup.
2. Clarified column 2 (within-fold TE) — allow `null` for entries where the writeup doesn't specify and no notebook is available. Three-valued boolean rather than two-valued.
3. Clarified column 16 (brute-force combinatorial search) — **must include a model-in-the-loop selection step**. Pure enumeration without selection is not brute-force.
4. Clarified column 17 (higher-order categorical combos) — covers enumeration with or without selection. If a brute-force selection step is present, ALSO mark column 16.
5. Clarified column 18 (numerics-as-cats then combos) — applies only when features were originally numeric (int/float) and converted, not when features were already categorical-typed.
6. Updated expected `n_fe_techniques_used` ranges per paradigm to match what the pilot observed — the schema captures FE technique *diversity*, not feature *count*. A 2,268-feature monster model uses ~7 distinct techniques.

## Design philosophy

1. **Boolean columns over free text.** Every category is TRUE or FALSE for each of the 45 entries. Avoids the 166-unique-tags problem the Pass 1 `fe_techniques` field has.
2. **Prefer granularity at the source.** If two techniques have meaningfully different implementations or implications (vanilla TE vs within-fold TE), they get separate columns. We can OR them into a coarser category later for cross-tabs; we can't split a TRUE cell into two without re-reading. **52 boolean technique columns in v2.**
3. **Clear inclusion criteria per column.** Each column has explicit "includes" and "excludes" rules with concrete examples from the corpus, so any second coder could replicate.
4. **Single-author-specific columns are acceptable.** If only cdeotte uses histogram-binned groupby, that's a measured fact worth structuring. "0 entries in the corpus use technique X except cdeotte" is itself a finding.
5. **In scope: feature engineering only.** Pre-modeling transformations of input features. NOT in scope: post-processing of model outputs, CV strategy, ensemble methods, hyperparameter tuning, model architecture choices.
6. **`pass3_source_confidence` column** explicitly tracks which sources were consulted for each row. Lets us measure the generational-drift concern (notebook+writeup = high; notes-only = low).
7. **Layered source strategy.** Stage 1 codes from Pass 2 MDs as a starting checklist. Stage 2 source-validates against original writeup + notebook. Stage-1-to-Stage-2 delta is itself a methodological finding.

## Boolean technique columns (52)

### Group A — Categorical encoding (7)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 1 | `uses_target_encoding_basic` | Single-statistic mean target encoding applied to one or more categorical columns. Vanilla "replace category with mean of target." | Multiple-statistic TE (next column). Within-fold leakage-safe TE (column 2). |
| 2 | `uses_target_encoding_within_fold` | Leakage-safe TE explicitly computed inside the CV loop (nested-fold target-aware FE; per-fold TE; "leakfree" TE). Iqbal s4e1; cdeotte signature. Three-valued: TRUE if explicitly stated in writeup or visible in notebook; FALSE if explicitly stated as globally-applied; **`null` if ambiguous** (writeup-only entries where author doesn't specify). | Vanilla TE applied to full training data (column 1). |
| 3 | `uses_te_multiple_aggregations` | Multiple TE statistics per categorical column (mean + median + min + max + std + nunique + skew). cdeotte's 7-encoding pattern. | Single TE statistic. |
| 4 | `uses_te_alternative_targets` | TE using a non-target column as the target. mahog s5e11 TE on `employment_status` and `debt_to_income_ratio`. | Standard TE on competition target. |
| 5 | `uses_count_encoding` | Replacing each category with its raw count in the training set. | Frequency encoding (next column — normalized to 0–1). |
| 6 | `uses_frequency_encoding` | Replacing each category with its normalized frequency (count / total). | Raw count encoding (previous column). |
| 7 | `uses_missing_indicator_features` | Encoding the *pattern* of missing values as a feature. cdeotte s5e2 NaN-base-2 bitstring; or per-column `is_missing` boolean features added. | Simple imputation (covered by Pass 1 `missing_data_strategy`). |

### Group B — Numeric transformations (5)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 8 | `uses_log_transform` | `log`, `log1p`, `log10` applied to feature columns. | Target log-transform only (modeling choice). |
| 9 | `uses_power_or_polynomial_transform` | `sqrt`, square, cube, higher powers, Box-Cox, Yeo-Johnson applied to feature columns. | Cross-feature polynomial interactions (covered by Group C). |
| 10 | `uses_binning_discretization` | Equal-width, quantile, or custom-threshold binning of a numeric column. Then treating bins as categorical or numeric. | Binning the *target* (modeling/CV choice). |
| 11 | `uses_digit_features` | Extracting individual digits from a numeric column as separate features. cdeotte float-position digits; mahog s5e11 digit interactions; ambrosm tps-feb-2022 decamer-count digits. | Casting numeric to integer. |
| 12 | `uses_rounding_multi_precision` | Rounding the same numeric column at multiple precisions then using each as features or groupby keys. cdeotte signature; greysky s5e4. | Single rounding step as preprocessing. |

### Group C — Interactions and combinatorial (6)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 13 | `uses_pairwise_multiplicative_interactions` | Hand-coded `a*b`, `a/b`, `a%b` between specific feature pairs. Mart Preusse `MonthlyIncome/Age`; gemstone aspect-ratio × carat. | Systematic enumeration (column 16). |
| 14 | `uses_pairwise_additive_interactions` | Hand-coded `a+b`, `a-b` between specific feature pairs. | Sums across many features at once (rowwise stats — column 26). |
| 15 | `uses_threshold_or_binary_flags` | Rule-based binary features: `(a > threshold)`, `(a > x) & (b > y)`. Bill Cruise s3e3 HR risk flags; adaubas s4e5 count-thresholds. | Domain-knowledge binary flags (Group E). |
| 16 | `uses_brute_force_combinatorial_search` | Systematic enumeration of feature combinations **with a model-in-the-loop selection step** (search and keep best). cdeotte s4e12 145K combos → 170 kept; arunklenin's brute-force at s3e24. | Hand-picked combos (columns 13–15). **Pure enumeration without selection** (cdeotte s5e6 uses all 162 combos without filtering) → use column 17 only. |
| 17 | `uses_higher_order_categorical_combos` | 3+ way categorical groupings (3 or more columns combined into one composite), with or without further TE/CE on top. cdeotte 2–6-way combos. Covers enumeration with or without selection — **if a brute-force selection step is also present, mark column 16 TRUE in addition**. | Pairwise (2-way) only. |
| 18 | `uses_numerics_as_categoricals_then_combos` | Treating a column that was **originally numeric (int/float)** as categorical (via binning or direct conversion) then combining with other features for combinatorial FE. cdeotte s4e12 numerics-as-cats + TE/CE pattern. | Plain numerics combined with plain numerics. **Does NOT apply when features were already categorical-typed** (e.g., string columns like Soil Type) — those are coded under columns 16/17 directly. |

### Group D — Aggregates and groupby (8)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 19 | `uses_groupby_basic_stats` | groupby + mean / median / std / min / max within a group. | Count / nunique (next column). Quantiles (column 21). |
| 20 | `uses_groupby_count_or_nunique` | groupby + count / nunique within a group. | Basic stats (previous column). |
| 21 | `uses_groupby_quantiles` | Multiple quantile values computed within groups as features (e.g., cdeotte `QUANTILES = [5,10,40,45,55,60,90,95]`). | A single percentile = covered by basic stats. |
| 22 | `uses_groupby_histogram_bins` | cdeotte's histogram-bin counts within groups (groupby + count of values in each of N bins). Distinctive cdeotte invention. | Standard groupby aggregates. |
| 23 | `uses_groupby_zscores` | Within-group standardization (subtract group mean, divide by group std) used as features. cdeotte s5e5 groupby z-scores; tilii s5e10. | Standard mean/std (covered by basic stats). |
| 24 | `uses_groupby_skew_or_higher_moments` | groupby skew, kurtosis, or other higher moments. | Mean/std (covered). |
| 25 | `uses_groupby_division_of_aggregates` | Second-order combinations of already-aggregated features (`count / nunique`, `std / count`). cdeotte s5e2. | Plain ratios between raw features (column 13). |
| 26 | `uses_rowwise_statistics` | sum / mean / std / max / min / count-above-threshold computed *across* multiple feature columns *within a row*. Viable when features commensurable. adaubas s4e5 Poisson-sum row-stats; oscarm524 log-transformed row stats. | Groupby aggregates (different axis). |

### Group E — Domain / temporal / structural (5)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 27 | `uses_domain_binary_flags` | Hand-crafted binary features that require domain knowledge. Bill Cruise s3e3 (Age<34, JobHopper). | Threshold flags computed without domain interpretation (column 15). |
| 28 | `uses_domain_ratios` | Domain-meaningful ratios (anatomical, financial, quality). Ravi s3e16 meat-yield, pseudo-BMI; Craig s3e8 aspect-ratio. | Generic pairwise ratios without domain rationale (column 13). |
| 29 | `uses_domain_ordinal_scales` | Encoding a categorical column to a domain-ordered numeric scale (gemstone clarity D→J, education levels). Craig s3e8 gemstone quality. | Generic label encoding without domain ordering. |
| 30 | `uses_datetime_decomposition` | Year / month / day / weekday / day-of-year / hour extracted from datetime columns. cdeotte s4e12 Policy Start Date. | Cyclical sin/cos encoding (next column). |
| 31 | `uses_cyclical_encoding` | sin / cos encoding of cyclical features (day-of-week, month, hour). mahog s5e8 yekenot cyclical features. | Plain datetime decomposition. |

### Group F — External-original-derived features (6)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 32 | `uses_original_target_mean_as_feature` | Simple mean of the external-original target computed per category and attached to the synthetic training data. | Smoothed / WoE / entropy variants (next column). |
| 33 | `uses_original_target_advanced_stats` | Smoothed mean, Weight of Evidence (WoE), entropy, log-odds from external-original target. masaya s6e2. | Plain mean (previous column). |
| 34 | `uses_exact_key_match_lookup` | Deterministic merge on a feature-tuple key joining synthetic to original. Sergey s3e14 `(fruitset, fruitmass)`; Irfan s5e7 `match_p`. | Approximate nearest-neighbor (next column). |
| 35 | `uses_approximate_neighbor_lookup` | KDTree, BallTree, FAISS, or other approximate nearest-neighbor lookup from synthetic to original; attaching neighbor's properties as features. cdeotte s6e3 cKDTree snap. | Exact key match (previous column). |
| 36 | `uses_drift_features` | Features measuring the difference / ratio between dataset distributions (train vs original). cdeotte s6e3 drift ratios. | Plain comparisons without distribution interpretation. |
| 37 | `uses_distribution_anomaly_features` | Benford's law deviation, statistical anomaly scores, distributional fingerprints. cdeotte s6e3 Benford. | Generic statistical features. |

### Group G — Learned / advanced derived (4)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 38 | `uses_autoencoder_latents` | DAE / VAE / Variational Autoencoder encoder outputs used as input features for a downstream model. Umar s3e13 frozen-encoder-as-classifier; tilii s5e10; masaya s6e2 DVAE. | DAE as the prediction model itself (e.g., for imputation). |
| 39 | `uses_pca_svd_components` | PCA / Truncated SVD / Kernel PCA components used as features. Iqbal s4e1 TF-IDF + SVD. | Random projection (next column). |
| 40 | `uses_random_projection_features` | Gaussian random projection (GRP), sparse random projection used as features. cdeotte s6e3 GRP on IBM original. | Linear dim reduction (previous column). |
| 41 | `uses_genetic_programming_features` | Symbolic-regression / GP-derived features (gplearn library). tilii s5e10 11 GP features at ensemble stage; masaya s6e2 gplearn. | Other nonlinear FE. |

### Group H — Text and string-pattern (3)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 42 | `uses_tfidf_features` | TF-IDF representations of a string column. Iqbal s4e1 Surname-as-text. | High-cardinality categorical encoded categorically. |
| 43 | `uses_character_or_string_pattern_features` | Character n-grams, substring extraction, length-of-string, regex pattern extraction. Mart Preusse s4e9 engine-string parsing for horsepower/displacement. | Plain TF-IDF (previous column). |
| 44 | `uses_lasso_generator_recovery` | Using a Lasso regression diagnostically to reverse-engineer the synthetic-data generator's target formula. tilii s5e10. | Lasso used as a base model. |

### Group I — Model-derived as features (3)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 45 | `uses_pseudo_labels_as_features` | Predicting test labels with one model, then attaching those predicted labels as features for another model. cdeotte s5e6 "pseudo-label COLUMNS" variant. | Pseudo-labels for training-set augmentation (modeling choice). |
| 46 | `uses_residual_features` | Residuals from one model used as features (or as targets) for the next model. cdeotte s5e5 residual chain (NN over LR residuals, XGB over NN residuals); s5e6 boosting over LR margin. | Plain stacking without residual structure. |
| 47 | `uses_outlier_or_aux_classifier_as_feature` | Training a classifier on an auxiliary target (outlier flag, IQR bin, category derived from rules), then using its OOFs as features for the main regressor. Mart Preusse s4e9 outlier-bin CatBoost classifier → OOF as feature. | Plain stacking. |

### Group J — Feature selection (3)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 48 | `uses_permutation_importance_selection` | Permutation importance used to rank and prune features. Ravi s3e24; viktortaran s3e6. | Other selection methods (next columns). |
| 49 | `uses_sfs_or_backward_elimination` | Sequential feature selection (SFS), backward elimination, or step-wise forward selection. adaubas s4e5 permutation + backward; stopwhispering s4e4 SFS per model. | Permutation importance only (previous column). |
| 50 | `uses_correlation_or_constant_dropping` | Dropping features by high pairwise correlation or near-zero variance. | Other selection (covered above). |

### Group K — Meta indicators (3)

| # | Column | Includes | Excludes |
|---|---|---|---|
| 51 | `explicit_minimal_or_no_fe` | Author explicitly states minimal or no FE was used, often as a deliberate choice. cdeotte s5e3 "small data → no FE"; Heitor s3e5 single XGB; ravaghi s4e11 "no FE." | Writeup that simply doesn't mention FE (missing data, not explicit minimal). |
| 52 | `uses_adversarial_validation_for_fe` | Adversarial validation (train classifier to distinguish train vs test, or synthetic vs original) used to filter features or filter rows. Hardy Xu s3e7 filter original; stopwhispering s4e4 adversarial-validation notebook. | Adversarial validation used only for diagnostic purposes. |
| 53 | `uses_forked_base_model_fe_uncatalogued` | Winner cites multiple forked public notebooks as base-model sources without enumerating the FE techniques used inside those notebooks. The winning ensemble *includes* those notebooks' FE but it isn't catalogued. Sergey s3e14 (8 forked base OOFs); Moonlit s4e3 (3 OOFs from public notebooks). Flag-only — doesn't double-count the techniques as TRUE in other columns. | Winner who cites one forked notebook AND describes its FE in detail (those techniques get coded individually). |

## Source-confidence column (1)

| Column | Allowed values | Definition |
|---|---|---|
| `pass3_source_confidence` | `notebook+writeup` / `writeup+notes` / `writeup-only` / `notes-only` | The basis on which the row was coded. `notebook+writeup` = highest confidence; both sources consulted. `writeup+notes` = original writeup file + Pass 2 MD. `writeup-only` = only writeup (no notebook published or pulled). `notes-only` = only Pass 2 MD (worst case; flag for follow-up). |

## Meta / admin columns (5)

| Column | Type | Purpose |
|---|---|---|
| `competition_ref` | string | Join key with Pass 1 and Pass 2. |
| `finish_rank` | int | Join key with Pass 1 and Pass 2. |
| `n_fe_techniques_used` | int | Derived: sum of TRUE values across the 52 technique columns. Answers "do single-model-FE wins use more techniques on average than ensemble-stacking wins?" |
| `pass3_notes` | string | Free-text per entry. Flags ambiguities, judgment calls, and "Pass 2 MD missed technique X" findings — those become Pass 2 corrections. |
| `pass3_date_coded` | date | When this row was finalized. Lets us track Stage 1 vs Stage 2 cells. |

**Sheet total: 53 boolean + 5 admin + 1 source-confidence = 59 columns × 45 rows = 2,655 cells.**

## Resolution of the v1 open questions

| v1 Open question | v2 resolution |
|---|---|
| Split `uses_target_encoding` into within-fold vs not? | **Split** — columns 1 and 2 are separate. |
| Is `uses_groupby_advanced` too vague? | **Split** — columns 19–25 break aggregates into 7 distinct columns instead of 1. |
| Add `uses_outlier_classification_as_feature`? | **Added** — column 47 (`uses_outlier_or_aux_classifier_as_feature`). |
| `uses_domain_features` too broad? | **Split** — columns 27–29: binary flags, ratios, ordinal scales. |
| Add `uses_explicit_feature_selection`? | **Added as 3 columns** — Group J (48–50): permutation, SFS/backward, correlation/constant. |
| Add `uses_residual_features`? | **Added** — column 46. |
| `uses_snap_or_kdtree_lookup` overlap with lookup paradigm? | **Split** — columns 34 and 35: exact key match vs approximate neighbor. Retained for granularity. |

## What's intentionally NOT in scope

- **Post-processing of model outputs.** OptimizedRounder, target reversal, probability calibration, threshold tuning. *Note: several distinctive corpus techniques fall here — Heitor s3e5 OptimizedRounder, Cross Sellers s4e7 target reversal — and won't be captured by the FE taxonomy. The schema is FE-specific by design.*
- **Cross-validation strategy.** Covered by Pass 1 `cv_strategy`.
- **Ensemble methods.** Covered by Pass 1 `ensemble_method`.
- **Hyperparameter tuning.** Covered by Pass 1 `hyperparameter_tuning`.
- **Model architecture choices.** Covered by Pass 1 `models_used`.
- **Pseudo-labeling for training data augmentation.** Distinct from `uses_pseudo_labels_as_features` (column 45), which is specifically pseudo-labels used *as features*.
- **Knowledge distillation.** Training-time technique.
- **Custom loss functions.** Modeling choice.

## Proposed workflow

**Stage 1 — Draft from Pass 2 MDs (~half day)**

1. Build the workbook sheet skeleton: create `FE Taxonomy` sheet in `data/kaggle_meta_analysis.xlsx` with the 58 columns above.
2. Read each of the 45 per-writeup MDs (`analysis/writeup-reevaluation/*.md`).
3. Code each row's 52 booleans based on the MD's "What's actually original" and "Dataset constraints" sections.
4. Set `pass3_source_confidence = notes-only` for every row at this stage.
5. Sanity check: compute `n_fe_techniques_used` distribution; flag entries with 0 or >15 for closer look.

**Stage 2 — Source-validate (~1–2 days)**

For each of the 45 entries:

1. Open the original writeup at `data/writeups/<slug>/<title>.txt`.
2. If a notebook exists at `data/writeups/<slug>/*.ipynb`, open it too.
3. Re-evaluate every TRUE/FALSE cell against the source material.
4. Add any techniques the MD missed (flip FALSE → TRUE).
5. Update `pass3_source_confidence` to `writeup+notes`, `notebook+writeup`, etc.
6. Record in `pass3_notes` any techniques added, with a tag like `[+from_writeup]` or `[+from_notebook]`.
7. Each "MD missed this" finding is also a Pass 2 audit signal — log them.

**Output deliverables**

- New `FE Taxonomy` sheet in `data/kaggle_meta_analysis.xlsx`
- Stage 1 → Stage 2 delta metric: how many cells flipped FALSE → TRUE during source validation, by category. This quantifies generational drift.
- New §4.9 paragraph in `research_report.md` describing FE-by-paradigm patterns (if the project extends).
- Possibly a heatmap figure: paradigm × FE category (boolean rate per cell).

## Pilot results (completed)

Pilot of 3 entries completed and documented in `PILOT.md`. Headline findings:
- **cdeotte s5e6** (heavyweight): 7 TRUE columns (expected 15–25, recalibrated to 6–12)
- **Sergey s3e14** (lookup): 1 TRUE column (matches recalibrated 1–4 range)
- **Heitor s3e5** (minimal-FE): 1 TRUE column (matches recalibrated 0–3 range)

**Key calibration finding:** the schema captures FE technique *diversity* (~5–12 for heavyweight wins), not FE feature *count* (which can be in the thousands). This is a feature of the schema, not a bug — it makes paradigm-level cross-tabs meaningful instead of dominated by cdeotte's 2,268-feature monster.

### Revised expected `n_fe_techniques_used` ranges per paradigm

| Paradigm | Expected range |
|---|---|
| Ensemble-stacking heavyweight (cdeotte s4e12 / s5e2 / s5e6 / s6e3) | 6–12 |
| Ensemble-stacking standard (most s3/s4/s5 winners) | 4–9 |
| Single-model heavy-FE | 8–15 |
| Lookup-exploit | 1–4 |
| Problem-fit NN | 2–6 |
| Community-template-tweak | 3–7 |
| Minimal-FE (explicit) | 0–3 |

Entries that fall well outside these ranges during the full pass are flags for re-examination — either a coding error or a methodologically interesting outlier.

## Aggregation paths (for later)

Because the schema is granular, several useful coarse groupings can be derived after coding:

- **`uses_any_target_encoding`** = columns 1 OR 2 OR 3 OR 4
- **`uses_any_groupby`** = columns 19 OR 20 OR 21 OR 22 OR 23 OR 24 OR 25
- **`uses_any_combinatorial_search`** = columns 16 OR (17 AND 18)
- **`uses_any_original_derived_feature`** = columns 32 OR 33 OR 34 OR 35 OR 36 OR 37
- **`uses_any_model_derived_feature`** = columns 45 OR 46 OR 47
- **`uses_any_explicit_selection`** = columns 48 OR 49 OR 50

Each of these is a one-line aggregate in pandas. So the granular schema doesn't preclude coarse analyses; it enables them.

---

**Next step:** react to the v2 schema. Flag any columns that should still split / merge / drop / add. Once the schema is locked, we pilot the 3 representative entries, then code the full 45.
