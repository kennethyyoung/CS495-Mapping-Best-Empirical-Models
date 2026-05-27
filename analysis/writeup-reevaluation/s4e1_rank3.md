# s4e1 — Rank 3: Iqbal Syah Akbar (iqbalsyahakbar)

> **Note:** Curated entry is rank-3 per spreadsheet — **first rank-3 entry in the set**. Rank-1 (Nikolay Slobodchuk) writeup not in set.

## Identifiers
- **Competition:** [playground-series-s4e1](https://www.kaggle.com/competitions/playground-series-s4e1) — *Binary Classification with a Bank Churn Dataset*
- **End date:** 2024-01-31 (3,632 teams) — **earliest entry now (Jan 2024)**.
- **Rank / score:** **3 of 3,632** · 0.90321 private LB (ROC AUC). Top 3: 0.90585 → 0.90462 → 0.90321 (~0.001 gaps each).
- **Team / Kaggle user:** Iqbal Syah Akbar / [iqbalsyahakbar](https://www.kaggle.com/iqbalsyahakbar) — author: *"I have finally reached top 3 in Playground Series after 11 months."*
- **Writeup:** [3rd Place Solution: CatBoost Encoding Galore](https://www.kaggle.com/competitions/playground-series-s4e1/writeups/iqbal-syah-akbar-3rd-place-solution-catboost-encod) (local: `data/writeups/playground-series-s4e1/3rd Place Solution_ CatBoost Encoding Galore _ Kaggle.txt`)
- **Notebook (published):** [ps4e1-3rd-place-solution](https://www.kaggle.com/code/iqbalsyahakbar/ps4e1-3rd-place-solution) (local). 53 cells.

## Dataset
Binary classification of `Exited` (bank churn), ROC AUC metric, 165,034 train rows. 13 features (mixed). **max_cardinality=2797** (likely `Surname` — high-cardinality text-like categorical column, ~3K unique names). Public original bank-churn dataset (`original_data_usage: yes`).

## What the spreadsheet currently records
- `primary_model: ensemble` (7 models), `best_single_model: catboost`, `dominant_base_model: gbm`
- `ensemble_method: weighted_blend` (Ridge classifier for weights), `cv_strategy: stratified_kfold` (5-fold for dev, **30-fold for submission**)
- `hyperparameter_tuning: optuna`, `original_data_usage: yes`
- `models_used`: logistic_regression, neural_network, xgboost, lightgbm, catboost (5 families; 3 CatBoost variants)
- **`fe_techniques: tfidf_svd, feature_creation, interaction_features, numeric_type_casting`** — TF-IDF+SVD is new
- `encoding_strategy: target_encoding`, `scaling: standard`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Specific technique cites | 3 named | **@arunklenin** — TF-IDF vectorization + TruncatedSVD on text-like features (credit-line); @aspillai — feature engineering ideas (Sun_Geo_Gend_Sal, etc.); @paddykb — data-leakage post-processing |
| **arunklenin recurring AGAIN** | Yes (earliest now) | **arunklenin spans the entire 27-month period** of our analysis: s4e1 (Jan 2024, TF-IDF+SVD source), s4e3 (Mar 2024, port source), s4e7 (Jul 2024, Cross Sellers team member), s6e3 (Mar 2026, cdeotte's references). Most-spanned single contributor by far. |
| Cross-author cameo | paddykb (152nd here), aspillai (11th here) | paddykb later cited at s4e10 ("all-features-as-categories"). Community continuity from Jan 2024 onward. |

## What's actually original to this author
- **TF-IDF + TruncatedSVD on text-like categorical + encode the SVD components as NEW categorical features via CatBoost encoding**: double-layer technique. Treat `Surname` as a text column → TF-IDF → SVD to 4 components → cast components as integers → CatBoost-encode them. Novel meta-FE.
- **3 different CatBoost variants** with different bootstrap types (none, Bayesian, Bernoulli), all at +0.902 CV. Diversity-via-bootstrap-strategy within the same model family.
- **CatBoost encoder is order-sensitive** discovery: `has_time=True` parameter + put original dataset **BEFORE** competition train when concatenating → best results. Implementation-level discovery unique to this writeup.
- **Three encoder types**: CatBoost built-in, category-encoders' CatBoost Encoder, M-Estimate Encoder — used for different model families (LR/NN like CatBoost Encoder; XGB/LGBM dislike too much CatBoost encoding → use M-Estimate too).
- **30-fold CV for submission** (5-fold for dev) — 12-hour run. Higher fold count for submission stability than typical 5-10 fold.
- **Within-pipeline preprocessing for leakage prevention**: *"I'm a freak when it comes to leakage prevention in cross-validation"* — every preprocessing step inside each model pipeline, not pre-computed. Same leakage-discipline theme as Cross Sellers s4e7 and stopwhispering s4e4.
- **LR used as encoding-experiment subject**: low-performance model used to test which features benefit from category-encoders CatBoost Encoder before applying to higher-performance models.
- **Multiple-concatenation-of-original-as-augmentation**: author notes (didn't fully exploit) that concatenating original dataset **twice** would have given best private LB.

## Dataset constraints that shaped this strategy
- **High-cardinality text-like column (Surname, ~3K unique)** → TF-IDF+SVD becomes viable. Standard TE-only path wouldn't capture text patterns.
- **Public original dataset + order-sensitive CatBoost encoder** → original-before-competition concat order matters; non-trivial implementation detail.
- **Bank churn dataset with mixed feature types** (numeric, categorical, text-like) → 3 encoder types + multi-pipeline approach is well-matched.
- **Wider top-3 margin (0.00123 to 1st)** than s4e3/s4e4 → 7-model + Ridge stacker + 30-fold is enough; not at the photo-finish meta-ensemble engineering level.

## Code vs writeup check
- ✓ Published notebook (53 cells) implements the full pipeline: 3 encoder classes, FE functions (nullify, salary/age/balance rounder, feature_generator, svd_rounder, FeatureDropper, Categorizer), 7 models with within-pipeline preprocessing
- ✓ Spreadsheet `fe_techniques` matches: TF-IDF+SVD, feature creation (AllCat, ZeroBalance), interaction features, numeric type casting (×100, ×10)
- ⚠ The 30-fold submission run + Ridge ensemble weight optimization is described in writeup but exact submission-time code may not be the published notebook's exact configuration

## Headline finding
s4e1 (Jan 2024) is the **earliest entry in the set** and introduces several techniques new to our analysis: **TF-IDF + SVD on text-like categorical → encode SVD components via CatBoost** (double-layer FE), **CatBoost-encoder-order-sensitivity** discovery, **30-fold CV for submission stability**. **arunklenin's contributions span the entire 27-month period**: TF-IDF+SVD here (Jan 2024) → port source at s4e3 (Mar 2024) → Cross Sellers team at s4e7 (Jul 2024) → cdeotte's s6e3 references (Mar 2026). The community network was robust from at least Jan 2024 — **paddykb, aspillai, arunklenin all appear in Jan 2024 ecosystem and recur through later writeups in our set.** Iqbal's writeup is one of the most technique-dense in the set: 7 models, 3 encoder types, double-layer SVD-then-encode FE, 30-fold submission CV.

## Surprising / unusual
- **First rank-3 entry in set** — documents the faithful-coding rule continues to apply (we evaluate whatever rank the spreadsheet codes).
- **TF-IDF + SVD on text-like Surname column** — first text-FE in set. The bank churn dataset's high-cardinality `Surname` is essentially a text feature; treating it as such enables otherwise-unavailable signal.
- **arunklenin spans Jan 2024 → Mar 2026** (27 months across 4 of our analyzed entries). **Most-recurring single community contributor** in the analysis set. Specific contribution here: TF-IDF+SVD technique that Iqbal credits.
- **CatBoost-encoder-order-sensitivity** is a subtle technical discovery. Most authors don't even know CatBoost-encoder's `has_time` matters. Reflects unusual depth of attention to implementation details.
- **NN in ensemble already in Jan 2024** — small architecture (32-64-16-4-1 LeakyReLU) but present. **Revises the earlier "GBDT-only-no-NN was early-2024 default" hypothesis**: NN inclusion was already happening in Jan 2024, just at smaller scale. The s4e3/s4e4 (Mar/Apr 2024) GBDT-only stance was author-specific (Moonlit, stopwhispering), not era-wide.
- **Ridge classifier for ensemble weights** = linear stacker — extends the linear-stacker coupling back to Jan 2024. **Linear stacker N=14 now** in chronological span Jan 2024 → Feb 2026.
- **Author's 11-month wait for top-3** — gives a sense of the typical Kaggler trajectory: months of regular participation before podium. Worth tracking how long other authors took to first podium.
