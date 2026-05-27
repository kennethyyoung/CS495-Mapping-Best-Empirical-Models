# s5e3 — Rank 2: cdeotte (Chris Deotte)

> **Note:** Curated entry is rank-2 per spreadsheet. Rank-1 was Guillaume HIMBERT (no writeup in local set). This is the third cdeotte entry in our analysis set (after s5e5, s5e6).

## Identifiers
- **Competition:** [playground-series-s5e3](https://www.kaggle.com/competitions/playground-series-s5e3) — *Binary Prediction with a Rainfall Dataset*
- **End date:** 2025-03-31 (4,381 teams)
- **Rank / score:** **2 of 4,381** · 0.90604 private LB (ROC AUC). Top 3: Guillaume HIMBERT 0.90654 → cdeotte 0.90604 → AndNov 0.90583. Margin 0.0005 to 1st, 0.0002 to 3rd.
- **Team / Kaggle user:** Chris Deotte / [cdeotte](https://www.kaggle.com/cdeotte) — third cdeotte entry
- **Writeup:** [2nd Place - GBDT + NN + SVR + Original Data](https://www.kaggle.com/competitions/playground-series-s5e3/writeups/chris-deotte-2nd-place-gbdt-nn-svr-original-data) (local: `data/writeups/playground-series-s5e3/2nd Place - GBDT + NN + SVR + Original Data _ Kaggle.txt`)
- **Notebook (published):** [rapids-svc-w-feature-engineering-lb-0-856](https://www.kaggle.com/code/cdeotte/rapids-svc-w-feature-engineering-lb-0-856) (local: `data/writeups/playground-series-s5e3/rapids-svc-w-feature-engineering-lb-0-856.ipynb`) — **cdeotte's *starter notebook*** (LB 0.856) with forward feature selection on interactions. The actual 2nd-place SVC model used "data as is without FE" and got LB 0.906 — so the published notebook is NOT the 2nd-place SVC config.

## Dataset
Binary classification of `rainfall`, ROC AUC metric, **2,190 train rows** (tiny — 6 years × 365 days). 12 features, **all numeric, no categoricals** (max_cardinality=0), no missing data. **`distribution_shift: TRUE`** (only second case after s5e12) — train is 6 years, test is 2 new years (temporal shift). Public original: 1 year × 366 rows. Author insight from comments: *"This train data is more like 366 real rows, then apply data augmentation to get 2190 rows. So it is still only signal from 366 rows which is very small data."*

## What the spreadsheet currently records
- `primary_model: ensemble`, **`best_single_model: SVC`** (first non-tree non-NN best single in the set), `dominant_base_model: other`
- **`cv_strategy: grouped`** (Group K Fold by year, 6 folds — first explicit grouped CV)
- **`ensemble_method: mean_blend`** (equal weight, distinct from stacking/HC/Ridge — chosen explicitly to avoid ensemble overfit)
- **`fe_techniques: none`** (first explicit "none" — author's deliberate small-data choice)
- `models_used`: XGBoost, CatBoost, TabPFN, LogisticRegression, SVC, SVR (6 families in final blend; 3 in the would-have-been-1st blend)
- `original_data_usage: concat_rows;merge_columns` (dual-mode — same as s5e6, cross-competition consistency)
- `distribution_shift: TRUE`, `n_rows: 2190`, `max_cardinality: 0`
- All fields accurately reflect the writeup.

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | cdeotte references *his own* starter notebooks (XGBoost starter, RAPIDS SVC starter) as templates, not external ports. |
| Author cited *by* others (forward propagation) | Yes | s5e3's "original-as-columns" technique is one of cdeotte's recurring patterns (also s5e6, eventually s6e3). His RAPIDS SVC starter notebook is a community asset. |
| Acknowledgment list | None visible | Like s5e5, cdeotte's s5e3 writeup is technique-only with no thank-you list. Consistent author pattern in early-s5 writeups. |

## What's actually original to this author
- **Explicit small-data-conditional strategy rule**: *"When train data is small (few rows) I do little or no feature engineering because it is easy to overfit train data. When data is large (many rows...), I do lots of feature engineering."* This is the most explicit articulation of the constraint→strategy mapping by any author in the set. Quotes the curse of dimensionality and a "10/25/50 columns per row" rule of thumb.
- **Three-model equal-weight blend that would have won 1st**: XGBoost (CV 0.893) + TabPFN (CV 0.894) + RAPIDS SVC poly-kernel (CV 0.896) → CV 0.898, Private LB 0.90728. Author actually submitted a 6-model blend that came 2nd (LB 0.90604) — concrete evidence that **adding models hurt** in this regime.
- **RAPIDS SVC with kernel='poly', degree=1, C=0.1** as best single model (LB 0.90610). First time a kernel SVM appears as the best single model — works because data is small + all-numeric + scaled.
- **TabPFN as a primary base model**: foundation model for tiny tabular datasets, scores LB 0.90193 by itself. Same TabPFN that appears in s6e3 (cdeotte ports it consistently into small-data contexts).
- **Group K Fold by year (6 folds)** to handle the temporal nature of train→test split (test is new years). Distinct distribution-shift handling from s5e12's post-cutoff CV.
- **Original-data dual-mode use**: rows for XGB + TabPFN, columns for SVC. Same dual-mode pattern as s5e6 — consistent author choice across two competitions.

## Dataset constraints that shaped this strategy
- **Effectively-366-real-rows (curse of dimensionality territory)** → no FE possible without overfitting. Author explicit: "366 rows, we already have 11 columns which is saturated." Forces simple "data as is" pipeline.
- **All numeric + small + standardized** → kernel methods (SVC, SVR) become competitive. Standard tree-based-only assumption breaks here.
- **Distribution shift (train years ≠ test years) but identifiable via year grouping** → Group K Fold by year is the natural CV strategy, different from s5e12's cutoff approach.
- **Wide ensemble adds noise**: equal-weight 3-model blend beats 6-model blend in private LB. Driven by small-data regime where each additional model adds variance more than it reduces it.

## Code vs writeup check
- ✓ Writeup explicitly lists the 3 best models with CV, public LB, private LB.
- ⚠ **Published notebook (`rapids-svc-w-feature-engineering-lb-0-856.ipynb`) is the starter** (LB 0.856), NOT the 2nd-place SVC component (LB 0.90610). The starter does forward feature selection on interactions; the 2nd-place SVC version uses "data as is" plus the original-as-columns trick. The actual 2nd-place SVC config isn't fully reproducible from the published notebook alone.
- ⚠ The 6-model final ensemble code isn't published — only the writeup describes it. CatBoost / LogisticRegression / XGBoost / SVR contributions are not reproducible without the missing notebooks.
- ✓ Spreadsheet `cv_strategy: grouped` matches the writeup's `train['group'] = train['id']//365` code.

## Headline finding
s5e3 is **cdeotte's small-data playbook** — the explicit counterpart to his large-data KGMON Playbook. The same author who wins s6e3 with 850 models, 4-level stacks, and LLM-coded pipelines (~150K rows, public original with real targets) wins 2nd at s5e3 with **no feature engineering, equal-weight mean blend of 3 models, kernel SVM as best single** (~2K rows, temporal shift). cdeotte's recipe is genuinely constraint-conditional even within his own work — but the conditioning is on **dataset size** (which he names explicitly), not arbitrary. Adding 3 more models to the blend actively hurt his private LB (3-model blend = LB 0.90728 = would have been 1st; 6-model blend = LB 0.90604 = actual 2nd). The "less is more" small-data lesson is concretely measurable.

## Surprising / unusual
- **Author explicitly articulates the constraint→strategy mapping** in his comment response: small data → no FE (curse of dimensionality), large data → heavy FE. This is the clearest meta-statement from any author in the set, and concrete validation of our constraint→strategy framework.
- **Adding more models hurt the actual submission** (3-model blend would have won 1st, 6-model blend came 2nd). Rare meta-evidence that "more is sometimes worse" in small data — and it's measurable here because cdeotte reports both ensemble configurations.
- **Kernel SVM (RAPIDS SVC poly-degree-1) as best single model** — first non-tree, non-NN best single in the analysis set. Suggests classical kernel methods are competitive in the small-data regime that all of s5/s6 mainline doesn't usually visit.
- **Within-author dual-strategy evidence is now strongest for cdeotte**: same author wins (or near-wins) with KGMON Playbook scaled-up FE+ensembles (s5e6 with 2268-col XGB monster) and KGMON-Playbook-absent simplicity (s5e3 with no-FE 3-model mean blend). The split happens at data size — Mahog flipped between strategies more arbitrarily, cdeotte flips them on a clear axis.
- **TabPFN appears here too** (also in s6e3, kirill0212's s6e4) — pattern: TabPFN tends to be in the ensemble for small-data or as a TabPFN-foundation-model contribution. Worth tracking.
