# s4e12 — Rank 1: cdeotte (Chris Deotte)

## Identifiers
- **Competition:** [playground-series-s4e12](https://www.kaggle.com/competitions/playground-series-s4e12) — *Regression with an Insurance Dataset*
- **End date:** 2024-12-31 (2,390 teams)
- **Rank / score:** 1 of 2,390 · 1.01706 private LB (RMSLE). Top 3 margin: 0.003 to 2nd, 0.004 to 3rd (moderate).
- **Team / Kaggle user:** Chris Deotte / [cdeotte](https://www.kaggle.com/cdeotte) — **fifth cdeotte entry**, earliest in our set (Dec 2024). First s4-era entry overall.
- **Writeup:** [1st Place - Single Model - Feature Engineering](https://www.kaggle.com/competitions/playground-series-s4e12/writeups/chris-deotte-1st-place-single-model-feature-engine) (local: `data/writeups/playground-series-s4e12/1st Place - Single Model - Feature Engineering _ Kaggle.txt`)
- **Notebook (published):** [first-place-single-model-cv-1-016-lb-1-016](https://www.kaggle.com/code/cdeotte/first-place-single-model-cv-1-016-lb-1-016) (local: `data/writeups/playground-series-s4e12/first-place-single-model-cv-1-016-lb-1-016.ipynb`) — 21 cells. Simplified 229-feature T4-GPU version (CV 1.019); cdeotte's actual final has 611 features on A100. Same notebook structure as s5e2's `first-place-single-model-lb-38-81`.

## Dataset
Regression on `Premium Amount`, RMSLE metric, 1.2M train rows. 20 features (mixed), 5.02% missing. **`max_cardinality: 167,381`** — highest in the analysis set, driven by Policy Start Date decomposition + 2–6-way categorical combinations. **No public original dataset** (`original_data_usage: none`) — first cdeotte writeup without one.

## What the spreadsheet currently records
- `primary_model: gbm`, `best_single_model: xgboost`, `dominant_base_model: gbm`
- **`ensemble_method: none`** — third single-model winner (after s5e4 greysky, s5e2 cdeotte)
- `models_used: xgboost` (single family)
- `cv_strategy: kfold`, `hyperparameter_tuning: manual`, `original_data_usage: none`
- `fe_techniques`: Label encoding; TE (mean/median/min/max/nunique) + CE per column; column combinations (2-6 way); treating numerics as categorical + TE/CE; Policy Start Date decomposition; **GPU-accelerated search of 145K+ combinations → 170 kept**
- `missing_data_strategy: imputation`, `encoding_strategy: target_encoding; label_encoding; count_encoding`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | cdeotte references his own September 2024 LASSO notebook for the column-combination technique source; no inbound ports. |
| Author cited *by* others | Yes | Same notebook structure as s5e2's "first-place-single-model" — recipe was already established by Dec 2024 and reapplied. Forward citation: cdeotte's own s5e2 writeup builds on this. |
| References to pre-our-set cdeotte work | 2 | Sept 2024 and Nov 2024 playground competitions (his "first two") — both used large ensembles because FE didn't move CV in those. |

## What's actually original to this author
- **Explicit FE-conditional strategy rule** (his clearest articulation to date): *"In my first two playground competitions (Sept 2024, Nov 2024), feature engineering didn't improve CV nor LB too much, so in those competitions, I spent my time building a large ensemble of diverse models. In this December competition, feature engineering helped improve CV score and LB score, so I was able to spend time building a single model and engineering features."* This is an **FE-effectiveness axis** beyond just data size.
- **GPU brute-force FE combinatorial search** — "I left my computer running day and night in a for-loop" iterating through **145,000+ combinations** of 2–6-way categorical groupings, training a small XGB on each, keeping the 170 that moved CV. Concrete numbers, explicit approach.
- **Single-XGB-with-heavy-FE recipe template** — written here for the first time in our set (Dec 2024). Same template re-used at s5e2 (Feb 2025) with the same notebook title "First Place - Single Model - Feature Engineering" and same author philosophy. The recipe is *templated* by this point in cdeotte's work.
- **Per-categorical-column 7-encoding pattern**: original + label + TE-mean + TE-median + TE-min + TE-max + TE-nunique + CE → 7 representations of every categorical column.
- **Numerics-as-categoricals + TE/CE** — explicitly applies categorical encoding tricks to numeric columns, then combines with other numerics/categoricals for more TE/CE.
- **611-feature single XGB on A100** (full) / 229-feature on T4 (published) — same simplified-but-still-wins pattern as s5e2.

## Dataset constraints that shaped this strategy
- **1.2M rows + 20 features + extreme max_cardinality (167K)** → enough data to support 600+ engineered features without overfitting; high-cardinality TE/CE remain stable with ~7 rows per unique value.
- **FE moves CV in this competition** → cdeotte makes the explicit call to spend time on FE rather than ensembling. **This conditioning is not data-size alone** — it's whether the dataset/generator has structure that FE can exploit. Some competitions don't.
- **No public original dataset** → eliminates the "merge_columns" / "original_as_columns" axis cdeotte uses in s5e2 and later. The FE has to come entirely from in-competition data combinatorics.
- **cdeotte's GPU + cuDF availability** → enables the 145K-combination search that would be infeasible on CPU.
- **Regression + RMSLE + moderate top-3 margin (0.003 to 2nd)** → like s5e2 and s5e4, the margin tolerates single-model strength; ensemble noise reduction isn't required.

## Code vs writeup check
- ✓ Notebook implements the pipeline: load + Policy Start Date decomposition + label encoding + 120 hand-picked combinations from the 170 kept + nested-fold TE function + 20-fold XGBoost
- ✓ Cell 8 markdown explicitly describes the offline GPU brute-force search; cell 9 hardcodes the 120 winning combinations as a Python list
- ✓ Cell 14 trains the actual model (`%%time` shows it's the main computation)
- ⚠ The 145K-combination search loop itself is NOT in the published notebook (offline, cdeotte's local A100)
- ⚠ Full 611-feature production version not published — only the 229-feature T4 version is. CV 1.019 vs 1.016 difference is the simplification cost.

## Headline finding
s4e12 (Dec 2024) is the **earliest single-model-with-heavy-FE win in cdeotte's body of work** and the recipe template that gets reused at s5e2 (Feb 2025) with identical notebook title and same single-XGB philosophy. The genuinely novel content is cdeotte's **explicit FE-effectiveness conditioning**: he diagnosed that FE moved CV in this competition (versus his Sept/Nov 2024 entries where it didn't) and chose strategy accordingly. The 145K-combination GPU brute-force search is the implementation of this insight — he literally measured FE's effect on every possible combination and kept what worked. This validates a *second conditioning axis* on top of dataset size: **whether the generator has FE-discoverable structure.**

## Surprising / unusual
- **Cdeotte explicitly diagnoses what makes single-vs-ensemble the right choice** (FE-effectiveness on CV), not just data size. Earliest articulation of his own constraint→strategy thinking.
- **145K combinations brute-forced** — concrete numbers. cdeotte's "for-loop running day and night" search style is here in explicit form. Implementation pattern for the heavy-FE single-model recipe.
- **No public original used** — first cdeotte writeup without it. The exploit-original toolkit isn't always available; when not, FE-combinatorics fills the gap.
- **Two cdeotte writeups share the title** "1st Place - Single Model - Feature Engineering" (s4e12 Dec 2024, s5e2 Feb 2025) — recipe is named and templated by Dec 2024.
- **Highest max_cardinality (167,381)** in the analysis set works fine — TE remains stable with 1.2M / 167K ≈ 7 rows per unique value. Sets a benchmark for how high cardinality can go before TE breaks.
- **Pre-our-set cdeotte references** (Sept 2024, Nov 2024 ensemble approaches) suggest there's a cdeotte timeline pre-Dec 2024 that uses different recipes — we lose those competitions' detail but the references frame his trajectory.
