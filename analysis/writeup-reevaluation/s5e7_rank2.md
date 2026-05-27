# s5e7 — Rank 2: Irfan Ahmad

> **Two notes on this entry:**
> 1. Curated entry is rank-2 per spreadsheet (`finish_rank: 2`); rank-1 was Rapfff (tied at 0.970647), no writeup or notebook for Rapfff in the local set.
> 2. **No discussion writeup exists** in the local set — only the published notebook. The "Public-notebook reuse" and "What's actually original" sections below are *code-only inferences*; we cannot distinguish what the author originated vs. inherited without authorial narrative.

## Identifiers
- **Competition:** [playground-series-s5e7](https://www.kaggle.com/competitions/playground-series-s5e7) — *Predict the Introverts from the Extroverts*
- **End date:** 2025-07-31 (4,329 teams)
- **Rank / score:** **2 of 4,329** · 0.970647 private LB (Accuracy). Top 2 tied at 0.970647; 3rd at 0.970445.
- **Team / Kaggle user:** Irfan Ahmad / [irfanahmad1](https://www.kaggle.com/irfanahmad1)
- **Writeup:** none in local set; spreadsheet `writeup_url` points only to the discussion page sorted by votes
- **Notebook (published):** [introverts-and-extroverts-0-974-competetion-win](https://www.kaggle.com/code/irfanahmad1/introverts-and-extroverts-0-974-competetion-win) (local: `data/writeups/playground-series-s5e7/2nd_introverts-and-extroverts-0-974-competetion-win.ipynb`)

## Dataset
Binary classification of `Personality` ∈ {Extrovert, Introvert}, **Accuracy** metric, **18,524 train rows** (smallest of any writeup in the analysis set — 30–40× smaller than typical s5/s6). 7 features (5 numeric, 2 categorical), **6.21% missing data** (first significant-missing case). Public original dataset available: `extrovert-vs-introvert-behavior-data-backup/personality_dataset.csv`, used for row-level join. Train/test CSVs not in `data/raw/`; schema fully visible in notebook cells 7 and 21.

## What the spreadsheet currently records
- `primary_model: ensemble`, `best_single_model: catboost`, `dominant_base_model: gbm`
- `ensemble_method: weighted_blend` (distinct from `stacking` / `hill_climbing` of other entries — simpler)
- `missing_data_strategy: fill_missing_category` (first non-"none"), `encoding_strategy: label_encoding` (distinct from TE-heavy others)
- `fe_techniques: original data merge as new feature (match_p)` — **a single FE technique, the simplest of any writeup so far**
- `models_used: catboost; xgboost; lightgbm` (3 listed; notebook actually trains 5 — also LightGBM-GOSS and LightGBM-DART)
- `hyperparameter_tuning: optuna` (used to tune ensemble weights and threshold; per-model params are hardcoded as "optimized")
- `n_rows: 18524`, `pct_missing: 6.21`, `metric: Accuracy`

## Public-notebook reuse
**Cannot determine without authorial narrative.** The notebook does not cite other authors in its markdown text (markdown is mostly styled HTML headers with "Step 1 / Step 2..." framing). What we can observe from code:
- `match_p` trick (cell 21) is presented as "KEY INSIGHT!" in the notebook's pedagogical voice — suggests the author considers it the load-bearing move, but doesn't tell us whether he invented it or ported it from a public discussion.
- Per-model hyperparameter dicts are described as "optimized" (e.g., cell 28: `'l2_leaf_reg': 3, 'border_count': 128`) but the Optuna search code is not in the notebook — suggests offline tuning, or possibly inherited tuned values.
- Notebook style is heavily pedagogical (HTML-styled markdown, emoji print statements, "Thank you for following along!") — points to the notebook being written for *beginner audience consumption*, not as a working research log.

## What the code does (in lieu of "what's original")
- **The `match_p` trick (cell 21)** is the *entire FE pipeline*. Deduplicates the public original on all 7 feature columns, then left-joins by feature-tuple. About X% of train and Y% of test rows get a `match_p` value (the original's Personality target) attached. Where no match exists, `match_p` is NaN. This is conceptually the *direct-row-join* analogue of s6e3's snap-feature / KDTree-lookup trick on the IBM original — but exact rather than nearest-neighbor, made possible by the tiny dataset and discrete feature space.
- **Five GBDT variants** (CatBoost native-cat, XGBoost label-encoded, LightGBM, LightGBM-GOSS, LightGBM-DART) — no neural networks. Trained per-model with hardcoded "optimized" params via a `Trainer` wrapper from `koolbox`.
- **Weighted-average ensemble via Optuna** (cell 41) with **negative weights allowed** (`trial.suggest_float(m, -1, 1)`, then normalized) and **simultaneous threshold tuning** (range 0.3–0.7). 500 trials. Mirrors wind1234it's s5e12 negative-weight HC innovation.
- **Final submission picks the single best-CV model** (cell 45), which could be one of the 5 GBDTs or the WeightedAverage — the notebook chooses dynamically rather than committing to the ensemble.
- Missing values filled with `"missing"` string for categoricals (matches `missing_data_strategy: fill_missing_category`).

## Dataset constraints that shaped this strategy
- **Tiny dataset (18K rows)** → forbids the 100+ model ensembles seen in s5/s6 (would overfit). Forces simple architecture: 5 GBDT variants + weighted blend.
- **Few features (7) + small discrete domain** → enables exact row-matching against the original dataset (the `match_p` trick), which would be infeasible with high-cardinality continuous features.
- **Accuracy metric (not AUC) + tied top-2** → threshold tuning becomes a first-class concern (the Optuna search jointly optimizes weights *and* threshold).
- **Significant missing values (6.21%)** → drives the explicit categorical-missing strategy ("fill with `missing` string"), which is unique among the writeups in scope.
- **Public original with row-mergeability** → makes the match_p trick the dominant FE move; everything else is secondary.

## Code vs writeup check
- ✓ Notebook fully implements the spreadsheet-recorded pipeline: load + original-merge + cat fill + label encode + 5-fold CV training of 5 GBDTs + Optuna weighted blend
- ✓ `original_data_usage: yes` and `fe_techniques` accurately captured
- ⚠ Spreadsheet `models_used` lists 3 categories; notebook trains 5 (also LightGBM-GOSS and LightGBM-DART as distinct boosting types)
- ⚠ Spreadsheet `hyperparameter_tuning: optuna` — true for ensemble weights + threshold (cell 41), but per-model params are hardcoded (no per-model Optuna study in the notebook). The "optimized" label in code is unverifiable without the upstream tuning notebook.
- ⚠ No discussion writeup means we lose authorial framing on what made the difference, what was tried-and-discarded, and what was inherited from public discussions.

## Headline finding
s5e7's curated rank-2 entry is the simplest pipeline in the analysis set: **one FE trick (row-merge with public original via `match_p`), 5 GBDT variants, Optuna-tuned weighted blend with threshold search, no neural networks, no stacking, no hill climbing.** The tiny dataset (18K rows) constraint rules out the heavy-ensemble strategies that win larger s5/s6 competitions. The `match_p` row-merge is conceptually the *exact-match* analogue of the s6 *nearest-neighbor* snap-feature / KDTree-lookup family — same constraint coupling (synthetic + known original), different implementation tier (exact-match enabled by small discrete feature space).

## Surprising / unusual
- **Notebook style is pedagogical / beginner-facing** (HTML-styled markdown, emoji prints, "Thank you for following along!" sign-off) — distinct from cdeotte/mahog/tilii's terse research notebooks. Suggests author's primary audience is learners, which may explain why the notebook gets published as the *competition-win* artifact rather than a working pipeline + separate clean version.
- **First entry with accuracy metric**; first with significant missing data (6.21%); first with `n_rows < 100K`. The constraint profile is so different from s5–s6 mainline that most of the meta-architecture patterns (stacking, HC, linear stackers, etc.) don't apply.
- **Negative ensemble weights with simultaneous threshold tuning** (cell 41) shows up months before wind1234it's s5e12 implementation — the negative-weight trick was already in use in the community by July 2025.
- **Cannot verify "What's original" or "Public-notebook reuse" from code alone** — this is the first writeup with this limitation, and a methodological note for future notebook-only evaluations.
