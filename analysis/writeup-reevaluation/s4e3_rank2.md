# s4e3 — Rank 2: Moonlit (yunqicao)

> **Note:** Curated entry is rank-2 per spreadsheet. Rank-1 (kailai) writeup not in set.

## Identifiers
- **Competition:** [playground-series-s4e3](https://www.kaggle.com/competitions/playground-series-s4e3) — *Steel Plate Defect Prediction*
- **End date:** 2024-03-31 (2,199 teams) — **earliest entry now (Mar 2024)**.
- **Rank / score:** **2 of 2,199** · 0.88939 private LB (Mean Columnwise AUC). Top 3: kailai 0.88977 → Moonlit 0.88939 → Samvel Kocharyan 0.88936.
- **Team / Kaggle user:** Moonlit / [yunqicao](https://www.kaggle.com/yunqicao) — self-described first Kaggle competition.
- **Writeup:** [2nd place solution: OOF Ensemble](https://www.kaggle.com/competitions/playground-series-s4e3/writeups/moonlit-2nd-place-solution-oof-ensemble) (local: `data/writeups/playground-series-s4e3/2nd place solution_ OOF Ensemble _ Kaggle.txt`)
- **Notebook (published):** [2nd-place-solution-steel-plate-defect-prediction](https://www.kaggle.com/code/yunqicao/2nd-place-solution-steel-plate-defect-prediction) (local). 37 cells.

## Dataset
Multiclass (originally multilabel — 7 binary defect types) — author dropped rows with multiple labels (small portion) and converted to multiclass via argmax. Mean Columnwise AUC metric. 19,219 train rows (small). **34 features, all numeric** (max_cardinality=0). Public original "faulty steel plates" UCI dataset used (`original_data_usage: concat_rows`).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: weighted_blend`
- `cv_strategy: stratified_kfold` (10-fold), `hyperparameter_tuning: optuna`, `outlier_treatment: drop` (multilabel rows dropped)
- `models_used`: xgboost, lightgbm, catboost, hist_gradient_boosting (**4 GBDTs only, no NN**)
- `fe_techniques`: Ratio (length/thickness); range × area interaction; min-max normalized thickness; feature dropping via CV + feature importance + correlation
- `original_data_usage: concat_rows`, `metric: Mean Columnwise AUC`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported / adapted | **5+ itemized** | Model 2 **replicated** from @noepinefrin's "0-89534-clustered-feature-lgbm-xgb-cat" notebook. Model 3 **adapted** from **@arunklenin's** "ps4e3-steel-plate-fault-prediction-multilabel" notebook. Final ensemble step adds @cyrilbourgeois's "playground-s4e03-xgboost-ensembler" output. Acknowledgments to @thomasmeiner (EDA+FE), @ankurgarg04 (model choice), @lucamassaron, @arnogils. |
| Author's own contribution | 1 of 3 OOF models | Author admits: *"simply ensembling the outputs from the public notebooks I mentioned with equal weights can get an excellent result"* (public LB 0.89684 / private 0.88923 from pure port-blend alone — would still be top-10). |
| Cross-author recurrence | **arunklenin** appears here (s4e3, Mar 2024, in port chain), at s4e7 (Jul 2024, as Cross Sellers team member), at s6e3 (Mar 2026, in cdeotte's references). **2-year recurring community contributor.** |

## What's actually original to this author
- **3-model OOF ensemble strategy**: one own pipeline (4 GBDTs, 10-fold CV, Optuna-tuned) + 2 public notebook OOF replications/adaptations → Nelder-Mead weight optimization.
- **Hand-engineered 3 features** + **drop 7 features** via CV + feature importance + pairwise correlation. Modest FE compared to s4-era heavy-FE winners.
- **Multilabel → multiclass conversion** by dropping rows with multiple labels (small portion) + argmax. Unusual data restructuring; author justified it by the small portion of multilabel rows.
- **Self-described first competition** — strong endorsement that **fork-heavy + small original additions can win top-3 for first-time competitors.** No claim of advanced technique invention.
- **Submission budget exhaustion → equal weights** in the final-step ensemble (validation-discipline anti-pattern; author explicit about not being able to validate the final blend).

## Dataset constraints that shaped this strategy
- **Small dataset (19K rows) + multiclass + all-numeric** → 4 GBDT families + modest FE + 10-fold CV is the natural baseline. No need for cdeotte-style heavy FE (too few rows) or NN diversity (too small).
- **Original multilabel structure** with rare multi-label rows → drop-and-convert-to-multiclass simplification.
- **Active public-notebook ecosystem in this competition** (multiple high-quality public notebooks at 0.89+ CV) → fork-heavy strategy is viable for newcomers.
- **Tight top-3 margin (0.00041)** → ensemble noise reduction has marginal value; OOF blending of public-notebook + own work is enough.

## Code vs writeup check
- ✓ Published notebook implements the 4-GBDT pipeline (XGB, LGBM, CatBoost, HGBC) with 10-fold CV + Optuna (cells 18, 20, 22, 24)
- ✓ FE function (cell 11) matches writeup's 3 engineered features
- ✓ Features-to-drop list (cell 13) matches writeup
- ⚠ The 3-model OOF blending + Nelder-Mead weight optimization is not directly visible in the published notebook (only Moonlit's own model is in the notebook; the other 2 are external OOF files referenced).
- ⚠ Final simple-ensemble step (with cyrilbourgeois's notebook output) is not in the published code.

## Headline finding
s4e3 (Mar 2024) is **the strongest fork-heavy-winning case for first-time competitors** in our set. Moonlit's 2nd place is primarily 3 OOF ensembles (1 own + 2 public-notebook replications/adaptations) plus a final equal-weight blend with another public notebook. She explicitly admits public-notebook blend alone scored 0.88923 private LB (top-10 by itself). **Fork-heavy ensembling is the documented entry-level path to top-3** — no novel techniques required, just careful OOF blending of strong public notebooks. **arunklenin appears here (Mar 2024), at s4e7 (Jul 2024, as team), at s6e3 (Mar 2026)** — 2-year recurring contributor across our entire analysis set.

## Surprising / unusual
- **First-time-competitor wins 2nd place via fork-heavy strategy** — author explicit about being a student in her first competition. Strong endorsement that the playground series rewards careful OOF blending of public notebooks, not just novel technique invention.
- **arunklenin recurring across 2 years**: s4e3 (Mar 2024, port source), s4e7 (Jul 2024, Cross Sellers team member), s6e3 (Mar 2026, cdeotte's references). Most-spanned community contributor in the set. Worth tracking what makes him a recurring source — likely his ability to produce strong baseline notebooks that others fork.
- **Multilabel → multiclass conversion by dropping multi-label rows** — unusual data restructuring, justified by "small portion" of such rows. Dataset-specific simplification.
- **"Public notebook blend alone scores 0.88923 (top-10)"** — explicit demonstration that fork-heavy can place top-10 with essentially zero original work. Strongest evidence in set for the "fork-heavy is a winning strategy" hypothesis.
- **GBDT-only ensemble** (4 GBDTs, no NN) — matches stopwhispering's s4e4 GBDT-only choice. **In April 2024 era (s4e3 + s4e4), winners were skipping NNs entirely.** NN inclusion in winning ensembles became more common in s4e7 (Cross Sellers) and later.
