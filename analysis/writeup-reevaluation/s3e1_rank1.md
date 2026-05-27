# s3e1 — Rank 1: Kirderf

## Identifiers
- **Competition:** [playground-series-s3e1](https://www.kaggle.com/competitions/playground-series-s3e1) — *Regression with a Tabular California Housing Dataset*
- **End date:** 2023-01-31 (689 teams) — **earliest entry now (Jan 12, 2023 writeup date)**.
- **Rank / score:** 1 of 689 · 0.55224 private LB (RMSE). 2nd: jcerpent (Jose Cáliz, same as s3e7's 2nd place) 0.55274, 3rd: NY 0.55292.
- **Team / Kaggle user:** Kirderf / [kirderf](https://www.kaggle.com/kirderf) — one-off author in our set.
- **Writeup:** [That was a surprise! Here is the 1st place solution....](https://www.kaggle.com/competitions/playground-series-s3e1/writeups/kirderf-that-was-a-surprise-here-is-the-1st-place-) (local: `data/writeups/playground-series-s3e1/That was a surprise! Here is the 1st place solution.... _ Kaggle.txt`)
- **Notebook (published):** [ps-s3e1-coordinates-key-to-victory](https://www.kaggle.com/code/dmitryuarov/ps-s3e1-coordinates-key-to-victory) (local) — **this is @dmitryuarov's FE notebook that Kirderf ported, not Kirderf's own winning notebook**.

## Dataset
Regression on California `MedHouseVal`, RMSE metric, 37,137 train rows. 9 features all numeric (max_cardinality=0) — California housing with latitude/longitude/MedInc/HouseAge etc. Public original California Housing dataset (`original_data_usage: concat_rows`).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: stacking` (3-level via AutoGluon internal)
- `cv_strategy: repeated_kfold`, **`hyperparameter_tuning: automated`** (AutoGluon handles), `missing_data_strategy: automated`, `scaling: automated`
- `models_used`: XGBoost, LightGBM, CatBoost, RandomForest, NN (all selected by AutoGluon's TabularPredictor)
- **`fe_techniques`: Coordinate-based geographic features (from public notebook)**
- `original_data_usage: concat_rows`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **1** | **@dmitryuarov's "ps-s3e1-coordinates-key-to-victory" notebook** — the entire FE pipeline (coordinate-based geographic features). Kirderf's own contribution = AutoGluon + this FE. |
| Academic citation | AutoGluon-Tabular paper (Erickson et al. 2020, arxiv 2003.06505) | Cites the academic paper for the framework. |
| Cross-author cameo | **@innixma (Nick Erickson, AutoGluon lead developer) commented**: *"This is awesome! I'm the lead developer of AutoGluon, and it is very rewarding to see it being used to achieve 1st place... AutoML system is able to assist Kaggle Grandmasters."* | **innixma's earliest engagement** documented in set (Jan 2023) — later commented on aldparis s4e5 (May 2024). **16-month documented engagement** by AutoGluon's author with Playground community. |

## What's actually original to this author
- **AutoGluon TabularPredictor as the entire training pipeline**: 8-fold trained XGB+LGBM+CatBoost+RF+NN ensemble with weighted ensemble + bootstrap aggregation + **3-level internal stacking** — all internally managed by AG. Different from human-crafted multi-model ensembles.
- **Fork @dmitryuarov's coordinate-based FE + AutoGluon = winning combo**. Author explicit: *"Manual FE before the training was important as well for the final score, so native end-to-end automl didn't get the 1st place."* **Pure AutoML wouldn't have won; FE port + AutoML was needed.**
- **Surprised-author win** ("That was a surprise! Here is the 1st place solution...") — **4th surprised-author win in set** (Bill Cruise s3e3, Umar s3e13, Mart Preusse s4e9, Kirderf s3e1).
- **"AutoGluon for AutoML novelty in Jan 2023"** — The Devastator's comment: *"It is really amazing that an AutoML system came up 1st on a competition. I don't remember it ever happening before."* Kirderf's win was framed as a milestone for AutoML in tabular Kaggle.

## Dataset constraints that shaped this strategy
- **California housing dataset with strong geographic signal** (latitude/longitude) → coordinate-based FE is the dominant lever (dmitryuarov's notebook title is literally "coordinates key to victory"). AutoGluon's generic ensembling handles the rest.
- **Small dataset (37K rows) + 9 features** → AutoGluon's 8-fold + 3-level stacking is well-matched scale-wise.
- **Public original Cal Housing dataset** → concat for training data augmentation.

## Code vs writeup check
- ✓ Writeup describes the AutoGluon + dmitryuarov FE pipeline
- ✓ Local notebook is dmitryuarov's FE source (Kirderf didn't publish his own pipeline notebook separately)
- ⚠ Kirderf's actual training pipeline (AutoGluon configuration, post-processing) not directly published

## Headline finding
s3e1 (Jan 12, 2023) is **the earliest entry now** and **the earliest AutoGluon-handles-everything winner in set** (Jan 2023). Predates Mahdi's s4e11 AutoGluon-as-ensembler (Nov 2024) by 22 months, ISoft's s3e17 AutoML-stack-of-stacks (Sep 2023) by 8 months. **AutoGluon was an established winning strategy by Jan 2023.** **innixma's earliest engagement** in our analyzed set (Jan 2023) — 16-month documented Playground engagement (Jan 2023 → May 2024 s4e5 comment). **Pure AutoML wouldn't have won** — author explicit: dmitryuarov's coordinate-based FE port + AutoGluon was the winning combo. **N=4 surprised-author wins** (Kirderf adds to Bill Cruise / Umar / Mart Preusse). **Fork-with-FE-additions N=4** (here Kirderf forked dmitryuarov's FE-only notebook + added AutoGluon training on top).

## Surprising / unusual
- **Earliest AutoGluon-handles-everything winner in set** (Jan 12, 2023). At the time, The Devastator commented this was unprecedented for AutoML in Kaggle: *"I don't remember it ever happening before."*
- **innixma (AutoGluon lead) commented** — earliest tool-author engagement in our set (Jan 2023). 16-month documented Playground series engagement.
- **Author's explicit "pure AutoML wouldn't have won"** — FE port + AutoML hybrid was needed. **Pure-AutoML alone is rarely enough**, even when it does the heavy lifting.
- **N=4 surprised-author wins now**: Kirderf ("that was a surprise!") joins Bill Cruise, Umar, Mart Preusse. All small-data (or high-variance LB) competitions.
- **Fork-with-FE-additions N=4** (Kirderf + Bill Cruise + Moonlit + Mart Preusse). Pattern variants: fork-base-model-add-FE (Bill Cruise), fork-OOFs-add-blending (Moonlit), fork-FE-add-AutoML (Kirderf), fork-NN-add-OOFs (Mart Preusse).
- **dmitryuarov's "coordinates key to victory" notebook** — coordinate-based FE community contribution. Author's notebook title literally says it's the key technique. **Geographic FE for geographic datasets** as obvious-but-effective insight.
- **2nd place is Jose Cáliz (jcerpent)** — same Jose Cáliz who placed 2nd at s3e7 (Apr 2023) with Hardy Xu winning. Cross-competition recurring competitor.
