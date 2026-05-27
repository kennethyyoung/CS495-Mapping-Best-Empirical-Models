# s4e10 — Rank 2: omidbaghchehsaraei (OMID BAGHCHEH SARAEI)

> **Note:** Curated entry is rank-2 per spreadsheet. Rank-1 was Hardy Xu ("CatBoost All The Way Down" — writeup exists locally but not in coded set). omidbaghchehsaraei is **in the community network** — cited twice in cdeotte's s6e3 references (TabTransformer + RealMLP ports).

## Identifiers
- **Competition:** [playground-series-s4e10](https://www.kaggle.com/competitions/playground-series-s4e10) — *Loan Approval Prediction*
- **End date:** 2024-10-31 (3,858 teams)
- **Rank / score:** **2 of 3,858** · 0.96913 private LB (ROC AUC). Top 3: Hardy Xu 0.96938 → omid 0.96913 → nadavcherry 0.96902 (1st–3rd within 0.00036, tight but not photo-finish).
- **Team / Kaggle user:** OMID BAGHCHEH SARAEI / [omidbaghchehsaraei](https://www.kaggle.com/omidbaghchehsaraei)
- **Writeup:** [2nd place solution](https://www.kaggle.com/competitions/playground-series-s4e10/writeups/omid-baghcheh-saraei-2nd-place-solution) (local: `data/writeups/playground-series-s4e10/2nd place solution _ Kaggle.txt`)
- **Notebook (published):** [ensemble-modeling-for-loan-approval](https://www.kaggle.com/code/omidbaghchehsaraei/ensemble-modeling-for-loan-approval) (local: `data/writeups/playground-series-s4e10/ensemble-modeling-for-loan-approval.ipynb`) — 40 cells; **9-model public notebook (not the winning 21–24-model private pipeline)**. Author explicit: *"The screenshots above are from my private notebook with over 20 models, not my public notebook with only 9 models. But the approach is the same."*

## Dataset
Binary classification of `loan_status`, ROC AUC metric, 58,645 train rows. 12 features (mixed), no missing data, max_cardinality=7. Public original dataset available (`original_data_usage: yes` — concat_rows).

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: hill_climbing`
- `cv_strategy: stratified_kfold`, `encoding_strategy: target_encoding`, `scaling: standard`
- `models_used`: LightGBM, XGBoost, CatBoost, ExtraTrees, RandomForest, KNN, MLP (7 in spreadsheet; notebook also has LightGBM-Dart, LightGBM-Goss as variants)
- `fe_techniques: original data concat; dual numeric+categorical representation` — light FE, mostly via paddykb's all-as-categorical technique
- `hyperparameter_tuning: not_described`, `best_single_model: not_described`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **1 itemized** | @paddykb's "PS s4e10 - No Keras, No Loan (cv 0.963)" — the *all-features-as-categories* technique, described as "a game-changer in this competition." Also referenced paddykb's "PG s4e10: Loan 🦈 SHAP" notebook in comments. |
| Acknowledgments | @siukeitin ("insightful posts and comments, Grandmaster title is well-deserved") | siukeitin is part of the s6 community network. Cross-author link to later writeups. |
| Author cited *by* others | Yes, heavily | omidbaghchehsaraei is cited **2× in cdeotte's s6e3 references** (TabTransformer port `nn2-1603.ipynb`, best-solo-RealMLP port `realmlp8-6300.ipynb`). His s4e10 work is part of the technique flow into the later KGMON Playbook. |
| Cross-author comments | Mahdi Ravaghi (s4e11 winner, placed 8th here): *"I also tried hill climbing but didn't have any success."* Confirms HC was a known/tested approach in late s4. |

## What's actually original to this author
- **HillClimbing-based ensemble** using the `hillclimbers` library (predates cdeotte's "GPU Hill Climbing" canonization at s5e5). HC was already a known technique in s4 — cdeotte's s5e5 naming was a refinement/canonization, not invention.
- **9-model base ensemble (public) → 21–24-model private ensemble** with same architecture. Diversity via multiple LightGBM variants (standard + DART + GOSS), XGBoost, CatBoost, plus non-tree models (ExtraTrees, RandomForest, KNN, MLP).
- **Validation discipline (anti-greedy submission)**: best LB score 0.97350 was NOT chosen because CV was lower (0.96954). Selected two safer submissions, both with higher CV and lower public LB but better private-LB-trustability. Same pattern as s6e2/s5e12/s4e11.
- **Single FE addition**: `risk_flag = (cb_person_default_on_file=='Y') & (loan_grade.isin(['C','D','E']))` — added specifically for poly-LGBM model diversity, not as a primary predictor.
- **paddykb's all-as-categorical applied here** — a fork-then-ensemble pattern (treat all features as categories, train models, add to ensemble). Light FE inherited from public notebook.

## Dataset constraints that shaped this strategy
- **Medium-size dataset (58K rows) + binary + tight-but-not-photo-finish margin (0.00036)** → multi-model HC ensembling is well-matched; no need for the heavy meta-architecture engineering of photo-finish cases.
- **Public original + low max_cardinality (7)** → simple concat_rows + minimal FE; the "exploit-original" toolkit is light (no snap features, no KDTree needed).
- **paddykb's public notebook with all-features-as-categories was high-CV (0.963)** → made the technique an obvious cite for the community; adopting it gave free diversity.

## Code vs writeup check
- ✓ Notebook (40 cells) implements 9 base models (LGBM, LGBM-DART, XGBoost, ExtraTrees, RandomForest, CatBoost, KNN, MLP, LGBM-GOSS) with `cross_validation` wrapper and `%%time` markers. Uses `hillclimbers` library (cell 1).
- ✓ Spreadsheet `ensemble_method: hill_climbing` matches.
- ⚠ **Published notebook is the 9-model public version**, not the 21–24-model private winning pipeline. The author's `poly-LGBM` model with the `risk_flag` feature is in the private notebook, not public.
- ⚠ Spreadsheet `best_single_model: not_described` is honest — the writeup doesn't enumerate per-model CV scores, so the spreadsheet doesn't claim one.

## Headline finding
s4e10 rank-2 is **the earliest validation-discipline case in the set** (Oct 2024 — earlier than s4e11 by 1 month, and 4 months before s6e2). Author explicitly chose lower-public-LB submissions because their CV was higher — same anti-greedy pattern that recurs through s4e11 (Mahdi), s5e12 (wind1234it), and s6e2 (masayakawamata). **Validation discipline has been a winning strategy from at least Oct 2024 onward; it's an established pattern, not a 2026 discovery.** omidbaghchehsaraei is also in the community network (cited in cdeotte's s6e3 references), and his HC use predates cdeotte's "GPU Hill Climbing" canonization at s5e5 — HC was already standard in s4.

## Surprising / unusual
- **Validation discipline coupling now N=4** (s6e2, s5e12, s4e11, **s4e10**). Earliest case is Oct 2024 — this is a *well-established* winning pattern in binary classification with tight margins, not a recent discovery.
- **HC use predates cdeotte's canonization** by 7 months. cdeotte at s5e5 (May 2025) wrote the "GPU Hill Climbing" starter notebook that popularized the technique, but HC via the `hillclimbers` library was already winning s4e10 in Oct 2024. cdeotte added GPU acceleration + community-asset framing.
- **paddykb's all-features-as-categories** is a community technique that propagates here. paddykb isn't in our analysis set as a winner but is a meaningful technique-source.
- **Single non-trivial FE feature** (the `risk_flag`) explicitly for *diversity* of one model, not for primary prediction. Echoes Tilii's s5e10 "GP-features-at-ensemble-stage" idea — FE-for-diversity is a recurring theme.
- **omidbaghchehsaraei's work flows into cdeotte's s6e3 KGMON Playbook** (2× cited as TabTransformer + RealMLP ports). Concrete evidence of the s4 → s6 technique flow through this author. The community network was already partially formed in Oct 2024.
