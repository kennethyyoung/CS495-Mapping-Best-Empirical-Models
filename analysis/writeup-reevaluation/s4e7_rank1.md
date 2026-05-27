# s4e7 — Rank 1: Cross Sellers (ravi20076 + arunklenin)

## Identifiers
- **Competition:** [playground-series-s4e7](https://www.kaggle.com/competitions/playground-series-s4e7) — *Binary Classification of Insurance Cross Selling*
- **End date:** 2024-07-31 (2,234 teams) — second-earliest entry in set (after s4e8 by 1 month).
- **Rank / score:** 1 of 2,234 · 0.89754 private LB (ROC AUC). Top 3 spread 0.00006 (photo-finish).
- **Team / Kaggle user:** **First team entry** — Ravi Ramakrishnan ([ravi20076](https://www.kaggle.com/ravi20076)) + Minato Namikaze ([arunklenin](https://www.kaggle.com/arunklenin)). Both later appear in cdeotte's s6e3 references (arunklenin cited there).
- **Writeup:** [Cross Sellers Winning approach](https://www.kaggle.com/competitions/playground-series-s4e7/writeups/cross-sellers-winning-approach-team-cross-sellers) (local: `data/writeups/playground-series-s4e7/Winning approach- Team Cross Sellers _ Kaggle.txt`)
- **Notebook (published):** [playgrounds4e07-featurestore](https://www.kaggle.com/code/ravi20076/playgrounds4e07-featurestore) (local: `data/writeups/playground-series-s4e7/playgrounds4e07-featurestore.ipynb`) — **8 cells, mostly markdown; only an illustration of the feature-store concept, not the actual 78-learner training pipeline.**

## Dataset
Binary classification of `Response` (cross-sell yes/no), ROC AUC metric, **11,504,798 train rows (11.5M — LARGEST in set)**. 11 features (mixed), no missing data, max_cardinality=3 (effectively binary categoricals). Public original dataset + target reversal trick: exact label duplicates between train.original and test.original allow reversing labels. **Optimistix at s4e8 references this competition as "last month's 11 million samples."**

## What the spreadsheet currently records
- `primary_model: ensemble`, **`best_single_model: CatBoost`**, `dominant_base_model: gbm`
- `ensemble_method: stacking`, `cv_strategy: stratified_kfold` (StratifiedKFold n_splits=5, random_state=42), `hyperparameter_tuning: manual`
- `models_used`: lightgbm, catboost, xgboost, neural_network (denselight, mlp, tab_resnet, tab_transformer, autoint) — 4 GBDT lineage + 5 NN architectures
- `fe_techniques`: **Feature store (12 versions)**; component models on feature subsets (previously insured, vehicle damage); feature importance via CatBoost single-fold
- `original_data_usage: concat_rows`, `n_rows: 11,504,798`, `max_cardinality: 3`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **1 itemized** | @rzatemizel's "stacking-xgb-lgbm-catb-ann" kernel — used as one of the 78 weak learners. |
| Acknowledgments | @uryednap, **@tilii7** (3rd here, our s5e10 winner), **@optimistix** (4th here, our s4e8 winner) | All three later become recurring podium finishers in our set. |
| Cross-author network | Yes | Tilii commented: *"Mine overlapped with yours quite a bit except for different neural networks."* Optimistix referenced this competition in his s4e8 writeup ("'only' 3 million samples instead of last month's 11"). **Confirms community pre-existed cdeotte's Dec 2024 era.** arunklenin (team member) later cited in cdeotte's s6e3 references. |

## What's actually original to this author
- **3-stage stacking pipeline**:
  - Stage 1: 7 models × {full data, component subsets (previously_insured, vehicle_damage)} = ~12+ models
  - Stage 2: Same 7 models × same options (independent retrain on different data)
  - Stage 3: **XGBoost stacker on selected OOFs** from Stages 1+2
  - Total: 78 weak learners across all stages, from 125 experiments
- **Component models on data subsets** — train models on data filtered by a feature value (e.g., previously_insured=True/False as separate datasets, vehicle_damage as separate datasets, then both combined). Conceptually a *data-split* version of reframing — different from s6e4's *target-split* binary-classifier reframing but same family.
- **"Did NOT use XGBoost in weak learners"** — only as final stacker. Deliberate choice to avoid XGB diversity collisions (XGB tested in isolation didn't improve final CV).
- **Target reversal post-processing** — discovered exact label duplicates between train.original and test.original on day 1; all submissions reversed labels for duplicates. New post-processing technique not seen elsewhere in the set.
- **Feature store with 12 versions (V1–V12)** — modular FE pipeline architecture. Each version is a reusable engineered dataset. Distinct from cdeotte-style monolithic FE-per-notebook pattern.
- **External GPU farm**: A6000×2, A6000Ada×2, A100, A5000×2, RTX4090, RTX3090 local PC. *"Decided not to use Kaggle free resources."* First explicit non-Kaggle compute investment in set; predates Optimistix's s4e8 Saturn/Lightning experiments and cdeotte's s4e12 A100 work.
- **MLOps discipline as explicit theme**: standard file naming, code automation, GitHub repo organization, experiment tracking. Authors call this out as a key takeaway.

## Dataset constraints that shaped this strategy
- **11.5M rows + 11 features + low cardinality** → "size of data makes it almost perfectly insulated from overfitting risks" (author quote). Justifies brute-force 78-weak-learner ensemble.
- **"Near-perfect CV-LB relation"** (author explicit) → CV-LB tracking works cleanly; no validation-discipline gymnastics needed.
- **Photo-finish top 3 (0.00006)** → still drives heavy ensembling, but CV-LB clarity removes the anti-greedy submission tension seen in s4e10/s4e11/s4e8.
- **Two strong binary-ish categoricals (previously_insured, vehicle_damage)** → makes data-split component-modeling viable (clean splits, sufficient data per split).
- **Public original with reversible duplicates** → enables target-reversal post-processing as a free win.

## Code vs writeup check
- ✓ Spreadsheet `ensemble_method: stacking` matches 3-stage architecture; `models_used` accurately captures the 7 base families (4 GBDTs + 5 NN architectures including some uncommon ones — Denselight, Autoint, Tab-Transformer).
- ✓ Spreadsheet `fe_techniques` accurately captures feature store + component models + CatBoost-single-fold importance.
- ⚠ **Published notebook is the 8-cell feature-store *illustration*** — not the 78-learner training pipeline. Author explicit: *"this kernel is an illustration only."* Actual production pipeline is in a (presumably private) GitHub repo.
- ⚠ Target-reversal post-processing logic is described in writeup but not in published code.

## Headline finding
s4e7 is the **first team-based win** in the set and the **largest dataset (11.5M rows)**. Strategy is **modular MLOps-discipline ensembling** — 3-stage stacking, 78 weak learners, 12-version feature store, component models on data subsets — implemented on a self-funded external GPU farm. **What worked here was the opposite of what wins in s5/s6**: author explicit list of "what did NOT work" includes *Linear approaches, Optuna, Hill Climb* — the same techniques that dominate s5/s6 winners. Reinforces that **technique effectiveness is competition-conditional**, not absolute. The community pre-cdeotte already had team-based, MLOps-disciplined, external-GPU strategies; cdeotte's later solo + cuDF + LLM-augmented work is a *different style*, not a paradigm shift.

## Surprising / unusual
- **First team entry** in the analysis set (Ravi + Minato). Different dynamic from solo wins.
- **"What did not work" list includes the s5/s6-dominant techniques**: Linear approaches, Optuna, Hill Climb. **Direct counter-evidence that "linear stacker is universal"** — for this team in this competition, linear approaches actively failed. **Nonlinear final stackers now N=4** in s4 era: s4e7 (XGBoost), s4e9 (DeepTables NN), s4e11 (AutoGluon), s5e8 (CatBoost).
- **External GPU farm explicit** — A6000×2 + A100 + RTX4090, no Kaggle resources. First documented external-compute strategy; predates Optimistix's s4e8 Saturn/Lightning by 1 month and cdeotte's s4e12 A100 by 5 months. Resource-investment-as-strategy was already established in mid-2024.
- **Target reversal post-processing** — exact-duplicates-allow-label-reversal trick. New post-processing technique unique to this writeup so far.
- **Component models on data subsets** (train separate models on previously_insured=True/False) — a *data-split* reframing, sibling to s6e4's *target-split* reframing. Both are forms of "split the problem into easier sub-problems."
- **MLOps discipline as explicit takeaway** — file naming, GitHub repo, experiment tracking. First time an author flags MLOps as load-bearing. Implicit in cdeotte's later work but never explicit.
- **Feature store as architecture** — 12 reusable engineered datasets. Modular alternative to cdeotte's monolithic per-notebook FE.
- **Competition context: 11M rows** → Optimistix at s4e8 (next month, 3M rows) explicitly compared scale: *"with 'only' 3 million samples instead of last month's 11"*. The community was tracking each other's competitions in detail.
