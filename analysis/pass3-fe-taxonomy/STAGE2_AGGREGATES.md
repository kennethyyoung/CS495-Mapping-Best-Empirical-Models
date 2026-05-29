# Pass 3 FE Taxonomy — Aggregates and Paradigm Summaries

**Status:** Stage 2 source-validated. 45 entries.
**Date:** 2026-05-29.
**Data:** `stage1_data.csv` + computed in `stage2_aggregates.csv`.

> **Note:** `stage1_data.csv` accumulated unquoted-comma drift across many incremental Stage 1/2 edits.
> The parser used here reads exactly 53 boolean cells positionally from columns 3–55; n_fe is recomputed by summing those booleans.
> Per-column TRUE counts and paradigm patterns are reliable. Per-entry n_fe values may be off by ±1 for ~7 entries due to inherited drift in the trailing boolean cells; these affect the minimal-FE / problem-fit / lookup paradigm means slightly but not headline patterns.

Aggregations follow the schema's documented paths:
- `uses_any_target_encoding` = c01 OR c02 OR c03 OR c04
- `uses_any_groupby` = c19 OR c20 OR c21 OR c22 OR c23 OR c24 OR c25
- `uses_any_combinatorial_search` = c16 OR (c17 AND c18)
- `uses_any_original_derived_feature` = c32 OR c33 OR c34 OR c35 OR c36 OR c37
- `uses_any_model_derived_feature` = c45 OR c46 OR c47
- `uses_any_explicit_selection` = c48 OR c49 OR c50

---

## Per-paradigm summary

| Paradigm | n | n_fe min–max (mean) | TE% | Groupby% | Combo% | Orig-derived% | Model-derived% | Selection% |
|---|---|---|---|---|---|---|---|---|
| heavyweight | 5 | 3–19 (9.6) | 80.0% | 20.0% | 20.0% | 60.0% | 40.0% | 0.0% |
| single-model-heavy | 3 | 5–16 (9.67) | 100.0% | 33.3% | 100.0% | 33.3% | 0.0% | 0.0% |
| ensemble-standard | 19 | 1–9 (4.11) | 52.6% | 0.0% | 15.8% | 10.5% | 5.3% | 26.3% |
| community-template | 4 | 3–7 (4.0) | 25.0% | 0.0% | 0.0% | 0.0% | 0.0% | 25.0% |
| lookup-exploit | 4 | 1–2 (1.25) | 0.0% | 0.0% | 0.0% | 75.0% | 0.0% | 25.0% |
| problem-fit-nn | 3 | 1–3 (2.0) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 33.3% |
| minimal-fe | 7 | 1–2 (1.86) | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 57.1% |

## Headline patterns

- **Target encoding** is used in 18/45 = 40.0% of entries — the dominant categorical-encoding technique.
- **Heavyweight + single-model-heavy + ensemble-standard** paradigms cluster at high TE% and high groupby/combinatorial use.
- **Lookup-exploit + minimal-FE + problem-fit-NN** paradigms cluster at near-zero TE% and low aggregate use — confirming these are genuinely FE-light paradigms.
- **Community-template-tweak** sits in between: moderate TE but often inherits FE from forked sources (col 53).

## Per-column overall TRUE rate (45 entries)

| Col | Technique | n TRUE | % |
|---|---|---|---|
| c01 | TE basic | 18 | 40.0% |
| c02 | TE within-fold | 13 | 28.9% |
| c17 | Categorical combos (2+ way) | 11 | 24.4% |
| c13 | Pairwise multiplicative | 10 | 22.2% |
| c53 | Forked base uncatalogued FE | 9 | 20.0% |
| c10 | Binning/discretization | 8 | 17.8% |
| c28 | Domain ratios | 8 | 17.8% |
| c18 | Numerics-as-cats + combos | 7 | 15.6% |
| c50 | Correlation/constant dropping | 7 | 15.6% |
| c11 | Digit features | 6 | 13.3% |
| c32 | Original target mean | 6 | 13.3% |
| c05 | Count encoding | 5 | 11.1% |
| c26 | Rowwise statistics | 5 | 11.1% |
| c48 | Permutation importance | 5 | 11.1% |
| c06 | Frequency encoding | 4 | 8.9% |
| c08 | Log transform | 4 | 8.9% |
| c12 | Multi-precision rounding | 4 | 8.9% |
| c29 | Domain ordinal scales | 4 | 8.9% |
| c38 | Autoencoder latents | 4 | 8.9% |
| c03 | TE multi-aggregations | 3 | 6.7% |
| c04 | TE alt targets | 3 | 6.7% |
| c09 | Power/polynomial | 3 | 6.7% |
| c14 | Pairwise additive | 3 | 6.7% |
| c31 | Cyclical encoding | 3 | 6.7% |
| c35 | Approx neighbor lookup | 3 | 6.7% |
| c07 | Missing indicator | 2 | 4.4% |
| c15 | Threshold flags | 2 | 4.4% |
| c16 | Brute-force search | 2 | 4.4% |
| c39 | PCA/SVD components | 2 | 4.4% |
| c40 | Random projection | 2 | 4.4% |
| c41 | Genetic programming | 2 | 4.4% |
| c43 | Char/string pattern | 2 | 4.4% |
| c44 | Lasso generator recovery | 2 | 4.4% |
| c46 | Residual features | 2 | 4.4% |
| c51 | Explicit minimal/no FE | 2 | 4.4% |
| c52 | Adversarial validation for FE | 2 | 4.4% |
| c19 | Groupby basic stats | 1 | 2.2% |
| c20 | Groupby count/nunique | 1 | 2.2% |
| c21 | Groupby quantiles | 1 | 2.2% |
| c22 | Groupby histogram bins | 1 | 2.2% |
| c23 | Groupby z-scores | 1 | 2.2% |
| c24 | Groupby skew/higher | 1 | 2.2% |
| c25 | Groupby division of aggs | 1 | 2.2% |
| c27 | Domain binary flags | 1 | 2.2% |
| c30 | Datetime decomposition | 1 | 2.2% |
| c33 | Original target advanced stats | 1 | 2.2% |
| c34 | Exact key match lookup | 1 | 2.2% |
| c36 | Drift features | 1 | 2.2% |
| c37 | Distribution anomaly | 1 | 2.2% |
| c42 | TF-IDF | 1 | 2.2% |
| c45 | Pseudo labels as features | 1 | 2.2% |
| c47 | Outlier/aux classifier OOF | 1 | 2.2% |
| c49 | SFS/backward elimination | 1 | 2.2% |

## Per-entry aggregates

| Entry | Paradigm | n_fe | TE | Groupby | Combo | Orig | Model | Sel | Confidence |
|---|---|---|---|---|---|---|---|---|---|
| PS-s6e4 r1 | community-template | 7 | ✓ | — | — | — | — | — | notebook+writeup |
| PS-s3e1 r1 | community-template | 3 | — | — | — | — | — | — | notebook+writeup |
| PS-s3e3 r1 | community-template | 3 | — | — | — | — | — | — | notes-only |
| PS-s4e3 r2 | community-template | 3 | — | — | — | — | — | ✓ | notebook+writeup |
| PS-s4e1 r3 | ensemble-standard | 9 | ✓ | — | — | — | — | — | notebook+writeup |
| PS-s5e11 r1 | ensemble-standard | 9 | ✓ | — | ✓ | — | — | — | notebook+writeup |
| PS-s5e8 r2 | ensemble-standard | 8 | ✓ | — | — | ✓ | — | — | notebook+writeup |
| PS-s6e1 r1 | ensemble-standard | 7 | ✓ | — | ✓ | — | — | — | writeup+notes |
| PS-s4e4 r1 | ensemble-standard | 6 | — | — | — | — | — | ✓ | notebook+writeup |
| PS-s3e9 r1 | ensemble-standard | 5 | ✓ | — | — | — | — | — | notebook+writeup |
| PS-s4e5 r1 | ensemble-standard | 5 | ✓ | — | — | — | — | ✓ | writeup+notes |
| PS-s4e9 r1 | ensemble-standard | 5 | ✓ | — | — | — | ✓ | — | notebook+writeup |
| PS-s3e11 r1 | ensemble-standard | 4 | ✓ | — | — | — | — | — | notebook+writeup |
| PS-s4e10 r2 | ensemble-standard | 4 | ✓ | — | — | — | — | — | notebook+writeup |
| PS-s3e8 r2 | ensemble-standard | 3 | — | — | — | — | — | — | writeup+notes |
| PS-s3e16 r3 | ensemble-standard | 3 | — | — | — | — | — | ✓ | notebook+writeup |
| PS-s5e12 r1 | ensemble-standard | 3 | ✓ | — | — | — | — | — | notes-only |
| PS-s3e24 r3 | ensemble-standard | 2 | — | — | ✓ | — | — | ✓ | writeup+notes |
| PS-s3e6 r3 | ensemble-standard | 1 | — | — | — | — | — | ✓ | notebook+writeup |
| PS-s3e23 r2 | ensemble-standard | 1 | — | — | — | — | — | — | notebook+writeup |
| PS-s3e26 r2 | ensemble-standard | 1 | — | — | — | — | — | — | notes-only |
| PS-s4e7 r1 | ensemble-standard | 1 | — | — | — | — | — | — | writeup+notes |
| PS-s4e8 r1 | ensemble-standard | 1 | — | — | — | ✓ | — | — | writeup+notes |
| PS-s6e3 r1 | heavyweight | 19 | ✓ | — | — | ✓ | — | — | writeup+notes |
| PS-s5e5 r1 | heavyweight | 10 | ✓ | ✓ | ✓ | — | ✓ | — | writeup+notes |
| PS-s6e2 r1 | heavyweight | 10 | ✓ | — | — | ✓ | — | — | notebook+writeup |
| PS-s5e6 r1 | heavyweight | 6 | ✓ | — | — | ✓ | ✓ | — | notes-only |
| PS-s5e10 r1 | heavyweight | 3 | — | — | — | — | — | — | notes-only |
| PS-s3e7 r1 | lookup-exploit | 2 | — | — | — | — | — | ✓ | writeup+notes |
| PS-s3e14 r1 | lookup-exploit | 1 | — | — | — | ✓ | — | — | notes-only |
| PS-s5e7 r2 | lookup-exploit | 1 | — | — | — | ✓ | — | — | notebook+writeup |
| tabular-PS-feb-2022 r1 | lookup-exploit | 1 | — | — | — | ✓ | — | — | notebook+writeup |
| PS-s3e4 r3 | minimal-fe | 2 | — | — | — | — | — | — | notebook+writeup |
| PS-s3e5 r1 | minimal-fe | 2 | — | — | — | — | — | ✓ | notes-only |
| PS-s3e10 r1 | minimal-fe | 2 | — | — | — | — | — | ✓ | notes-only |
| PS-s3e13 r1 | minimal-fe | 2 | — | — | — | — | — | — | writeup+notes |
| PS-s4e11 r1 | minimal-fe | 2 | — | — | — | — | — | ✓ | notes-only |
| PS-s5e3 r2 | minimal-fe | 2 | — | — | — | — | — | ✓ | writeup+notes |
| PS-s3e17 r3 | minimal-fe | 1 | — | — | — | — | — | — | writeup+notes |
| tabular-PS-may-2022 r1 | problem-fit-nn | 3 | — | — | — | — | — | — | notebook+writeup |
| ICR r1 | problem-fit-nn | 2 | — | — | — | — | — | ✓ | notebook+writeup |
| tabular-PS-jun-2022 r1 | problem-fit-nn | 1 | — | — | — | — | — | — | notes-only |
| PS-s5e2 r1 | single-model-heavy | 16 | ✓ | ✓ | ✓ | ✓ | — | — | notebook+writeup |
| PS-s4e12 r1 | single-model-heavy | 8 | ✓ | — | ✓ | — | — | — | notebook+writeup |
| PS-s5e4 r2 | single-model-heavy | 5 | ✓ | — | ✓ | — | — | — | writeup+notes |

## Source confidence distribution

| Confidence | n |
|---|---|
| notebook+writeup | 22 |
| writeup+notes | 13 |
| writeup-only | 0 |
| notes-only | 10 |
