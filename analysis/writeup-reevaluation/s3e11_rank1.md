# s3e11 — Rank 1: AmbrosM (ambrosm)

## Identifiers
- **Competition:** [playground-series-s3e11](https://www.kaggle.com/competitions/playground-series-s3e11) — *Regression with a Tabular Media Campaign Cost Dataset*
- **End date:** 2023-06-15 (952 teams) — **earliest entry now (Jun 2023)**.
- **Rank / score:** 1 of 952 · 0.29322 private LB (RMSLE). Top 3 within 0.00002 (photo-finish).
- **Team / Kaggle user:** AmbrosM / [ambrosm](https://www.kaggle.com/ambrosm) — **the recurring technique-source author himself wins**. Previously cited in our analyzed set: s3e23 (log transform + Nyström LR for oscarm524), s4e5 (most-important-feature for aldparis), s4e8 (EDA notebooks for Optimistix). **N=4 connections now**: 1 win + 3 citations as source.
- **Writeup:** [#1: A Zoo of Models](https://www.kaggle.com/competitions/playground-series-s3e11/writeups/ambrosm-1-a-zoo-of-models) (local: `data/writeups/playground-series-s3e11/#1_ A Zoo of Models _ Kaggle.txt`)
- **Notebook (published):** [pss3e11-zoo-of-models](https://www.kaggle.com/code/ambrosm/pss3e11-zoo-of-models) (local).

## Dataset
Regression on `cost`, RMSLE metric, 360,336 train rows. 16 features (mixed). **Duplicate-heavy: 360K rows → 3K unique groups after feature selection.** Public original dataset (`original_data_usage: concat_rows`). `distribution_shift: FALSE` (author explicit: "Training and test data adhere to the same distribution so that we may trust the cv scores completely.")

## What the spreadsheet currently records
- `primary_model: ensemble` (18 models), `dominant_base_model: gbm`, `ensemble_method: weighted_blend`
- `cv_strategy: kfold`, `hyperparameter_tuning: manual`, `scaling: log`
- `models_used`: lightgbm, xgboost, catboost, random_forest, extra_trees, histgb, ridge, nn (**8 model families** — "Zoo of Models")
- **`fe_techniques`: Feature subset selection across models; **duplicate grouping (360K→3000 groups)**; log1p target transformation; store_sqft treated as categorical**
- `original_data_usage: concat_rows`, `encoding_strategy: target_encoding; one_hot_encoding`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0 itemized** | ambrosm's writeup is technique-focused with no citations to other notebooks. He's the *source* in our community map, not a downstream consumer. |
| Cross-author cameos in comments | Sergey Saharovskiy (s3e14 winner one month later, placed 14th here), Möbius (3rd here, well-known Kaggler) | ambrosm comments on Sergey's "record submission count of 71 in 14 days" — flags overfitting risk. Same Sergey later wins s3e14 with lookup-exploit + 8-OOF stack. |
| Author's downstream impact | Heavy — cited as technique-source 3+ times in our analyzed set (s3e23, s4e5, s4e8) | First win-and-source-author documented as both roles in our set. |

## What's actually original to this author
- **"Zoo of Models" approach** — 8 model families × multiple variants = 18 models. Ridge regression for ensemble weights. **Earliest Ridge-as-stacker in our analyzed set** (Jun 2023).
- **Duplicate grouping for training-speed optimization**: 360K rows → 3K unique groups. *"Training with 3000 groups rather than 360'000 samples speeds up the development cycle massively."* New hypothesis on watch — does duplicate-heavy data invite this technique elsewhere?
- **Numerical-disguised-as-categorical detection via partial dependency plot**: noticed `store_sqft` had only 20 unique values + non-monotonic PDP curve → categorical-treated (OHE / TE). Explicit PDP-based feature-type discovery. New methodological technique.
- **log1p(target) + expm1(pred)** for RMSLE — match transformation to loss. Joins LAD-for-MAE (s3e16 Ravi) pattern of **matching loss function / transformation to metric**.
- **Feature subset selection across models**: each model trained on a different feature subset, blended at ensemble level. **Diversity-via-feature-subset N=2 now** (here Jun 2023 → Ravi s3e16 Aug 2023). Predates Ravi's documented case.
- **Hierarchical clustering of model predictions (dendrogram)** for diversity analysis — identified 4 clusters: feature-augmented models, RF/ET, NN, GBDTs. Methodological tool for ensemble selection.
- **Trust-CV-completely** when train/test distribution matches — explicit precondition stated.

## Dataset constraints that shaped this strategy
- **Massive duplication (360K → 3K unique groups)** → enables duplicate-grouping speedup; same insight could be missed by other authors who train on full 360K rows.
- **`distribution_shift: FALSE` + author-verified same-distribution** → unlocks trust-CV-completely mindset; minimal need for LB-probing or anti-greedy submission selection.
- **One numerical-disguised-as-categorical feature (`store_sqft`)** → PDP detection + categorical treatment unlocks signal that other authors might miss.
- **Photo-finish margin (0.00002)** → 18-model zoo + Ridge stacking + diversity-via-feature-subsets handles the marginal-gain regime well.

## Code vs writeup check
- ✓ Notebook (`pss3e11-zoo-of-models`) implements all the techniques described
- ✓ Author shows dendrogram + bar chart + PDP plots in writeup
- ⚠ Specific 18-model variant list and Ridge weight assignments visible only in code

## Headline finding
s3e11 (Jun 2023) is **the earliest entry now** and **the recurring technique-source author (ambrosm) wins here** — confirms our community-graph framing: technique sources are also winners themselves. ambrosm's recipe: 18-model Zoo + Ridge-as-stacker + duplicate-grouping (360K→3K) + numerical-disguised-as-categorical detection via PDP + log1p-for-RMSLE. **Earliest Ridge-as-stacker in our set** (predates by 5+ months everything else). **Earliest "Trust-CV-completely" framing** — predates aldparis's s4e5 (May 2024) and Mahdi's s4e11 (Nov 2024) by 11-17 months. **PDP-based categorical detection** and **duplicate-grouping speedup** are two new methodological techniques that don't appear elsewhere in our set.

## Surprising / unusual
- **AmbrosM wins his own competition** — recurring technique-source author also a 1st place winner. **N=4 connections to ambrosm now**: 1 win at s3e11 + 3 prior citations as source (s3e23, s4e5, s4e8). Like arunklenin (5 entries), ambrosm is a community-graph node.
- **Earliest Ridge-as-stacker in set (Jun 2023)** — predates cdeotte's s5e5 GPU Hill Climbing (May 2025) and later Ridge uses by 5-23 months. **Ridge ensemble was established practice in s3 era.**
- **Duplicate-grouping speedup (360K→3K)** — first time we see explicit duplicate-handling-as-speedup. Unique to duplicate-heavy datasets.
- **PDP-based detection of numerical-disguised-as-categorical** — methodological technique for finding hidden feature types. Hadn't seen this elsewhere in the set.
- **Hierarchical clustering of model predictions (dendrogram)** for diversity analysis — explicit methodological tool. Most other authors just stack many models and hope for diversity; ambrosm validates it.
- **"Trust CV completely" precondition explicit**: same-distribution train/test → trust CV unconditionally. Predates the s4e5 (aldparis) and s4e11 (Mahdi) similar framings by 11-17 months.
- **Sergey Saharovskiy in comments (placed 14th)** — same Sergey who wins s3e14 next month with lookup-exploit + Ridge stacker (which adaubas provided). ambrosm's casual mention of Sergey's "71 submissions in 14 days" is a friendly warning about overfitting; turns out Sergey's discipline improved by s3e14.
- **3 of 4 ambrosm-attributed techniques recur in later writeups**: log-transform (s3e23 oscarm524), important-feature-detection (s4e5 aldparis), EDA depth (s4e8 Optimistix). **The technique-source role of ambrosm is genuine — his writeup at s3e11 is the upstream of those.**
