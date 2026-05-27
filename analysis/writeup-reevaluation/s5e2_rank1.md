# s5e2 — Rank 1: cdeotte (Chris Deotte)

## Identifiers
- **Competition:** [playground-series-s5e2](https://www.kaggle.com/competitions/playground-series-s5e2) — *Backpack Prediction Challenge*
- **End date:** 2025-02-28 (3,393 teams)
- **Rank / score:** 1 of 3,393 · 38.61628 private LB (MSE). Top 3 margin moderate (~0.017 to 3rd). cdeotte's 4th 1st-place in our analysis set.
- **Team / Kaggle user:** Chris Deotte / [cdeotte](https://www.kaggle.com/cdeotte) — fourth cdeotte entry
- **Writeup:** [1st Place - Single Model - Feature Engineering](https://www.kaggle.com/competitions/playground-series-s5e2/writeups/chris-deotte-1st-place-single-model-feature-engine) (local: `data/writeups/playground-series-s5e2/1st Place - Single Model - Feature Engineering _ Kaggle.txt`)
- **Notebook (published):** [first-place-single-model-lb-38-81](https://www.kaggle.com/code/cdeotte/first-place-single-model-lb-38-81) (local: `data/writeups/playground-series-s5e2/first-place-single-model-lb-38-81.ipynb`) — 36 cells with extensive markdown. **Simplified 138-feature version** (T4 GPU 16GB); cdeotte's actual final had 500 features on A100 80GB. The published notebook STILL wins 1st place. This is the notebook cdeotte ports into s6e3 as `xgb3-1200.ipynb`.

## Dataset
Regression on `Price`, MSE metric. **Combined train = 4 million rows** (train.csv 300K + training_extra.csv ~3.7M). Spreadsheet's `n_rows: 300000` is the primary train only — undercount; the extra is the bulk and is loaded together in the notebook. 10 features: 1 numeric (`Weight Capacity (kg)`) + 8 categorical + target, plus 1.91% missing. Author quote: *"4 million rows. This means we do not need to fear overfitting train. We can make hundreds/thousands of new features and every time our CV improves our LB will improve too!"* — the dataset size is the strategy-shaping constraint. Public original dataset used (`original_data_usage: merge_columns` — columns-only, "manufacture suggested retail price" feature).

## What the spreadsheet currently records
- `primary_model: gbm`, **`best_single_model: XGBoost`**, `dominant_base_model: gbm`
- **`ensemble_method: none`** — single XGBoost model. Second single-model entry (after s5e4 greysky).
- `models_used: XGBoost` (single family, single model)
- `hyperparameter_tuning: none` — author iterated on FE rather than hyperparams (manual depth/lr from experimentation)
- `cv_strategy: kfold`, `original_data_usage: merge_columns` (columns only — distinct from cdeotte's later s5e3/s5e6 dual-mode)
- `fe_techniques` is unusually granular: groupby aggs (mean/std/count/min/max/nunique/skew); groupby histogram bins; groupby quantiles; NaN base-2 encoding; numerical rounding/binning; digit extraction from floats; categorical column combinations (all pairs); division features
- `n_rows: 300000` — **inaccurate** (combined train is 4M; spreadsheet appears to count train.csv only). Worth flagging.

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks / discussions explicitly cited | **1 itemized** | Digit-extraction-from-float technique credited to @jordanbarker (linked discussion post). cdeotte's own starter notebook is the structural basis. |
| Author cited *by* others | Yes (heavy) | This `first-place-single-model-lb-38-81` notebook is referenced in cdeotte's s5e3 writeup (as "original-as-columns" technique source), s5e6 writeup (Feb 2025 entry), and is ported into s6e3 as `xgb3-1200.ipynb`. cdeotte's own most-self-referenced notebook in the analysis set. |

## What's actually original to this author
- **The "single powerful model" philosophy explicitly stated**: *"My favorite solution in a Kaggle competition is a powerful single model versus a large ensemble."* Won via 300+ XGBoost iterations testing thousands of FE ideas, keeping the best 500 features for the final single XGB.
- **Histogram-binned groupby features** — cdeotte's own invention. *"I had fun inventing this technique. I have never seen it being used before."* Groups Weight Capacity by Price, computes histogram bin counts within each group, returns the counts as features.
- **Quantile-aggregated groupby features** with `QUANTILES = [5,10,40,45,55,60,90,95]` — 8 quantile values per group as 8 features.
- **All-NaNs-as-base-2 column**: packs NaN pattern across categorical columns into a single float feature via `train["NaNs"] += train[c].isna() * 2**i`. Each unique NaN-pattern bitstring becomes its own value. Powerful as a `groupby` key.
- **Rounding-at-different-precisions binning** (`for k in range(7,10)`) for the dominant numeric feature, then groupby on the rounded versions. Manual multi-resolution binning.
- **Float32 digit-extraction** for the dominant numeric column — cited as @jordanbarker's idea but cdeotte scales it across positions 1–9 and uses with groupby.
- **Nested-fold target-aware FE** to prevent leakage: outer fold for non-target FE, inner fold for target-aware aggregations.
- **Division-of-aggregations features**: `count/nunique`, `std/count` — second-order combinations of already-aggregated features.

## Dataset constraints that shaped this strategy
- **4 million rows + relatively few base features (10)** → enough data that a single XGB with 500 engineered features doesn't overfit. cdeotte's strategy decision: single-model + heavy FE replaces multi-model + light FE because the FE+data product saturates the model. Author explicit: "we do not need to fear overfitting train."
- **One dominant numeric feature (Weight Capacity) with strong predictive structure** → enables digit extraction, multi-resolution binning, rounding-then-groupby, quantile-of-Price-per-Weight-Capacity. The FE is heavily focused on extracting structure from this one column.
- **"Weird and unnatural" synthetic data** (author's words) with strong generator artifacts → FE has high marginal returns; nested-fold target-aware groupby tricks become viable.
- **Available public original + author's GPU access** → enables "MSRP-style" merge_columns FE and the cuDF/cuML 4M-row groupby pipeline.
- **Regression + MSE + moderate top-3 margin** → like s5e4 greysky, the margin doesn't require ensemble noise reduction; single-model strength suffices.

## Code vs writeup check
- ✓ Notebook (36 cells) implements the entire pipeline: load 4M rows, NaN-base-2, rounding, digit extraction, cat combinations, nested-fold groupby aggs (mean/std/count/median/min/max/skew/nunique), quantile aggs, histogram aggs, division features, XGBoost training (7 inner × 7 outer folds)
- ✓ Spreadsheet `fe_techniques` field accurately enumerates all techniques in the writeup
- ⚠ Spreadsheet `n_rows: 300000` undercounts the actual combined training data (train.csv 300K + training_extra.csv ~3.7M = 4M loaded together in the notebook). The strategy is shaped by 4M, not 300K.
- ⚠ Notebook is the *simplified 138-feature version* per author; the actual 500-feature winning solution code is not public.
- ⚠ `cv_strategy: kfold` is correct but loses the nested-fold structure (inner for target-aware FE, outer for evaluation).

## Headline finding
s5e2 is cdeotte's **single-model-with-heavy-FE win at 4M rows** — adding a fourth distinct cdeotte recipe to our within-author dataset. The full cdeotte strategy hierarchy is now visible across our 4 entries:
- **Tiny data (~2K, s5e3)**: no FE, equal-weight mean blend of 3 models, kernel SVM
- **Large data (~4M, s5e2)**: single XGB with 500 hand-engineered features
- **Medium data (~750K, s5e5, s5e6)**: many models, GPU HC ensemble
- **Modern KGMON era (~594K, s6e3)**: 4-level stack with LLM-coded models

The s5e2 win directly contradicts the "many OOFs + linear stacker" coupling (no ensemble at all) **and** the "fork-heavy + framework" coupling (only 1 named cite — jordanbarker for digits). This is cdeotte's purest "find every signal with one model" win, viable because 4M rows can absorb 500 features without overfitting.

## Surprising / unusual
- **Single XGB with 500 features beats ensemble approaches** in this competition. Author tested 300+ XGB models and kept the best one — different from his usual ensemble pattern. Concrete evidence that ensemble vs single-model is *data-size and FE-saturation conditional*, not author-conditional.
- **Histogram-binned groupby aggregations are cdeotte's own invention** here and don't appear in other writeups in our set. Worth tracking forward.
- **Spreadsheet `n_rows: 300000` is inaccurate** (actual combined train is 4M). The dataset-size constraint is what drove the single-model strategy; if we used `n_rows` for constraint analysis we'd misclassify this. Methodology note for INDEX.
- **The 138-feature simplified version (Kaggle T4 GPU) STILL wins** — the actual A100/500-feature version is overkill. Suggests the FE plateau is reached well before 500 features for this dataset.
- **Now 4 of our 13 entries are cdeotte**. Within-author analysis is rich: same author wins with 4 different recipes across 4 different competition profiles. The constraint→strategy framing has the strongest single-author support from cdeotte's body of work.
