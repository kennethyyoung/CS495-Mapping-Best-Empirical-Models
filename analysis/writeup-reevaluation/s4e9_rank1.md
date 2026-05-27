# s4e9 — Rank 1: Mart Preusse (martinapreusse)

## Identifiers
- **Competition:** [playground-series-s4e9](https://www.kaggle.com/competitions/playground-series-s4e9) — *Regression of Used Car Prices*
- **End date:** 2024-09-30 (3,066 teams) — this is the **Sept 2024 cdeotte referenced** in his s4e12 retrospective as a "FE didn't help" month.
- **Rank / score:** 1 of 3,066 · 62917.06 private LB (MSE). Top 3 margin ~41 (62917→62958 on a ~62K scale = tight).
- **Team / Kaggle user:** Mart Preusse / [martinapreusse](https://www.kaggle.com/martinapreusse)
- **Writeup:** [#1 solution - stacked NN](https://www.kaggle.com/competitions/playground-series-s4e9/writeups/mart-preusse-1-solution-stacked-nn) (local: `data/writeups/playground-series-s4e9/# 1 solution - stacked NN _ Kaggle.txt`)
- **Notebook (published):** [ps4e9-cat-svr-lgbm-nn-py](https://www.kaggle.com/code/martinapreusse/ps4e9-cat-svr-lgbm-nn-py) (local). Author's Ridge-ensemble pipeline (would have placed 2nd or 3rd). The actual winning NN-stacked submission was a forked yekenot notebook with OOFs added.

## Dataset
Regression on used-car `price`, MSE metric, 188,533 train rows. 12 features (mixed), 1.28% missing, **max_cardinality=1897** (likely Brand or Model column). Public original dataset used (`original_data_usage: concat_rows`). Has rich text fields (engine string from which horsepower/displacement extracted).

## What the spreadsheet currently records
- `primary_model: ensemble`, **`best_single_model: neural_network`** (DeepTables NN winning), `dominant_base_model: neural_network`
- `ensemble_method: stacking`, `cv_strategy: stratified_kfold`, `hyperparameter_tuning: optuna`
- `models_used`: LightGBM, CatBoost, SVR, NN, XGBoost, AutoGluon (6 families)
- **`outlier_treatment: outlier_classification`** (first non-"not_described" value in this field) — IQR-based outlier-bin classifier
- `fe_techniques`: text_feature_extraction (horsepower/displacement from engine string), mileage_binning, **outlier_classification (IQR price_bin)**, target_encoding_median (leakfree per fold), catboost_oof_as_feature
- `encoding_strategy: target_encoding; label_encoding`, `scaling: standard`, `rare_class_handling: rare_grouping`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **2 itemized** + 4 specific author cites | (1) @yekenot's DeepTables NN starter — **forked and modified for the actual winning submission**. (2) Implicit fork of public XGB hyperparameters (author forgot the source). Specific cites: @siukeitin (RBF SVR), @tilii7 + @roberthatch (outlier classification idea), @noodl35 (LGBM hyperparameters), **@cdeotte** ("made the entrance to NNs simple for me"). |
| Cross-author community membership | Yes | Author thanks cdeotte explicitly. cdeotte (placed 81st here) commented on this writeup: *"Your use of median with target encoding and building a stack over classification predictions was creative and effective."* cdeotte later references Mart at s4e12 ("Congratulations winning 1st place in Used Car Playground comp!"). Cross-author bidirectional flow. |
| Forward propagation | Yes | yekenot (DeepTables notebook source for this win) later cited 4× in cdeotte's s6e3 references. The DeepTables/NN pattern propagates forward through the community. |

## What's actually original to this author
- **The winning submission was a last-day spontaneous fork of yekenot's DeepTables NN starter** — Mart added 4 OOF predictions as numerical features (SVR, LGBM5, CatBoostClassifier-outlier, XGB) → NN ensemble with CV 72468, won 1st. First final submission (Ridge ensemble) would have placed 2nd. **NN-as-final-stacker via OOFs-as-features is the unique mechanism** — first time we see NN-stacker chosen over linear/HC.
- **Outlier classification via IQR-bin CatBoost classifier** → use the OOFs as a feature for downstream regressors. CatBoost serves *both* as classifier (price-bin) and regressor (price) — same model family, two roles.
- **Median target encoding** (not mean), leakfree per fold. Variant of standard TE more robust to outliers — well-matched to a price-prediction task with skewed distribution.
- **Diversity strategy with explicit "what didn't work" section** — XGB explicitly didn't help him; cdeotte's FE techniques (from cdeotte's public discussion post) explicitly didn't work for Mart either. *FE-effectiveness varies even within a competition by which specific FE techniques an author tries.*
- **Two final submissions kept** as risk diversification (Ridge ensemble + NN ensemble) — the NN ensemble (which Mart was less confident in) won. Not strict validation discipline, but related risk-management.

## Dataset constraints that shaped this strategy
- **Regression + MSE + skewed price distribution + outliers** → outlier classification as a feature engineering technique is well-matched (predict outliers, use prediction as feature). Median TE preserved against price-skew distortion.
- **High max_cardinality (1897) + categorical Brand/Model** → label-encoding + rare-grouping + median-TE makes high-cardinality cats stable.
- **Text fields (engine string)** → enables horsepower/displacement extraction as engineered numeric features.
- **Sept 2024 era**: cdeotte's specific FE didn't help (his s4e12 retrospective claim), and Mart confirms — but Mart found *other* FE that worked. **FE-effectiveness is a per-technique-per-author intersection**, not just competition-level.

## Code vs writeup check
- ✓ Published notebook implements the Ridge-ensemble pipeline (CatBoost + SVR + LGBM + NN, Ridge stacking). Author note ("Edit"): including CatBoostClassifier + LGBM1_st + LGBM5_st in the notebook would push private to 62957.83525 — would have placed top 3.
- ⚠ **The actual winning submission is NOT in this notebook** — it's a forked yekenot DeepTables NN notebook with 4 OOF features added. The forked notebook isn't in our local set.
- ⚠ `bin_price` function (outlier classification) and CatBoost classifier hyperparameters are in the writeup but the winning notebook's exact integration isn't fully published.

## Headline finding
s4e9 (Sept 2024) is the **earliest entry in the analysis set** and validates a non-obvious finding: **FE-effectiveness is per-technique-per-author**, not just competition-level. cdeotte at s4e12 said FE didn't help him in Sept 2024 (he placed 81st in this comp). Mart Preusse confirms cdeotte's specific FE techniques didn't work for him either — but Mart found *different* FE (outlier classification, median TE, text extraction, CatBoost-OOF-as-feature) that did work. He won with a last-day NN-stacker over a Ridge stacker (would have been 2nd). First explicit non-linear stacker win in the set: DeepTables NN as the final meta-learner, with OOFs added as numerical features.

## Surprising / unusual
- **NN as final stacker** (DeepTables NN with OOFs as input features) — first time in our set. Different mode of stacking than Ridge/HC/CatBoost: uses NN's representational power to combine OOFs. Adds nuance to the "linear final stacker" coupling — when an NN starter notebook is available and "robust to changes," it can be repurposed as a meta-learner.
- **CatBoost as classifier AND regressor in same pipeline** — outlier-bin classifier OOFs become features for the price regressor. Within-model-family role-splitting.
- **Two winners' FE diagnoses in conflict on the same competition**: cdeotte said Sept 2024 FE didn't help (he placed 81st); Mart won 1st partly with FE techniques. Resolution: cdeotte's specific FE didn't work; Mart's *different* FE did. **FE-effectiveness is technique-specific, not competition-uniform.**
- **Last-day spontaneous winning decision** — Mart's primary effort (Ridge ensemble) would have placed 2nd. He spontaneously forked yekenot's NN notebook on the last day and added OOF features → won. Validates "keep diverse submissions" as a risk-management strategy.
- **yekenot's DeepTables NN** (the basis for Mart's win) gets cited 4× later in cdeotte's s6e3 references. Mart's s4e9 win provided a community-validated demonstration that helped propagate yekenot's notebook.
- **cdeotte placed 81st here** but went on to win s4e12 (Dec 2024) and s5e2 (Feb 2025), s5e5 (May 2025), s5e6 (Jun 2025), s6e3 (Mar 2026). cdeotte's trajectory: started outside top-10 in early 2024 → dominant by Dec 2024 onward.
