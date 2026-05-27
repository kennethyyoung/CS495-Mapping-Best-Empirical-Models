# s3e6 — Rank 3: Viktor Taran (viktortaran)

> **Note:** Curated entry is rank-3 per spreadsheet. Rank-1 (Sujith K Mandala) and rank-2 (JohnG29) writeups not in set. **Very minimal writeup** (4-bullet tip list, ~10 lines of actual content).

## Identifiers
- **Competition:** [playground-series-s3e6](https://www.kaggle.com/competitions/playground-series-s3e6) — *Regression with a Tabular Paris Housing Price Dataset*
- **End date:** 2023-04-15 (703 teams) — **earliest entry now (mid-Apr 2023)**.
- **Rank / score:** **3 of 703** · 214,935 private LB (RMSE). Wider gaps than typical: 1st-2nd 690, 2nd-3rd 1,645.
- **Team / Kaggle user:** Viktor Taran / [viktortaran](https://www.kaggle.com/viktortaran) — one-off author in our analyzed set.
- **Writeup:** [3rd place](https://www.kaggle.com/competitions/playground-series-s3e6/writeups/viktor-taran-3rd-place) (local: `data/writeups/playground-series-s3e6/3rd place. _ Kaggle.txt`)
- **Notebook (published):** [ps-s-3-e-6](https://www.kaggle.com/code/viktortaran/ps-s-3-e-6) (local).

## Dataset
Regression on house prices (Paris dataset), RMSE metric, 22,730 train rows (small). 17 features (mixed), max_cardinality=2 (very simple binary categoricals). Public original Paris housing dataset.

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: stacking`
- `cv_strategy: repeated_kfold` (5 folds × 10 repeats), `hyperparameter_tuning: optuna`, `encoding_strategy: one_hot_encoding`
- `models_used`: XGBoost, CatBoost, RandomForest, LightGBM (4 GBDTs)
- **`fe_techniques`: Permutation importance for feature selection (per model separately)**
- `original_data_usage: concat_rows`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | Author cites discussion #388361 for original-data link but no notebook ports. |

## What's actually original to this author
- **CAT + XGB + RF as level 1, LGBM as metamodel** — tree-based stacker. Counter to Ridge/mean stacker dominance and to Mahog's s5e11 anti-LGBM-stacker observation. **Tree-based stacker at rank-3 here**; for this competition it worked.
- **Permutation importance per model separately** — applied to each of the 4 base models independently. **Earliest case in set** (Apr 2023); Ravi at s3e16 (Aug 2023) used same technique 4 months later.
- **Repeated KFold (5×10)** — repeated CV for robust scoring. Predates ambrosm's s3e11 (Jun 2023) by 2 months.

## Dataset constraints that shaped this strategy
- **Small dataset (22K rows) + simple binary categoricals (max_card=2)** → standard 4-GBDT stack is well-matched; no exotic FE needed.
- **Wider top-3 gaps (1.6K out of ~214K)** → not photo-finish; reasonable ensemble + careful CV wins top 3.
- **Public original available** → concat for additional training data.

## Code vs writeup check
- ✓ Writeup describes the 4-step approach concisely
- ✓ Notebook available (`ps-s-3-e-6`)
- ⚠ Writeup is ~10 lines of content (4 bullets). Detail comes from the notebook.

## Headline finding
s3e6 (Apr 15, 2023) is **the earliest entry now** by 15 days. **Permutation importance per model separately is observed at s3e6 (Apr 2023)** — predates Ravi at s3e16 (Aug 2023) by 4 months. **Repeated KFold (5×10) at s3e6** predates ambrosm s3e11 (Jun 2023) by 2 months. **LGBM as final metamodel** — tree-based stacker (counter to Ridge/mean/HC pattern). Standard 4-GBDT stack works for this small/simple dataset. Very minimal writeup (4-bullet tip list, ~10 lines) — author's notebook carries the detail.

## Surprising / unusual
- **Tree-based metamodel (LGBM)** at rank-3 — counter to the dominant Ridge/mean/HC stacker pattern. For this small-data simple-feature regime, it worked. **N=2 cases of tree-based stacker** (s3e6 LGBM + s5e8 Mahog CatBoost), both at rank 2-3, both small-to-medium data.
- **Permutation-importance-per-model earliest** (Apr 2023) — predates Ravi's s3e16 (Aug 2023) by 4 months. Common technique but earliest documented case is here.
- **Repeated KFold (5×10) earliest** — predates ambrosm's s3e11 (Jun 2023) by 2 months.
- **Very minimal writeup** (~10 lines, 4 bullets) — among the shortest in set. Notebook-and-tip-list style.
- **One-off author** — Viktor Taran doesn't appear elsewhere in our set as winner.
- **Same-date as s3e7** (Apr 30 next, Apr 15 here) — both April 2023.
