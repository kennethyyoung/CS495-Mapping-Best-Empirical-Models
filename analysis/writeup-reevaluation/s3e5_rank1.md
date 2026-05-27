# s3e5 — Rank 1: Heitor Rapela Medeiros (rapela)

## Identifiers
- **Competition:** [playground-series-s3e5](https://www.kaggle.com/competitions/playground-series-s3e5) — *Ordinal Regression with a Tabular Wine Quality Dataset*
- **End date:** 2023-03-31 (901 teams) — **earliest entry now (Mar 2023)**.
- **Rank / score:** 1 of 901 · 0.59674 private LB (Cohen Kappa — **first Cohen Kappa metric in set**). 2nd: NHopeT 0.59621, 3rd: Gilles Vandewiele 0.59588.
- **Team / Kaggle user:** Heitor Rapela Medeiros / [rapela](https://www.kaggle.com/rapela) — one-off author in our set.
- **Writeup:** [[1st place solution] Single model (RAPIDS XGBoost)](https://www.kaggle.com/competitions/playground-series-s3e5/writeups/heitor-rapela-medeiros-1st-place-solution-single-m) (local: `data/writeups/playground-series-s3e5/[1st place solution] Single model (RAPIDS XGBoost) _ Kaggle.txt`)
- **Notebook (published):** [tpss3e5-1st-place-solution-rapids-xgboost](https://www.kaggle.com/code/rapela/tpss3e5-1st-place-solution-rapids-xgboost) (local).

## Dataset
Ordinal regression on `quality` (multiclass, integer wine quality scores), **Cohen Kappa** metric (first in set), 2,056 train rows (small). 12 features all numeric (max_cardinality=0). Public original Wine Quality dataset available — **Heitor chose NOT to use it** (overfit his local CV).

## What the spreadsheet currently records
- **`primary_model: gbm` (single model!)**, `best_single_model: XGBoost`, `dominant_base_model: gbm`
- **`ensemble_method: none`** — fourth single-model winner in set (after s4e12, s5e2 cdeotte; s5e4 greysky)
- `cv_strategy: stratified_kfold` (10-fold), `hyperparameter_tuning: optuna`
- `models_used: XGBoost` (single family, single model)
- **`fe_techniques: None — FE tried but worsened CV; post-processing with OptimizedRounder for ordinal class cutoffs`**
- `original_data_usage: none` (chose not to use despite availability)

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Specific technique cites | 3 named | (1) **@paddykb's "Regression_OptimiseClassCutoff" notebook** — OptimizedRounder for ordinal class cutoffs (the key post-processing technique). (2) @abhishek (Kaggle Grandmaster) — discussion post. (3) @carlmcbrideellis — mentioned in discussion. |
| **paddykb recurring**: cited at s3e5 (OptimizedRounder), s3e10 (2nd place, GBM commenter), s3e14 (Sergey's FLAML-BFI port source), s4e10 (Omid's all-features-as-categories source) | N=4 entries | paddykb joins the recurring community contributor list. |

## What's actually original to this author
- **Single XGBoost model wins** (no ensemble, no FE, no original data) — **fourth single-model winner in set, EARLIEST (Mar 2023)**. Counter to dominant ensemble pattern. Strategy: focus all effort on one strong model + careful CV + ordinal post-processing.
- **RAPIDS XGBoost (GPU) — earliest documented use in set (Mar 2023)**. *"I started with the RAPIDS XGBoost. For training, I used Kaggle GPUs."* Predates cdeotte's later RAPIDS-heavy approaches (s4e12 Dec 2024) by 9 months. **RAPIDS/cuDF GPU acceleration was established in s3 era.**
- **OptimizedRounder for ordinal regression** — predict continuous values via XGB (`reg:squarederror`), then per-fold optimize class cutoffs on validation predictions for Cohen Kappa. Cuts-finding is itself part of Optuna's objective.
- **Trust-CV discipline against public-LB pressure**: explicit — *"I saw myself going down on the public leaderboard, but in the end, I decided not to use the additional dataset because it was overfitting a lot on my local CV."* Resisted public-LB temptation. Same pattern as ambrosm s3e9/s3e11 trust-CV theme.
- **No-original-data wins** — chose against the dominant "use original" pattern based on CV evidence. **N=1 counter to original-use** at small-data scale; one's data choice depends on what CV says.
- **K=5 vs K=10 explicit comparison** for CV — settled on K=10 as more reliable for this dataset.

## Dataset constraints that shaped this strategy
- **Tiny dataset (2056 rows) + 12 numeric features** → ensembling has diminishing returns vs single optimized model. Heavy FE / multiple base models would overfit.
- **Ordinal target + Cohen Kappa metric** → OptimizedRounder post-processing is natural (predict continuous, round to integer classes by metric-optimized cutoffs).
- **Public original overfits CV** → don't use. Author's data-decision was CV-driven, not "use original by default."
- **RAPIDS XGBoost GPU available** → enables fast Optuna iteration on small-but-tunable problem.

## Code vs writeup check
- ✓ Notebook published implementing the pipeline
- ✓ Writeup details all 4 key components: RAPIDS XGB + StratifiedKFold(10) + Optuna + OptimizedRounder
- ✓ Author confirms data-decision logic + paddykb citation

## Headline finding
s3e5 (Mar 2023) is **the earliest entry now** and the **earliest single-model winner in set (4th total: s3e5 → s4e12 → s5e2 → s5e4)**. **Single RAPIDS XGBoost + OptimizedRounder + Optuna + 10-fold CV** beats ensembles when data is tiny + ordinal target + careful CV. **RAPIDS XGBoost on GPU appears earliest in set (Mar 2023)** — predates cdeotte's s4e12 (Dec 2024) by 9 months. **Now 4 cdeotte-canonized techniques pre-existed in community**: HC (s3e23 oscarm524), brute-force FE (s3e24 arunklenin), Ridge-as-stacker (s3e11 ambrosm), **RAPIDS/cuDF GPU acceleration (s3e5 Heitor)**. **paddykb cited as OptimizedRounder source** — joins the recurring contributor list (N=4 entries citing his work). **No-original-data wins** — author chose to NOT use original based on CV evidence, counter to dominant pattern.

## Surprising / unusual
- **Earliest single-model winner in set** (Mar 2023). N=4 cases now spanning 23 months: s3e5 → s4e12 → s5e2 → s5e4.
- **RAPIDS XGBoost / GPU acceleration earliest documented (Mar 2023)** — 9 months before cdeotte. **Fourth cdeotte-canonized technique confirmed pre-existing**.
- **No-original-data deliberate choice** — counter to dominant pattern. Author's data-decision was CV-driven; original overfit his local CV.
- **First Cohen Kappa metric in set** — ordinal regression-specific.
- **OptimizedRounder for ordinal-class cutoff** — generic technique (predict continuous, optimize integer cutoffs). paddykb's notebook is the source.
- **paddykb cited N=4 times**: s3e5 (OptimizedRounder), s3e10 (commenter), s3e14 (FLAML-BFI port), s4e10 (all-features-as-categories). **paddykb joins recurring contributor list alongside ambrosm/arunklenin/siukeitin (all N=5) and ambrosm-tier.**
- **K=5 vs K=10 explicit comparison** documented — rare methodological detail. Most authors don't justify K choice.
- **Tiny-data single-model wins** here (2K rows) vs s3e13 Umar's tiny-data autoencoder-ensemble wins (707 rows). **At extreme small-data, both single-model + simple-ensemble strategies can win** — depends on metric and signal type.
