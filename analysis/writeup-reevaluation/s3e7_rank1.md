# s3e7 — Rank 1: Hardy Xu (hardyxu52) — first win, earliest entry

## Identifiers
- **Competition:** [playground-series-s3e7](https://www.kaggle.com/competitions/playground-series-s3e7) — *Binary Classification with a Tabular Reservation Cancellation Dataset*
- **End date:** 2023-04-30 (same date as s3e8! 678 teams — smallest yet) — **earliest entry now (Apr 2023)**.
- **Rank / score:** 1 of 678 · 0.92415 private LB (ROC AUC). 2nd: Jose Cáliz 0.92179 (0.0024 gap), 3rd: **Craig Thomas 0.92138** (same Craig who won 2nd at s3e8 next day).
- **Team / Kaggle user:** Hardy Xu / [hardyxu52](https://www.kaggle.com/hardyxu52) — **THIRD Hardy Xu entry**. Trajectory now: 1st at s3e7 (Apr 2023) → 2nd at s3e26 (Dec 2023/Jan 2024) → 1st at s4e10 (Oct 2024). **3 entries spanning 18 months, 2 wins.**
- **Writeup:** [1st place solution](https://www.kaggle.com/competitions/playground-series-s3e7/writeups/hardy-xu-1st-place-solution) (local: `data/writeups/playground-series-s3e7/1st place solution _ Kaggle.txt`)
- **Notebook:** **none**.

## Dataset
Binary classification of reservation cancellation, ROC AUC metric, 42,100 train rows (small). 18 features (mixed). 3 disguised-categorical numeric features: `type_of_meal_plan`, `room_type_reserved`, `market_segment_type`. **Heavy duplicate structure**: 1,531 duplicate pairs (dropping booking_status), distributed across train (562 with OPPOSITE labels!), test (253), train↔test (716).

## What the spreadsheet currently records
- `primary_model: ensemble` (6 models), `dominant_base_model: gbm`, `ensemble_method: mean_blend`
- `cv_strategy: repeated_stratified_kfold` (3 folds × 3 repeats), `hyperparameter_tuning: manual`
- `models_used`: XGBoost, LightGBM (2 families, 6 variants)
- **`fe_techniques`: Categorical feature identification; OHE vs native encoding comparison; duplicate/leakage exploitation (opposite label assignment; predict 0.5 for test duplicates); adversarial validation to filter original dataset; removal of train duplicates with test counterparts**
- `original_data_usage: concat_rows`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | Hardy Xu's writeup is technique-focused, no code-port citations. |
| Specific technique cites | **@siukeitin** ("predict 0.5 for test duplicates" suggestion) | siukeitin appears again — recurring as technique source across s3e7, s3e23, s4e5, s4e8, s4e10. |
| Cross-author cameos | Jose Cáliz (2nd here) comments suggesting median for AUC; Craig Thomas (3rd here, 2nd at s3e8 next day). |

## What's actually original to this author
- **Opposite-label assignment exploit**: 716 test rows had a train-set "twin" (identical features). Author assigned the OPPOSITE label to test → +0.014 LB boost. **Dataset structure-driven exploit**: train pairs with identical features had opposite labels (label noise/ambiguity), so the same pattern should hold for train↔test pairs. This is a *different* lookup-exploit from Sergey's s3e14 (which was identity-lookup) — here it's *inversion-lookup*.
- **0.5 prediction for test-test duplicate pairs** (from @siukeitin): when two test rows are duplicates, predict 0.5 → +0.003 LB boost. AUC-specific trick (about ranking).
- **3 categorical handling approaches tested in parallel** (as-is, OHE, native LGBM categorical) → multiple model variants → mean blend.
- **Adversarial validation to filter original dataset**: trained classifier between train+original → bimodal predicted-probability distribution for original → kept models with both full and reduced (17% pruned) original. **N=2 cases of adversarial validation** in set (here + s4e4 stopwhispering 12 months later).
- **Tree expressiveness unusually important**: XGB 'exact' algorithm (vs 'hist'), max_depth 12-13; LGBM larger max_leaves and max_bin. Dataset-specific finding contrary to typical depth=4-6 defaults.
- **Removed 562 train duplicates with opposite labels + 716 train-twin-with-test** → improves CV reliability.
- **Author's reaction to public discovery of exploit**: *"I naively hoped to keep this secret to myself, but it was quickly discovered by the rest of the community."* Real-time visibility of competition dynamics — exploits don't stay secret.

## Dataset constraints that shaped this strategy
- **Heavy duplicate structure with opposite-label pairs** in train → drives the entire duplicate-handling strategy. Unique dataset property (not all competitions have this).
- **Train↔test duplicate pairs** → enables the inversion-lookup exploit. Like s3e14's lookup, this requires generator-property exploitability.
- **3 disguised-categorical numerics + small dataset (42K)** → multi-way encoding comparison is feasible and useful (each approach generates one base model).
- **No exotic constraints** beyond the duplicate structure → standard XGB+LGBM ensemble.

## Code vs writeup check
- ✗ **No notebook published** (Hardy Xu doesn't publish notebooks — same as s3e26 / s4e10).
- ✓ Writeup details all 6 model configurations + duplicate counts + adversarial validation results.

## Headline finding
s3e7 (Apr 2023) is the **earliest entry now** and **Hardy Xu's first win in our analyzed set**. **Hardy Xu trajectory now spans 18 months across 3 entries** (2 wins): s3e7 (Apr 2023, mean-blend + lookup-exploit) → s3e26 (Dec 2023, NN-stacker + PLE academic technique) → s4e10 (Oct 2024, HC ensemble). **Within-author technique evolution**: mean-blend → NN-stacker → HC. **Opposite-label assignment exploit** (different from Sergey s3e14's identity-lookup): when train pairs have opposite labels for identical features, assign opposite to train-twin test rows. +0.014 LB boost — *dataset-structure-driven, not universal*. **Adversarial validation N=2 now** (here + s4e4 stopwhispering). **Author's "I naively hoped to keep this secret"** is rare visibility into the social dynamics of exploit discovery — exploits become public the moment they show up on the leaderboard.

## Surprising / unusual
- **Hardy Xu's earliest entry pushed back to Apr 2023** — 18-month documented trajectory across 3 entries, 2 wins. Within-author evolution: simple mean-blend → NN-stacker-with-academic-PLE → HC ensemble. **Author iterates on technique sophistication over time.**
- **Inversion-lookup exploit** (assign OPPOSITE label to test twin) is a distinct exploit family from identity-lookup (s3e14 Sergey assigns SAME label). Both are lookup-based but inverted. **Inversion exploit requires train having opposite-label pairs.**
- **562 train pairs with identical features but opposite labels** — significant label noise in the train data. Author removed these as a CV-cleanup step.
- **Tree expressiveness unusually important** (max_depth 12-13, XGB 'exact' algorithm) — counter to standard depth=4-6 GBDT defaults. Dataset-specific finding worth flagging.
- **Adversarial validation appears earliest at s3e7** (Apr 2023) — predates stopwhispering's s4e4 (Apr 2024) by 12 months. **Adversarial validation was established practice in s3 era.**
- **siukeitin recurring**: cited at s3e7 (Hardy), s3e23 (oscarm524), s4e5 (aldparis), s4e8 (Optimistix), s4e10 (omidbaghchehsaraei). **N=5 entries citing siukeitin's contributions** — same N as ambrosm and arunklenin. **Three most-recurring community contributors are now: ambrosm (N=5), arunklenin (N=5), siukeitin (N=5).**
- **Real-time exploit discovery dynamics**: *"quickly discovered by the rest of the community."* Public-LB-prominence forces exploit publication. Worth noting for understanding competition dynamics.
- **Craig Thomas placed 3rd here AND 2nd at s3e8 (same end date)** — community heavyweights converging at same time period.
