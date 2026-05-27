# s3e8 — Rank 2: Craig Thomas (craigmthomas)

> **Note:** Curated entry is rank-2 per spreadsheet. Rank-1 (Thierry Neusius) writeup not in set.

## Identifiers
- **Competition:** [playground-series-s3e8](https://www.kaggle.com/competitions/playground-series-s3e8) — *Regression with a Tabular Gemstone Price Dataset*
- **End date:** 2023-04-30 (734 teams — smallest yet) — **earliest entry now (Apr 2023)**.
- **Rank / score:** **2 of 734** · 570.14008 private LB (RMSE). 1st-2nd gap 0.38, 2nd-3rd 0.08.
- **Team / Kaggle user:** Craig Thomas / [craigmthomas](https://www.kaggle.com/craigmthomas) — doesn't appear elsewhere as winner in our set.
- **Writeup:** [2nd Place Solution](https://www.kaggle.com/competitions/playground-series-s3e8/writeups/craig-thomas-2nd-place-solution) (local: `data/writeups/playground-series-s3e8/2nd Place Solution _ Kaggle.txt`)
- **Notebook (published):** [play-s3e8-eda-models](https://www.kaggle.com/code/craigmthomas/play-s3e8-eda-models) (local).

## Dataset
Regression on gemstone `price`, RMSE metric, 193,573 train rows. 10 features (mixed). Public original gemstone dataset (`original_data_usage: concat_rows`). Gemstone-specific categoricals: cut, clarity, color (natural ordering: Fair → Ideal, D → J, FL → I3).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: stacking` (2-level)
- `cv_strategy: kfold` (10-fold), `hyperparameter_tuning: random_search`, `encoding_strategy: ordinal_encoding`
- `models_used`: XGBoost, LightGBM, CatBoost, Ridge, NN (5 families)
- **`fe_techniques`: Ordinal encoding of gemstone quality categoricals; aspect ratio features; carat × aspect ratio interaction; encoding methodology comparison via CV**
- `original_data_usage: concat_rows`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | Author's writeup focuses on his own custom-framework results; no notebook ports cited. |
| Cross-author cameos | @samuelcortinhas (30th here) comment asking about framework | Samuel Cortinhas later cited by Ravi (s3e16). Recurring community member. |
| Self-built tooling | **Custom AutoML-like framework** | Author: *"similar to AutoML but different in that it leaves the feature exploration and stacking up to me. Basically it handles all the details about the mechanics of how to read the datasets and build the various models, and lets me focus on transforming features (scaling, quantizing, etc), injecting engineered features, or performing customized post processing. In addition to that, it does hyper-parameter tuning through random parameter space searching (kind of like Optuna, but again, custom)."* **Second custom framework after ISoft's Statmining at s3e17.** |

## What's actually original to this author
- **Custom AutoML-like framework with FE-stays-with-human design**: handles mechanics (data loading, model building, HP search) but defers FE + stacking to the author. *"Generate 40-50 models of one type, see upper/lower bounds, then iterate."* Methodological middle-ground between pure-AutoML (ISoft s3e17) and hand-crafted pipelines.
- **1,709 first-level + 105 second-level = 1,816 models total** — **largest model count in our set** (~10-20× more than other ensemble approaches). Made feasible by the custom framework.
- **Threshold-based first-level selection**: started with CV RMSE < 574, stepped down by 0.1 → optimal cutoff was 572.6. Systematic OOF-quality-threshold approach for picking which base models go into second level.
- **Ordinal encoding of domain-ordered categoricals**: cut, clarity, color have natural ordering in gemstone domain (Fair → Ideal etc.) → numeric scale. *"Make sure that LightGBM, CatBoost, and XGBoost didn't treat those columns as categorical in nature."* **Counter-pattern to ambrosm's "treat numerical as categorical" approach** — same encoding-strategy-by-domain-knowledge insight in opposite direction.
- **Aspect ratio + carat interaction**: standardized aspect ratio / exaggerated carat → segments low vs high value gemstones. **Domain-knowledge FE** (like Ravi's anatomical ratios for crab at s3e16).
- **Lookup-exploit FAILED here**: tried Sergey-s3e14-style original-to-test lookup matching (398 original rows duplicated in test). Public LB lift +0.05 but **private LB DROP +0.1**. Author hedged submission; the version WITHOUT exploit won. **Counter-example to s3e14 lookup-exploit success — exploit is dataset-specific.**
- **NN stacker overfits → switched to Ridge**: Craig's NN level-2 had slightly better CV but worse public LB → confirmed overfit on private LB. **Same observation as Mahog s5e11** ("nonlinear stackers were much worse than linear") but 24 months earlier.

## Dataset constraints that shaped this strategy
- **Domain with naturally-ordered categoricals** (gemstone quality scales) → ordinal encoding is natural. Distinct from datasets where "categoricals are arbitrary labels" (where TE/OHE matter).
- **Public original with some test-row overlap (398 rows)** → lookup-exploit was *available* but didn't generalize cleanly to private LB. Generator-property differs from s3e14 (where exploit dominated).
- **Medium-small dataset (193K rows)** → enables 1,800+ models in custom framework; NN stackers overfit (small-ish data + too-flexible stacker).
- **Standard regression + RMSE** → no exotic metric handling needed.

## Code vs writeup check
- ✓ Published notebook is EDA + initial model exploration (`play-s3e8-eda-models`)
- ✓ Writeup describes the 2-level stacking pipeline + threshold-selection methodology
- ⚠ Custom framework + 1,816 model training runs are NOT in the published notebook (private framework code)
- ⚠ Final Ridge stacker model assembly not in published code

## Headline finding
s3e8 (Apr 2023) is **the earliest entry now** and the **largest model-count entry in our set** (1,816 total models, 1,709 first-level + 105 second-level). Custom AutoML-like framework with human-FE-control middle-ground design enables this scale. **Counter-example to s3e14 Sergey's lookup-exploit success**: Craig tried the same exploit (398 duplicates), gained public LB but lost private LB → wisely hedged → won 2nd without exploit. **Lookup-exploit is dataset-specific**: when generator preserves (X,y) pairs faithfully it wins (s3e14); when it doesn't, the exploit overfits public LB and fails private (here). **Anti-NN-stacker observation** (NN stackers overfit) matches Mahog's s5e11 finding 24 months later. **Ordinal encoding of domain-ordered categoricals** (cut/color/clarity for gemstones) is the encoding-strategy-by-domain-knowledge applied in the opposite direction from ambrosm's "treat numerical as categorical" — same insight, different application.

## Surprising / unusual
- **Largest model-count entry in set** (1,816 models). Custom framework makes this feasible at small data scale.
- **Custom AutoML-like framework with FE-stays-with-human design** — second custom framework in set (after ISoft's Statmining at s3e17). Methodological middle-ground between pure-AutoML and hand-crafted pipelines.
- **Counter-example to lookup-exploit success**: s3e14 Sergey won with original-to-test lookup; here Craig tried same approach, gained public LB but lost private LB. **Lookup-exploit is dataset-specific** — when generator preserves (X,y) pairs faithfully → wins; when it doesn't → overfits public LB. Worth tracking: which datasets have faithful generator-preservation?
- **NN-stacker-overfit warning at s3e8** (Apr 2023) — same as Mahog's s5e11 (Nov 2025) 19 months later. Two independent winners observed the same.
- **Ordinal encoding of domain-ordered categoricals** for gemstone quality (cut/color/clarity). Counter to ambrosm's "treat numerical as categorical" (s3e9 AgeInDays, s3e11 store_sqft). Same encoding-strategy-by-domain-knowledge insight in opposite directions. **Constraint: when categoricals have natural order → ordinal; when numeric has few/non-monotone unique values → categorical.**
- **Threshold-based first-level selection methodology** — systematically step CV threshold down to find optimal first-level model pool. Different from "use all OOFs" or "HC-select."
- **Author wisely hedged on lookup-exploit** — submitted with AND without exploit, the non-exploit version won. **Hedging is a documented winning strategy** — author kept two submissions in different directions.
