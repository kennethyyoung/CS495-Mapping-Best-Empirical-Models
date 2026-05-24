# s5e10 — Rank 1: Tilii (tilii7)

## Identifiers
- **Competition:** [playground-series-s5e10](https://www.kaggle.com/competitions/playground-series-s5e10) — *Predicting Road Accident Risk*
- **End date:** 2025-10-31 (4,082 teams)
- **Rank / score:** 1 of 4,082 · 0.05563 private LB (MSE). **Top 4 tied at 0.05563**; next ~200 competitors at 0.05564. Author: "this seems extreme even by Kaggle standards."
- **Team / Kaggle user:** Tilii / [tilii7](https://www.kaggle.com/tilii7) — frequent commenter in the s5–s6 community (cited in s5e11, s5e12, s6e1, s6e2 writeups)
- **Writeup:** [1st place - I think it was genetic programming](https://www.kaggle.com/competitions/playground-series-s5e10/writeups/1st-place-i-think-it-was-genetic-programming) (local: `data/writeups/playground-series-s5e10/1st place - I think it was genetic programming _ Kaggle.txt`)
- **Notebooks (published):** [s5e10 Genetic Programming Features](https://www.kaggle.com/code/tilii7/s5e10-genetic-programming-features) (GP derivation) and [s5e10 TabM tuned further](https://www.kaggle.com/code/tilii7/s5e10-tabm-tuned-further) (TabM port from masayakawamata + further Optuna tuning); locals in `data/writeups/playground-series-s5e10/`

## Dataset
Regression on `accident_risk`, MSE metric, 517,754 train rows. 13 features (mixed), max_cardinality=3 (almost entirely numerical/binary). Notable: Tilii used Lasso on the training data to *reverse-engineer the synthetic generator's target formula* (≈ 0.3·curvature + 0.2·(lighting=night) + 0.1·(weather≠clear) + 0.2·(speed_limit≥60) + 0.1·(accidents>2)). **No mention of an external public original dataset** in the writeup — `original_data_usage: yes` in the spreadsheet appears to refer to the competition-provided train data, not an external Kaggle dataset (possible spreadsheet semantic mismatch — flag).

## What the spreadsheet currently records
- `primary_model: ensemble`, `best_single_model: ` *(empty)*, `dominant_base_model: gbm`
- `cv_strategy: kfold` (regression, not stratified), `hyperparameter_tuning: optuna`, `ensemble_method: hill_climbing; stacking`
- `models_used`: XGBoost, CatBoost, NN, Lasso, AutoGluon, Autoencoder (writeup also names Keras FM, TabM, TF embedding networks)
- `fe_techniques`: Autoencoder latent features, **11 genetic programming features**, XGBoost residual boosting, multiple feature type representations
- `original_data_usage: yes` — semantically ambiguous in this case (no external dataset evident in writeup); other s5/s6 entries use the field to mark *external* original usage.

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **2 itemized** + 5 broad thanks | (1) **TabM notebook from @masayakawamata** — port + further Optuna tuning (the published `s5e10-tabm-tuned-further.ipynb` is the adapted version); (2) **XGB residual boosting technique from @cdeotte** (added too late to help much). Broad thanks: @cdeotte, @siukeitin, @optimistix, @mikhailnaumov, @mahoganybuttstrings. |
| Cross-author network position | Cited *to* | Tilii is heavily cited *in* s5e11, s5e12, s6e1, s6e2, s6e3 community comments. cdeotte commented on this writeup: *"I particularly like Genetic Programming, AutoEncoder, and Keras FM. I will need to try these in future competitions."* — and indeed cdeotte's s6e3 KGMON Playbook uses all three. **Direct propagation: techniques tested by Tilii in s5e10 → cited and used by cdeotte in s6e3 four months later.** |

## What's actually original to this author
- **Genetic programming features added at the ENSEMBLING stage, not as base-model inputs.** Tilii's key insight: GP features didn't work as base-model features or single-model additions, but *did* work when added as inputs to the second-level ensembler (alongside the base-model OOFs). 11 features → 0.00001 improvement.
- **Two-level meta-architecture with intermediate nonlinear stackers:** (1) ~40–50 base models → (2) Keras NN ensemble → (3) CatBoost ensemble using Keras output as baseline + 11 GP features (essentially residual boosting at the ensemble layer) → (4) HC of 4 such two-level ensembles. The intermediate stackers are nonlinear, which is a partial deviation from the "linear stacker is universal" pattern (the *final* HC is linear-blend, so the meta-meta-stacker stays linear).
- **Lasso as diagnostic tool** — used not for prediction but to *discover the synthetic generator's target formula*. Then a separate GP run constrained to only [+, −, ×, ÷] reproduced essentially the same formula independently — confirming the generator structure. Unique among the writeups.
- **TabM fine-tuning beyond masayakawamata's original** — three Optuna-tuned parameter sets that beat the original TabM CV score, all published in the secondary notebook.

## Dataset constraints that shaped this strategy
- **Regression + MSE + 4-way tie at 0.05563 + ~200 competitors at 0.05564** → most extreme photo-finish so far. Makes marginal ensemble tricks (GP-at-ensemble-stage, residual-boost-ensembler) the only remaining levers because base-model improvements stopped mattering 3 weeks before deadline.
- **Underlying target is nearly linear** (Lasso recovers most signal at CV 0.058) → nonlinear features add only tiny ensemble-level diversity, not core predictive power. Explains why GP features failed at the base level but worked at the ensemble level (where small uncorrelated signal helps).
- **Author's 3-week time budget + late plateau** → drove the "throw many ensembling tricks at the wall" approach rather than deep per-model tuning. Same constraint motivated the GP-at-ensemble-stage discovery.
- **No external public original dataset** (in the s6 sense) → the exploit-original toolkit isn't applicable; Lasso-reverse-engineering of the generator is the closest analog Tilii has.

## Code vs writeup check
- ✓ `s5e10-genetic-programming-features.ipynb` shows the 11 GP feature derivations including the deeply-nested formula for GP_11 (sqrt/abs/sin/cos chains)
- ✓ `s5e10-tabm-tuned-further.ipynb` is the TabM port from masayakawamata with three Optuna-tuned configs (two commented out)
- ⚠ The 40–50 base-model code, the Keras NN ensembler, the CatBoost residual ensembler, and the final HC are **not** in the published notebooks
- ⚠ Spreadsheet `models_used` undercounts: writeup also names Keras FM, TabM, TF embedding networks (vs spreadsheet's "NN" lumped category)
- ⚠ `original_data_usage: yes` is ambiguous (no external Kaggle dataset evident) — possible spreadsheet semantic mismatch with the s6-era use of this field

## Headline finding
Tilii won the most extreme photo-finish in the analysis set (top 4 tied at 0.05563) by **ensemble-stage engineering** — adding GP features at the second-level stacker rather than as base features, using CatBoost as a residual booster *on the Keras ensemble's predictions*, then HC-blending several such two-level ensembles. The base-model strength saturated 3 weeks before deadline; everything that moved the needle after that lived at the meta-architecture layer. The published Lasso-as-diagnostic and the GP-at-ensemble-stage trick are the most distinctive original contributions.

## Surprising / unusual
- **GP features at ensemble stage, not base stage** — first time we see this placement. Worth tracking whether other writeups use the same pattern.
- **Lasso used to reverse-engineer the generator's target formula** — diagnostic-only use of Lasso, not predictive. Concrete example of how synthetic-data exploitation works *without* an external original dataset (recover the generator instead of using a real-world source).
- **Concrete cross-month technique propagation**: cdeotte commented on this writeup saying he'd try GP + AE + Keras FM in future competitions — and the s6e3 KGMON Playbook (4 months later) explicitly uses all three. Direct line from s5e10 idea → s6e3 production use.
- **Intermediate stackers were nonlinear** (Keras NN + CatBoost-with-baseline), even though the final HC layer is linear-blend. Partial wrinkle on the "linear stacker is universal" coupling — depends on whether you count only the final layer or the whole pipeline.
- **Author's "I think it was genetic programming" title** — explicit acknowledgement that the winning margin is so small (0.00001 between trial GP-vs-no-GP) that attribution itself is uncertain. Three Kagglers tied with him.
