# s3e16 — Rank 3: Ravi Ramakrishnan (ravi20076)

## Identifiers
- **Competition:** [playground-series-s3e16](https://www.kaggle.com/competitions/playground-series-s3e16) — *Regression with a Crab Age Dataset*
- **End date:** 2023-08-31 (1,429 teams) — **earliest entry now (Aug 2023)**.
- **Rank / score:** **3 of 1,429** · 1.33513 private LB (MAE — first MAE metric in set). Top 3 within 0.00084: Epikt 1.33429 → Emincan Yilmaz 1.33510 → Ravi 1.33513.
- **Team / Kaggle user:** Ravi Ramakrishnan / [ravi20076](https://www.kaggle.com/ravi20076) — second Ravi entry in our analyzed set. **Ravi trajectory now**: **3rd at s3e16 (Aug 2023)** → 3rd at s3e24 (Dec 2023) → 1st at s4e7 team (Jul 2024). Three of his entries in set, plus cdeotte's s6e3 reference.
- **Writeup:** [3rd private 6th public | Brute-force ensemble | Post-processing](https://www.kaggle.com/competitions/playground-series-s3e16/writeups/ravi-ramakrishnan-3rd-private-6th-public-brute-for) (local: `data/writeups/playground-series-s3e16/3rd private 6th public _ Brute-force ensemble_ Post-processing _ Kaggle.txt`)
- **Notebook (published):** [playgrounds3e16-eda-baseline](https://www.kaggle.com/code/ravi20076/playgrounds3e16-eda-baseline) (local). 51 cells — EDA + baseline (Ravi's published, not the full winning pipeline).

## Dataset
Regression on `Age` (integer 4-20 typically), MAE metric, 74,051 train rows. 8 features (1 categorical `Sex` with M/F/I — max_cardinality=3, rest numeric). Public original crab-age dataset + Ravi generated additional synthetic data from the data generator notebook (concat for training).

## What the spreadsheet currently records
- `primary_model: ensemble` (5 GBDTs), `dominant_base_model: gbm`, `ensemble_method: stacking`
- `cv_strategy: stratified_kfold` (5-fold), `hyperparameter_tuning: optuna`, `encoding_strategy: label_encoding`
- `models_used`: xgboost, lightgbm, catboost, gradient_boosting, histgb (5 GBDTs, **no NN**)
- **`fe_techniques`: Domain features (meat yield/surface area/weight ratios/pseudo BMI/viscera ratio); log transform on weight; **post-processing (round to nearest integer)**; feature subset selection (6-10 features per model)**
- `original_data_usage: concat_rows`, `metric: MAE`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly used | 2 | (1) The **official data generator notebook** ("make-synthetic-crab-age-data" by @inversion / Kaggle) — Ravi varied parameters to **generate MORE synthetic data** and concatenated. (2) Domain feature ideas from @pandeyg0811's discussion post #415721 (meat yield, surface area, pseudo BMI, etc.). |
| Cross-author cameo | @pandeyg0811 (domain features source), @inversion (data generator) | First time generator notebook is explicitly used to extend training data |

## What's actually original to this author
- **Generator-driven data augmentation**: ran the official generator notebook with varied parameters to **generate more synthetic data**, then concat with train + original. *Different from "use public original" — this is "use the generator itself to make more data."* New technique-source category.
- **Domain features for anatomical regression**: meat yield, surface area, weight/shuck-weight ratio, pseudo BMI, weight/length-squared, viscera ratio — domain-knowledge FE for a biology dataset. Different from row-wise stats (s4e5 aldparis) or brute-force combinatorics (s3e24 — same author).
- **Feature subsets per model (6-10 features each)** — train several candidates from same OOF structure with different feature subsets. Diversity-via-feature-subset rather than diversity-via-hyperparameter or diversity-via-model-family.
- **Post-processing: round to nearest integer** for integer-target regression. Improved CV and LB.
- **Optuna + LAD regression** for ensemble weight tuning — Least Absolute Deviation suits the MAE metric.
- **Same Ravi recurring pattern**: brute-force at s3e24 (Dec 2023), feature-subset diversity here (s3e16 Aug 2023), team scaling at s4e7 (Jul 2024). Modular/iterative approach throughout.

## Dataset constraints that shaped this strategy
- **Small dataset (74K rows) + few features (8) + integer regression target** → no need for large NN; tree-based ensemble + post-processing (rounding) is well-matched. Reinforces "small data → no NN" pattern.
- **Biology/anatomy domain with measurable ratios** → domain features are the natural FE direction. Generic row-wise statistics or brute-force combos wouldn't capture meat-yield, BMI semantics.
- **MAE metric + integer target** → post-processing rounding directly improves the metric. LAD ensemble matches the loss.
- **Public original + data generator available** → enables data augmentation via generator parameter sweeps (Ravi's distinct contribution here).

## Code vs writeup check
- ✓ Notebook (51 cells) is Ravi's EDA + baseline — focuses on early exploration. The full 5-model ensemble + LAD weight tuning isn't in this notebook.
- ⚠ Generated-additional-synthetic-data parameters aren't shared; only described in writeup
- ⚠ Specific feature subsets (6-10 features per model) aren't enumerated

## Headline finding
s3e16 (Aug 2023) is **the earliest entry now** and Ravi's **second-earliest documented Kaggle competition in our set**. The writeup introduces **generator-driven data augmentation** (running the official data generator notebook with varied parameters to produce additional synthetic data) — a new technique-source category beyond "public original" and "public notebook ports." **Domain features for biology task** (anatomical ratios) — different from other all-numeric writeups' generic FE. **Ravi's recurring trajectory now spans 11+ months**: 3rd at s3e16 (Aug 2023) → 3rd at s3e24 (Dec 2023) → 1st team at s4e7 (Jul 2024) → mentioned in cdeotte's s6e3 references. Same iterative MLOps-discipline style throughout.

## Surprising / unusual
- **Generator-driven data augmentation** — first time we see this technique. Author used the official data-generation notebook with varied parameters to produce *more synthetic data*, then concat with train + original. Goes beyond "exploit public original."
- **Domain features for biology dataset** — meat yield, pseudo BMI, viscera ratio. Domain-knowledge-driven FE for a specific dataset domain. Different from generic FE in all-numeric writeups.
- **Feature-subset-diversity strategy** — different ensemble members see different feature subsets (6-10 each), generated from same OOF structure. **Diversity-via-feature-subset** as distinct strategy from diversity-via-hyperparameter or diversity-via-model-family.
- **Ravi recurring**: 3rd at s3e16 → 3rd at s3e24 → 1st team at s4e7. Same author shows consistent iterative refinement.
- **No NNs at all** in his 5-model GBDT ensemble. Reinforces "small data + few features + no original-discovery → GBDT-only" pattern for early 2023 era.
- **LAD regression for ensemble weight tuning** suits the MAE metric — matching loss function to ensemble objective. Subtle but principled.
- **Wide 1st-2nd gap (0.00081)** but very tight 2nd-3rd (0.00003) — suggests 1st place had a meaningful edge while 2nd-3rd were essentially equivalent.
- **Detailed acknowledgment list in comments** (13 named contributors in his reply thread) — author engages heavily with the community even at 3rd place.
