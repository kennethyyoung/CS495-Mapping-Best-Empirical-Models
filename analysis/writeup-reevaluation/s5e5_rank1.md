# s5e5 — Rank 1: cdeotte (Chris Deotte)

> **Caveat:** No notebook in local set (writeup-only evaluation). Author's GPU Hill Climbing *starter notebook* is referenced (`https://www.kaggle.com/code/cdeotte/gpu-hill-climbing-cv-0-05930`) but not scraped. Per-cell verification not possible; pipeline reconstructed from writeup + spreadsheet.

## Identifiers
- **Competition:** [playground-series-s5e5](https://www.kaggle.com/competitions/playground-series-s5e5) — *Predict Calorie Expenditure*
- **End date:** 2025-05-31 (4,316 teams)
- **Rank / score:** 1 of 4,316 · 0.05841 private LB (RMSLE). Top 3: cdeotte 0.05841 → mahog 0.05842 → nice kazusan 0.05843 (0.00002 between 1st and 3rd — extreme photo-finish, similar to s5e10).
- **Team / Kaggle user:** Chris Deotte / [cdeotte](https://www.kaggle.com/cdeotte) — third cdeotte entry (also won s6e3 and s5e6)
- **Writeup:** [1st Place - GPU Hill Climbing!](https://www.kaggle.com/competitions/playground-series-s5e5/writeups/chris-deotte-1st-place-gpu-hill-climbing) (local: `data/writeups/playground-series-s5e5/1st Place - GPU Hill Climbing! _ Kaggle.txt`)
- **Notebook:** **none in local set** — author's published "GPU Hill Climbing starter notebook" referenced but not scraped

## Dataset
Regression on `Calories`, **RMSLE** metric (first RMSLE in the analysis set), 750K train rows. **8 features, all numeric, no NaNs, no categoricals** (`has_categorical: False`, max_cardinality=2) — the cleanest dataset profile in the set. Public original dataset minimally used (`original_data_usage: concat_rows` — just appended as training rows, no column-level exploitation).

## What the spreadsheet currently records
- `primary_model: ensemble`, `best_single_model: xgboost`, `dominant_base_model: gbm`, `ensemble_method: hill_climbing`
- `cv_strategy: kfold` (regression, no stratification)
- `hyperparameter_tuning: manual`, `original_data_usage: concat_rows` (rows only — distinct from s5e6's `concat_rows;merge_columns`)
- `models_used`: XGBoost, CatBoost, NN, LinearRegression
- `fe_techniques`: log1p transforms; product/division/sum/diff pairs; binned features (9 bins); groupby z-score features (26); residual modeling (NN on LR residuals, XGB on NN residuals); cuML TargetEncoder
- Coding is granular and matches the writeup's enumerated techniques.

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | Author does not cite ports. References *his own* published starter notebooks (GPU HC starter, NN MLP starter) which others may have forked, but no inbound ports into this solution. |
| Author cited *by* others (forward propagation) | Yes | This writeup is where the "**GPU Hill Climbing**" technique gets its name and starter-notebook. cdeotte explicitly lists this win as "May 2025: Calorie Comp, RMSLE, GPU HillClimbing, 1st" in his s5e6 writeup (one of 6 prior monthly wins he recycles into the KGMON Playbook). The technique flows forward into s5e6 → s6e3. |
| Acknowledgment list | None visible | Unusual for the s5/s6 set — most writeups acknowledge ~4–6 community names. cdeotte's s5e5 writeup is technique-focused without thank-you list. |

This is *not* fork-heavy. cdeotte's s5e5 contribution appears to be substantially his own work — a counterexample to the "Heavy public-notebook coverage + author with framework" coupling for this same author's later competitions. The fork-heavy pattern in s5e6 → s6e3 may have emerged *after* he published his GPU HC starter notebook (which then became a community resource).

## What's actually original to this author
- **GPU Hill Climbing of hundreds-of-candidates → 7-model final ensemble.** The name of the technique gets canonized in this writeup. Final 7 HC-selected models with their hand-determined weights:

  | Weight | Model | Notes | CV |
  |---|---|---|---|
  | 1/12 | XGBoost | cuML TE features (3 variants) | 0.0605–0.0608 |
  | 1/4 | XGBoost | product features | 0.05951 |
  | 1/6 | CatBoost | binned + groupby | 0.05937 |
  | 1/6 | NN over LR | residual training | 0.05999 |
  | 1/6 | XGB over NN | residual training | 0.05989 |

- **Residual modeling *chain*** — NN trained on LR residuals, then XGB trained on NN residuals. Author explicit: the XGB-over-NN-residuals did *not* improve single-model CV, but added diversity that improved HC ensemble CV. First time we see a multi-step residual chain across different model families.
- **GroupBy z-score features** (26 generated): pick 1–3 features as the grouping key (e.g., Sex × Age × Weight_bin), compute z-score for a target feature (e.g., Heart_Rate). Author's standardized technique for the no-categoricals case — converts numeric demographics into within-group anomaly signals.
- **Product/division/sum/difference combinatorics over log1p versions** of all 8 features — the all-pairs systematic FE for an all-numeric dataset.
- **9-bin equal-width discretization → 81-unique pairwise combinations as categoricals** — manufactures categorical features from numerics to feed CatBoost's native handling.
- **Retrain on 100% train with `iterations × 1/(K-1)` more than the 5-Fold early-stopping average** — author explicitly says he uses this in *every* Kaggle competition. Now appears as a recurring feature across his s5e5 / s5e6 / s6e3 writeups.

## Dataset constraints that shaped this strategy
- **All-numeric features + no NaNs + no categoricals** → standard TE-on-categoricals path unavailable. Forces the *binning → manufactured-categorical → CatBoost* trick and the *groupby z-score* feature family.
- **Public original minimally informative** (used only for row concat, not columns) → the FE has to extract signal from the 8 numeric features directly via combinatorics and groupby aggregations, not via cross-source merging.
- **Regression + RMSLE + 750K rows + tight top-3 margin (0.00002)** → diversity-driven HC of many candidates wins; the photo-finish margin makes "poor-CV but diverse" models valuable (cdeotte explicitly notes his XGB-TE models have 0.06XX CV but still help the final ensemble).
- **cdeotte's GPU access** → "hundreds of candidate models" is feasible; without GPU the candidate pool would be much smaller.

## Code vs writeup check
- ✗ **No notebook in local set.** Pipeline described in detail in writeup; cannot verify cell-by-cell.
- ✓ All 7 HC-selected models, their CV scores, and their weights are explicit in the writeup table.
- ✓ Author describes the "100% retrain with 1/(K-1) iteration boost" trick verbatim — same wording later appears in s5e6 and s6e3.
- ⚠ The "hundreds of candidate models" pool is not enumerated. We only see the 7 HC-selected survivors; the candidate-generation strategy is implied but not detailed.
- ⚠ Without the notebook we can't verify the exact XGBoost / CatBoost / NN architectures or hyperparameters.

## Headline finding
s5e5 is **the canonical "GPU Hill Climbing" writeup** — where cdeotte names the technique and publishes the starter notebook that becomes a community artifact. The recipe is recognizably the KGMON Playbook in even earlier form (8 months before s6e3): GPU HC + cuML + residual modeling + retrain-on-100% + diversity-over-single-CV. Notably, this competition is *not* fork-heavy — cdeotte builds it largely from his own techniques without porting public notebooks, suggesting the "Heavy public-notebook coverage + author with framework" coupling emerges in his *later* competitions once a community formed around his starter notebooks. The fork-heaviness in s6e3 is a downstream effect of cdeotte's own earlier publishing.

## Surprising / unusual
- **Smallest acknowledgment list of any s5/s6 winner** — no thank-you names, no itemized public-notebook ports. Unusual relative to the pattern where every other winner names 4–8 community contributors. cdeotte's s5e5 is technique-only.
- **Top 3 are cdeotte, mahog, nice kazusan** — third concentration of the small-community names (cdeotte/masayakawamata/mahog appear on most s5/s6 podiums). nice kazusan is a community member not yet in our analysis set.
- **First all-numeric dataset** in the analysis set — drives a fundamentally different FE strategy (binning + groupby + numeric combinatorics) than the categorical-heavy s5/s6 mainline. Worth tracking whether the next no-categoricals case follows the same pattern.
- **The "GPU Hill Climbing" name and starter notebook are canonized here.** Trace forward: s5e5 names it → s5e6 lists it among 6 prior recipes → s6e3 formalizes it as KGMON Playbook step #5. Concrete example of a single author's technique becoming a framework over 9 months.
- **The residual modeling *chain*** (LR→NN→XGB) is unique to this writeup so far. Single-pair residual modeling appears later (s5e6, s5e10's Keras→CatBoost) but the *triple-cascade* is here. Worth tracking whether this scales or stays a one-off.
