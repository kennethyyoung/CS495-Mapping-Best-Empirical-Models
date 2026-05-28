# Pass 3 FE Taxonomy — Stage 1 Complete (all 45 entries)

**Status:** Stage 1 coding complete. `pass3_source_confidence = notes-only` for all 45.
**Branch:** `phase9/fe-taxonomy`.
**Date:** 2026-05-28.
**Data:** `stage1_data.csv` (45 rows × 53 boolean columns + 5 admin + 1 source-confidence).

This document summarizes Stage 1 results: 53 boolean technique columns coded from Pass 2 MDs alone for all 45 entries. Stage 2 (source validation against original writeups + notebooks) will follow.

---

## Distribution of n_fe_techniques_used

| Count | Entries |
|---|---|
| 0 | 1 |
| 1 | 17 |
| 2 | 5 |
| 3 | 6 |
| 4 | 1 |
| 5 | 5 |
| 6 | 3 |
| 7 | 2 |
| 8 | 4 |
| 10 | 1 |
| 15 | 1 |
| 19 | 1 |

**Median: 2. Mean: ~3.5.** The corpus is bimodal: a long left tail (most entries at 1–3 techniques) and a small right tail (cdeotte s5e2, s5e6, s5e5; s6e2, s6e3) carrying heavyweight ensembles.

This bimodality is the methodologically interesting finding. It echoes the pilot's calibration: most winners do **less FE than expected**, and the schema is correctly distinguishing high-diversity heavyweights from focused recipes.

---

## All 45 entries — Stage 1 TRUE counts and paradigm fit

| Entry | n_fe | Paradigm | Expected | Fit |
|---|---|---|---|---|
| **Heavyweight ensemble-stacking (6–12)** | | | | |
| s5e2 cdeotte | 15 | single-model heavy-FE | 6–15 | **at top** |
| s5e6 cdeotte (pilot) | 6 | heavyweight | 6–12 | **in range** |
| s5e5 cdeotte | 8 | heavyweight | 6–12 | **in range** |
| s4e12 cdeotte | 8 | single-model heavy-FE | 6–15 | **in range** |
| s6e2 masayakawamata | 10 | heavyweight | 6–12 | **in range** |
| s6e3 cdeotte (KGMON) | 19 | heavyweight | 6–12 | **above** (full-scale outlier) |
| s5e10 Tilii | 4 | heavyweight | 6–12 | below |
| **Single-model heavy-FE (6–15)** | | | | |
| s5e4 greysky | 6 | single-model heavy-FE | 6–15 | **in range** |
| **Ensemble-stacking standard (4–9)** | | | | |
| s4e1 Iqbal | 8 | standard | 4–9 | **in range** |
| s5e11 mahog | 7 | standard | 4–9 | **in range** |
| s6e1 mahog | 7 | standard | 4–9 | **in range** |
| s5e8 mahog | 5 | standard | 4–9 | **in range** |
| s4e4 stopwhispering | 5 | standard | 4–9 | **in range** |
| s4e9 Mart Preusse | 5 | standard | 4–9 | **in range** |
| s4e5 adaubas | 5 | standard | 4–9 | **in range** |
| s3e8 Craig Thomas | 3 | standard | 4–9 | low |
| s3e16 Ravi | 3 | standard | 4–9 | low |
| s5e12 wind1234it | 3 | standard | 4–9 | low |
| s3e24 Ravi | 2 | standard | 4–9 | below |
| s4e10 omidbaghchehsaraei | 2 | standard | 4–9 | below |
| s3e23 oscarm524 | 1 | standard | 4–9 | below |
| s3e9 ambrosm | 1 | standard | 4–9 | below |
| s3e11 ambrosm | 1 | standard | 4–9 | below |
| s3e6 viktortaran | 1 | standard | 4–9 | below |
| s4e8 Optimistix | 1 | standard | 4–9 | below |
| s4e7 Cross Sellers | 0 | standard | 4–9 | below (under-documented) |
| s3e26 Hardy Xu | 1 | NN-stacker standard | 4–9 | below |
| **Community-template-tweak (3–7)** | | | | |
| s6e4 kirill0212 | 6 | community-template | 3–7 | **in range** |
| s3e3 Bill Cruise | 3 | community-template | 3–7 | **in range** (low) |
| s4e3 Moonlit | 3 | community-template | 3–7 | **in range** (low) |
| s3e1 Kirderf | 1 | community-template | 3–7 | below (single-fork) |
| **Lookup-exploit (1–4)** | | | | |
| s3e14 Sergey (pilot) | 1 | lookup | 1–4 | **in range** |
| s3e7 Hardy Xu | 1 | lookup-exploit | 1–4 | **in range** |
| s5e7 Irfan | 1 | lookup | 1–4 | **in range** |
| TPS Feb 2022 ambrosm | 1 | lookup-exploit | 1–4 | **in range** |
| **Problem-fit NN (1–6)** | | | | |
| TPS May 2022 ambrosm+Pourchot | 2 | problem-fit NN | 1–6 | **in range** |
| TPS Jun 2022 Sebastian | 1 | problem-fit NN | 1–6 | **in range** |
| ICR room722 | 1 | problem-fit NN | 1–6 | **in range** |
| **Minimal-FE (0–3)** | | | | |
| s3e13 Umar | 2 | minimal | 0–3 | **in range** |
| s5e3 cdeotte | 1 | minimal | 0–3 | **in range** |
| s3e5 Heitor (pilot) | 1 | minimal | 0–3 | **in range** |
| s3e10 seascape | 1 | minimal | 0–3 | **in range** |
| s4e11 Mahdi | 1 | minimal | 0–3 | **in range** |
| s3e17 ISoft | 1 | AutoML-stack | 0–3 | **in range** |
| **No-writeup notebook-only** | | | | |
| s3e4 Ollie Kemp | 1 | distinctive | n/a | n/a |

**Fit summary:**
- **In range or above:** 29 / 45 (64%)
- **Below range:** 16 / 45 (36%)

The 36% below-range rate is high. Two structural reasons:

1. **Pass 2 MDs are FE-summary-light.** They typically list 2–5 techniques even when the actual notebook has 5–10. This is the generational drift the pilot anticipated. Stage 2 source validation should flip cells FALSE→TRUE.
2. **Some winners genuinely do minimal FE.** ambrosm s3e9/s3e11, oscarm524, Optimistix s4e8, Mahdi s4e11 all explicitly emphasized model diversity or CV discipline over heavy FE. These genuinely belong in lower ranges and may justify recalibrating "ensemble-stacking standard" from 4–9 to a wider 1–9.

---

## Most-used columns across the corpus (TRUE rate)

| Col | Column | TRUE count | % of 45 |
|---|---|---|---|
| 1 | `uses_target_encoding_basic` | 19 | 42% |
| 51 | `explicit_minimal_or_no_fe` | 8 | 18% |
| 13 | `uses_pairwise_multiplicative_interactions` | 7 | 16% |
| 11 | `uses_digit_features` | 7 | 16% |
| 18 | `uses_numerics_as_categoricals_then_combos` | 7 | 16% |
| 2 | `uses_target_encoding_within_fold` | 6 TRUE (rest null/false) | 13% |
| 28 | `uses_domain_ratios` | 6 | 13% |
| 10 | `uses_binning_discretization` | 6 | 13% |
| 17 | `uses_higher_order_categorical_combos` | 6 | 13% |
| 5 | `uses_count_encoding` | 5 | 11% |
| 26 | `uses_rowwise_statistics` | 5 | 11% |
| 32 | `uses_original_target_mean_as_feature` | 5 | 11% |

**Headline:** TE basic is the single most-used technique (42%), validating its first-class position in the schema. After that, the distribution is long-tailed — no single technique dominates beyond TE.

## Least-used columns (NEVER TRUE in Stage 1)

Columns that no entry triggered (in Stage 1):
- col 3 `uses_te_multi_aggregations` (1 TRUE — only s4e12 cdeotte)
- col 4 `uses_te_alternative_targets` (3 TRUE — cdeotte s5e6, mahog s5e8, s5e11)
- col 6 `uses_frequency_encoding` (3 TRUE — s4e4, s6e2, s6e3, s6e4)
- col 9 `uses_power_polynomial_transform` (1 TRUE — s5e12)
- col 14 `uses_pairwise_additive` (1 TRUE — s5e5)
- col 15 `uses_threshold_or_binary_flags` (1 TRUE — s4e5)
- col 19–25 (groupby family) (mostly only s5e2 cdeotte triggers these)
- col 29 `uses_domain_ordinal_scales` (1 TRUE — s3e8 gemstones)
- col 30 `uses_datetime_decomposition` (1 TRUE — s4e12)
- col 31 `uses_cyclical_encoding` (3 TRUE — s5e8, s6e1, s6e3)
- col 33 `uses_original_target_advanced_stats` (1 TRUE — s6e2)
- col 34 `uses_exact_key_match_lookup` (2 TRUE — s3e14, s5e7)
- col 35 `uses_approximate_neighbor_lookup` (2 TRUE — s6e3, TPS Feb 2022)
- col 36 `uses_drift_features` (1 TRUE — s6e3)
- col 37 `uses_distribution_anomaly_features` (1 TRUE — s6e3)
- col 38 `uses_autoencoder_latents` (4 TRUE — s3e13, s5e10, s6e2, s6e3)
- col 39 `uses_pca_svd_components` (2 TRUE — s4e1, s6e3)
- col 40 `uses_random_projection_features` (1 TRUE — s6e3)
- col 41 `uses_genetic_programming_features` (2 TRUE — s5e10, s6e2)
- col 42 `uses_tfidf_features` (2 TRUE — s4e1, s6e3)
- col 43 `uses_character_or_string_pattern_features` (2 TRUE — s4e9, TPS May 2022)
- col 44 `uses_lasso_generator_recovery` (1 TRUE — s5e10)
- col 45 `uses_pseudo_labels_as_features` (1 TRUE — s5e6)
- col 46 `uses_residual_features` (3 TRUE — s5e5, s5e6, s5e10)
- col 47 `uses_outlier_or_aux_classifier_as_feature` (1 TRUE — s4e9)
- col 48 `uses_permutation_importance_selection` (4 TRUE — s3e6, s3e16, s3e24, s4e5)
- col 49 `uses_sfs_or_backward_elimination` (2 TRUE — s4e4, s4e5)
- col 50 `uses_correlation_or_constant_dropping` (1 TRUE — s4e3)
- col 52 `uses_adversarial_validation_for_fe` (2 TRUE — s3e7, s4e4)
- col 53 `uses_forked_base_model_fe_uncatalogued` (4 TRUE — s3e1, s4e3, s5e7?, s6e4)

**Many singleton columns** (only 1–2 entries). This is *expected* per the schema's design philosophy ("Single-author-specific columns are acceptable"). The schema is a *map of what's possible*, not a frequency-driven taxonomy.

---

## Schema gaps surfaced (Stage 1)

Beyond the gaps documented in `PILOT.md` and `STAGE1_RESULTS.md`, the full pass surfaced:

1. **2-way categorical combos** — col 17 specifies 3+ way only; col 13 specifies multiplicative numeric. 2-way categorical concatenation/crosses (mahog s5e8 bigrams, kirill0212 s6e4 pairwise crosses, cdeotte s5e2 all-pairs cats) doesn't strictly fit either. Recommend: **broaden col 17 to "2+ way" OR add a separate "uses_pairwise_categorical_combos" column.**

2. **Geographic FE** — Kirderf s3e1's coordinate-based features (latitude/longitude → distances/clusters) have no clean column. Recommend: **add `uses_geographic_features` column** (or treat as col 27 domain-binary if cluster/region flags).

3. **NN-internal preprocessing as FE vs architecture** — PLE (s3e26), per-feature embeddings (ICR), categorical NN embeddings (s3e26) are partly preprocessing, partly architecture. Coded as col 10 (binning) for PLE since closest fit. Leaving out-of-scope as architectural; document explicitly.

4. **Train-to-test internal lookup** — Hardy Xu s3e7's opposite-label assignment to train-twin test rows isn't synthetic-to-original (col 34) or approximate-neighbor (col 35). Schema gap. Could add `uses_train_test_lookup` or treat as col 34 variant.

5. **Generator reverse-engineering** — ambrosm TPS Feb 2022's reverse-transformation of decamer counts to recover the seed-driven sequence isn't captured. Distinct from col 44 (Lasso-based) and col 35 (KDTree). Singleton in corpus.

6. **Single-fork base FE uncatalogued** — col 53 requires "multiple" forks. Kirderf s3e1 (single dmitryuarov fork doing all FE) and Cross Sellers s4e7 (heavily under-documented feature store) don't fit strictly. Recommend: **relax col 53 wording to "one or more uncatalogued forked sources contributing FE."**

7. **Cross Sellers under-documentation** — entire feature store (12 versions) is in proprietary GitHub repo not available. Stage 2 may not resolve. Note as data limitation.

---

## Recommended schema revisions before Stage 2

| # | Change | Cost |
|---|---|---|
| 1 | Broaden col 17 to "2+ way categorical combos" (or add separate pairwise-cat column) | Affects ~5 entries (s5e2, s5e8, s6e4, possibly more) |
| 2 | Add col 54 `uses_geographic_features` | Affects 1 entry currently (s3e1); future-proofs for any geographic dataset |
| 3 | Relax col 53 to "one or more forked sources with uncatalogued FE" | Affects ~3 entries (s3e1, s4e7, possibly s3e14) |
| 4 | Document train-test internal lookup as col 34 variant or add column | Affects 1 entry (s3e7); singleton |

Recommendation: **apply revisions 1 and 3** before Stage 2; defer 2 and 4 (singleton-driven, may not generalize).

---

## What Stage 2 should focus on

Source-validation priorities by paradigm:

1. **High-priority Stage 2:** Below-range entries with available notebooks (s3e23 oscarm524, s4e10 omidbaghchehsaraei, s4e3 Moonlit, s3e16 Ravi, s5e8 mahog) — likely to surface 2–5 more techniques per entry.

2. **Medium-priority Stage 2:** Heavyweight entries (s5e2, s5e5, s6e2, s6e3) — already strong but may add cdeotte signature techniques (multi-aggregation TE, division-of-aggregates).

3. **Low-priority Stage 2:** Writeup-only entries with no notebook (s3e7 Hardy Xu, s3e13 Umar, s3e17 ISoft, s3e24 Ravi, s4e7 Cross Sellers, s4e8 Optimistix, s5e5 cdeotte) — can't verify beyond writeup.

4. **Skip / data-limited:** s4e7 Cross Sellers (proprietary repo), TPS Jun 2022 (notebook flagged buggy by author).

---

## Verdict

Stage 1 is complete. The schema works at scale across the corpus:
- 64% of entries fit their paradigm range
- Heavyweight entries skew high (s5e2, s6e3) as expected — these are full-FE-spectrum applications
- Below-range entries cluster in two groups: (a) genuinely minimal FE (validated against MD claims), (b) Pass 2 MD under-summarization (Stage 2 fix)
- 4 schema gaps identified, 2 worth fixing before Stage 2

**Next step:** apply revisions 1 and 3 (or skip and proceed directly to Stage 2). Then begin Stage 2 source-validation, starting with high-priority entries (~15 entries with notebooks where Stage 2 has highest ROI).
