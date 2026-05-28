# Pass 3 FE Taxonomy — Schema Proposal

**Status:** Draft for review.
**Branch:** `phase9/fe-taxonomy`.
**Author:** Kenneth Young.
**Date:** 2026-05-28.

This document proposes the structured-coding schema for Pass 3 — the FE taxonomy that unlocks "what feature engineering do winners use?" as a queryable question. React to anything that feels mis-bucketed, missing, or over-granular before any coding work begins.

## Design philosophy

1. **Boolean columns over free text.** Every category is TRUE or FALSE for each of the 45 entries. This makes cross-tabs trivial and avoids the 166-unique-tags problem the Pass 1 `fe_techniques` field has.
2. **~20–25 categories total.** Too few and everything is `uses_target_encoding`; the schema can't distinguish paradigms. Too many and most cells are FALSE; sparsity returns. 24 boolean technique columns feels like the sweet spot.
3. **Clear inclusion criteria per category.** Each column has an explicit "what counts" and "what doesn't count" rule so any second coder could replicate.
4. **In scope: feature engineering only.** Pre-modeling transformations of input features. NOT in scope: post-processing of model outputs (OptimizedRounder, target reversal, calibration), CV strategy, ensemble methods, hyperparameter tuning.
5. **`pass3_source_confidence` column** explicitly tracks which sources were available for each entry (notebook + writeup is highest confidence; writeup-only is lowest). Lets us measure the generational-drift concern.
6. **Layered source strategy.** Stage 1 codes from Pass 2 MDs as a starting checklist. Stage 2 source-validates against the original writeup + notebook. The delta between Stage 1 and Stage 2 is itself a methodological finding.

## Boolean technique columns (24)

Listed with rough functional groups for readability. The actual sheet will have all 24 as siblings.

### Group A — Categorical encoding (4 columns)

| Column | Includes | Excludes |
|---|---|---|
| `uses_target_encoding` | Any form of target-mean encoding: vanilla TE, smoothed TE, M-estimate, CatBoost encoder (when explicitly applied as preprocessing), within-fold leakage-safe TE. | CatBoost's internal handling of categoricals when it's just the model's default behavior with no explicit encoder choice. Ordinal/label encoding. |
| `uses_te_multiple_aggregations` | Multiple TE statistics per column (mean + median + min + max + std + nunique + skew). cdeotte's signature 7-encoding pattern is the canonical example. | A single TE statistic (mean only). One alternative aggregation alone (e.g., median-only TE). |
| `uses_te_alternative_targets` | TE using a non-target column as the target — e.g., mahog's s5e11 TE on `employment_status` and `debt_to_income_ratio` instead of the actual `loan_payback` target. | Standard TE on the competition target. Auxiliary classifiers whose OOFs become features (that's a different category). |
| `uses_count_or_frequency_encoding` | Count encoding (replace category with its frequency). Frequency-as-feature. | One-hot encoding. Label encoding. |

### Group B — Numeric transformations (4 columns)

| Column | Includes | Excludes |
|---|---|---|
| `uses_log_or_power_transform` | `log1p`, `log`, `sqrt`, square, cube, Box-Cox, Yeo-Johnson applied to feature columns. | Log transform of the *target* only (that's a metric/target choice, not FE). |
| `uses_binning_discretization` | Equal-width binning, quantile binning, custom-threshold binning, then treating the bins as categorical or numeric features. | Binning the *target* (e.g., target binning for stratified CV — that's a CV choice). |
| `uses_digit_features` | Extracting individual digits from a numeric column as separate features. cdeotte float-position digits; mahog `s5e11` digit interactions. | Single integer-cast of a float. |
| `uses_rounding_multi_precision` | Rounding the same numeric column at multiple precisions (e.g., `round(x, 0)`, `round(x, 1)`, `round(x, 2)`) then using each as features or groupby keys. cdeotte signature. | Single rounding step as part of normal preprocessing. |

### Group C — Interactions and combinatorial (3 columns)

| Column | Includes | Excludes |
|---|---|---|
| `uses_manual_pairwise_interactions` | Hand-coded specific interactions: `a*b`, `a/b`, `a+b`, `a-b`, `(a > threshold) & (b > threshold)`. Bill Cruise s3e3 `risk_flag`, Mart Preusse `MonthlyIncome/Age` ratio, gemstone aspect-ratio × carat. | Systematic enumeration of all pairs (that's the next column). |
| `uses_brute_force_combinatorial_search` | Systematic enumeration of feature combinations with a model-in-the-loop selection step. cdeotte s4e12 145K combinations → 170 kept; greysky 6-way TE combinatorics; arunklenin's brute-force at s3e24. | A few hand-picked pairs (that's the previous column). |
| `uses_higher_order_categorical_combos` | 3+ way categorical groupings (combining 3 or more columns into one composite category), with or without further TE/CE on top. cdeotte 2–6-way category combos. | Pairwise (2-way) combos only — those are covered by `uses_manual_pairwise_interactions` if hand-picked, or `uses_brute_force_combinatorial_search` if enumerated. |

### Group D — Aggregate / groupby features (4 columns)

| Column | Includes | Excludes |
|---|---|---|
| `uses_groupby_basic_aggregates` | groupby with mean / median / std / min / max / count / nunique within a group. The classic groupby pattern. | Row-wise statistics (across columns within a row) — that's a different column. |
| `uses_groupby_quantiles` | Multiple quantile values computed within groups as features (e.g., cdeotte's `QUANTILES = [5,10,40,45,55,60,90,95]`). | A single percentile (e.g., just the median) — that's covered by `uses_groupby_basic_aggregates`. |
| `uses_groupby_advanced` | Less-common groupby techniques: histogram-bin counts within groups (cdeotte invention), groupby z-scores, groupby skew, division-of-aggregations (`count/nunique`). | Standard groupby (covered by basic). Quantiles (covered separately). |
| `uses_rowwise_statistics` | sum / mean / std / max / min / count-of-nonzero / count-of-thresholds computed *across* multiple feature columns *within a row*. Viable when features are commensurable (same units). adaubas s4e5 Poisson-sum row-stats; tilii GP features. | Groupby aggregates (different axis). |

### Group E — Domain / structural / temporal (3 columns)

| Column | Includes | Excludes |
|---|---|---|
| `uses_domain_features` | Hand-engineered features that require domain knowledge of the problem area. Bill Cruise s3e3 HR risk flags (Age<34, JobHopper); Ravi s3e16 anatomical ratios (meat yield, pseudo BMI); Craig s3e8 gemstone aspect ratio. | Generic FE that doesn't need domain knowledge (digit features, pairwise interactions). |
| `uses_datetime_decomposition` | Extracting year / month / day / weekday / day-of-year / week-of-year / hour from date or datetime columns. cdeotte s4e12 Policy Start Date decomposition. | Cyclical encoding (sin/cos) — that's the next column. |
| `uses_cyclical_encoding` | Sin/cos encoding of cyclical features (day-of-week, month, hour-of-day) so the model sees continuous wrap-around. mahog s5e8 yekenot cyclical features. | Plain datetime decomposition (covered separately). |

### Group F — External-original-derived features (2 columns)

| Column | Includes | Excludes |
|---|---|---|
| `uses_original_target_stats` | Statistics computed from an external original dataset's target column (mean / smoothed mean / WoE / entropy / target std) and attached as features to the synthetic training data. masaya s6e2; mahog s5e8 TE-bigrams using original targets. | Concatenating original rows for training (that's `external_original_use_mode = rows-only` in Pass 1). |
| `uses_snap_or_kdtree_lookup` | "Snap" each row to nearest neighbor in the original dataset (KDTree, BallTree, or exact key matching) and attach that neighbor's properties as features. cdeotte KGMON Playbook snap features; Irfan s5e7 match_p; Sergey s3e14 (this is the lookup-exploit paradigm). | Just concatenating the original dataset (covered by Pass 1). |

### Group G — Learned / advanced features (3 columns)

| Column | Includes | Excludes |
|---|---|---|
| `uses_autoencoder_latents` | Training a DAE (denoising autoencoder) or VAE on features and using the encoder's latent layer outputs as input features for a downstream model. Umar s3e13 frozen-encoder-as-classifier; tilii s5e10 AE latents; masaya s6e2 DVAE. | DAE used directly as the prediction model (e.g., for imputation where the task IS reconstruction) — that's modeling, not FE. |
| `uses_dim_reduction_features` | PCA / SVD / Truncated SVD / GRP / t-SNE / UMAP components used as input features. Iqbal s4e1 TF-IDF + SVD; cdeotte s6e3 PCA+GRP on IBM original. | Dimensionality reduction used only for visualization. |
| `uses_genetic_programming_features` | Symbolic-regression / GP-derived features (gplearn library; tilii's s5e10 11 GP features at ensemble stage; masaya s6e2 gplearn). | Any other FE that happens to be nonlinear. |

### Group H — Text and exotic (2 columns)

| Column | Includes | Excludes |
|---|---|---|
| `uses_text_features` | Treating a column as text and applying TF-IDF, character n-grams, word embeddings, or extracting structured info from text strings. Iqbal s4e1 Surname-as-text + TF-IDF; Mart Preusse s4e9 engine-string parsing. | A high-cardinality categorical that happens to be string-typed but is treated categorically (covered by encoding columns). |
| `uses_lasso_generator_recovery` | Using a Lasso regression diagnostically to reverse-engineer the synthetic-data generator's target formula. tilii s5e10 (recovered the 0.3×curvature + 0.2×lighting + … formula). | Lasso used as a base model. |

### Group I — Negative / meta indicators (3 columns)

| Column | Includes | Excludes |
|---|---|---|
| `explicit_minimal_or_no_fe` | Author explicitly states minimal or no FE was used, often as a deliberate choice (cdeotte s5e3 "small data → no FE"; Heitor s3e5 "no FE, single XGB"). | Just a writeup that doesn't mention FE — that's missing data, not explicit minimal FE. |
| `uses_pseudo_labels_as_features` | Predicting test labels with one model, then using those predicted labels as features for another model. Different from pseudo-labeling for training data augmentation. cdeotte s5e6 pseudo-label COLUMNS variant. | Pseudo-labels used only for retraining (that's training augmentation, not FE). |
| `uses_adversarial_validation_for_fe` | Adversarial validation (train classifier to distinguish source from target) used to filter or select features (or filter original-dataset rows used as training augmentation). Hardy Xu s3e7; stopwhispering s4e4. | Adversarial validation used only for diagnostic purposes. |

## Source-confidence column (1)

| Column | Allowed values | Definition |
|---|---|---|
| `pass3_source_confidence` | `notebook+writeup` / `writeup+notes` / `writeup-only` / `notes-only` | The basis on which the row was coded. `notebook+writeup` = both source files were available and consulted. `writeup+notes` = original writeup file was consulted plus the Pass 2 MD as a checklist. `writeup-only` = only the original writeup was consulted (no notebook published). `notes-only` = only the Pass 2 MD was consulted (worst case — flag for follow-up). |

## Meta / admin columns (5)

| Column | Type | Purpose |
|---|---|---|
| `competition_ref` | string | Join key with Pass 1 and Pass 2. |
| `finish_rank` | int | Join key with Pass 1 and Pass 2. |
| `n_fe_techniques_used` | int | Derived count: sum of TRUE values across the 24 technique columns. Lets us answer "do single-model-FE wins use more techniques on average than ensemble-stacking wins?" |
| `pass3_notes` | string | Free-text notes per entry. Flags ambiguities, judgment calls, and especially "Pass 2 MD missed technique X" findings — those become Pass 2 corrections. |
| `pass3_date_coded` | date | When this row was finalized. Lets us track Stage 1 vs Stage 2 cells. |

## What's intentionally NOT in scope

Boundary clarifications, so the scope is unambiguous:

- **Post-processing of model outputs.** OptimizedRounder for ordinal classification, target reversal at submission time, probability calibration, threshold tuning, predicted-label-as-submission tweaks. These aren't feature engineering — they're post-modeling.
- **Cross-validation strategy.** Stratified vs plain k-fold, post-cutoff CV, year-grouped CV. Covered by Pass 1 `cv_strategy`.
- **Ensemble methods.** Stacking, hill climbing, mean blending, weighted blending. Covered by Pass 1 `ensemble_method`.
- **Hyperparameter tuning.** Optuna, GridSearch, manual. Covered by Pass 1 `hyperparameter_tuning`.
- **Model architecture choices.** Choice of XGBoost vs LightGBM, custom NN architectures, AutoGluon configuration. Covered by Pass 1 `models_used`.
- **Pseudo-labeling for training data augmentation.** That's a training-time technique, not FE. (Distinct from `uses_pseudo_labels_as_features` which is specifically pseudo-labels used *as features*.)
- **Knowledge distillation.** Training-time loss/label technique. Already corrected in s6e2 audit.
- **Custom loss functions** (e.g., LightGBM custom MSLE). That's a modeling choice.

## Open questions for your reaction

1. **Granularity check on encoding.** Should `uses_target_encoding` split into within-fold vs not? You've read these writeups more carefully than I have — does this distinction matter?

2. **Boundary on aggregates.** Is `uses_groupby_advanced` too vague? I've grouped histogram-bins, z-scores, and division-of-aggregations together. They could be three separate columns.

3. **Should there be a `uses_outlier_classification_as_feature` column?** Mart Preusse's s4e9 outlier-classifier-OOFs-as-features pattern is distinctive but rare in the corpus. May not justify its own column.

4. **Domain features — too broad?** Currently one column for any domain-knowledge-driven FE. Could split into "domain-specific binary flags" vs "domain-specific ratios" if there's enough volume in each.

5. **Is "feature selection" itself a category?** Permutation importance, backward elimination, SFS — these are *selection*, not creation. Currently out of scope but you may want it as one column (`uses_explicit_feature_selection`).

6. **Should we add `uses_residual_features`?** cdeotte's residual modeling chain (NN over LR residuals, XGB over NN residuals) appears in s5e5 and elsewhere. It's the model's predictions becoming features for the next model, which is borderline FE / borderline ensembling.

7. **Lookup-exploit category overlap.** `uses_snap_or_kdtree_lookup` is partly redundant with the lookup-exploit paradigm classification in Pass 2. Worth keeping for granularity?

## Proposed workflow

**Stage 1 — Draft from Pass 2 MDs (half day)**

1. Build the workbook sheet skeleton: create `FE Taxonomy` sheet in `data/kaggle_meta_analysis.xlsx` with the 30 columns above.
2. Read each of the 45 per-writeup MDs (`analysis/writeup-reevaluation/*.md`).
3. Code each row based on the MD's "What's actually original" and "Dataset constraints" sections.
4. Set `pass3_source_confidence = notes-only` for every row at this stage.
5. Sanity-check: compute `n_fe_techniques_used` distribution; flag entries with 0 or with >10.

**Stage 2 — Source-validate (1–2 days)**

For each of the 45 entries:

1. Open the original writeup at `data/writeups/<slug>/<title>.txt`.
2. If a notebook exists at `data/writeups/<slug>/*.ipynb`, open it too.
3. Re-evaluate every TRUE/FALSE column against the source material.
4. Add any techniques the MD missed (flip cells from FALSE to TRUE).
5. Update `pass3_source_confidence` to `writeup+notes`, `notebook+writeup`, etc.
6. Record in `pass3_notes` any techniques added from Stage 1, with a tag like `[+from_writeup]` or `[+from_notebook]`.
7. Each "MD-missed-this" finding is also a Pass 2 audit signal — log them.

**Output deliverables**

- New `FE Taxonomy` sheet in `data/kaggle_meta_analysis.xlsx`
- Stage 1 → Stage 2 delta metric: how many cells flipped FALSE → TRUE during validation, by category. This quantifies generational drift.
- New §4.9 paragraph in `research_report.md` describing FE-by-paradigm patterns (if the project extends).

## Pilot plan

Before coding all 45 entries, pilot with **2–3 representative entries** to validate the schema:

- **One ensemble-stacking heavyweight:** cdeotte s5e6 (the KGMON-proto entry) — should hit many encoding + aggregate + combinatorial columns
- **One lookup-exploit:** Sergey s3e14 — should be sparse on most columns, TRUE on `uses_snap_or_kdtree_lookup`, possibly `uses_count_or_frequency_encoding`
- **One minimal-FE:** Heitor s3e5 — should be TRUE on `explicit_minimal_or_no_fe` and mostly FALSE elsewhere

If the schema cleanly handles these three, it'll handle the rest. If we find ourselves squinting at boundaries, the schema needs revision.

---

**Next step:** react to the schema. Flag any columns that should be split / merged / dropped / added. Once the schema is locked, we pilot 3 entries, then commit to the full 45.
