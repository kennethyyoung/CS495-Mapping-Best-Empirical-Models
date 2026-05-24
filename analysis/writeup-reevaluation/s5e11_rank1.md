# s5e11 — Rank 1: mahoganybuttstrings (Mahog)

## Identifiers
- **Competition:** [playground-series-s5e11](https://www.kaggle.com/competitions/playground-series-s5e11) — *Predicting Loan Payback*
- **End date:** 2025-11-30 (3,724 teams)
- **Rank / score:** 1 of 3,724 · 0.92939 private LB (ROC AUC). Top 3 spread: 0.92939 → 0.92934 → 0.92917 (0.00022 between 1st and 3rd — moderate, not photo-finish).
- **Team / Kaggle user:** Mahog / [mahoganybuttstrings](https://www.kaggle.com/mahoganybuttstrings) — same author as s6e1
- **Writeup:** [1st place - A lot of features, a lot of models, and a little bit of luck](https://www.kaggle.com/competitions/playground-series-s5e11/writeups/1st-place-a-lot-of-features-a-lot-of-models-an) (local: `data/writeups/playground-series-s5e11/1st place - A lot of features, a lot of models, and a little bit of luck _ Kaggle.txt`)
- **Notebook (published):** [PG S5E11 - XGB - CV 0.92818 PB 0.92923](https://www.kaggle.com/code/mahoganybuttstrings/pg-s5e11-xgb-cv-0-92818-pb-0-92923) (local: `data/writeups/playground-series-s5e11/pg-s5e11-xgb-cv-0-92818-pb-0-92923.ipynb`) — the *best single XGB model only*; the 100-model Ridge/HC ensemble code isn't published. **This is the notebook cdeotte explicitly ported into s6e3 as `mahog-700.ipynb`.**

## Dataset
Binary classification of loan payback, ROC AUC metric, 593,994 train rows. 12 features (mixed), max_cardinality=30 (highest among s5/s6 writeups so far — has higher-cardinality categoricals like `credit_score` ranges). Synthetic data with a public original loan dataset (`original_data_usage: concat_rows` — original rows concatenated into training). No distribution shift flagged. Train/test CSVs not in `data/raw/`; schema recovered from notebook.

## What the spreadsheet currently records
- `primary_model: ensemble`, `best_single_model: XGBoost`, `dominant_base_model: gbm`, `ensemble_method: hill_climbing; stacking`, `cv_strategy: stratified_kfold`
- **`hyperparameter_tuning: none`** — author explicitly says "I trained as many diverse models as possible and not spend that much time tuning them"
- `original_data_usage: concat_rows` (distinct from s6's `yes` — captures the *type* of use)
- `models_used`: 16 families listed; writeup actually shows 23 (also LAMA-DenseLight, LAMA-Dense, TabulaRNN, ExcelFormer, ModernNCA). Spreadsheet undercount.
- `fe_techniques`: digit extraction, pairwise/triple/quadruple digit interactions + TE/CE, base feature pairs + TE/CE, quantile binning, categorical credit_score, **TE with alternative targets** (a distinctive technique discussed below)

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **1 itemized + 6 broad thanks** | Round features ported from [masayakawamata's s5e11 notebook](https://www.kaggle.com/code/masayakawamata/s5e11-single-xgb-add-features); broad thanks to @cdeotte, @masayakawamata, @yekenot, @yeoyunsianggeremie, @jklol86, @mikhailnaumov |
| External Kaggle datasets used as input | 1 | Original loan dataset (referenced for TE on alternative targets, concatenated rows in training) |
| Author cited *by* other winners | Yes, heavily | This notebook (`pg-s5e11-xgb-cv-0-92818-pb-0-92923`) was explicitly ported into cdeotte's s6e3 solution as `mahog-700.ipynb`. mahog also cited in masayakawamata's s6e2 and his own s6e1 work was preceded by this. |

Attribution is similar to s6e1 — 1 explicit port + a thank-you list. The notebook itself became a community asset that propagated forward into at least s6e3.

## What's actually original to this author
- **Digit interaction combinatorics:** pairwise/triple/quadruple combinations of digits *across different numerical features*, each TE/CE encoded. Goes beyond the single-feature digit features seen in other writeups.
- **Target encoding with alternative targets**: TE features using `employment_status` and `debt_to_income_ratio` as the prediction target (not the actual `loan_payback` y). Uses auxiliary structure in the data to encode information that isn't directly target-encoded. Unique among the writeups so far.
- **Mixed Ridge + HC ensembling** — both methods used, and "HC was slightly better on CV but about the same on PB," so the final ensemble combines both. Nonlinear stackers (LGBM/CB/NN) tested and rejected as "much worse than linear methods" — explicit confirmation of the universal linear-stacker pattern.
- **Diversity-first, no hyperparameter tuning** — explicit competition-strategy choice: train 23+ model families with default hyperparameters rather than tune any one model deeply. Author notes he plans to switch strategy next month, and indeed does in s6e1.
- **Best single model would have placed 2nd by itself** (XGB CV 0.92818 / PB 0.92923 vs 2nd place 0.92934). The 100-model ensemble adds only 0.00016 on top — similar to the s6e1 pattern where his best single placed 7th.

## Dataset constraints that shaped this strategy
- **Synthetic data with public original concatenated as training rows** → unlocks TE on alternative targets (employment_status / debt_to_income_ratio), since the original has those columns and can compute auxiliary target statistics; also enables more diverse FE because more rows = more signal for binning + digit features.
- **Moderate top-N margin (0.00022)** + **long signal tail** (best single near podium, ensemble adds tiny increment) → similar profile to s6e1; rewards quantity of FE + diversity of models. No need for validation-discipline gambits.
- **Higher max_cardinality (30) than the s6 quartet** → makes target/count/frequency encoding more powerful; explains why TE+CE on combinations of base features, digits, and interaction triples/quadruples produced so much signal.
- **Many public notebooks and discussion contributors already engaged** → standard FE primitives (digits, TE, round features) all available to import; author can focus on *combinatorics* of these primitives rather than inventing new ones.

## Code vs writeup check
- ✓ Published notebook is the best-single XGB only (matches name); confirms digit features, pairwise TE/CE, 5-fold CV (but tilii flagged in comments a `pred /= 5` that should be `pred /= 20` — minor bug that didn't affect leaderboard since predictions were ranked)
- ✓ Notebook is the exact one cdeotte ported into s6e3's `mahog-700.ipynb` reference
- ⚠ The 100-model Ridge/HC ensemble code is **not** in the published notebook — only the single XGB. All 22 other base models live elsewhere unpublished.
- ⚠ Spreadsheet `models_used` lists 16, but writeup shows 23 distinct families (missing: LAMA-DenseLight, LAMA-Dense, TabulaRNN, ExcelFormer, ModernNCA, plus XGBoost-regression and LightGBM-dart as separate entries).
- ⚠ `hyperparameter_tuning: none` is unusual — most writeups would say `random_search` or similar; mahog's explicit "no tuning" stance is captured correctly.

## Headline finding
mahog won s5e11 with **diversity-without-tuning** (23 model families × heavy FE combinatorics × Ridge+HC stacker) — the strategy he *inverted* one month later in s6e1 (10 model families × heavy hyperparameter tuning × Ridge stacker). Two consecutive 1st-place finishes by the same author using opposite strategies. The competition profile (long signal tail, moderate margin, high cardinality, original dataset available) made FE combinatorics + diversity the better lever this time.

## Surprising / unusual
- **TE with alternative targets** (employment_status, debt_to_income_ratio) — first time this technique appears in the re-evaluation. Worth flagging for future writeups: do other winners use auxiliary-target TE?
- **Same author, opposite strategies in adjacent months** (s5e11 diversity-no-tuning, s6e1 strength-with-tuning, both 1st place). Direct within-author evidence that the constraint→strategy coupling is the right unit of analysis. Author explicitly anticipates the switch: "I feel like I should change this strategy a bit next comp."
- **Best single model would have placed 2nd by itself** — once again the ensemble's margin over best-single is small (0.00016 here, 0.02 RMSE in s6e1). Suggests mahog's recipe is fundamentally "build one very strong model with heavy FE, then ensemble cheaply for safety."
- **This notebook is the most-citation-receiving artifact in the s5–s6 community to date** — explicitly ported into cdeotte's s6e3 solution, broadly referenced elsewhere. Acts as a community-shared baseline.
