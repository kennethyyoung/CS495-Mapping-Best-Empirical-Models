# s6e4 — Rank 1: cstdy / kirill0212

## Identifiers
- **Competition:** [playground-series-s6e4](https://www.kaggle.com/competitions/playground-series-s6e4) — *Predicting Irrigation Need*
- **End date:** 2026-04-30
- **Rank / score:** 1 of ~2,300+ teams · 0.98158 balanced accuracy
- **Team / Kaggle user:** cstdy / [kirill0212](https://www.kaggle.com/kirill0212)
- **Writeup:** [1st place: One vs Rest approach](https://www.kaggle.com/competitions/playground-series-s6e4/writeups/1st-place-one-vs-rest-approach) (local: `data/writeups/playground-series-s6e4/1st place_ One vs Rest approach _ Kaggle.txt`)
- **Notebook:** [PS6e4 Ensemble CV 0.98155](https://www.kaggle.com/code/kirill0212/ps6e4-ensemble-cv-0-98155) (local: `data/writeups/playground-series-s6e4/ps6e4-ensemble-cv-0-98155.ipynb`)

## Dataset
Multiclass classification on `Irrigation_Need` ∈ {Low, Medium, High}, balanced accuracy metric, 630K train rows. 19 features: 11 numeric (soil, weather, field — `Soil_pH`, `Soil_Moisture`, `Organic_Carbon`, `Electrical_Conductivity`, `Temperature_C`, `Humidity`, `Rainfall_mm`, `Sunlight_Hours`, `Wind_Speed_kmh`, `Field_Area_hectare`, `Previous_Irrigation_mm`) and 8 categorical (`Soil_Type`, `Crop_Type`, `Crop_Growth_Stage`, `Season`, `Irrigation_Type`, `Water_Source`, `Mulching_Used`, `Region`). Class structure key: Low and High are rarely confused; Medium vs High is the hard distinction. External data used: yes — `miadul/irrigation-water-requirement-prediction-dataset` (Kaggle Datasets), concatenated into training. Train/test CSVs not in `data/raw/`; schema recovered from notebook cell 0.

## What the spreadsheet currently records
- `primary_model: gbm`, `ensemble_method: stacking`, `best_single_model: XGBoost`
- `models_used`: XGBoost, LightGBM, CatBoost, RealMLP, TabM, LR, HistGBM, YDF, GNN, Transformer
- `fe_techniques`: digit features, magnitude rounding, frequency encoding, pairwise interaction crosses, target encoding
- `cv_strategy: stratified_kfold`, `original_data_usage: yes`
- These fields are accurate at the *component* level but describe what was used, not what was originated.

## Public-notebook reuse
| Source | Count | Share of final 61 OOFs |
|---|---|---|
| @wguesdon's 30-model OOF dataset | 30 | 49% |
| Other named public contributors (mahog, utaazu, yunsuxiaozi, include4eto, yekenot, mikhail_naumov, maria_nadeem, lucas_moraes, rohit, ashish, gnn) | ~24 | ~39% |
| kirill0212's own models | 6–7 | ~10% |

Source attribution is explicit in both writeup and notebook (cells 20–24, where loaded features are prefixed with each public author's handle). Author states even his own FE is "still based on public notebooks." Key Low-vs-High observation credited to discussion [#690677](https://www.kaggle.com/competitions/playground-series-s6e4/discussion/690677).

## What's actually original to this author
- **Two-binary-classifier reframing** of the 3-class problem: Model 1 = Low vs Rest on full data; Model 2 = Medium vs High trained only on Med+High rows, OOFs for full data
- **Probability recombination formulas:** P(Low) = P(M1), P(Med) = (1−P(M1))·(1−P(M2)), P(High) = (1−P(M1))·P(M2)
- **Ensembling pipeline:** logit transform + `LogisticRegressionCV` on each binary classifier's OOFs across all 61 models, averaged over `SEED_LIST = [60, 0, 2809]`
- **Threshold search (cell 48):** 2D grid over class-mean offsets (a, b) ∈ [0, 0.01] step 0.0002, optimizing balanced accuracy

## Dataset constraints that shaped this strategy
- **Multiclass + severe imbalance (High class small) + balanced-accuracy metric** → the binary reframe is metric-driven: balanced accuracy weights the rare class equally, so the Medium-vs-High decision that a single 3-way model averages over deserves its own dedicated classifier.
- **Public observation that Low and High are almost never confused** (discussion #690677) → makes the binary decomposition information-preserving rather than destructive. The reframing strategy is *enabled* by the class structure, not invented in a vacuum.
- **Available external dataset** (`miadul/irrigation-water-requirement-prediction-dataset`) → unlocks the `original_data_usage: yes` axis and supports digit + magnitude-rounding FE that exploits cross-source value alignment.
- **Many public notebooks already covered FE/preprocessing** → made fork-heavy OOF ensembling cheap and freed effort for the meta-architecture (the actual win).

## Code vs writeup check
- ✓ External `orig` dataset loaded and concatenated (cell 1)
- ✓ Kirill's own FE — digit features + magnitude rounding (cell 1), pairwise interaction crosses (cell 4), TargetEncoder per-fold (cell 19)
- ✓ wguesdon's 30 OOFs loaded as `.npy` from external dataset (cell 23)
- ✓ Two-binary-classifier architecture (cells 38–46), probability recombination (cell 47), threshold search (cell 48)
- ⚠ Writeup says 6 own-models, code shows 7 after exclusions in cell 24 — likely because `my_rmlp_xgb_2` is a blend, not a clean own-model

## Headline finding
~90% of the winning ensemble's OOFs came from other Kaggle users. Kirill's winning edge was a *meta-architecture* — the two-binary-classifier reframing, logit-blended LR stack, and balanced-accuracy threshold search — not the FE or base models the spreadsheet attributes to him.

## Surprising / unusual
Unusually explicit attribution — the writeup gives an exact 30/25/6 breakdown of OOF sources and even credits the key observation to a discussion post. Most writeups will not be this transparent.
