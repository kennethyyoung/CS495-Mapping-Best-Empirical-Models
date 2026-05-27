# s3e4 — Rank 3: Ollie Kemp (olliekemp)

> **Caveats:** Curated entry is rank-3 per spreadsheet. **No writeup published** — notebook-only evaluation (like s5e7). Spreadsheet's `winner_1st: not described` and `winner_2nd: not described` reflect incomplete capture from leaderboard JSON (actual 1st: Dmitry, 2nd: Numanynklr per local leaderboard.json).

## Identifiers
- **Competition:** [playground-series-s3e4](https://www.kaggle.com/competitions/playground-series-s3e4) — *Binary Classification with a Tabular Credit Card Fraud Dataset*
- **End date:** 2023-01-30 (641 teams) — **earliest entry now (Jan 30, 2023)**.
- **Rank / score:** **3 of 641** · 0.83163 private LB (ROC AUC). Top 3: Dmitry 0.83268 → Numanynklr 0.83238 → Ollie Kemp 0.83163.
- **Team / Kaggle user:** Ollie Kemp / [olliekemp](https://www.kaggle.com/olliekemp) — one-off author in our set.
- **Writeup:** **none**.
- **Notebook (published):** [3rd-place-solution-ensemble-catboost](https://www.kaggle.com/code/olliekemp/3rd-place-solution-ensemble-catboost) (local). 17 cells.

## Dataset
Binary classification of credit card fraud, ROC AUC metric, 219,129 train rows. 30 features all numeric (PCA-anonymized V1-V28 + Time + Amount per the original Kaggle Credit Card Fraud structure). Heavy class imbalance (fraud is rare). **No public original used** (the original Credit Card Fraud is the basis but author doesn't merge).

## What the spreadsheet currently records
- `primary_model: gbm`, `best_single_model: catboost`, `dominant_base_model: gbm`
- `ensemble_method: mean_blend`, `cv_strategy: kfold` (4-fold), **`rare_class_handling: undersample`** (first explicit undersample value)
- **`hyperparameter_tuning: custom`** (first "custom" value — author's own random_jump tuner)
- `models_used: catboost` (single family)
- **`fe_techniques: aggregates`** (V_sum, V_min, V_max, V_avg, V_std, V_pos, V_neg, V_range over V columns)
- `original_data_usage: none`, `scaling: standard`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **Unknown** — no writeup to confirm | Notebook is self-contained; no notebook ports cited in code comments. |
| Imports | `imblearn.under_sampling.RandomUnderSampler` for class-imbalance handling | Standard imbalance library. |

## What the code does (in lieu of "what's original")
- **Custom `CatTune` class**: joint hyperparameter tuner that searches (n_estimators, max_depth, learning_rate, l2_leaf_reg) + (sample_rate, weight0, weight1) simultaneously. **Treats sampling rate and class weights as tunable hyperparameters alongside CatBoost params.** Grid search over a 12-combination space.
- **Aggregate-statistics FE** over V columns: V_sum, V_min, V_max, V_avg, V_std, V_pos (count > 0), V_neg (count < 0), V_range. **Row-wise statistics FE family** (same as aldparis s4e5, oscarm524 s3e23) — natural for PCA-anonymized features.
- **Random-jump pseudo-ensemble**: take best grid-search params → add Gaussian noise to each hyperparameter (lr += N(0, 0.001); depth += round(N(0, 1)); etc.) → train new CatBoost → average predictions over 500 iterations. **500-model ensemble via hyperparameter perturbation** — same model family, perturbed hyperparameters, predictions averaged.
- **RandomUnderSampler + class weights** for fraud-class imbalance — undersampled training data + per-class weight adjustment.
- **CatBoost Pool object** with weighted samples + label-aware undersampling.

## Dataset constraints that shaped this strategy
- **Heavy class imbalance (credit card fraud) + binary + ROC AUC** → undersampling + class weights are natural; jointly tuning sampling rate + weights is principled.
- **PCA-anonymized V columns + all-numeric** → aggregate statistics over V columns is the dominant FE (no domain knowledge possible due to anonymization).
- **219K rows** → enough data for 500-iteration random-jump ensemble; not so much that pure brute-force breaks down.
- **No public original** (the original IS the data generator basis) → can't use exploit-original toolkit.

## Code vs writeup check
- ✗ **No writeup.** Pipeline reconstructed from notebook alone.
- ✓ Notebook is self-contained and well-organized (17 cells with markdown headers): imports, CatTune class, FE function, data load, hyperparam tuning, random-jump pseudo-ensemble, submission.

## Headline finding
s3e4 (Jan 30, 2023) is **the earliest entry now** and shows **rare-class handling via joint hyperparameter tuning of sampling rate + class weights** alongside CatBoost params (first explicit `rare_class_handling: undersample`). **Custom random-jump pseudo-ensemble** (500 CatBoost models with Gaussian-perturbed hyperparameters, averaged) — alternative to Optuna or standard grid search. **Aggregate-statistics FE over PCA-anonymized V columns** — row-wise statistics family applied to anonymized-numeric regime. **First "custom" hyperparameter tuning value** in spreadsheet (vs Optuna/random_search/manual).

## Surprising / unusual
- **Joint hyperparameter tuning of model params + sampling rate + class weights** — author's CatTune class treats imbalance handling as a tunable hyperparameter, not a fixed preprocessing step. Principled approach to class-imbalance.
- **Custom random-jump pseudo-ensemble** as alternative to Optuna — author adds Gaussian noise to each hyperparameter and re-trains. **500-iteration averaging via hyperparameter perturbation.** Different from cdeotte's "save all Optuna trial OOFs" approach (s6e1) but related principle: many slightly-different-hyperparameters models for diversity.
- **First explicit `rare_class_handling: undersample`** in set. Most other writeups don't mention class-imbalance handling explicitly (or have balanced datasets).
- **Aggregate statistics over PCA-anonymized features** — row-wise FE family applied to anonymized-numeric regime where domain-knowledge FE is impossible.
- **Notebook-only evaluation**: like s5e7 Irfan, can't separate origination from inheritance without authorial narrative.
- **Spreadsheet's `winner_1st: not described`** is a data quality gap — actual 1st-2nd from leaderboard.json are Dmitry / Numanynklr. Worth noting for methodology audit.
- **Earliest single-model entry by 2 months** before s3e5 (Heitor's Mar 2023 RAPIDS XGB). But s3e4 is rank-3, s3e5 is rank-1 — different positions.
