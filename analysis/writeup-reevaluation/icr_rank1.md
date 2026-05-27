# ICR Age-Related Conditions — Rank 1: room722

## Identifiers
- **Competition:** [icr-identify-age-related-conditions](https://www.kaggle.com/competitions/icr-identify-age-related-conditions) — *ICR - Identifying Age-Related Conditions*
- **End date:** 2023-08-14 (**6,430 teams — LARGEST in set**). **First Featured/monetized competition** in set (other 43 are Playground).
- **Rank / score:** 1 of 6,430 · 0.30626 private LB (Weighted Multiclass Loss). 2nd: Banana Overfit Capybaras 0.32586, 3rd: siguo 0.33974. **Wide margin to 2nd (0.02), even wider to 3rd (0.034)** — author dominated.
- **Team / Kaggle user:** room722 / [room722](https://www.kaggle.com/room722) — first competition for this author per comments; **solo gold medal** in Featured competition is significant.
- **Writeup:** [How on Earth did I win this competetion?](https://www.kaggle.com/competitions/icr-identify-age-related-conditions/writeups/room722-how-on-earth-did-i-win-this-competetion) (local: `data/writeups/icr-identify-age-related-conditions/1st_How on Earth did I win this competetion_ _ Kaggle.txt`)
- **Notebook (published):** [icr-adv-model](https://www.kaggle.com/room722/icr-adv-model) + supplementary `adv_model_training.ipynb` (local).

## Dataset
Binary classification of age-related medical conditions, **Weighted Multiclass Loss** metric (first in set), **617 train rows (second-tiniest in set)**. 57 features (mixed), max_cardinality=2 (binary categoricals), 0.37% missing. **`distribution_shift: TRUE`**. **Featured/monetized competition** with prize pool.

## What the spreadsheet currently records
- **`primary_model: neural_network`** (third NN-primary winner), **`best_single_model: NN`**, **`dominant_base_model: neural_network`**
- `ensemble_method: mean_blend`, `cv_strategy: repeated_kfold`, `encoding_strategy: label_encoding`
- `models_used: NN` (NN-only — no GBDT, no other)
- **`fe_techniques`: No FE (overfitting); multi-label CV strategy; reweighting probabilities at output**
- `missing_data_strategy: imputation`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Specific technique cites | 1 named | **@SAMUEL muelsamu**'s "simple-tabpfn-approach-for-score-of-15-in-1-min" notebook — **probability reweighting technique** from this notebook. |
| Academic citation | **Variable Selection Network from TFT paper** (Lim et al. 2019, arxiv 1912.09363) | **Academic-paper-as-technique-source N=5 now**. Same TFT paper cited by s6e1 mahog ("VSN" model). |
| Cross-author cameos | @cdeotte (806th here), @cpmpml CPMP (901st here, Grandmaster of Grandmasters), @ravi20076 (854th) | **cdeotte's pre-dominance presence** pushed back to Aug 2023 (commenter here). CPMP first appearance in set. |

## What's actually original to this author
- **Custom NN with Variable Selection Network architecture** — TFT-paper-derived. Same architecture family later appears in s6e1 mahog's models.
- **No standard normalization (MinMax/Standard Scaler)**: instead, **linear projection with 8 neurons per feature**. Per-feature learned embeddings.
- **Huge dropout cascade**: 0.75 → 0.5 → 0.25 for 3 main layers. **Extreme regularization for tiny-data regime.**
- **Probability reweighting at output** (credit @SAMUEL muelsamu) — adjusts predictions to match expected class proportions.
- **10-fold CV × 10-30 repeats per fold + pick best 2 models per fold**: heavy training-stability management. Author explicit: *"the training was so unstable that the cv-scores could vary from 0.25 to 0.05 for single fold, partially due to large dropout values, partially due to little amount of train data."* **Variance management via repeated training + best-pick.**
- **Multi-label CV strategy**: trained baseline DNN → derived "hardness" label from validation predictions ((y_true=1 AND y_pred<0.2) OR (y_true=0 AND y_pred>0.8) → 1, else 0) → CV-stratified on (target × hardness). **Novel CV approach.**
- **NN-only at 617 rows** — counter to typical "small data → no NN" wisdom. Worked via the multiple stability mechanisms.
- **Surprised win**: *"How on Earth did I win this competition? I hoped to be in top 10%, but never dreamed of something more."* **5th surprised-author win in set.**

## Dataset constraints that shaped this strategy
- **TINY data (617 rows) + Featured/monetized + 6,430 teams** → enormous overfitting pressure, especially given $XX,000 prize incentive. Heavy regularization (huge dropout) + repeated training + best-pick = variance management. Author acknowledges luck factor but credits DNN architecture.
- **57 features + binary categoricals (max_card=2) + distribution_shift=TRUE** → variable selection (VSN architecture) helps filter relevant features under distribution shift.
- **Weighted Multiclass Loss metric** → probability reweighting at output directly improves the metric.
- **"Greeks" metadata available for train but not test** → ignored entirely (overfit risk). Same domain-aware decision pattern as Heitor s3e5 ("don't use original if it overfits CV").

## Code vs writeup check
- ✓ `icr-adv-model` notebook + supplementary training notebook attached to writeup
- ✓ Writeup details architecture choices (8-neuron-per-feature embeddings, dropout schedule, multi-label CV)
- ⚠ Variable Selection Network implementation detail visible in notebook

## Headline finding
**ICR Aug 2023** is the **first Featured/monetized competition in set** (6,430 teams — largest by far) and the **third NN-primary winner**. room722 won solo gold with **NN-only architecture (Variable Selection Network from TFT paper)** at **617 rows** — counter to typical small-data-no-NN wisdom. Strategy: huge dropout (0.75!) + repeated training (10×10-30) + multi-label CV + probability reweighting + per-feature 8-neuron embeddings instead of standard normalization. **5th surprised-author win** ("How on Earth did I win?"). **cdeotte commented (806th here)** — pre-dominance presence pushed back to Aug 2023. **CPMP (Grandmaster of Grandmasters)** first appearance in set. **Academic-paper-as-technique-source N=5** with TFT paper (same paper later cited by s6e1 mahog for VSN models — direct cross-competition academic citation persistence).

## Surprising / unusual
- **First Featured/monetized competition in set** (6,430 teams, largest). Different competition culture from Playground. Prize pool increased overfitting pressure.
- **Third NN-primary winner** — joins TPS May 2022 (two-branch NN) and TPS Jun 2022 (DAE imputation). All 3 NN-primary winners are pre-2024.
- **TINY data (617 rows) + NN-only wins** — counter to typical "small data → no NN" wisdom. Worked via heavy regularization (dropout 0.75) + repeated training + best-pick + multi-label CV. **"Sufficient stability management can make NN viable on tiny data."**
- **Variable Selection Network from TFT paper** (Lim et al. 2019, arxiv 1912.09363) — academic technique. **Cross-competition academic citation persistence**: same paper later cited by s6e1 mahog for VSN models (Jan 2026). **Academic technique appears 29 months apart in two different writeups.**
- **5th surprised-author win** — joins Kirderf s3e1, Bill Cruise s3e3, Umar s3e13, Mart Preusse s4e9. **Pattern reinforced: surprise wins happen at small-data / high-variance LB competitions.**
- **cdeotte pre-dominance presence pushed back to Aug 2023** (commenter here, 806th place). His pre-dominance era is now Feb 2023 → Dec 2024 (22 months) with multiple intermediate appearances.
- **CPMP (Jean-Francois Puget, Grandmaster of Grandmasters)** comments — first time a top-rank Grandmaster comments in our analyzed set. **Featured competitions attract the heaviest Kaggle names.**
- **Multi-label CV strategy** — train baseline → derive hardness label → CV-stratify on (target × hardness). New technique.
- **No standard normalization, instead per-feature linear projection (8 neurons each)** — counter-pattern. Learned embeddings for numeric features.
- **Solo gold in Featured competition** is a notable Kaggle achievement (room722's first competition per comments). **First-competition-solo-gold-at-Featured-level** is exceptionally rare.
