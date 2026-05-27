# s3e26 — Rank 2: Hardy Xu (hardyxu52)

> **Note:** Curated entry is rank-2 per spreadsheet. Rank-1 (kailai, same as s4e3 winner) writeup not in set. **No notebook published** — author explicit in comments: *"all my work was done locally."*

## Identifiers
- **Competition:** [playground-series-s3e26](https://www.kaggle.com/competitions/playground-series-s3e26) — *Multi-Class Prediction of Cirrhosis Outcomes*
- **End date:** 2024-01-01 (1,661 teams — smallest in set) — **earliest entry now**, December 2023 playground series.
- **Rank / score:** **2 of 1,661** · 0.39230 private LB (Log Loss — **first Log Loss metric**). Top 3: kailai 0.39104 → Hardy Xu 0.39230 → Fengqian 0.39420.
- **Team / Kaggle user:** Hardy Xu / [hardyxu52](https://www.kaggle.com/hardyxu52) — **same author as s4e10 1st place winner** (10 months later). Trajectory: 2nd at s3e26 (Jan 2024) → 1st at s4e10 (Oct 2024).
- **Writeup:** [2nd Place: with help from NNs](https://www.kaggle.com/competitions/playground-series-s3e26/writeups/hardy-xu-2nd-place-with-help-from-nns) (local: `data/writeups/playground-series-s3e26/2nd Place_ with help from NNs. _ Kaggle.txt`)
- **Notebook:** **none** — author worked locally; nothing published.

## Dataset
Multiclass (3 cirrhosis outcomes: survival / death / transplant), **Log Loss** metric (first in set), 7,905 train rows (**smallest in set**). 19 features (mixed). max_cardinality=3 (small categoricals — edema, stage).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: stacking` (NN as stacker)
- `cv_strategy: not_described`, `hyperparameter_tuning: optuna`
- `models_used`: lightgbm, xgboost, nn (3 model types)
- **`fe_techniques: Piecewise linear encoding (PLE) for continuous features; embedding layers for categorical features (edema, stage); value rounding for GBT features`**
- `original_data_usage: not_described`, `n_rows: 7,905`, `max_cardinality: 3`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | Author doesn't cite Kaggle notebooks; cites academic paper and blog instead. |
| Academic citations | 2 | (1) **PLE paper** — arxiv 2203.05556 (Gorishniy et al. "On Embeddings for Numerical Features in Tabular Deep Learning", NeurIPS 2022). (2) Sebastian Raschka's "Deep Learning for Tabular Data" blog post. |
| Acknowledgments | None named | Unusual — most s4-era authors thank specific contributors. Hardy Xu's writeup is purely technique-focused. |

## What's actually original to this author
- **PLE (Piecewise Linear Encoding) for continuous features in NN** — first appearance of this academic technique in our set. Applied to each continuous feature individually; embedding layers for categorical (edema, stage); binary features fed as 0/1. NN alone achieved private LB 0.401 (top 10%) — strong individual model.
- **NN-as-final-stacker** with custom architecture innovations:
  1. **Per-class-probability weights** (each class within each model's prediction gets its own weight) — not a single scalar weight per model
  2. **Cross-prediction weight calculation** (each model's weights computed using ALL 3 model predictions, not just itself)
  3. These changes gave +0.004 boost vs simple average
- **NN-as-final-stacker N=2 now**: s3e26 (Hardy Xu, Jan 2024, NN with custom weight architecture) → s4e9 (Mart Preusse, Sept 2024, DeepTables NN with OOFs as features). **Earliest case now.**
- **10-Optuna-hyperparameter-set averaging per GBDT** (XGB and LGBM) — variance reduction via hyperparameter-space averaging.
- **Author trajectory**: explicitly started this competition to *learn NN for tabular*: *"I had trouble getting good results with them in past competitions, often finding they performed worse in the private leaderboard."* Successfully reframed his own NN-skepticism.

## Dataset constraints that shaped this strategy
- **Smallest dataset in set (7,905 rows) + multiclass + Log Loss** → small-data regime; standard heavy-ensembling overfits. Author's choice: 3 models + custom NN stacker is well-matched.
- **Mostly continuous features + few categoricals (edema, stage)** → PLE for continuous + embeddings for categoricals is a NN-friendly preprocessing scheme.
- **No public original** (`original_data_usage: not_described`) → can't exploit-original; FE has to come from within-data signal.
- **Log Loss metric (probability-calibration-sensitive)** → stacking with NN (which learns calibration implicitly) matches the metric well; simple averaging may distort probability calibration.

## Code vs writeup check
- ✗ **No notebook published.** Author confirms in comments: all work done locally. Pipeline reconstructed from writeup text only.
- ✓ Spreadsheet `fe_techniques` accurately captures the PLE + embeddings + GBT-rounding combination.
- ⚠ Custom NN-stacker architecture (per-class weights, cross-prediction weight calculation) is described in writeup but not reproducible without code.
- ⚠ The 10 Optuna hyperparameter sets aren't enumerated.

## Headline finding
s3e26 (Dec 2023 / Jan 2024) is **the earliest entry now** and introduces **PLE (Piecewise Linear Encoding)** — an academic technique from a 2022 NeurIPS paper — for NN-friendly preprocessing of continuous features. Hardy Xu's NN-as-final-stacker with custom per-class-probability weights pushes back the earliest NN-stacker case to Jan 2024. **NN-as-final-stacker N=2 now** (s3e26 Hardy Xu → s4e9 Mart Preusse). Hardy Xu's trajectory continues into our analysis set: 2nd here, then 1st at s4e10 (Oct 2024). **Smallest dataset in set (7,905 rows)** — small-data regime drove the minimal-models + careful-stacker recipe.

## Surprising / unusual
- **First Log Loss metric** in set. **First multiclass classification with 3 small classes** (cirrhosis outcomes).
- **Smallest dataset in set (7,905 rows)** — smaller even than s5e7 (18K) and s5e3 (2K → but s5e3's effective signal was 366 rows after original-augmentation accounting).
- **PLE (Piecewise Linear Encoding) — first academic-paper-cited technique** in set (also new: arxiv 2203.05556). OpenFE at s4e4 was a similar academic-tool citation. **Academic-paper-as-technique-source emerges as a new acknowledgment category.**
- **NN-as-final-stacker pushed back to Jan 2024** (Hardy Xu, s3e26) — earliest case. Previously thought s4e9 (Sept 2024, Mart Preusse) was earliest.
- **Custom NN-stacker weight architecture**: per-class weights + cross-prediction weight calculation. Sophisticated design vs typical scalar-weight stackers.
- **No acknowledgments to other Kagglers** in writeup — unusual; technique-focused only. Cites paper + blog, not community. Different style from s4-era community-heavy thank-yous.
- **Hardy Xu trajectory documented across set**: 2nd at s3e26 (Jan 2024) → 1st at s4e10 (Oct 2024). Within-author improvement over 10 months.
- **Author's NN-skepticism-overcome motivation**: started competition specifically to improve NN-for-tabular knowledge. Motivation-driven technique experimentation rather than pure competition-driven.
