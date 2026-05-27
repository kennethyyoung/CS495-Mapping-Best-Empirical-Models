# s6e1 — Rank 1: mahoganybuttstrings (Mahog)

## Identifiers
- **Competition:** [playground-series-s6e1](https://www.kaggle.com/competitions/playground-series-s6e1) — *Predicting Student Test Scores*
- **End date:** 2026-01-31
- **Rank / score:** 1 of ~3,500+ teams · 8.57273 private LB (RMSE) · 8.56634 CV. Top 3 spread: 8.57273 → 8.57689 → 8.57775 (0.00502 between 1st and 3rd).
- **Team / Kaggle user:** Mahog / [mahoganybuttstrings](https://www.kaggle.com/mahoganybuttstrings) — title "(I've ran out of catchy phrases :V)" implies 5th-or-later 1st place in the series
- **Writeup:** [1st place - (I've ran out of catchy phrases :V)](https://www.kaggle.com/competitions/playground-series-s6e1/writeups/1st-place-ive-ran-out-of-catchy-phrases-v) (local: `data/writeups/playground-series-s6e1/1st place - (I've ran out of catchy phrases _V) _ Kaggle.txt`)
- **Notebook (published):** [PG S6E1 - Ridge ensemble](https://www.kaggle.com/code/mahoganybuttstrings/pg-s6e1-ridge-ensemble-cv-8-56634-lb-8-57273) (local: `data/writeups/playground-series-s6e1/pg-s6e1-ridge-ensemble-cv-8-56634-lb-8-57273.ipynb`) — *Ridge meta-learner; the 190 base OOFs live in external Kaggle dataset `pg-s6e1-oofs`*

## Dataset
**Regression on `exam_score`, RMSE metric, 630K train rows. 11 features (mixed)** — first non-classification and first-without-public-original among the s6 writeups. No external dataset used (`original_data_usage: none`). Author observed that "CV/LB correlation was even better than S5E8/S5E11 and there was a decent amount of signal" — the dataset rewarded model strength beyond a long signal tail, with diminishing-but-real gains continuing to the end of the competition. Train/test CSVs not in `data/raw/`; schema recovered from notebook.

## What the spreadsheet currently records
- `primary_model: neural_network`, `best_single_model: RealMLP`, `dominant_base_model: neural_network`, `ensemble_method: stacking`, `cv_strategy: kfold`, `hyperparameter_tuning: random_search`
- **`original_data_usage: none`** — first of the s6 quartet
- `models_used`: RealMLP, XGBoost, TabM, CatBoost, DeepTables, LightGBM, Keras MLP, ResNet, FTTransformer, FFM (10 families; 7 NN + 4 GBDT — NN dominant by count, consistent with `dominant_base_model: neural_network`)
- `fe_techniques`: cyclical encoding, formula-based score feature (from public discussion), categorical copy of numerics for TE, digit features, TE (mean/std/skew) of feature and digit combinations, ordinal mapping of categoricals (GBDT set), Isotonic Regression post-processing
- Coding is accurate; `dominant_base_model: neural_network` *also* matches majority-by-count here (unlike s6e3 / s6e2 where the label was contested).

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **3 itemized** | (1) Cyclical features from @yekenot's notebooks; (2) formula-based feature from competition discussion [#665915](https://www.kaggle.com/competitions/playground-series-s6e1/discussion/665915); (3) ordinal categorical mapping from @cdeotte's notebook |
| Broad acknowledgments | 6 | @cdeotte, @yekenot, @omidbaghchehsaraei, @siukeitin, @masayakawamata, @mikhailnaumov |
| External Kaggle datasets used as input | 1 | `pg-s6e1-oofs` — author's *own* OOF dataset (190 model OOFs, generated locally) |
| Author cited *by* other winners | Yes | mahog appears as @mahoganybuttstrings in cdeotte's s6e3 references **5 times** and is named in masayakawamata's s6e2 thanks. With s6e1's citation of cdeotte/yekenot, the cross-citation network across the s6 quartet now has N=4 winners citing each other. |

Attribution depth sits between s6e3 (39 numbered refs) and s6e2 (no itemized refs) — three specific FE elements are credited, but the model pipeline and ensemble structure are framed as the author's own work. The 190 OOFs are all locally generated, not forks of public OOF dumps.

## What's actually original to this author
- **Two-feature-set design:** one optimized for NNs (cyclical + categorical copies + TE on digit combos), one for GBDTs (ordinal-mapped categoricals + base features + digit features). Explicit recognition that different model families want different representations — a structural choice rarely articulated in other writeups.
- **TE on digit combinations** (mean/std/skew) — extends the standard digit-feature technique into a TE-aggregated form.
- **Strength-over-diversity inversion:** explicitly *focused on stronger models rather than many different models* — opposite of masayakawamata's s6e2 strategy. Best single model (RealMLP) placed 7th on the LB by itself; the ensemble only gained 0.02 on top of that.
- **Hyperparameter-sweep-as-diversity:** WandB sweeps on RealMLP/TabM/GBDTs with **all trial OOFs saved into the ensemble** (not just the best per family). This took him from 8.5335 to 8.5309 — the largest single performance boost he reported.
- **Centered Isotonic Regression post-processing** applied at *two* points: (1) per-OOF before stacking, and (2) on Ridge output before submission. Applied in both stages was demonstrably better than either alone.
- **RidgeCV(alpha=[1]) stacker** — same family choice as masayakawamata (linear, anti-overfit) but with a fixed alpha rather than CV-searched.

## Dataset constraints that shaped this strategy
- **Regression + RMSE metric + no public original** → no "exploit-original" toolkit is available, so the FE has to extract signal from the synthetic features alone. Forces reliance on universal techniques (digits, TE combinations, cyclical, formula-based features from discussion).
- **CV/LB correlation reported as unusually strong** (better than S5E8/S5E11) and **long signal tail** (gains continued to deadline) → makes "stronger models" worthwhile rather than "diverse weak models" — the marginal model genuinely helps. The opposite competition profile from s6e2.
- **Small feature space (11 features, max_cardinality=7)** → makes exhaustive FE feasible (cyclical × digit × categorical-copy × TE combinations) without combinatorial blow-up.
- **Mature S6E1-era ecosystem** (yekenot's cyclical features, cdeotte's ordinal mapping, discussion #665915's formula already public) → key building blocks are easy to import; the author can spend effort on hyperparameter search and ensemble construction rather than baseline FE.

## Code vs writeup check
- ✓ Ridge ensemble notebook loads ~190 OOFs from `/kaggle/input/pg-s6e1-oofs/` (cell 2), each accompanied by a `*_oof.csv` for the training fold predictions
- ✓ Centered Isotonic Regression applied per-OOF before Ridge stacking (cell 4) and again on Ridge output (cell 12) — matches the "before AND after" two-stage post-processing the writeup describes
- ✓ RidgeCV(alphas=[1]) used as stacker (cell 7) — single fixed alpha, no CV search over alpha
- ⚠ The 190 OOF generation code is not in the published notebook (lives in the external `pg-s6e1-oofs` Kaggle dataset). The two-feature-set FE pipeline is described in the writeup but not in code form here.
- ⚠ Notebook uses plain `KFold` (regression-appropriate) not `StratifiedKFold` — spreadsheet correctly records `cv_strategy: kfold` (vs `stratified_kfold` for the classification s6 entries).

## Headline finding
mahog won s6e1 by **strength-over-diversity** — the opposite of masayakawamata's s6e2 strategy. With CV/LB unusually correlated and the dataset still rewarding marginal improvements at the deadline, scaling up *quality* of each base model (hyperparameter sweeps × every-trial-OOF saved × 10 architecture families) plus Ridge + double isotonic post-processing was the winning formula. The lack of a public original dataset eliminated the "exploit-original" axis that drove s6e2/s6e3/s6e4.

## Surprising / unusual
- **Best single model placed 7th on the LB** by itself — the ensemble only added 0.02 of RMSE improvement over a single RealMLP. Demonstrates that this competition's signal could be largely captured by one strong model, sharply different from s6e2 where ensembling was the lever.
- **Two contradictory winning strategies in adjacent months** (s6e2 = diversity-wins, s6e1 = strength-wins, same author community, same model families). Strong evidence that strategy is dataset-constrained, not author-constrained.
- **"Save every hyperparameter-tuning trial's OOF and feed all of them to the stacker"** is a clever combination of HP tuning + ensembling that doesn't have an obvious name in the literature and isn't captured by the spreadsheet's `hyperparameter_tuning: random_search`.
- **mahog cross-citation density**: cited 5 times in s6e3 (cdeotte) + named in s6e2 (masayakawamata) + cites cdeotte and yekenot in s6e1. All 4 s6 winners are part of one tight cross-citation network.
