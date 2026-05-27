# s3e9 — Rank 1: AmbrosM (ambrosm) — SECOND win

## Identifiers
- **Competition:** [playground-series-s3e9](https://www.kaggle.com/competitions/playground-series-s3e9) — *Regression with a Tabular Concrete Strength Dataset*
- **End date:** 2023-05-15 (765 teams — smallest yet) — **earliest entry now (mid-May 2023)**.
- **Rank / score:** 1 of 765 · 12.21599 private LB (RMSE). 2nd-3rd tied at 12.23484 (0.018 gap to 1st).
- **Team / Kaggle user:** AmbrosM / [ambrosm](https://www.kaggle.com/ambrosm) — **second ambrosm win in our analyzed set** (s3e9 May 15, then s3e11 Jun 15). 1-month back-to-back wins. **N=5 ambrosm connections now** (2 wins + 3 prior citations as source) — ties arunklenin as most-recurring contributor.
- **Writeup:** [#1 Solution: Cross-validation and diversity win](https://www.kaggle.com/competitions/playground-series-s3e9/writeups/ambrosm-1-solution-cross-validation-and-diversity-) (local: `data/writeups/playground-series-s3e9/#1 Solution_ Cross-validation and diversity win _ Kaggle.txt`)
- **Notebook (published):** [pss3e9-winning-model](https://www.kaggle.com/code/ambrosm/pss3e9-winning-model) (local). **Plus separate EDA notebook "pss3e9-eda-which-makes-sense"** which is later cited by oscarm524 at s3e23 (Nov 2023).

## Dataset
Regression on `Strength`, RMSE metric, 5,407 train rows (small). **9 features all numeric** (max_cardinality=0). No missing data, no public original used. `AgeInDays` has few distinct values + highly nonlinear non-monotone relationship to target → treated as categorical.

## What the spreadsheet currently records
- `primary_model: ensemble` (7 models), `dominant_base_model: gbm`, `ensemble_method: mean_blend`
- `cv_strategy: repeated_kfold`, **`hyperparameter_tuning: manual`** (author explicitly anti-Optuna)
- `models_used`: LightGBM, XGBoost, CatBoost, GradientBoostingRegressor, HistGradientBoostingRegressor, RandomForest, Ridge (7 families, no NN)
- **`fe_techniques`: Nonlinear features for linear regression (from partial dependence plots); feature selection by CV; target encoding of AgeInDays (treated as categorical)**
- `original_data_usage: none`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | ambrosm's writeup explicitly *warns against* this: *"Don't copy code from high-scoring public notebooks unless the quality of that code shows up in a good cross-validation score. The best-scoring public notebooks are at the top of the list only because they overfit the public leaderboard."* |
| Author's downstream impact (cited later) | ambrosm's EDA notebook "pss3e9-eda-which-makes-sense" cited by oscarm524 at s3e23 (Nov 2023) for ambrosm's EDA methodology | Direct technique-source-to-cite trace |

## What's actually original to this author
- **Statistical-rigor framing of "Optimize CV, ignore public LB"**: explicit math — 5407 train samples vs 721 public LB samples → *"A 5407-sample average is a measurement - a 721-sample average is random variable. If you want to test the quality of a dice, you better throw it eight times rather than only once."* **Most quantitatively-framed trust-CV argument in set.**
- **First explicit anti-Optuna stance**: *"Just run Optuna and then change the seed of the KFold. You'll see that the Optuna-found hyperparameters don't survive the change of seed."* In comments: *"Optuna's understanding of hyperparameters isn't perfect, either: It just selects a hundred points in a seven-dimensional space and evaluates them with a randomized algorithm."* Counter-pattern to dominant Optuna use in later writeups.
- **PDP-based detection of disguised-categorical features (AgeInDays)** — same motif as s3e11's `store_sqft`. **Within-author recurring methodology** across consecutive months.
- **Nonlinear features for linear (Ridge) regression from PDP analysis** — derive feature transformations from partial dependence plots to make linear models nonlinear-aware.
- **"Don't copy high-CV-public-LB code without CV verification"** — anti-blind-fork principle. Counter-pattern to fork-heavy strategies (s4e3 Moonlit, s4e7 Cross Sellers).
- **"AmbrosM playbook" emerging** across his 2 wins (s3e9 + s3e11, 1 month apart): EDA notebook + winning model notebook + 7-18 model zoo + Ridge or mean blend + PDP-based feature analysis + treat-disguised-categoricals-as-categorical + manual HP tuning + trust CV completely.

## Dataset constraints that shaped this strategy
- **Small dataset (5407 rows) + 9 numeric features + no original** → ensembling has marginal returns; FE-via-PDP + careful CV is the lever.
- **Public LB tiny (721 samples)** → ambrosm's statistical argument applies: public LB is high-variance, CV is reliable.
- **`AgeInDays` is disguised-categorical** → PDP detection + TE captures this signal.
- **Standard regression / no novel constraints** → reflects ambrosm's "general-purpose recipe" applies here.

## Code vs writeup check
- ✓ Two published notebooks: EDA + winning model
- ✓ Writeup describes the 7-model ensemble + manual HP tuning + PDP-based features for Ridge + AgeInDays TE
- ⚠ Specific model variants and weights visible in code

## Headline finding
s3e9 (May 15, 2023) is **the earliest entry now** and **ambrosm's first of two back-to-back wins** (s3e9 → s3e11, 1 month apart). **N=5 ambrosm connections** (2 wins + 3 prior citations as source) ties arunklenin as the most-recurring community contributor in our analyzed set. **First explicit anti-Optuna stance** in set — ambrosm argues Optuna's local optima don't survive seed changes, prefers manual tuning. **Most quantitatively-framed trust-CV argument** (5407 train samples vs 721 public LB samples — *"public LB is a coin flip"*). PDP-based detection of disguised-categorical features recurs within-author (s3e9 AgeInDays → s3e11 store_sqft). The **"AmbrosM playbook"** is now visible: EDA notebook + winning model notebook + 7-18 model zoo + Ridge or mean blend + PDP-based feature analysis + treat-disguised-categoricals-as-categorical + manual HP + trust CV completely.

## Surprising / unusual
- **Second back-to-back ambrosm win** (s3e9 May 15 → s3e11 Jun 15) — same author wins 2 consecutive monthly competitions with the same recipe family. Rare in our set.
- **First explicit anti-Optuna stance** — ambrosm: *"Optuna doesn't find robust optima"*. Manual HP tuning preferred. Counter-pattern to later writeups that lean heavily on Optuna (s4e1 Iqbal, s4e9 Mart, s5e2 cdeotte, s5e3 cdeotte, etc.).
- **Statistical framing of trust-CV** — most quantitative argument in set. Sample-size-based reasoning (5407 vs 721).
- **PDP-based disguised-categorical detection** confirmed N=2 within-author (AgeInDays s3e9 → store_sqft s3e11). **Methodological consistency across competitions.**
- **Anti-blind-fork stance**: "don't copy public-LB-overfitting code." Counter to documented fork-heavy strategies (Moonlit s4e3, Cross Sellers s4e7, Sergey s3e14).
- **ambrosm's EDA notebooks become community references**: oscarm524 at s3e23 cites "ambrosm's EDA notebook." **EDA-as-shared-asset** is a recurring pattern from this author.
- **ambrosm N=5 ties arunklenin** as most-recurring community contributor.
