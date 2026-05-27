# s5e6 — Rank 1: cdeotte (Chris Deotte)

> **Caveat:** No notebook available in local set (writeup-only evaluation, mirror of s5e7's notebook-only). Per-cell verification not possible; pipeline reconstructed from writeup text + spreadsheet alone.

## Identifiers
- **Competition:** [playground-series-s5e6](https://www.kaggle.com/competitions/playground-series-s5e6) — *Predicting Optimal Fertilizers*
- **End date:** 2025-06-30 (2,648 teams)
- **Rank / score:** 1 of 2,648 · 0.38652 private LB (MAP@3). Top 3: cdeotte 0.38652 → masayakawamata 0.38518 → mahog 0.38513 (top 3 are the same community-heavyweight names that appear across the analysis set).
- **Team / Kaggle user:** Chris Deotte / [cdeotte](https://www.kaggle.com/cdeotte) — second cdeotte entry (also won s6e3)
- **Writeup:** [1st Place - Fast GPU Experimentation with RAPIDS cuDF cuML](https://www.kaggle.com/competitions/playground-series-s5e6/writeups/chris-deotte-1st-place-fast-gpu-experimentation-wi) (local: `data/writeups/playground-series-s5e6/1st Place - Fast GPU Experimentation with RAPIDS cuDF cuML _ Kaggle.txt`)
- **Notebook:** **none in local set** — author references his code in the writeup but no `.ipynb` was scraped

## Dataset
Multiclass classification of `Fertilizer Name` (7 classes), **MAP@3** metric (first ranking metric in the analysis set — sensitive to top-3 calibrated probabilities), 750K train rows. 9 features (mixed), max_cardinality=11. Synthetic data generated from a public original; importantly, **author noted (from a discussion post he read before competing) that the original's targets are random numbers** — meaning original-as-rows adds noise, while original-as-columns lets models "reverse-engineer the Kaggle synthetic data generation process." This priors-from-discussion shaped his strategy from day one.

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: hill_climbing`
- `cv_strategy: repeated_stratified_kfold` (first time — ported from @bizen250's public notebook)
- `hyperparameter_tuning: manual` (depths 4/10/18 set explicitly, not searched)
- `original_data_usage: concat_rows;merge_columns` — **both modes explicitly used** in the same final ensemble
- `models_used`: xgboost, lightgbm, catboost, neural_network, linear_regression
- `fe_techniques`: all pairs/triples/quadruples of 8 features (162 combos); TE of 162 combos × 7 binary targets (2268 cols); TE using original dataset; **residual boosting (XGB over LR base margin)**; pseudo labeling; repeated KFold seed averaging; retrain on 100% data
- Coding is unusually accurate and granular — all 7+ playbook techniques captured.

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **4 itemized** in the 9-model final ensemble | (1) @bizen250's RepeatedStratifiedKFold XGB; (2) @ayushchandramaurya's stacking XGB over LGBM; (3) @elainedazzio's XGB depth=18 with original-as-rows; (4) @ricopue's NN. cdeotte trains many seeds per ported model (e.g., 50 XGBs, 100 NNs). |
| cdeotte's own model contributions | 5 of 9 | Original-as-columns XGB (depth 4 + depth 10), Stacking NN, Stacking XGB with pseudo-label COLUMNS, NN with pseudo-label ROWS. |
| Approximate fraction of public-notebook OOFs in final | ~44% by model count, weighted by seed-multiplied prediction sets (~300 total) | This is the *earlier, smaller* version of the same fork-heavy pattern seen in s6e3 (39 references). The KGMON Playbook *is* fork-heavy by design. |

**Quote (author's reply to mahog in comments):** *"This diverse monster model [original-as-columns + 2268 TE features] boosted an ensemble of public notebooks from CV 0.384 to 0.386. So this diverse model was probably the secret sauce!"* — explicit framing: cdeotte's own contribution sits *on top of* a public-notebook baseline ensemble.

## What's actually original to this author
- **Original-as-columns + cuDF Target Encoding at scale**: 162 categorical column-combinations (pairs/triples/quadruples of 8 features) × 7 binary targets = 1134 TE cols, then doubled by also TE-ing against the original dataset → 2268 features fed to a single XGBoost. Author claims "no public notebook used the [original-as-columns] technique" in this comp. Required 50GB GPU VRAM.
- **Boosting over LR residuals** (XGBoost's `dtrain.set_base_margin(LR_LOGITS)`) — author's named "overlooked XGBoost trick"; ported into multiple ensembles.
- **Two-stage stacking with NN + GBDT at level 2, then averaged**: Stage 1 binary-per-class predictors (no need for multi-class at base layer), Stage 2 NN with categorical-cross-entropy on stage-1 OOFs, then a separate Stage 2 XGB with `multi:softprob`, then average. The level-2 NN was previously his s5e4 contribution.
- **Multi-seed averaging tuned to MAP@K**: trains each model 30–100 times with different seeds and averages probabilities before top-3 selection. Per his own framing, this is one of two things that "secured 1st place."
- **The KGMON Playbook *itself* — but in its earlier, unbranded form.** The writeup lists 6 techniques from his previous 6 playground wins (Dec 2024 to May 2025): cuDF FE, Boosting over Residuals, Use Original Data, cuML, Stacking, GPU HillClimbing. Each links to a prior solution. This is the proto-version of what becomes s6e3's "KGMON Playbook 2026" 9 months later.

## Dataset constraints that shaped this strategy
- **Synthetic data + public original with RANDOM original-targets** → original-as-rows adds noise (other public notebooks did this naively), but original-as-columns lets the model reverse-engineer the generator. Author read this in a discussion post pre-competition and built his solution around it. Direct example of how a *sub-constraint* of the original-data availability (whether original targets are informative) flips the strategy.
- **MAP@K metric (ranked top-3 selection on multiclass probabilities)** → calibration matters disproportionately, so multi-seed averaging gives unusually large gains. Author: "each fold of each 5-Fold XGB has average MAP@3=0.376 but when we average the probabilities from 100 5-Fold XGB and then compute MAP@3, we achieve 0.380!" 0.004 MAP@3 gain from seed averaging alone.
- **9 features all categorical-treatable + author's GPU access (A100 80GB)** → enables the 162-combo × 7-target × 2-dataset TE-feature explosion (2268 cols) that would be infeasible on CPU.
- **Mature community of public-notebook contributors for this specific competition** → cdeotte can port 4 distinct strong public solutions and ensemble his own monster model on top, rather than building everything from scratch.

## Code vs writeup check
- ✗ **No notebook in local set.** Writeup describes pipeline; cannot verify cell-by-cell. Spreadsheet `fe_techniques` is unusually granular and matches the writeup's enumerated techniques.
- ✓ Spreadsheet `original_data_usage: concat_rows;merge_columns` accurately captures the author's deliberate dual-mode use (rare among entries — most others use one mode or the other).
- ✓ All 6+ playbook elements named in the writeup match the spreadsheet `fe_techniques` field.
- ⚠ Without the notebook, we cannot verify the exact NN architecture, the specific Optuna/manual hyperparameter values, or the HC weight distribution across the 9 models.

## Headline finding
s5e6 is the **proto-KGMON-Playbook** — same author, same recipe family as s6e3, scaled down (~300 prediction sets vs 850 in s6e3) and without the LLM-augmented coding workflow. cdeotte explicitly enumerates 6 techniques *carried forward from his previous 6 monthly wins* (Dec 2024 – May 2025) and applies them again here. The s6e3 KGMON Playbook 2026 is essentially this same recipe, formalized, branded, and scaled with LLM agents 9 months later. Strongest evidence yet that **strategy IS author-stable when the dataset constraint profile is similar** (synthetic + classification + public original + medium-large rows), even as it remains *competition-conditional* across different constraint profiles. The cdeotte playbook converged early and now just absorbs new techniques (LLMs, more models) without changing its core shape.

## Surprising / unusual
- **Top 3 are all in our analysis set's community**: cdeotte (1st), masayakawamata (2nd), mahog (3rd). All three are repeat winners across s5/s6 and heavy cross-citers. s5e6 is a concentrated snapshot of the small-community dynamic.
- **cdeotte explicitly lists 6 prior monthly wins** at the top of the writeup, linking each — the closest thing we have to an author's own meta-analysis of their own technique trajectory. Useful primary source for "what is the cdeotte playbook" question.
- **Original-targets-are-random** is the *sub-constraint* that flipped his strategy: same competition profile (synthetic + has-original) leads to either original-as-rows OR original-as-columns depending on whether the original's target signal is real. The constraint→strategy framework needs to distinguish these sub-cases.
- **mahog in comments**: *"i also thought of using TE features but I could only do 2-way combinations (the feature count exploded after that)."* mahog hits the FE-combinatorics ceiling without cuML/GPU; cdeotte's GPU access was a hard prerequisite for the winning monster model. Hardware as constraint.
- **Within-author playbook continuity over 9+ months** (s5e6 → s6e3, same recipe, scaled with LLMs). Compare to Mahog's *within-author strategy reversals* (s5e8/s5e11/s6e1). Different authors handle constraint-changes differently — cdeotte sticks with a stable recipe and scales it; Mahog flips strategies per competition.
