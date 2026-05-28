# Pass 3 FE Taxonomy — Stage 1 Results (extended pilot, 5 entries)

**Status:** Extended pilot. Stage 1 coding only (`pass3_source_confidence = notes-only`).
**Branch:** `phase9/fe-taxonomy`.
**Date:** 2026-05-28.

After the 3-entry pilot triggered 6 schema revisions (v3 locked), this extended pilot codes **5 more** representative entries — one per paradigm not yet stress-tested — against the v3 schema before committing to the full 45. If new schema issues surface here, revise once more; if not, proceed to the remaining 37.

## Entry selection rationale

| Entry | Paradigm | Why this entry |
|---|---|---|
| adaubas s4e5 | ensemble-stacking standard (non-cdeotte) | First R2 metric; all-numeric Poisson-sum; row-wise stats family |
| greysky s5e4 | single-model heavy-FE | 1552-feature single LGBM; counter-aesthetic to ensembles |
| room722 ICR | problem-fit NN | 617 rows; VSN architecture from TFT paper; Featured competition |
| Bill Cruise s3e3 | community-template-tweak | Forked starter + 7 domain HR features added |
| Mart Preusse s4e9 | distinctive ensemble (NN-stacker) | Outlier classifier as feature; text parsing; NN meta-learner |

## Stage 1 results — all 8 entries so far

| Entry | Paradigm | Expected | Stage 1 TRUE | In range? |
|---|---|---|---|---|
| cdeotte s5e6 (pilot) | heavyweight | 6–12 | 6 | yes |
| Sergey s3e14 (pilot) | lookup | 1–4 | 1 | yes |
| Heitor s3e5 (pilot) | minimal | 0–3 | 1 | yes |
| **adaubas s4e5** | ensemble standard | 4–9 | **5** | yes |
| **greysky s5e4** | single-model heavy | 8–15 | **6** | **below** |
| **room722 ICR** | problem-fit NN | 2–6 | **1** | **below** |
| **Bill Cruise s3e3** | community-template | 3–7 | **3** | yes (low) |
| **Mart Preusse s4e9** | distinctive ensemble | 4–9 | **5** | yes |

Two entries fall below their paradigm range — see "Below-range analysis" below.

---

## Entry 4: adaubas s4e5 (May 2024)

**Sources for Stage 1:** Pass 2 MD only (`notes-only`).

| # | Column | Justification (from MD) |
|---|---|---|
| 1 | `uses_target_encoding_basic` | MD: "target encoding on row sum" — TE applied to the engineered row-sum feature. |
| 2 | `uses_target_encoding_within_fold` | **null** — MD doesn't specify whether the row-sum TE was computed within-fold; needs writeup/notebook check. |
| 15 | `uses_threshold_or_binary_flags` | MD: "count threshold features (nb_sup6/7/8)" — count of features above thresholds 6, 7, 8 per row. Schema col 15 includes section explicitly names "adaubas s4e5 count-thresholds." |
| 26 | `uses_rowwise_statistics` | MD: "Row-wise statistics (sum/std/max)." Schema col 26 includes section names "adaubas s4e5 Poisson-sum row-stats." |
| 48 | `uses_permutation_importance_selection` | MD: "permutation + backward feature selection" — permutation importance is the first step. |
| 49 | `uses_sfs_or_backward_elimination` | MD: same — "backward feature selection" is the second step. Schema col 49 includes section names "adaubas s4e5 permutation + backward." |

**Stage 1 TRUE count: 5** (col 2 = null, not counted).

**Notes:**
- **Sorted-features (siukeitin technique)** — row-axis sorted-position features used as features. **Not captured by any column.** Distinctive technique that may appear elsewhere (siukeitin is cited at s4e8 and s4e10 too). Flag for schema discussion.
- **Target transformation (subtract feature mean × 0.1)** — modeling-side, out of scope.
- **Negative-weight Ridge** — meta-learner choice, out of scope.

---

## Entry 5: greysky s5e4 (April 2025)

**Sources for Stage 1:** Pass 2 MD only (`notes-only`).

| # | Column | Justification (from MD) |
|---|---|---|
| 1 | `uses_target_encoding_basic` | MD: "6-way Target Encoding combinatorics on 12 base/rounded columns." |
| 2 | `uses_target_encoding_within_fold` | **null** — MD silent on whether TE was within-fold. Heavy FE pipeline lives in a separate `podcast-dataset-generator` notebook not in our local set. |
| 12 | `uses_rounding_multi_precision` | MD: "rounded-then-halved versions of three numerics." Schema col 12 includes section explicitly names "cdeotte signature; greysky s5e4." |
| 13 | `uses_pairwise_multiplicative_interactions` | MD: "`Mul_Hpp_Elm = Host_Popularity_% × round(Episode_Length)`, similar Gpp variant" — hand-coded pairwise products. |
| 17 | `uses_higher_order_categorical_combos` | MD: "pair_size = 1..6" → 3-way through 6-way categorical groupings. Per v3 col 16 clarification, pure enumeration without selection → col 17 only, NOT col 16. |
| 18 | `uses_numerics_as_categoricals_then_combos` | MD: "12 base/rounded columns" — rounded numerics (Episode_Length, Host_Popularity_%, etc.) treated as categoricals for TE combos. Originally numeric, converted via rounding. |
| 26 | `uses_rowwise_statistics` | MD: "Descriptive statistics on TE column values: mean/std/min/max aggregated globally, by pair_size, by source column. Reduces TE-combo-explosion to fixed-dimensional features." — row-wise stats applied across the TE-derived columns. |

**Stage 1 TRUE count: 6** (col 2 = null, not counted).

**Notes:**
- **Below expected range (6 < 8–15 for single-model heavy-FE).** Two plausible reasons:
  1. The 1552 features come from few techniques applied DEEPLY (6-way combinatorics on 12 columns → thousands of combos; then descriptive-stat aggregation reduces back to fixed dim). High *feature count*, modest *technique diversity*. Consistent with the calibration finding (schema measures diversity, not count).
  2. The heavy FE pipeline lives in the separate `podcast-dataset-generator` notebook NOT in our local set. Stage 2 source-validation may reveal more techniques only documented there. Flag for Stage 2.
- **TE descriptive stats** — the aggregation step (mean/std/min/max of TE values by metadata group) is an unusual technique. Coded under col 26 (rowwise) since it produces row-level summary features. Could plausibly be col 3 (multiple TE aggregations) if interpreted as "many TE statistics per row." Stage 2 should resolve.
- **Multi-seed averaging** — ensemble of seeds, captured by Pass 1.

---

## Entry 6: room722 ICR (August 2023)

**Sources for Stage 1:** Pass 2 MD only (`notes-only`).

| # | Column | Justification (from MD) |
|---|---|---|
| 51 | `explicit_minimal_or_no_fe` | MD `fe_techniques`: "No FE (overfitting)". Author explicitly chose no FE because of 617-row overfitting risk in a Featured competition. Analogous to Heitor s3e5. |

**Stage 1 TRUE count: 1.**

**Notes:**
- **Below expected range (1 < 2–6 for problem-fit NN).** Author's "problem-fit NN" answer was the **architecture** (Variable Selection Network from TFT paper) + heavy regularization (dropout 0.75) + repeated training + multi-label CV + probability reweighting. **All of this is out of scope for an FE-focused schema** (architecture, CV, post-processing). The schema is correctly capturing "minimal FE by design."
- **Per-feature 8-neuron linear projections** (replacing standard normalization) — learned per-feature embeddings inside the NN. **Not captured by any column.** Could arguably extend col 38 (autoencoder latents) to "learned numeric embeddings," but per-feature projection trained jointly with the model is more architectural than FE. Flag for discussion, not for v4 revision yet.
- **Multi-label CV strategy** (derive hardness label from baseline, CV-stratify on target × hardness) — CV strategy with auxiliary-target derivation. Out of scope (Pass 1 `cv_strategy`).
- **Probability reweighting at output** — post-processing, out of scope.
- **TFT-paper-derived VSN architecture** — academic-paper-as-technique-source pattern (N=5 across set). Architectural, out of scope.
- This entry effectively reclassifies as "minimal-FE problem-fit NN" — 1 TRUE column matches the minimal-FE range (0–3). The problem-fit NN range (2–6) assumed problem-aware FE; this entry shows the architecture-only variant.

---

## Entry 7: Bill Cruise s3e3 (February 2023)

**Sources for Stage 1:** Pass 2 MD only (`notes-only`).

| # | Column | Justification (from MD) |
|---|---|---|
| 26 | `uses_rowwise_statistics` | MD: "`AttritionRisk = sum of 5 binary flags`" — composite risk score = rowwise count/sum of binary indicators. Schema col 26 includes "count-above-threshold computed *across* multiple feature columns *within a row*." |
| 27 | `uses_domain_binary_flags` | MD: "`Age_risk = (Age < 34)`, `HourlyRate_risk = (HourlyRate < 60)`, `Distance_risk = (DistanceFromHome >= 20)`, `YearsAtCo_risk = (YearsAtCompany < 4)`, `JobHopper = (NumCompaniesWorked > 2) & (AverageTenure < 2.0)`" — five HR-domain-meaningful threshold flags. Schema col 27 includes section names "Bill Cruise s3e3 (Age<34, JobHopper)." |
| 28 | `uses_domain_ratios` | MD: "`MonthlyIncome/Age` ratio + `AverageTenure = TotalWorkingYears / NumCompaniesWorked`" — HR-domain-meaningful financial/tenure ratios. |

**Stage 1 TRUE count: 3.**

**Notes:**
- Fits community-template-tweak range (3–7) at the low end.
- **Forked starter notebook** (khawajaabaidullah's XGB+LGBM+CatBoost) — but the base notebook itself does NO FE (per khawajaabaidullah's own comment: *"my notebook does nothing but combines three simple models"*). So **col 53 (`uses_forked_base_model_fe_uncatalogued`) FALSE** — no uncatalogued base-model FE to flag.
- Public original IBM HR dataset used as `concat_rows` for training data — covered by Pass 1 `original_data_usage`, NOT a Pass 3 column by design.
- This is the **cleanest community-template-tweak example so far** — small, targeted FE addition (7 features) on top of a thin starter notebook.

---

## Entry 8: Mart Preusse s4e9 (September 2024)

**Sources for Stage 1:** Pass 2 MD only (`notes-only`).

| # | Column | Justification (from MD) |
|---|---|---|
| 1 | `uses_target_encoding_basic` | MD: "Median target encoding (not mean), leakfree per fold." **Coding judgment:** col 1 specifies "mean" in its description, but median is the closest single-statistic-TE column. Stage 2 may surface whether to broaden col 1 or split off a column. |
| 2 | `uses_target_encoding_within_fold` | MD: "leakfree per fold" — explicitly stated within-fold. |
| 10 | `uses_binning_discretization` | MD: "mileage_binning" — explicit binning of a numeric column. |
| 43 | `uses_character_or_string_pattern_features` | MD: "text_feature_extraction (horsepower/displacement from engine string)." Schema col 43 includes section names "Mart Preusse s4e9 engine-string parsing for horsepower/displacement." |
| 47 | `uses_outlier_or_aux_classifier_as_feature` | MD: "outlier_classification (IQR price_bin)" — CatBoost classifier trained on IQR-bin outlier flags, OOFs used as features for downstream regressors. Schema col 47 includes section names "Mart Preusse s4e9." |

**Stage 1 TRUE count: 5.**

**Notes:**
- Fits ensemble-stacking standard range (4–9).
- **Median TE coded under col 1** despite col 1's description specifying "mean." Stage 2 should resolve whether to:
  - (a) broaden col 1 to "any single-statistic TE,"
  - (b) split a separate `uses_median_target_encoding` column, or
  - (c) leave as a coding-judgment call documented in `pass3_notes`.
- **Rare-category grouping** (`rare_class_handling: rare_grouping` in Pass 1) — common preprocessing step not represented in Pass 3 schema. Captured by Pass 1; potentially out-of-scope here but worth tracking.
- **DeepTables NN as meta-learner** — ensemble method (Pass 1), NOT FE.
- **Forked yekenot DeepTables notebook** — but Mart enumerates what each base contributes (4 OOFs documented). Doesn't trigger col 53.
- **3 OOFs from base regressors (SVR, LGBM5, XGB)** as inputs to NN meta-learner — standard stacking, captured by Pass 1 `ensemble_method`.

---

## Below-range analysis

Two entries fell below their paradigm-expected ranges:

### greysky s5e4 (6 vs expected 8–15 single-model heavy)

**Diagnosis:** The schema captures technique *diversity*, not feature *count*. greysky's 1552-feature pipeline comes from few techniques applied deeply (6-way TE combinatorics + descriptive-stat aggregation). The heavy FE work lives in a separate notebook (`podcast-dataset-generator`) not in our set — Stage 2 source-validation may surface 2–4 more techniques only documented there.

**Action:** Flag for Stage 2 priority. If Stage 2 still shows ≤8, consider broadening the "single-model heavy-FE" range to 6–15.

### room722 ICR (1 vs expected 2–6 problem-fit NN)

**Diagnosis:** room722's "problem-fit" answer was *architectural* (VSN from TFT paper) + regularization + CV design. The FE side was deliberately minimal due to 617-row overfitting risk. The schema correctly captures this as `explicit_minimal_or_no_fe` (col 51). The problem-fit NN paradigm includes both "FE-driven NN" and "architecture-driven NN" variants; the latter scores low on FE diversity.

**Action:** Reclassify problem-fit NN expected range as **1–6** to accommodate architecture-only variants. Or leave at 2–6 and flag the architecture-only subset separately. Recommend the former — simpler.

---

## Schema gaps / candidate revisions

The 5 new entries surfaced these candidate gaps:

1. **Median / non-mean single-statistic TE** (Mart Preusse) — col 1 specifies mean. Either broaden col 1 to "any single-statistic TE" or add a sibling column. **Recommend: broaden col 1**, change description to "Single-statistic target encoding (mean, median, or another single statistic) applied to one or more categorical columns."

2. **Sorted-features** (adaubas, via siukeitin technique) — row-axis sorted-position features. Not captured. **Recommend: note in `pass3_notes` for now; if 3+ entries use it, add column 54 in a future revision.** Don't widen schema preemptively.

3. **TE descriptive-stat aggregation across combos** (greysky) — meta-aggregation of TE-derived columns. Coded under col 26 (rowwise) — closest fit. **No revision needed**; document the judgment call.

4. **Per-feature learned numeric embeddings inside NN** (room722) — partly architectural. **Out of scope** per the schema's "FE only, not architecture" boundary. Document.

5. **Rare-category grouping** (Mart Preusse, many others) — common preprocessing technique. Captured by Pass 1 `rare_class_handling`. **Out of scope** for Pass 3 to avoid duplication. Document.

**Net recommendation:** **one small revision** — broaden col 1 to include median and other single-statistic TE variants. The other gaps either don't merit a column (use `pass3_notes`) or are out-of-scope by design.

---

## Verdict: proceed to full 45-entry pass after minor col 1 update

- 8 entries coded; 6 within paradigm range, 2 below for explainable reasons (calibration of expected ranges, not schema breakage).
- Schema captures the techniques it should; gaps are at the margins.
- One small revision proposed: broaden col 1 description to include median/other single-statistic TE.
- Two range recalibrations recommended:
  - Single-model heavy-FE: 6–15 (was 8–15)
  - Problem-fit NN: 1–6 (was 2–6)

Ready to proceed once these three adjustments are applied (or explicitly waived).
