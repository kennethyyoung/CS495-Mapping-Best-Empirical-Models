# s4e11 — Rank 1: Mahdi Ravaghi (ravaghi)

## Identifiers
- **Competition:** [playground-series-s4e11](https://www.kaggle.com/competitions/playground-series-s4e11) — *Exploring Mental Health Data*
- **End date:** 2024-11-30 (2,685 teams)
- **Rank / score:** 1 of 2,685 · 0.94184 private LB (Accuracy). Top 3 within 0.00003 — photo finish (2nd and 3rd tied at 0.94181).
- **Team / Kaggle user:** Mahdi Ravaghi / [ravaghi](https://www.kaggle.com/ravaghi) — **first non-heavyweight community winner in the analysis set** (not cdeotte/mahog/tilii/masayakawamata).
- **Writeup:** [1st place solution](https://www.kaggle.com/competitions/playground-series-s4e11/writeups/mahdi-ravaghi-1st-place-solution) (local: `data/writeups/playground-series-s4e11/1st place solution _ Kaggle.txt`)
- **Notebook (published):** [s04e11-mental-health-prediction-ensemble](https://www.kaggle.com/code/ravaghi/s04e11-mental-health-prediction-ensemble) (local: `data/writeups/playground-series-s4e11/s04e11-mental-health-prediction-ensemble.ipynb`) — 55 cells; **his own public notebook used as OOF source** for the winning ensemble. Contains 7 GBDTs + L2 LR stacker. The actual winning ensemble (24 models + AutoGluon stacker) lives in a separate unpublished pipeline.

## Dataset
Binary classification of `Depression`, Accuracy metric, 140,700 train rows. 19 features (mixed). **16.12% missing data (highest in analysis set)** — author leaves it as-is and lets each model handle natively. Synthetic data with available public original (`original_data_usage: concat_rows`). Class imbalance (majority negative). High-cardinality `Name` column (cardinality up to 422).

## What the spreadsheet currently records
- `primary_model: ensemble`, **`best_single_model: AutoGluon`** (first AutoGluon-as-best-single), `dominant_base_model: gbm`
- `ensemble_method: stacking`, `cv_strategy: stratified_kfold`, `hyperparameter_tuning: optuna`
- `models_used`: xgboost, lightgbm, catboost, logistic_regression, gradient_boosting, adaboost, autogluon (7 model families — first time AdaBoost appears)
- **`fe_techniques: not_applicable`** — author explicit: "I didn't do any feature engineering and did not drop any features"
- `missing_data_strategy: imputation`, `encoding_strategy: ordinal_encoding; one_hot_encoding` (first time non-TE encoding dominates)
- `original_data_usage: concat_rows`
- `n_rows: 140,700`, `pct_missing: 16.12`, `max_cardinality: 422`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0 itemized** | Author refers to his own published `s04e11-mental-health-prediction-ensemble` notebook as the OOF source for the winning pipeline; no external ports cited. |
| Acknowledgments | @optimistix, @tilii7 ("support and encouragement") | First explicit cross-link to the s5/s6 heavyweight community — *Mahdi mentions optimistix and tilii but ISN'T cited by cdeotte/mahog/masayakawamata in any of our analyzed s5/s6 writeups*. Suggests a parallel sub-community in late s4. |
| Method-level inheritance | AutoGluon as ensembler | Author used the same approach in s4e10 — *"It worked really well last month, so I decided to try it again."* Within-author method persistence across competitions. |

## What's actually original to this author
- **AutoGluon-as-the-ensembler.** First time in the set a learned framework (rather than Ridge/HC/CatBoost/cuML LR) is the final stacker. Mahdi explicitly tested HC, Ridge, LR, and Ridge+LR combinations vs AutoGluon — AutoGluon won on CV by a wide enough margin to be the obvious choice. Provides counterevidence (or at least an alternative implementation) to the "linear final stacker" coupling: AutoGluon is itself an ensemble + meta-learner, so at the user-facing layer it's the "stacker," but internally it's nonlinear.
- **AutoGluon-as-base-model AND as-ensembler simultaneously**: 2 AutoGluon models in the 24-model base ensemble (with/without original) were "the two most important models." The final stacker AutoGluon then re-blended all OOFs including its own.
- **Multi-pipeline data-variant diversity**: same models trained on 4 different data pipelines (with/without original dataset × 2 minor variations), generating diversity via data variant rather than only model variant.
- **24-model final selected from 69 trained.** "Fewer models and a simpler ensembling approach worked better this time around."
- **Validation discipline (anti-greedy submission choice):** chose CV 0.94173 submission over a CV 0.94150 alternative even though the alternative's public LB was higher. *"I decided to trust the CV score."* Matches the s6e2 / s5e12 pattern.
- **Trust-the-data-as-is for synthetic competitions** — author explicit in comments: *"based on what I've learned about synthetic datasets since I began competing in TPS, it's usually best to leave the inconsistencies in the data as is"* — implicit FE-effectiveness conditioning (different from cdeotte's framing but same conclusion: don't FE synthetic data unless it helps).

## Dataset constraints that shaped this strategy
- **High missing data (16.12%) + many categoricals + synthetic data** → leaves missing values as-is, lets each model handle natively. Imputation/dropping would lose information about the missingness pattern itself.
- **Photo-finish margin (0.00003 spread top 3)** → validation discipline matters (third case of this coupling in the set).
- **FE doesn't move CV** (matches cdeotte's diagnosis of Nov 2024 in his s4e12 writeup as a "FE didn't help" month) → no FE; effort goes into model diversity + ensembling. Cross-author confirmation of the same competition characteristic from two winners' perspectives.
- **140K rows + 19 features + class imbalance** → standard playground regime where multi-model + good stacking dominates; AutoGluon's NN+GBDT-mix internal ensembling is well-matched.

## Code vs writeup check
- ✓ Published notebook (55 cells) implements the 7-base-model pipeline: CatBoost, XGBoost, LightGBM, LightGBM-GOSS, LightGBM-DART, GradientBoosting, AdaBoost — each via `get_data(model)` + Trainer class + 5-fold CV. L2 Logistic Regression stacker (cells 26+) provides one ensembling path.
- ✓ Hyperparameters are hardcoded as "optimized" dicts in cell 16 (`lr_params` etc.) — suggests offline Optuna tuning.
- ⚠ **Published notebook does NOT have the winning 24-model + AutoGluon-stacker pipeline.** It's the OOF-source notebook for the actual winning ensemble. The 4 data pipelines, 2 AutoGluon base models, and AutoGluon ensembler code are not public.
- ⚠ The L2 LR stacker in the notebook is NOT the chosen final ensembler — Mahdi explicitly tested it and AutoGluon won by a wider CV margin. The notebook leaves the user with a strong but not winning solution.

## Headline finding
s4e11 is the **first non-heavyweight-community winner in the analysis set** and the first **AutoGluon-as-ensembler** win. Mahdi Ravaghi's recipe is methodologically interesting: no FE, multi-pipeline diversity (4 data variants × 7 GBDTs + 2 AutoGluon = 24 selected from 69 trained), AutoGluon as the final stacker (chosen after head-to-head testing against HC/Ridge/LR/Ridge+LR). The validation-discipline pattern recurs (3rd case): chose lower-public-LB submission because its CV was higher. Implicit FE-effectiveness conditioning matches cdeotte's explicit Nov 2024 diagnosis — two winners independently concluded FE wouldn't help this dataset.

## Surprising / unusual
- **First explicit AutoGluon-as-ensembler** in the set. AutoGluon won a head-to-head CV test against HC, Ridge, LR, and Ridge+LR combinations. The "linear stacker is universal" pattern needs another caveat: when AutoGluon is one of the tested options, it can win by enough margin to be chosen.
- **First non-heavyweight-community winner.** Mahdi's writeup acknowledges optimistix and tilii but doesn't cite cdeotte/mahog/masayakawamata, and isn't himself cited by them in any of our analyzed s5/s6 writeups. Suggests a parallel late-s4 sub-community that didn't fully merge with the s5/s6 heavyweight cluster.
- **Cross-author confirmation of FE-doesn't-help**: cdeotte (s4e12, retrospective) said Nov 2024 was a FE-doesn't-help month; Mahdi (s4e11, contemporaneously) won that exact month by doing no FE. Same observation from two perspectives, two months apart.
- **Validation discipline coupling now N=3** (s6e2, s5e12, s4e11) — strong enough to be a robust coupling, all binary classification with tight margins.
- **First time AdaBoost appears** in the models_used list. Unusual in modern playground winners.
- **First missing-data-heavy case (16.12%)** treated with "leave as-is and let models handle natively" rather than imputation strategies. Spreadsheet `missing_data_strategy: imputation` may be slightly off; the notebook does some imputation but author's principle is "leave the inconsistencies."
