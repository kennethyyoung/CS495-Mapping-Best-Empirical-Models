# s3e24 — Rank 3: Ravi Ramakrishnan (ravi20076)

> **Caveat:** No notebook published (writeup-only). Curated entry is rank-3.

## Identifiers
- **Competition:** [playground-series-s3e24](https://www.kaggle.com/competitions/playground-series-s3e24) — *Binary Prediction of Smoker Status using Bio-Signals*
- **End date:** 2023-12-31 (1,908 teams) — **earliest entry now (Dec 2023, same month as s3e26 but ends 1 day earlier)**.
- **Rank / score:** **3 of 1,908** · 0.87938 private LB (ROC AUC). Top 3 within 0.00008 (photo-finish).
- **Team / Kaggle user:** Ravi Ramakrishnan / [ravi20076](https://www.kaggle.com/ravi20076) — **same author as s4e7 Cross Sellers team member**. Trajectory: 3rd at s3e24 (Dec 2023) → 1st team at s4e7 (Jul 2024) → cited in s6e3 (Mar 2026).
- **Writeup:** [#3 Private 8 Public approach - simple ensemble with probing](https://www.kaggle.com/competitions/playground-series-s3e24/writeups/ravi-ramakrishnan-3-private-8-public-approach-simp) (local: `data/writeups/playground-series-s3e24/#3 Private 8 Public approach - simple ensemble with probing _ Kaggle.txt`)
- **Notebook:** **none** — author worked locally.

## Dataset
Binary classification of smoker status (bio-signals), ROC AUC metric, 159,256 train rows. **23 features all numeric** (max_cardinality=0, no categoricals). Public original dataset (`original_data_usage: concat_rows`).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, **`ensemble_method: weighted_blend; hill_climbing; stacking`** (3 methods tested)
- `cv_strategy: stratified_kfold` (10×1), `hyperparameter_tuning: none` (manual per-model)
- `models_used`: lightgbm, xgboost, catboost, random_forest, logistic_regression, **tabnet, neural_network, gam** (8 families — first TabNet, first GAM in set)
- **`fe_techniques: Brute-force feature combinations (80-120 kept); permutation importance for feature pruning`** — **brute-force FE search 1 year before cdeotte's s4e12 145K-combo search**
- `original_data_usage: concat_rows`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Specific technique cites | 4 named | **@arunklenin** — "comprehensive EDA + brute-force features" (his `ps3e24-eda-feature-engineering-ensemble` notebook is the explicit FE source); @cv13j0 (pseudo-label notebook); @oscarm524 (reference notebook); @paddykb (LGBM pipeline contributor) |
| **arunklenin recurring AGAIN — now N=5 entries spanning 28 months** | Yes | s3e24 (Dec 2023, **brute-force FE source**) → s4e1 (Jan 2024, TF-IDF+SVD source) → s4e3 (Mar 2024, port source) → s4e7 (Jul 2024, Cross Sellers team member) → s6e3 (Mar 2026, cdeotte's references). **5 of our 26 analyzed entries reference arunklenin's work**, longest-spanning contributor by far. |

## What's actually original to this author
- **Brute-force feature combinatorial search at s3e24 (Dec 2023) — predates cdeotte's s4e12 145K-combo search by exactly 12 months.** Ravi credits **arunklenin** as the source; arunklenin's public notebook had this approach. Ravi adopted at 80-120 features (smaller scale than cdeotte's later 170).
- **Permutation importance for feature pruning** — sklearn-standard technique applied at scale.
- **10×1 stratified k-fold beats 10×3 repeated** — author tested, no improvement from repeats. Different from cdeotte's later repeated-stratified-kfold preference (s5e6, s4e5).
- **8-model-family pipeline including TabNet and GAM**: 3 CatBoost variants, 5 LightGBM variants, 3 XGBoost variants, Random Forest, Logistic Regression, TabNet, MLP, GAM. **First TabNet and first GAM in our set.**
- **"Probing"** as explicit technique — manually modified some model weights in-fold based on LB feedback. Author flags as risky (chose to do it carefully; rejected "blind probing"). Cautionary anti-pattern flagged.
- **Tried 3 ensemble methods** (HC, Optuna, Stacking) — Optuna correlated best with LB → chosen as final. Author's explicit Optuna-vs-others comparison is one of the few in our set.

## Dataset constraints that shaped this strategy
- **All-numeric features (no categoricals)** → TE-on-categoricals path unavailable; brute-force numeric-feature-combination search becomes the FE strategy. Same constraint profile as s4e5 (aldparis, all-numeric).
- **Medium dataset (159K rows)** + binary + ROC AUC + photo-finish margin → multi-model ensembling with careful selection (Optuna) is well-matched.
- **Public original available + community of strong contributors** → fork-heavy + carefully-attributed adoption (Ravi cites 4 specific contributors).

## Code vs writeup check
- ✗ **No notebook published.** Pipeline reconstructed from writeup only.
- ✓ Spreadsheet `fe_techniques` accurately captures brute-force + permutation importance.
- ✓ Spreadsheet `ensemble_method` correctly lists all 3 methods tested.
- ⚠ The specific 80-120 brute-force features list isn't enumerated; the probing weight modifications aren't shown.

## Headline finding
s3e24 (Dec 2023) **pushes back the earliest brute-force-FE-combinatorial-search by 12 months** before cdeotte's s4e12 (Dec 2024) canonical version. The technique was already in use, credited to **arunklenin's public notebook** (who shared it on the s3e24 discussion). cdeotte's later 145K-combo GPU scaling is the *industrial-grade refinement*, not the invention. **arunklenin's contribution now spans 5 entries across 28 months** (Dec 2023 → Mar 2026) — most-spanning single community contributor in the set, **and source of the brute-force-FE pattern that cdeotte later canonized**.

## Surprising / unusual
- **Brute-force FE search 12 months earlier than cdeotte's s4e12 version** — strongly reinforces the "community pre-existed cdeotte's canonization" finding from s4e8/s4e10/s4e7. **cdeotte's Dec 2024 "first 145K-combo GPU search" was scaling an already-known technique, not inventing it.**
- **arunklenin spans 28 months / 5 entries — increases his recurrence from 4 to 5**. Specific contribution traced back: brute-force-FE-combinatorial-search originated in his s3e24 notebook. arunklenin is functionally the most-influential pre-cdeotte community contributor in our analyzed set.
- **First TabNet and first GAM in set.** TabNet appears later in s4e7 (Cross Sellers) and s4e11 (Mahdi); GAM doesn't reappear. Statistical models like GAM are rarely included in modern Kaggle ensembles.
- **"Probing" as explicit technique** (manual weight modification based on LB feedback) — risky meta-technique; author flagged anti-pattern of "blind probing." Worth tracking if other writeups use probing.
- **Ravi Ramakrishnan trajectory documented**: 3rd at s3e24 (Dec 2023) → 1st at s4e7 team (Jul 2024). 7-month within-author progression to a 1st-place finish.
- **Author's explicit takeaway list reflects validation-discipline ethos**: "Rely on CV", "Don't over-complicate", "Model parameter tuning is secondary to FE", "Probe with care." Implicit validation-discipline framing — same theme as Optimistix s4e8.
- **Ends 2023-12-31** (one day earlier than s3e26 which ends 2024-01-01). Both are December 2023 Kaggle Playground entries.
