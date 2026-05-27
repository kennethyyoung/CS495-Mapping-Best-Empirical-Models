# s3e23 — Rank 2: Oscar Aguilar (oscarm524)

> **Note:** Curated entry is rank-2 per spreadsheet (tied with 1st at 5 decimals: 0.79429). **Notebook IS available** (44-cell `ps-s3-ep23-eda-modeling-submission.ipynb`) despite session context suggesting otherwise.

## Identifiers
- **Competition:** [playground-series-s3e23](https://www.kaggle.com/competitions/playground-series-s3e23) — *Binary Classification with a Software Defects Dataset*
- **End date:** 2023-11-30 (1,702 teams) — **earliest entry now (Nov 2023)**.
- **Rank / score:** **2 of 1,702** · 0.79429 private LB (ROC AUC) — *tied at 5 decimals with 1st place (theod)*. 3rd at 0.79427.
- **Team / Kaggle user:** Oscar Aguilar / [oscarm524](https://www.kaggle.com/oscarm524) — recurring community contributor (cited at s4e5 by aldparis, s4e8 by Optimistix, s5e5 by cdeotte). His own trajectory: 2nd at s3e23 (Nov 2023) → recurring podium finisher through s5/s6.
- **Writeup:** [#2 Solution | 8 Models Ensemble](https://www.kaggle.com/competitions/playground-series-s3e23/writeups/oscar-aguilar-2-solution-8-models-ensemble) (local: `data/writeups/playground-series-s3e23/#2 Solution _ 8 Models Ensemble _ Kaggle.txt`)
- **Notebook (published):** [ps-s3-ep23-eda-modeling-submission](https://www.kaggle.com/code/oscarm524/ps-s3-ep23-eda-modeling-submission) (local). 44 cells with extensive version history (Oct 2-11, 2023).

## Dataset
Binary classification of software defects, ROC AUC metric, 101,763 train rows. 22 features all numeric (max_cardinality=0). **No public original used** (`original_data_usage: none`). Top 3 within 0.00002 — photo-finish (1st/2nd tied at 0.79429).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, **`ensemble_method: hill_climbing`**
- `cv_strategy: stratified_kfold`, `hyperparameter_tuning: manual`, `scaling: log`
- `models_used`: lightgbm, xgboost, catboost, random_forest, extra_trees, histgb, logistic_regression, nn (8 families)
- **`fe_techniques: Log transformation of all features (core improvement); PCA/t-SNE/clustering tried but failed`**
- `original_data_usage: none`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Specific technique cites | 2 named + 1 cited HC discussion | (1) **@ambrosm** — log-transform suggestion (discussion #445015) + Nyström LogisticRegression notebook (boosted LB 0.7907 → 0.79099). (2) **@sauravpandey11** — Simple ANN notebook (boosted LB 0.79099 → 0.79101). HC method via competition discussion #444784. |
| **ambrosm recurring**: cited at s3e23 (Nov 2023), s4e5 (aldparis May 2024), s4e8 (Optimistix Aug 2024) | N=3 entries spanning 9 months | Like arunklenin, ambrosm is a recurring technique-source in the community. Specializes in EDA-driven FE suggestions and unusual model variants (Nyström LR). |

## What's actually original to this author
- **Hill Climbing ensemble of 8 models** — pushes HC use back to **November 2023**. Predates omidbaghchehsaraei's s4e10 (Oct 2024) by 11 months, cdeotte's s5e5 (May 2025) by 18 months. **HC was already standard practice in s3 era.**
- **Layered ensemble construction**: start with 6 tree-based models + HC → 0.7907; add Nyström LR → 0.79099; add NN → 0.79101. Incremental validation per addition.
- **Nyström LogisticRegression** — kernel-approximation-via-Nyström-features applied to LR. Unusual model variant; sourced from ambrosm. First time Nyström methods appear in our set.
- **Pre-Optuna era** — `hyperparameter_tuning: manual` confirms; multiple competition writeups in s3 era manage with manual + small grid HP work, not heavy Optuna sweeps.

## Dataset constraints that shaped this strategy
- **All-numeric features (no categoricals) + skewed distributions** → log-transform of all features becomes the dominant FE. Same constraint family as s4e5 (aldparis) and s3e24 (Ravi). **Three all-numeric writeups so far, each with a different dominant FE technique**: row-wise statistics (s4e5), brute-force combinations (s3e24), log transformation (s3e23).
- **No public original** → can't exploit-original; FE has to come from within-data transformations. Same as s4e5.
- **Photo-finish margin (0.00002)** → 8-model HC ensemble is appropriate; selection-via-HC handles the marginal-gain regime.
- **101K rows + 22 features** → standard mid-data regime; no need for cdeotte-style heavy FE or single-model heroics.

## Code vs writeup check
- ✓ Notebook has 44 cells with detailed version history (Oct 2-11, 2023 — built iteratively over 10 days)
- ✓ Notebook contents (per first-cell TOC): EDA, Baseline Modeling 1.0, Baseline Modeling 2.0 (with HC added in version 2)
- ✓ Author's published notebook is the OOF source; the 8-model HC ensemble is built on top
- ⚠ The final 8-model HC submission may not be exactly the published notebook's last version (writeup notes "I decided to select another ensemble that had a slightly higher LB score")

## Headline finding
s3e23 (Nov 2023) is **the earliest entry in the set** and pushes back the Hill Climbing technique to November 2023 — **18 months before cdeotte canonized "GPU Hill Climbing" at s5e5 (May 2025)**. HC was the established community ensembling approach by Nov 2023, sourced from a competition discussion (#444784). Adds another community member (Oscar Aguilar / oscarm524) to the recurring-contributor list (now cited at s4e5, s4e8, s5e5 by other authors). **Log transformation of all features** as a primary FE technique when features are skewed-numeric (no categoricals) — credited to @ambrosm. Reinforces the pattern: **all-numeric writeups have author-specific dominant FE** (row-wise stats, brute-force combos, log transform), no universal pattern.

## Surprising / unusual
- **HC pushed back to Nov 2023** (18 months before cdeotte's "GPU Hill Climbing" canonization). Combined with omidbaghchehsaraei s4e10 and arunklenin's brute-force FE at s3e24, **at least 3 of cdeotte's later "named" techniques pre-existed in the community** (HC, brute-force FE combinations, dual-mode original use).
- **oscarm524 trajectory documented**: 2nd at s3e23 (Nov 2023) → recurring podium finisher through s5/s6 (cited as 4th-12th in our s5/s6 entries).
- **ambrosm recurring as technique-source** (N=3 entries spanning 9 months): s3e23 (log-transform + Nyström LR), s4e5 (most-important-feature suggestion), s4e8 (EDA notebooks). Another community-flow node alongside arunklenin.
- **Nyström LogisticRegression** — first appearance of kernel-approximation methods in our set. Doesn't recur (probably too niche).
- **44-cell notebook with detailed version history** (Oct 2-11, 2023) — gives unusual visibility into iterative development. Other authors don't typically publish version-by-version notebook timelines.
- **All-numeric writeups so far show different dominant FE per author**: s4e5 row-wise stats (aldparis), s3e24 brute-force combos (Ravi), s3e23 log transform (oscarm524). No universal "all-numeric → X" pattern; the FE choice is author-specific even within this constraint family.
- **Tied at 5 decimals with 1st place** (both at 0.79429). Photo-finish margin even tighter than most other entries in set.
