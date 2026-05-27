# TPS May 2022 — Rank 1: AmbrosM + Pourchot ("The Team") — FOURTH ambrosm win

## Identifiers
- **Competition:** [tabular-playground-series-may-2022](https://www.kaggle.com/competitions/tabular-playground-series-may-2022) — *Tabular Playground Series - May 2022*
- **End date:** 2022-05-31. **Earliest entry now (May 2022)** — before TPS Jun 2022.
- **Rank / score:** 1 of 1,xxx · 0.99833 private LB (ROC AUC). 2nd: Joe Cooper 0.99826, 3rd: Outatime 0.99826.
- **Team / Kaggle user:** **The Team** = AmbrosM ([ambrosm](https://www.kaggle.com/ambrosm)) + Laurent Pourchot ([pourchot](https://www.kaggle.com/pourchot)). **FOURTH ambrosm win in set** (TPS Feb 2022 → **TPS May 2022** → s3e9 May 2023 → s3e11 Jun 2023).
- **Writeup:** [#1 Solution: A Two-Branch Network](https://www.kaggle.com/competitions/tabular-playground-series-may-2022/writeups/the-team-1-solution-a-two-branch-network) (local: `data/writeups/tabular-playground-series-may-2022/#1 Solution_ A Two-Branch Network _ Kaggle.txt`)
- **Notebook (published):** [tpsmay22-keras-test-tuned](https://www.kaggle.com/code/pourchot/tpsmay22-keras-test-tuned) (Pourchot's tuned version, local).

## Dataset
Binary classification (machine state 0 or 1), ROC AUC metric, 900,000 train rows. 31 features (mixed — f_00-f_30 numeric + 10 character columns ch0-ch9 + 1 string feature f_27 with 741,354 unique values → max_cardinality). `distribution_shift: FALSE`. No public original.

## What the spreadsheet currently records
- **`primary_model: neural_network`** (second NN-primary winner in set), **`best_single_model: Keras NN`**, **`dominant_base_model: neural_network`**
- `ensemble_method: mean_blend`, `cv_strategy: stratified_kfold`, `hyperparameter_tuning: manual`, `encoding_strategy: ordinal_encoding`, `scaling: standard`
- `models_used`: Keras NN, LightGBM (LGBM tested but excluded from final blend)
- **`fe_techniques`: Xgbfir interaction graph analysis identifying two disconnected feature components; two-branch NN architecture restricting interactions to graph components; unique_characters feature; pairwise interaction features (i_02_21, i_05_22, i_00_01_26)**
- `original_data_usage: none`, `max_cardinality: 741354`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Specific technique cites | 4 named | (1) **@sudalairajkumar (SRK)** — xgbfir output dataset (key technique source). (2) **@cabaxiom** — unique_characters feature. (3) **@wti200** — feature interactions analysis. (4) **@pourchot** — architecture optimization (co-author). |
| Author's own predecessor notebook | "Advanced Keras notebook" (`tpsmay22-advanced-keras` by ambrosm) — public baseline that the team built two-branch architecture on top of. **Self-fork-with-architecture-tweak pattern.** |
| Tool reference | **Xgbfir** (XGBoost Feature Interactions Reshaped) library — GitHub limexp/xgbfir | New tool in set for feature-interaction analysis. |

## What's actually original to this author
- **Two-Branch Neural Network architecture inferred from feature-interaction graph structure**: Used xgbfir to find interactions → graph of interactions had two disconnected connected components → built NN with two branches that each handle one component. **Architecture mirrors data's interaction structure.** First example of structure-from-data in our set.
- **First team entry in set (and pre-dates Cross Sellers s4e7 by 14 months)**. The Team = ambrosm + pourchot. Team-based winning predates the s4e7 (Jul 2024) Cross Sellers case.
- **LightGBM `interaction_constraints` parameter** — tested with same feature partitions as the NN branches; reached LB 0.99778 but didn't make final blend. **New technique not used elsewhere in set.** Generic version of two-branch architecture for tree models.
- **Self-fork-with-architecture-tweak**: started from ambrosm's own "Advanced Keras notebook," only changed the architecture to two-branch. Otherwise identical. **Within-author iteration on a baseline notebook.**

## Dataset constraints that shaped this strategy
- **Competition hint about feature interactions** (in intro text): *"includes a number of different feature interactions. This competition is an opportunity to explore various methods for identifying and exploiting these feature interactions."* Author followed the hint to identify interactions via xgbfir.
- **Feature interactions form 2 disconnected graph components** → architecturally separable. Architecture-from-data principle viable here because the interaction structure is clean.
- **900K rows + 31 features + binary AUC** → enough scale for NN training; balanced complexity.
- **Mix of numeric, character, and string features** → custom embeddings + interaction features (i_02_21 etc.) needed.

## Code vs writeup check
- ✓ Pourchot's `tpsmay22-keras-test-tuned` notebook implements the two-branch architecture
- ✓ Writeup explains the xgbfir-graph-to-architecture mapping with specific feature lists per branch

## Headline finding
TPS May 2022 (May 2022) is **the earliest entry now** and **AmbrosM's FOURTH win** in our set. **ambrosm N=7 connections now** (4 wins + 3 source citations) — definitively the most-recurring community contributor (surpasses siukeitin and arunklenin at N=5-6). **Second NN-primary winner** (back-to-back with TPS Jun 2022 — both NN-primary, both with custom architectures). **First team entry in set** (The Team = ambrosm + pourchot, pre-dates Cross Sellers s4e7 by 14 months). **Architecture-from-data-structure principle**: two-branch NN built to mirror the disconnected components of the feature-interaction graph (discovered via xgbfir). Different from generic-architecture-tuning — architecture mirrors data structure. **xgbfir tool** + **LightGBM interaction_constraints parameter** are new techniques in set.

## Surprising / unusual
- **Fourth ambrosm win** — TPS Feb 2022 → **TPS May 2022** → s3e9 → s3e11. **ambrosm N=7 connections** (4 wins + 3 citations) — most-recurring community contributor by clear margin.
- **Two consecutive NN-primary winners** (TPS May 2022 + TPS Jun 2022, May-Jun 2022). Both with custom architectures matching problem structure. **NN-primary clustered in TPS-era**. After s3 + s4 + s5 eras, NN-primary doesn't recur until s4e9 NN-stacker (Sep 2024) and s4e11 AutoGluon-as-ensembler.
- **First team entry in set** (May 2022) — pre-dates Cross Sellers s4e7 (Jul 2024) by 14 months. **Team-based winning is not new to s4 era.**
- **Architecture-from-data-structure principle**: NN architecture mirrors data's interaction graph. **First case in set.** Author quote: *"we needed a network which restricted feature interactions to the connected components of the graph (other interactions produce noise)."* Architectural decision driven by EDA, not generic tuning.
- **Competition hint followed literally**: intro text said "various methods for identifying and exploiting these feature interactions" → ambrosm took the hint. **Reading competition descriptions carefully = winning edge.**
- **LightGBM `interaction_constraints` parameter** — tree-equivalent of the two-branch NN. Tested, didn't make blend but reached LB 0.99778. **Generic tree-side technique for interaction restriction.**
- **sudalairajkumar (SRK, Kaggle Grandmaster)** as technique source — first SRK appearance in our set. Recurring Kaggle name.
- **Self-fork-with-architecture-tweak**: ambrosm's own "Advanced Keras notebook" was the baseline; team only added the two-branch architecture. **Within-author iteration on own baseline.**
