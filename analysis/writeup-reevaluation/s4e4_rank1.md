# s4e4 — Rank 1: Johannes Heller (stopwhispering)

## Identifiers
- **Competition:** [playground-series-s4e4](https://www.kaggle.com/competitions/playground-series-s4e4) — *Regression with an Abalone Dataset*
- **End date:** 2024-04-30 (2,606 teams) — **earliest entry now (Apr 2024)**.
- **Rank / score:** 1 of 2,606 · 0.14374 private LB (RMSLE). 2nd-3rd at 0.14411–0.14412 (~0.0004 gap to 1st — wider than other tight cases).
- **Team / Kaggle user:** Johannes Heller / [stopwhispering](https://www.kaggle.com/stopwhispering) — placed 3rd at s5e10 (Tilii's win) and 13th at s5e3 (cdeotte's small-data).
- **Writeup:** [1st Place Solution for the Regression with an Abalone Dataset Competition](https://www.kaggle.com/competitions/playground-series-s4e4/writeups/johannes-heller-1st-place-solution-for-the-regress) (local: `data/writeups/playground-series-s4e4/1st Place Solution for the Regression with an Abalone Dataset Competition _ Kaggle.txt`)
- **Notebooks (published):** 3 notebooks locally — `abalone-feature-engineering-preprocessor.ipynb` (the FE pipeline, 41 cells), `abalone-classic-ml-models.ipynb`, `abalone-eda-adversarial-validation.ipynb`. **Unusual breadth of public notebooks** for one author in one comp.

## Dataset
Regression on `Rings` (integer 1-29, RMSLE metric), 90,615 train rows. 8 features (7 numeric + 1 categorical `Sex` with M/F/I — max_cardinality=3). No missing data. **`distribution_shift: TRUE`** (third case after s5e12, s5e3) — original Abalone dataset (UCI) is distribution-shifted from synthetic train; author uses original *for training in each fold, never for validation*.

## What the spreadsheet currently records
- `primary_model: ensemble` (49 models), `best_single_model: autogluon` (CV 0.14592), `dominant_base_model: gbm`
- `ensemble_method: weighted_blend` (Nelder-Mead on OOFs), `cv_strategy: kfold` (NOT stratified — author explicit), **`hyperparameter_tuning: bayesian`** (WandB Sweeps)
- `models_used`: lightgbm, xgboost, catboost, hist_gradient_boosting, random_forest, autogluon (6 families; **no neural networks** — author anti-NN-for-tabular stance)
- **`fe_techniques: automated_fe (OpenFE), feature_selection (sequential)`** — first OpenFE use in set
- `encoding_strategy: one_hot_encoding`, `scaling: standard`, `original_data_usage: concat_rows`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **2 itemized** | (1) @endofnight17j03's ANN ensemble — added at 17% weight to the final blend (the only ANN in the ensemble). (2) Prajwal Anagani's (@inagana) **"XGB Classifier with Softmax Regression Head"** — adopted despite author admitting *"I still don't know why it works."* |
| Specific technique cites | @siukeitin (broccoli beef) — custom MSLE loss for LGBM | siukeitin again — same author cited at s4e5, s4e8, s4e10 (recurring technique source). |
| Academic citation | **OpenFE** (Zhang et al. 2022, NeurIPS) — automated feature generation tool | First academic-tool citation in set. Hypothesis on watch: automated FE tools as alternatives to hand-crafted FE. |
| Cross-author flow | Prajwal Anagani's regression-head trick adopted by 1st place; visible in comments. Stopwhispering's own work doesn't get cited in later s5/s6 writeups in our set. |

## What's actually original to this author
- **OpenFE pipeline + Sequential Feature Selection per model family**: OpenFE generates many candidate features (`freq(Shell_weight)`, `(Whole_weight/Shucked_weight)`, `log(Whole_weight)`, etc.); SFS keeps ~20 best per model family (LGBM/XGB/CatBoost individually).
- **49-model Nelder-Mead weighted blend with NEGATIVE coefficients summing to 0.997**: author quote — *"seemed cheesy to me but consistently outperformed coefficients clipped at min=0.0 and scaled to sum to 1.0. Thus I kept the optimized coefficients."* **Negative weights N=4 now** (s4e5 Ridge, s5e7 Optuna, s5e12 HC, s4e4 Nelder-Mead) — portable across stackers.
- **Train-on-original-in-fold, never-validate-on-original**: distribution-shift handling. Use original Abalone as training augmentation in each CV fold, but validate only against synthetic competition rows. **Predates s5e12 post-cutoff CV by 20 months** — different operationalization of "validate on what test resembles."
- **Custom loss functions for RMSLE metric**: LGBM custom MSLE, XGB `reg:squaredlogerror`, log1p/expm1 for others. Implementation rigor for non-standard metric.
- **Anti-NN-for-tabular stance** (explicit): *"In an earlier tabular data competition I tried different neural network architectures only to observe that none of them is competitive. I guess the papers claiming ANNs are finally on a par with GBDTs for tabular data haven't done proper preprocessing and fine-tuning."* Counter-pattern to most other s4 winners who include NNs.
- **MLOps**: custom Python package for trainer/CV/prediction code, Kaggle API + local PyCharm workflow, WandB Sweeps for Bayesian HP optimization. Explicit MLOps takeaway — same theme as Cross Sellers s4e7.
- **Heavy-tail prediction failure as a documented "did not work"**: max prediction was 20 Rings (29 in train); SMOTE/augmentation/outlier exclusion all worsened CV. Reports it as a known gap rather than hiding it.

## Dataset constraints that shaped this strategy
- **Distribution shift between original Abalone and synthetic train** → train-on-original-only-not-validate scheme. Author explicit: validating on original would mislead since LB resembles synthetic, not original.
- **RMSLE metric + integer-discrete target (Rings 1-29) + heavy tail** → custom loss functions per model family; Classifier-with-Regression-Head trick works because target is discrete.
- **Small dataset (90K rows) + only 8 base features** → automated FE (OpenFE) becomes the FE strategy — too few base features for cdeotte-style combinatorics, but a small search space is well-matched to AutoFE tools that generate candidate features systematically.
- **Single categorical (Sex with 3 cats)** → only OHE matters; no TE-combinatorics path.
- **Moderate margin (~0.0004 to 2nd)** → 49-model ensemble has marginal returns but not at the photo-finish level of other winners.

## Code vs writeup check
- ✓ Published `abalone-feature-engineering-preprocessor.ipynb` (41 cells) implements the FE pipeline: Ratio features generator, etc. Confirms OpenFE-style transformations.
- ✓ Published `abalone-eda-adversarial-validation.ipynb` documents the distribution-shift discovery (adversarial validation = training a classifier to distinguish train vs test; high accuracy implies shift).
- ⚠ The 49-model training pipeline + Nelder-Mead weight optimization is NOT in the published notebooks. The actual ensemble code is referenced but not local.
- ⚠ OpenFE feature generation code not directly visible; FE preprocessor notebook shows downstream transformations.

## Headline finding
s4e4 (Apr 2024) is the **earliest entry now** and introduces **OpenFE (academic automated-FE tool)** to the analysis set — alternative to hand-crafted FE for datasets with few base features. Author's recipe: OpenFE-generated features → SFS to ~20 per model family → 49 GBDTs with WandB Bayesian-tuned hyperparameters → Nelder-Mead weighted blend with negative coefficients (N=4 for this technique now). **Anti-NN-for-tabular** explicit stance (counter-pattern to most other s4 winners). Distribution-shift handling via train-on-original-in-fold-only-not-validate predates s5e12's post-cutoff CV by 20 months. Stopwhispering's MLOps discipline (custom Python package, WandB Sweeps) matches the Cross Sellers s4e7 theme — **MLOps as a recurring s4-era pattern**.

## Surprising / unusual
- **OpenFE (academic automated-FE tool) as primary FE strategy** — first in set. Cites Zhang et al. 2022 NeurIPS paper. Adds a new technique-source category: academic tools/papers, not just public notebooks.
- **Anti-NN-for-tabular explicit stance** — *"papers claiming ANNs are on par with GBDTs for tabular data haven't done proper preprocessing and fine-tuning."* Counter-pattern; most other s4-s6 winners include NNs (TabM, RealMLP, DeepTables, etc.).
- **"Classifier with Softmax Regression Head" (XGB multi:softprob + softmax regression head)** — unusual technique credited to Prajwal Anagani; author admits *"I still don't know why it works."* Worth tracking forward.
- **Negative-weight ensemble N=4** spans 13 months and 4 stacker families: s4e4 Nelder-Mead (Apr 2024), s4e5 Ridge (May 2024), s5e7 Optuna (Jul 2025), s5e12 HC (Dec 2025). The cancellation-via-negative-weight pattern is solidly portable.
- **Train-on-original-only-no-validate scheme** for distribution-shift handling — different from s5e12's cutoff CV and s5e3's year-grouping. Three different distribution-shift handling techniques across 3 competitions.
- **Author published 3 notebooks** for this comp (FE preprocessor, classic ML models, EDA + adversarial validation). Multiple-notebook publishing style. Possibly a thoroughness/portfolio pattern of certain authors.
- **MLOps as theme (custom Python package, Kaggle API, WandB Sweeps)** — matches Cross Sellers s4e7. MLOps discipline is an early-s4 recurring theme that may have predated cdeotte-era ad-hoc starter notebooks.
- **Adversarial validation** explicitly used (its own published notebook) — detecting train-test distribution shift via classifier separability. New technique in set worth tracking.
