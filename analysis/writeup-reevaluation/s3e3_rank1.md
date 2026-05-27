# s3e3 — Rank 1: Bill Cruise (bcruise)

## Identifiers
- **Competition:** [playground-series-s3e3](https://www.kaggle.com/competitions/playground-series-s3e3) — *Binary Classification with a Tabular Employee Attrition Dataset*
- **End date:** 2023-02-28 (665 teams) — **earliest entry now (Feb 2023)**.
- **Rank / score:** 1 of 665 · 0.90185 private LB (ROC AUC). 2nd: Prasad 0.90178, 3rd: Cup of Dim 0.90146.
- **Team / Kaggle user:** Bill Cruise / [bcruise](https://www.kaggle.com/bcruise) — one-off author in our set.
- **Writeup:** ["1st place. That was unexpected..."](https://www.kaggle.com/competitions/playground-series-s3e3/writeups/bill-cruise-1st-place-that-was-unexpected) (local: `data/writeups/playground-series-s3e3/1st place. That was unexpected... _ Kaggle.txt`)
- **Notebook (published):** [starting-strong-xgboost-lightgbm-catboost](https://www.kaggle.com/code/bcruise/starting-strong-xgboost-lightgbm-catboost) — author's forked version of @khawajaabaidullah's original notebook.

## Dataset
Binary classification of employee attrition, ROC AUC metric, 1,677 train rows (very tiny — third-tiniest in set after s3e13 707 and s3e5 2056). 34 features (mixed). HR/employment domain (Age, MonthlyIncome, YearsAtCompany, NumCompaniesWorked, DistanceFromHome, etc.). Public original IBM HR Analytics Attrition dataset (`original_data_usage: concat_rows`).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: weighted_blend`
- `cv_strategy: stratified_kfold`, `hyperparameter_tuning: none`, `scaling: standard`, `encoding_strategy: ordinal_encoding`
- `models_used`: XGBoost, LightGBM, CatBoost (3 GBDTs — directly from forked notebook)
- **`fe_techniques`: Domain-driven risk flags (age<34; hourly rate<60; distance>=20; tenure<4 years; job hopper); composite AttritionRisk score; MonthlyIncome/Age ratio; AverageTenure (TotalWorkingYears/NumCompaniesWorked)**
- `original_data_usage: concat_rows`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked | **1 — the entire base notebook** | @khawajaabaidullah's "Starting Strong - XGBoost + LightGBM + CatBoost" — Bill explicitly: *"My only big change was to add some feature engineering before training the same models."* khawajaabaidullah commented: *"my notebook does nothing but combines three simple models. it's all you for coming up with these genius FE ideas."* |
| Specific discussion thread | Bill's "Adding Risk Factors" discussion #378994 — where he developed the FE before the fork |
| Cross-author cameo | **@cdeotte commented**: *"Congratulations Bill. Well done!"* — **earliest cdeotte appearance in our analyzed set (Feb 2023)** as outside-top-3 observer. |

## What's actually original to this author
- **Domain-driven HR FE — risk flags + composite score**: explicit business-logic features for employee-attrition prediction:
  - `Age_risk = (Age < 34).astype(int)` — younger employees more likely to leave
  - `HourlyRate_risk = (HourlyRate < 60).astype(int)` — lower-paid more likely to leave
  - `Distance_risk = (DistanceFromHome >= 20).astype(int)` — long commute → leave
  - `YearsAtCo_risk = (YearsAtCompany < 4).astype(int)` — new employees more likely to leave
  - `JobHopper = ((NumCompaniesWorked > 2) & (AverageTenure < 2.0)).astype(int)` — interaction binary flag
  - `AttritionRisk = sum of 5 binary flags` — composite risk score
  - `MonthlyIncome/Age` ratio + `AverageTenure = TotalWorkingYears / NumCompaniesWorked` — engineered ratios
- **"Risk flag + composite" FE pattern** — interpretable + cheap + effective. Different from anonymized-numeric aggregates (s3e4 olliekemp) or row-wise statistics (s4e5 aldparis). **Domain-knowledge HR FE family** — like anatomical ratios (s3e16 Ravi) or gemstone-quality ordinal (s3e8 Craig). Each domain has its own FE family.
- **Author's "unexpected win"** — wasn't tracking competition closely; *"hadn't even selected any submissions because I wasn't expecting to do well as I watched my public LB score slip."* **Third surprised-author win in set** (Umar s3e13, Mart Preusse s4e9).

## Dataset constraints that shaped this strategy
- **Very tiny dataset (1,677 rows) + 34 features** → heavy curse-of-dimensionality (~2% feature density). FE must be CAREFUL — over-engineered features overfit at this scale.
- **HR domain with interpretable features** (Age, MonthlyIncome, etc.) → domain-knowledge FE is feasible. Anonymized features wouldn't allow this.
- **Public original IBM HR dataset + community starter notebook** → 3-model fork is the natural base; Bill adds 7 domain features on top.

## Code vs writeup check
- ✓ Notebook is the published fork with FE code added; matches writeup exactly
- ✓ Spreadsheet `fe_techniques` enumerates all 7 features accurately

## Headline finding
s3e3 (Feb 2023) is **the earliest entry now** and a **fork-with-FE win**: Bill Cruise forked @khawajaabaidullah's 3-model GBDT notebook and added 7 domain-driven HR risk-flag features → 1st place. Same fork-heavy strategy as Moonlit s4e3 (first-time competitor port-and-win) but with explicit domain FE rather than just public-notebook blending. **cdeotte's earliest appearance in our analyzed set is here** (Feb 2023, as outside-top-3 commenter): *"Congratulations Bill."* **cdeotte was watching the playground series 19 months before his Dec 2024 first win at s4e12** — substantially longer pre-dominance period than we previously documented. **Domain-knowledge FE family** (risk flags + composite scores + ratios) — different from generic FE families (row-wise stats, brute-force combos, etc.). Each problem domain has its own FE shape.

## Surprising / unusual
- **Earliest cdeotte appearance pushed back to Feb 2023** — cdeotte's pre-dominance era is now documented as 19+ months (Feb 2023 commenter → Dec 2024 first win). His later "KGMON Playbook" canonizations come after ~22 months of community observation/participation.
- **Third surprised-author win** in set: Bill Cruise s3e3 (Feb 2023, "unexpected"), Umar s3e13 (Jul 2023, "surprisingly #1"), Mart Preusse s4e9 (Sep 2024, "did I really make it?"). **Surprised wins happen at small-data / high-variance competitions** — when LB tracking is unreliable, even authors who weren't tracking can win.
- **Domain-knowledge HR FE** with explicit business-logic interpretation (Age<34 = risk, JobHopper = NumCompaniesWorked>2 AND tenure<2). Most other writeups use generic FE families; here domain knowledge dominates.
- **Composite risk score** (sum of 5 binary flags) — simple, interpretable, effective FE addition.
- **N=3 fork-with-FE-additions winners**: Bill Cruise s3e3 (forked 3-model + added 7 features), Moonlit s4e3 (forked 2 of 3 OOFs + added 1), Mart Preusse s4e9 (forked yekenot's DeepTables + added 4 OOF features). **Pattern**: take a strong public starter notebook + add 1-7 original features = top-3 winnable.
- **Tiny dataset (1,677 rows) + 34 features + careful domain FE** wins without ensembling-heavy tactics.
