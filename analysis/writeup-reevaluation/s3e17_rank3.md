# s3e17 — Rank 3: ISoft (mathurinache, Mathurin Ache)

> **Caveat:** No notebook (writeup-only). Curated entry is rank-3 per spreadsheet.

## Identifiers
- **Competition:** [playground-series-s3e17](https://www.kaggle.com/competitions/playground-series-s3e17) — *Binary Classification of Machine Failures*
- **End date:** 2023-09-30 (1,502 teams) — **earliest entry now (Sept 2023)**.
- **Rank / score:** **3 of 1,502** · 0.98539 private LB (ROC AUC). Note 1st place 0.98796 with 0.00246 gap — **widest 1st-2nd gap in set** (winner [Deleted] account, presumably banned for leakage exploit).
- **Team / Kaggle user:** ISoft / [mathurinache](https://www.kaggle.com/mathurinache) (Mathurin Ache). Doesn't appear elsewhere in our analyzed set.
- **Writeup:** [3rd solution: based on 90% multi AutoML solutions](https://www.kaggle.com/competitions/playground-series-s3e17/writeups/isoft-3rd-solution-based-on-90-multi-automl-soluti) (local: `data/writeups/playground-series-s3e17/3rd solution _ based on 90_ multi AutoML solutions _ Kaggle.txt`). **Very short writeup — 421 lines total, mostly UI cruft + comments; ~30 lines of actual content.**
- **Notebook:** **none in local set**.

## Dataset
Binary classification of machine failures, ROC AUC metric, 136,429 train rows. 13 features (mixed). **max_cardinality=9,976** (high — likely Product ID column). No missing data.

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: stacking` (meta-model on AutoML outputs)
- `cv_strategy: not_described`, **`hyperparameter_tuning: automated`** (AutoML handles)
- **`models_used: light_automl, h2o_automl, flaml, lazy_classifier`** — 4 AutoML frameworks (writeup also mentions Statmining = proprietary)
- **`fe_techniques: None described — AutoML handles internally`** — first "no FE" entry where it's because AutoML handles it
- `original_data_usage: not_described`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly used | 2 (10% of final ensemble) | "the 10% of the model comes from the 2 best public submissions" — fork-heavy at the *finishing stage*, not the core strategy. |
| Cross-author cameos | Geremie Yeo (yeoyunsianggeremie, 16th here) — recurring at s5e5, s5e11, s4e9 | Geremie's comment: "Ensembling the top public notebooks into the model predictions really worked for this one. Also experienced the same outcome!" Confirms fork-blend-on-top works for top-20 finishes. |

## What's actually original to this author
- **Pure AutoML-stack-of-stacks strategy** — first in set. 5 AutoML frameworks ensembled (Light AutoML, H2O AutoML, FLAML, Lazy Classifier, **Statmining AutoML — ISoft's PROPRIETARY private solution**). First three contribute the most.
- **Proprietary AutoML framework** (Statmining) — first appearance of a closed-source private tool in our analyzed entries. Other authors use only public tools (cdeotte's cuDF/cuML, AutoGluon, etc.).
- **Resource-conservative**: 6 hours total on 4-core 8GB RAM machine, 1 hour max per AutoML. Counter-pattern to cdeotte-style GPU-heavy approaches.
- **No FE, no hand-crafted models, no manual hyperparameter tuning** — fully delegated to AutoML frameworks. Author meta-stacks their outputs + 10% public-notebook submissions.

## Dataset constraints that shaped this strategy
- **Resource constraints (4 cores / 8GB)** → AutoML's automated time-budget management (1hr per framework) fits the hardware. Heavy hand-crafted ensembling would have been infeasible.
- **Binary + ROC AUC + 136K rows** → standard AutoML-friendly task profile. AutoML frameworks have well-tested defaults for this kind of problem.
- **Wide 1st-2nd gap (0.00246) + deleted-account winner** → suggests leakage exploit by 1st place. Author's CV-trust strategy paid off; he avoided overfitting to leakage tricks.

## Code vs writeup check
- ✗ **No notebook published.**
- ✓ Spreadsheet `models_used` matches writeup's 5 AutoML frameworks (minus Statmining which is private).
- ⚠ The meta-model on top of AutoML outputs is described as "stacking" but specific stacker (Ridge? LR? Another AutoML?) isn't named in writeup.
- ⚠ The 2 public submissions used aren't cited.

## Headline finding
s3e17 (Sept 2023) is the **earliest entry now** and **the first pure-AutoML winner** in the set. ISoft (mathurinache) won 3rd place by stacking 5 AutoML frameworks (Light AutoML + H2O + FLAML + Lazy Classifier + proprietary Statmining) plus 10% from public notebooks. **No FE, no hand-crafted models, no manual HP tuning** — completely delegated to AutoML. **Resource-conservative**: 6h on 4-core 8GB. Different paradigm from the s4-s6 cdeotte/mahog hand-crafted heavy-ensembling style. **AutoML-stack-of-stacks is a documented alternative path to top-3** for resource-constrained participants. The author appears nowhere else in our analyzed set — unlike most other authors who have multi-entry trajectories.

## Surprising / unusual
- **First pure-AutoML-only winner** in set. Other entries with AutoML (s4e8 Optimistix, s4e11 Mahdi) used AutoGluon as ONE component or as the ensembler — not as the entire base-model pool.
- **First appearance of a proprietary tool** (Statmining AutoML, ISoft's private framework). All other writeups use only public/open tools.
- **Resource-conservative strategy** (6h on 4 CPU cores, 8GB RAM) — counter-pattern to cdeotte-style A100 / external GPU farm. **AutoML is a documented low-resource path to top-3.**
- **Very short writeup** (≤30 lines of actual content) — one of the most minimal writeups in the set. Different style from the detailed s4-s6 norm.
- **Author doesn't appear elsewhere** in our analyzed entries — unlike most authors who have multi-entry trajectories. Mathurin Ache is a one-off winner in our set.
- **Wide 1st-2nd gap (0.00246)** with deleted-account 1st place — suggests leakage exploit by winner. ISoft's CV-trust + AutoML defaults insulated him from this.
- **AutoML-stack as alternative paradigm**: completely sidesteps the s4-s6-era pattern of FE-and-models-and-stacker. Reduces effort to "pick AutoML frameworks, run them, combine outputs."
- **Pseudo-labeling mentioned as "slightly better"** but not used — implicit hint that author left some signal on the table.
