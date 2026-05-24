# s5e12 — Rank 1: wind1234it

## Identifiers
- **Competition:** [playground-series-s5e12](https://www.kaggle.com/competitions/playground-series-s5e12) — *Diabetes Prediction Challenge*
- **End date:** 2025-12-31 (4,206 teams)
- **Rank / score:** 1 of 4,206 · 0.70504 private LB (ROC AUC). Top 3 spread: 0.70504 → 0.70502 → 0.70497 (0.00007 across 1st–3rd — photo finish).
- **Team / Kaggle user:** [wind1234it](https://www.kaggle.com/wind1234it)
- **Writeup:** [1st Place Solution | Hill Climbing + Ridge Ensemble](https://www.kaggle.com/competitions/playground-series-s5e12/writeups/1st-place-solution-hill-climbing-ridge-ensembl) (local: `data/writeups/playground-series-s5e12/1st Place Solution _ Hill Climbing + Ridge Ensemble _ Kaggle.txt`)
- **Notebook (published):** [s5e12 | 1st place solution | HC & Ridge](https://www.kaggle.com/code/wind1234it/s5e12-1st-place-solution-hc-ridge) (local: `data/writeups/playground-series-s5e12/s5e12-1st-place-solution-hc-ridge.ipynb`) — 1 markdown + 1 56KB code cell; meta-ensemble only, base OOFs live in external `oof-diabetic` Kaggle dataset

## Dataset
Binary classification of `diagnosed_diabetes`, ROC AUC metric, 700K train rows, 25 mixed features. **`distribution_shift: TRUE`** — train data has a roughly identifiable cutoff (`CUTOFF_ID = 678260` in the notebook) after which the distribution matches test. Public original diabetes dataset available (`original_data_usage: yes`). Score absolute range is low (~0.70), meaning weak per-feature signal — ensembling has large marginal value. Train/test CSVs not in `data/raw/`; schema recovered from notebook config.

## What the spreadsheet currently records
- `primary_model: ensemble`, **`cv_strategy: post_cutoff`** (a value not seen in s6), `ensemble_method: hill_climbing; stacking`
- `dominant_base_model: gbm`, `original_data_usage: yes`, `distribution_shift: TRUE` (only entry so far with this flag)
- `models_used`: XGBoost, LightGBM, CatBoost, NN, Ridge, AutoML (also HistGradientBoosting visible in code)
- `fe_techniques`: ratio features (medical domain pairs), polynomial (sq/cb), target encoding, original data concat
- All accurate; `cv_strategy: post_cutoff` is the only schema value in the codebook specifically introduced for this case.

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks / discussions explicitly named | **1 itemized port + 5 broad thanks** | (1) "post-cutoff cross-validation approach" explicitly credited to **@masayakawamata** (cited before masayakawamata himself wins s6e2). Author has one base model literally named `01122025_XGB_Masaya_approach`. Broad thanks: @daylighth, @laureanoarcanio, @tilii, @mikhailnaumov, @siukeitin. |
| External Kaggle datasets used as input | 1 | `oof-diabetic` — author's *own* OOF dataset, ~100 model OOFs spanning XGB / LGB / CatBoost / HistGB / NN / Ridge stacks / prior HC ensembles. Includes "ensembles-of-ensembles" (HC outputs fed back as HC inputs). |
| Cross-author network position | Cited *to* | Cites masayakawamata (S5-era contact); broad-thanks list overlaps with the s6-era community (tilii, mikhailnaumov, siukeitin all appear in s6 writeups). The community is contiguous across s5→s6. |

Attribution is sparse on items but explicit on the conceptually most important one (post-cutoff CV from masayakawamata). The other ~100 base OOFs are author-generated.

## What's actually original to this author
- **Two-stage meta-ensemble: HC selection → Ridge stacking on top-N.** Stage 1 hill-climbing greedy forward selection (rank-blend, negative weights allowed −0.3..+0.5, GPU AUC) picks ~60 from ~100 candidates. Stage 2 Ridge regression (α=10) on top-36 rank-transformed predictions, fit on post-cutoff data only.
- **Cutoff identification (`CUTOFF_ID = 678260`).** Manual probe to find where train distribution starts matching test, so validation can be restricted to the matching region. Different from masayakawamata's CV–LB discipline: this is structural rather than empirical.
- **Negative weights in HC blending** (range −0.3 to +0.5) — lets models *subtract* predictions when they correlate with errors of other models. Uncommon outside this writeup.
- **Rank transformation before blending** — handles base models with different output scales without requiring calibration.
- **HC of ensembles, not just single models** — feeds prior Ridge / HC outputs back in as candidate models (visible in the MODELS list: multiple entries are themselves stacks). Meta-meta-ensembling.
- **Anti-greedy final-submission choice**: had Ridge top-34/α=5 with private LB 0.70514 (better than chosen) but rejected it because public LB gap was too wide. Same family of judgement as masayakawamata's s6e2 move.

## Dataset constraints that shaped this strategy
- **Distribution shift between train and test** → forces a non-standard validation strategy. Optimizing on full CV would chase pre-cutoff patterns that don't generalize. Post-cutoff CV is the technique that makes the rest of the pipeline measurable.
- **Tight top-N margin (0.00007 spread) + low absolute score (0.70x) + weak per-feature signal** → ensembles have large marginal value AND single-model CV is high-variance gambling. The two-stage HC+Ridge meta-architecture is precisely the toolkit for this profile.
- **Public original dataset available** → unlocks "Orig_as_columns" feature engineering (one of the base models explicitly named for this) and confirms the s6-era exploit-original pattern extends back into s5.
- **Many public discussion contributors already in the community** (masayakawamata's post-cutoff idea, tilii's diagnostics, etc.) → the conceptual key (post-cutoff CV) was a recent community innovation the author could adopt rather than discover.

## Code vs writeup check
- ✓ Notebook is a single ~56KB code cell + markdown intro — confirms the HC + Ridge architecture, lists ~100 MODELS entries, defines `CUTOFF_ID = 678260` and post-cutoff-only training for Ridge
- ✓ `RIDGE_TOP_N = 36`, `RIDGE_ALPHA = 10.0`, rank-blending HC with negative weights — matches writeup
- ✓ Model name `01122025_XGB_Masaya_approach` and `Orig_as_columns` confirm explicit ports of named techniques
- ⚠ The base-model training code is **not** in the published notebook — ~100 OOFs live in the `oof-diabetic` external dataset. Full reproducibility would require those scripts.
- ⚠ The `models_used` field doesn't capture HistGradientBoosting (visible in the MODELS list) or the "ensemble-of-ensembles" structure (where Ridge stacks and prior HC outputs are themselves candidate models inside the meta-HC).

## Headline finding
s5e12 was won by **distribution-shift-aware validation** combined with a HC+Ridge two-stage meta-ensemble. The conceptual key — post-cutoff CV — was credited to masayakawamata (a S5-era community innovation) and ported here; the author's contribution was scaling it up with ~100 base models, allowing negative HC weights, and using ensembles-of-ensembles as candidates. The validation discipline pattern previously identified for s6e2 (photo-finish + ROC AUC) is here driven by a *different* root cause (distribution shift), not the photo-finish.

## Surprising / unusual
- **First case where distribution shift is the headline constraint.** Forces a custom validation scheme that doesn't appear in any of the four s6 writeups. The spreadsheet has `cv_strategy: post_cutoff` as a value, but this is essentially a one-off bespoke approach, not a reusable category.
- **The same author (masayakawamata) shows up cross-period**: he wins s6e2 in Feb 2026 with validation-discipline framing, but his "post-cutoff CV" technique was already informing the s5e12 winner (a different person) in Dec 2025. Suggests techniques propagate through the community faster than competitions, and "who wins" is often "who applied the latest technique best."
- **HC with negative weights and ensembles-as-candidates** — both are unusual moves not present in the s6 quartet. Possibly an artifact of weak-signal datasets where standard stacking saturates.
- **Score values around 0.70 (vs 0.91+ in s6e3 churn, 0.95+ in s6e2 heart, 0.98+ in s6e4 irrigation)** — the diabetes task was much harder. Worth tracking whether absolute-score-level correlates with which strategy family wins.
