# s5e4 — Rank 2: Farukcan Saglam (greysky)

> **Note:** Curated entry is rank-2 per spreadsheet. Rank-1 was cdeotte (writeup "1st Place - RAPIDS cuML Stack - 3 Levels" exists locally but is not in the coded set). This re-evaluation is greysky's rank-2 writeup. Notebook `podcast-model-training.ipynb` is the published 6-cell minimal training script; the heavy FE work lives in a separately-referenced `greysky/podcast-dataset-generator` notebook **not in our local set**.

## Identifiers
- **Competition:** [playground-series-s5e4](https://www.kaggle.com/competitions/playground-series-s5e4) — *Predict Podcast Listening Time*
- **End date:** 2025-04-30 (3,310 teams)
- **Rank / score:** **2 of 3,310** · 11.50787 private LB (MSE — RMSE-scale ~3.39). Top 3: cdeotte 11.44833 → greysky 11.50787 → stopwhispering 11.53591. 1st place won by a *wide* margin (0.06 MSE) for once — not a photo-finish.
- **Team / Kaggle user:** Farukcan Saglam / [greysky](https://www.kaggle.com/greysky) — appears in cdeotte's s6e3 references (PS S5E4 LGBM port `lgbm-8200.ipynb`)
- **Writeup:** [2nd Place | Single LightGBM and Target Encoding](https://www.kaggle.com/competitions/playground-series-s5e4/writeups/farukcan-saglam-2nd-place-single-lightgbm-and-targ) (local: `data/writeups/playground-series-s5e4/2nd Place _ Single LightGBM and Target Encoding _ Kaggle.txt`)
- **Notebook (published):** [podcast-model-training](https://www.kaggle.com/code/greysky/podcast-model-training) (local: `data/writeups/playground-series-s5e4/podcast-model-training.ipynb`) — 6 minimal cells: load parquet → cast cats → fit LGBM → predict → submit. The 1552-feature FE pipeline lives in a separate notebook ([podcast-dataset-generator](https://www.kaggle.com/code/greysky/podcast-dataset-generator)) not in our local set.

## Dataset
Regression on `Listening_Time_minutes`, MSE metric, 750K train rows. 11 features (mixed), 2.83% missing, **max_cardinality=100** (highest in set — `Podcast_Name` is high-cardinality categorical, enabling deep TE combinatorics). No explicit mention of public original dataset (`original_data_usage: not_described`).

## What the spreadsheet currently records
- `primary_model: gbm`, `best_single_model: lightgbm`, `dominant_base_model: gbm`
- **`ensemble_method: none`** — first entry with no ensembling at all (single model, no stacking, no HC, no weighted blend)
- **`cv_strategy: none`** — author admits no CV during final training; one-fold for FE impact checks only
- **`models_used: lightgbm`** — single family, single model class
- **`hyperparameter_tuning: none`** — author kept the same params throughout (due to 4-hour training time)
- `fe_techniques`: target_encoding_pairs (**1-6 way**), interaction_features, rounding_features, te_descriptive_stats
- `original_data_usage: not_described`, `max_cardinality: 100`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported into solution | **0** | greysky describes his own pipeline; no inbound ports cited. |
| External dataset used as input | 1 | Author's *own* `podcast-listening-huge-dataset` (Kaggle Dataset he published with the pre-engineered 1552-feature parquet) — the heavy FE happens upstream of the published training notebook |
| Cross-author flow (forward) | Yes | cdeotte (1st place) commented: *"I reviewed and studied all your code during the competition and incorporated ideas into my final solution."* greysky's rank-2 work fed directly into cdeotte's rank-1 ensemble. Later, greysky's s5e4 LGBM notebook is one of the 39 references cdeotte ports in s6e3 (`lgbm-8200.ipynb`). |
| Cross-author flow (backward, mentioned in comments) | Yes | greysky to cdeotte: *"Thanks to your answers in the discussions, I used cuDF and cuML for the first time for data manipulation. If I hadn't used those libraries, I wouldn't have been able to conduct enough experiments to achieve 2nd place."* |

## What's actually original to this author
- **Single-LightGBM, no-ensemble, no-CV winning strategy** — a *minimalist counter-aesthetic* to the cdeotte/mahog/tilii multi-model ensemble pattern. Won 2nd by ensuring one model has every possible signal extracted, rather than diversifying across models.
- **1552-feature FE pipeline from 11 base features** (138× expansion). Composed of:
  - **6-way Target Encoding combinatorics** on 12 base/rounded columns (pair_size = 1..6). Goes deeper than cdeotte's 4-way in s5e6 (162 combos there) — likely producing thousands of TE features that the descriptive-stats aggregations summarize.
  - **Descriptive statistics on TE column values**: mean/std/min/max aggregated globally, by pair_size, by source column. Reduces TE-combo-explosion to fixed-dimensional features.
  - **Rounded interaction features**: `Mul_Hpp_Elm = Host_Popularity_% × round(Episode_Length)`, similar Gpp variant, and rounded-then-halved versions of three numerics.
- **Kaggle parallel-notebook experimentation pattern**: greysky runs 5 experiments in parallel using Kaggle's notebook quota, then 5 more, etc. ~1 hour per experiment with 1552 features. Different from cdeotte's local-GPU + RAPIDS approach to the same scale.
- **LGBM hyperparameters tuned for high-feature-count regime**: `colsample_bytree=0.25` (low — only sample 25% of features per tree), `max_depth=15`, `num_leaves=480`, `n_iter=12000` (high), `learning_rate=0.008` (low). Author: "There are a huge number of features with strong predictive power. Because of that, I set a low colsample_bytree and high max_depth and num_leaves."

## Dataset constraints that shaped this strategy
- **High-cardinality categorical (max=100) + many numeric features → exhaustive multi-way TE combinatorics is extremely productive**. The 1552-feature pipeline is feasible because every TE combination has enough rows per group to compute stable statistics. 6-way TE wouldn't work on a tiny dataset.
- **MSE/RMSE regression metric + wide top-3 margin (0.06)** → unlike photo-finish competitions where every 0.0001 matters, this one rewards getting ONE model genuinely strong. Greysky's strategy of "make one model see every signal" is well-matched to a margin where ensemble noise reduction is overkill.
- **CPU-only constraint** (greysky trains on Kaggle CPUs) → drives the strategy toward fewer but larger experiments rather than many GPU iterations. The 4-hour training time per experiment forced low hyperparameter tuning.
- **Public original not explicitly used** → unlike most s5/s6 winners. greysky's strategy doesn't depend on the exploit-original toolkit; the in-data signal is enough at this scale.

## Code vs writeup check
- ✓ Published `podcast-model-training.ipynb` is minimal (6 cells): imports, load parquet, set cat columns, fit LGBM with the exact hyperparameters listed in writeup, predict, submit. Confirms `objective='l2'`, `n_iter=12000`, `max_depth=15`, `learning_rate=0.008`, `num_leaves=480`, `colsample_bytree=0.25`.
- ⚠ **The 1552-feature FE pipeline is NOT in the published training notebook** — author references a separate `greysky/podcast-dataset-generator` notebook with the actual FE code. We don't have it locally. The training notebook just loads the pre-built parquet.
- ⚠ The training notebook uses just one seed (random_state=42); writeup mentions "5 different seeds" for the actual submission — the multi-seed averaging code isn't shown.
- ⚠ Spreadsheet `cv_strategy: none` is accurate (no CV folds in the training notebook), but writeup mentions one-fold CV for feature-impact checks — minor nuance.

## Headline finding
greysky won rank-2 with **the minimalist counter-aesthetic to the s5/s6 ensemble pattern**: a single LightGBM model on a 1552-feature pipeline (built from just 11 base features via 6-way TE combinatorics + descriptive stats + rounding interactions), no CV, no ensembling, no hyperparameter tuning. The competition's wide top-3 margin (0.06 MSE) made this viable where photo-finish competitions would not. Notably, cdeotte (1st place with a 3-level cuML stack) explicitly *studied greysky's code during the competition* and "incorporated ideas" — concrete bidirectional cross-author flow within a single competition. greysky's s5e4 LGBM later became one of the 39 references cdeotte ports into s6e3's KGMON Playbook.

## Surprising / unusual
- **First single-model winner in the analysis set** — counter-evidence to the universal-ensembling assumption. The "many OOFs at linear-stacker scale" coupling explicitly does not apply.
- **No CV, no hyperparameter tuning, no ensembling** — minimalist trifecta. Author explicit: long training time made tuning impractical; he focused all effort on FE instead.
- **6-way TE combinatorics** — extends beyond cdeotte's 4-way in s5e6. Combined with descriptive-statistics aggregation (mean/std/min/max of TE values across combos), reduces what would be a runaway feature count to a manageable 1552.
- **Bidirectional cross-author flow within a single competition** confirmed explicitly: cdeotte studied greysky's code mid-competition, greysky learned cuDF/cuML from cdeotte's discussions. They finished 1st and 2nd respectively with very different strategies but enriched by each other's contributions.
- **CPU-only + Kaggle parallel-notebook quota** as an alternative to GPU-heavy approaches. Different hardware constraint, different experimentation pattern, same competitive results.
- **Wide top-3 margin (0.06 MSE)** — first competition in the s5/s6 set where 1st was not a photo-finish. Suggests photo-finish margins may be the *exception* rather than the rule when we look across more competitions.
