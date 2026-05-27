# s4e5 — Rank 1: aldparis (adaubas, Adam Daubas)

## Identifiers
- **Competition:** [playground-series-s4e5](https://www.kaggle.com/competitions/playground-series-s4e5) — *Regression with a Flood Prediction Dataset*
- **End date:** 2024-05-31 (2,788 teams) — **earliest entry in the set now (May 2024)**.
- **Rank / score:** 1 of 2,788 · 0.86905 private LB (R2 — first R2 metric in set). Top 3 within 0.00003.
- **Team / Kaggle user:** aldparis / [adaubas](https://www.kaggle.com/adaubas) (Adam Daubas) — referenced by Mahdi Ravaghi at s4e10 ("the implementation that you used and another by @adaubas which included cross-validation and early stopping") for his HC implementation.
- **Writeup:** [#1st place solution](https://www.kaggle.com/competitions/playground-series-s4e5/writeups/aldparis-1st-place-solution) (local: `data/writeups/playground-series-s4e5/#1st place solution _ Kaggle.txt`)
- **Notebook (published):** [pss4e05-1st-place-solution-ensemble-with-ridge](https://www.kaggle.com/code/adaubas/pss4e05-1st-place-solution-ensemble-with-ridge) (local: `data/writeups/playground-series-s4e5/pss4e05-1st-place-solution-ensemble-with-ridge.ipynb`) — 35 cells; **the ensemble/Ridge code only**, not the 30+ GBM training pipelines.

## Dataset
Regression on `FloodProbability`, **R2 metric (first in set)**, 1,117,957 train rows. 21 features **all numeric, no categoricals** (max_cardinality=0), no missing data. **Synthetic data — sum of Poisson distributions** (author's EDA finding); original dataset exists but is "completely different from train dataset" — referenced for EDA only, not used as training data (`original_data_usage: none` is accurate in that respect).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: weighted_blend`
- **`cv_strategy: repeated_stratified_kfold`** (3 repeats × 5 folds — same as cdeotte's s5e6 only)
- `hyperparameter_tuning: optuna`, `original_data_usage: none` (no concat)
- `models_used`: XGBoost, LightGBM, CatBoost, AutoGluon (4 families; 30+ variants)
- `fe_techniques`: Row-wise statistics (sum/std/max); sorted features; count threshold features (nb_sup6/7/8); target encoding on row sum; target transformation (subtract feature mean × 0.1); permutation + backward feature selection
- `metric: R2 Score`, `n_rows: 1,117,957`, `max_cardinality: 0`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **2 itemized** | (1) @mfmfmf3's "AutoGluon Starter" — adapted as one of the OOF sources. Author calls mfmfmf3 *"the real promoter of AutoGluon in this competition."* (2) @igorvolianiuk's "Flood Prediction LGBM." |
| Specific technique cites | @siukeitin (sorted-features-as-FE), @act18l (target transformation idea), @ambrosm (most-important-feature suggestion) | Same siukeitin / ambrosm cited at s4e8, s4e10. **Cross-competition recurring technique sources.** |
| Cross-author cameo | **@innixma (Nick Erickson, AutoGluon co-author) commented**: *"Congrats and welcome to the AutoGluon Hall of Fame!"* | Tool-author engagement with competition writeups. Cross-community link beyond Kaggle. |
| Acknowledgments | @mdoroch, @lashfire, @mattop, @tilii7 (3rd here) | Tilii again present; same community web. |

## What's actually original to this author
- **EDA-driven discovery of generator structure**: dataset is a sum of Poisson distributions. Author discovered that sum of 16-17 of the 17 original features remains Poisson, but sum of 18-20 doesn't (and doesn't in test either). This shaped FE: *understand the generator, not just exploit a public original*.
- **Row-wise statistics FE family** (commensurable-features regime): sum, std, max of each row's feature values. Plus sorted-features (siukeitin), count-thresholds (nb_sup6/7/8), TE-on-row-sum, target transformation that separates "strong signal (sum)" from "noisy signal (deviance from sum)."
- **Ridge meta-learner with `positive=False, fit_intercept=False`** — allows negative weights (Tilii in comments doubted this mattered; author insisted CV told him otherwise). Predates s5e12 wind1234it's negative-weight HC by 7 months.
- **Permutation + backward feature selection** as primary technique (sklearn-style) — explicit feature pruning, not just FE addition.
- **First 10 days: default hyperparameters + focus on FE + ensemble loop.** Then Optuna only on a small set of hyperparameters (depth, num_leaves, regularization, sampling) with 5400s max timeout. Disciplined order: FE first, hyperparameters last.
- **Trust-CV discipline (anti-blind-blending)**: *"I'm proud to have made only 2 submissions between the 18th of May and the end, to win on public and private LB."* Made minimal submissions because CV-LB was reliable.
- **Default grow_policy as diversity source**: each GBM (XGB / CB / LGBM) has a different default grow_policy → "gives variety of predictions" without explicit hyperparameter sweeps.

## Dataset constraints that shaped this strategy
- **All-numeric features (no categoricals) + commensurable feature scale + Poisson-sum structure** → row-wise statistics become first-class FE. Sorted-features and count-thresholds are also viable. Standard TE-on-categoricals path is irrelevant.
- **No useful public original** (different distribution from train) → exploit-original toolkit doesn't apply. Author exploits the *generator structure* (Poisson sum) via EDA instead.
- **"Near-perfect CV-LB"** (author explicit — same as Cross Sellers s4e7) → trust-CV strategy + minimal submissions becomes optimal. No need for anti-greedy validation discipline (different from photo-finish-tight-margin cases like s4e10).
- **1.1M rows + 21 numeric features** → enough data for 30+ GBM variants + Ridge meta-learner; not so large that brute-force is needed.

## Code vs writeup check
- ✓ Published notebook implements the Ridge ensemble pipeline (cells 11+: `do_ensemble` function with StratifiedKFold + Ridge over OOFs)
- ✓ Cell 5 lists the model variants: 5 XGB, 3 LGBM, 6 CatBoost + AutoGluon — confirms ~14+ base model OOFs (more variants exist but cell 5 selects subset)
- ✓ Hierarchical clustering (cell 7) used for model-similarity analysis — feature selection at the ensemble level
- ⚠ The 30+ GBM training notebooks are NOT in the published notebook (only OOF files loaded). FE pipelines per model also not directly reproducible from the published notebook alone.
- ⚠ AutoGluon copy notebook (`pss4e05-copy-autogluon-starter`) referenced separately; not in our set.

## Headline finding
s4e5 (May 2024) is the **earliest entry in the set** and demonstrates the **EDA-driven generator-exploitation strategy** as an alternative to cdeotte's later "use public original as columns" pattern. When no useful public original exists, understanding the SYNTHETIC GENERATOR'S structure (Poisson sum here) can produce equally powerful FE — row-wise statistics, sorted features, count thresholds. Author's discipline is notable: 10 days FE + ensemble before any hyperparameter tuning, only 2 submissions in the final 13 days, Ridge with negative weights from CV evidence alone. **Validation discipline (trust-CV) coupling extends back to May 2024 — N=6 now if we count this trust-CV variant.**

## Surprising / unusual
- **First R2 metric** in the set; first competition where ALL features are numeric (no categoricals) with no useful public original.
- **Generator-structure exploitation** (Poisson sum discovery) as an alternative to public-original exploitation. Hypothesis: when original is unavailable or unhelpful, EDA-discovered generator structure becomes the FE lever.
- **Row-wise statistics** as primary FE — only viable when features are commensurable (same units / same scale). New FE family hypothesis on watch.
- **Negative-weight Ridge predates s5e12's negative-weight HC by 7 months.** Adaubas's `positive=False` Ridge in May 2024 → wind1234it's negative-weight HC in Dec 2025. Same conceptual technique surfaces in different stacker families.
- **Innixma (AutoGluon author) personally commented** — *"welcome to the AutoGluon Hall of Fame."* Tool authors actually engage with these competition writeups; the community extends beyond Kaggle's user base.
- **Tilii (3rd here, our s5e10 winner) doubted Ridge-vs-LinearRegression mattered** ("we are talking about miniscule differences on the 5th decimal place"). Author insisted CV told him otherwise. Disagreement-in-comments is rare and methodologically interesting; suggests two strong practitioners can have different convictions about which technique matters at saturation.
- **Mahdi Ravaghi's s4e10 comment** references adaubas's HC implementation specifically — adaubas's published code becomes a community-shared HC reference.
- **Trust-CV with 2 submissions in 13 days** is the most disciplined submission count in the set. Author's confidence in CV-LB relation was extreme.
