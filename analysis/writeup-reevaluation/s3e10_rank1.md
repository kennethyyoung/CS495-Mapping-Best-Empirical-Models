# s3e10 — Rank 1: Piotr Szulc (seascape)

## Identifiers
- **Competition:** [playground-series-s3e10](https://www.kaggle.com/competitions/playground-series-s3e10) — *Binary Classification with a Tabular Pulsar Dataset*
- **End date:** 2023-05-31 (807 teams — smallest yet) — **earliest entry now (May 2023)**.
- **Rank / score:** 1 of 807 · 0.03029 private LB (Log Loss). 2nd: Patrick Blackwill 0.03072, 3rd: **aldparis 0.03075** (adaubas appearance even earlier).
- **Team / Kaggle user:** Piotr Szulc / [seascape](https://www.kaggle.com/seascape) — one-off author in our set.
- **Writeup:** [1st place solution](https://www.kaggle.com/competitions/playground-series-s3e10/writeups/piotr-szulc-1st-place-solution) (local: `data/writeups/playground-series-s3e10/1st place solution _ Kaggle.txt`)
- **Notebook (published):** [how-to-detect-pulsars-with-gam-1st-place](https://www.kaggle.com/code/seascape/how-to-detect-pulsars-with-gam-1st-place) — **.Rmd (R Markdown) — first R notebook in our set**.

## Dataset
Binary classification of pulsar detection, **Log Loss** metric (third in set after s3e26, s3e17), 117,564 train rows. **9 features all numeric** (max_cardinality=0). No missing data, no public original used.

## What the spreadsheet currently records
- **`primary_model: other`** (GAM — first "other" primary model in set), **`best_single_model: GAM`** (first GAM-as-best-single), **`dominant_base_model: linear`** (first "linear" dominant)
- `ensemble_method: stacking`, `cv_strategy: stratified_kfold`, `hyperparameter_tuning: none`
- `models_used`: GAM, XGBoost, Lasso (3 models — GAM is primary, XGB+Lasso predictions are *features* for GAM)
- **`fe_techniques`: XGBoost predictions as GAM input features; Lasso predictions as GAM input features; interaction terms in GAM**
- `original_data_usage: none`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | seascape's writeup is technique-focused with no community citations. R-based solution, distinct from the Python-dominant ecosystem. |
| Cross-author cameos | paddykb (2nd here) — comment: *"GBMs are such a heavy Kaggle default that it is instructive to see other methods do well. Smoothness & continuity FTW :)"*; **aldparis (3rd here)** — adaubas earliest appearance now. |

## What's actually original to this author
- **GAM (Generalized Additive Model) as PRIMARY MODEL** — first time in our set. Not just one of many; the centerpiece. XGB and Lasso are *demoted to feature engineering* (their predictions become input features for GAM).
- **Reversed stacking direction**: typically tree models are at the top of the stack; here, GBDTs are *at the bottom* and a linear-smooth model (GAM) is at the top. Inverts the usual stacker hierarchy.
- **First R-based solution** in our set (.Rmd notebook). The R/Kaggle ecosystem differs from the dominant Python/cuDF stack.
- **Anti-boosting philosophy explicit**: *"Boosting is based on trees, which, in my opinion, are not able to find 'real' relationships. Because real world relationships are rather continuous in nature — and decision trees only approximate it... GAM has built-in regularization; it selects parameters by performing internal crossvalidation. This makes it very convenient, and I could freely add interactions and features created from the XGB and LASSO model."*
- **Interaction terms in GAM** — explicit feature interactions added to GAM model.

## Dataset constraints that shaped this strategy
- **Few features (9) + all numeric + already high-level** → "feature engineering is basically impossible, it's just a matter of finding the right relationship." Forces a model-choice approach rather than FE approach. Smooth-relationship-finding model (GAM) is well-matched.
- **Binary + Log Loss** → calibrated probabilities matter; GAM produces smooth calibrated predictions (better than tree-based discrete outputs for probability calibration).
- **Medium dataset (117K rows) + no original** → all in-data signal; GAM with built-in regularization avoids overfitting in this single-source regime.
- **paddykb's affirming comment**: "Smoothness & continuity FTW" — community acknowledgment that the continuous-relationships argument is valid for this dataset.

## Code vs writeup check
- ✓ Author published R Markdown notebook with title literally "How to detect pulsars with GAM (1st place)"
- ✓ Writeup describes the GAM + XGB-as-feature + Lasso-as-feature + interaction-terms structure
- ⚠ Specific GAM smooth specifications + interaction terms not enumerated in writeup excerpt; presumably in .Rmd

## Headline finding
s3e10 (May 2023) is **the earliest entry now** and the **first GAM-as-primary-model winner in our set**. **R-based solution (.Rmd)** — first time we see a non-Python winner. Author Piotr Szulc's explicit **anti-boosting / pro-continuity philosophy** argues that trees only approximate the continuous relationships of the real world, while GAM models them directly. The unusual structure — GAM at the top of the stack with XGB and Lasso predictions demoted to *input features* — inverts the typical stacker hierarchy. **adaubas appears as 3rd place here (May 2023)** — pushes his earliest documented Kaggle presence in our set back by 2 months from s3e14 (Jul 2023). adaubas trajectory now spans 12 months: 3rd at s3e10 → contributor at s3e14 → 1st at s4e5.

## Surprising / unusual
- **First GAM-as-primary-model winner** — GAM appeared as one of 8 models in s3e24 (Ravi), but here it's the centerpiece. **Linear-smooth model wins.**
- **First R-based winning solution** in set (.Rmd notebook). R/Kaggle ecosystem differs from Python-dominant pipeline.
- **Reversed stacker hierarchy**: typically tree models are at the top of the stack; here, GBDTs are *at the bottom* (their predictions are inputs to GAM). Inversion of usual Kaggle pattern.
- **Anti-boosting philosophy explicit**: *"trees only approximate continuous relationships"*. Different aesthetic from the dominant boosting-heavy s4-s6 era.
- **adaubas pushed back to May 2023**: 3rd here (s3e10) → contributor s3e14 (Jul 2023) → 1st s4e5 (May 2024). 12-month trajectory documented.
- **"Few features + high-level features → FE is impossible, only model choice matters"** — explicit principle from author. New hypothesis to track.
- **Built-in CV-based regularization in GAM** — algorithmic feature that simplifies hyperparameter tuning (`hyperparameter_tuning: none` is spreadsheet-confirmed, but it's not "no tuning" — it's "tuning is done by the model itself internally").
- **paddykb (2nd here) is a recurring community member** (cited at s4e10 by Omid for "all-features-as-categories", at s3e14 by Sergey for FLAML-BFI port). His comment here affirming the GAM choice shows community openness to non-boosting approaches.
