# s5e8 — Rank 2: mahoganybuttstrings (Mahog)

> **Note:** Curated entry is rank-2, not rank-1. The s5e8 winner was Optimistix (0.97801 private LB); no rank-1 writeup is in the local set. This re-evaluation is Mahog's rank-2 writeup (0.97794 private LB, ~0.00007 behind 1st), consistent with `finish_rank: 2` in the spreadsheet. Useful as the third Mahog entry for within-author constraint→strategy analysis.

## Identifiers
- **Competition:** [playground-series-s5e8](https://www.kaggle.com/competitions/playground-series-s5e8) — *Binary Classification with a Bank Dataset*
- **End date:** 2025-08-31 (3,365 teams)
- **Rank / score:** **2 of 3,365** · 0.97794 private LB (ROC AUC). Top 3 spread: 0.97801 → 0.97794 → 0.97790 (1st–3rd within 0.00011, moderate-tight).
- **Team / Kaggle user:** Mahog / [mahoganybuttstrings](https://www.kaggle.com/mahoganybuttstrings) — third Mahog entry in the set (also won s5e11 and s6e1)
- **Writeup:** [2nd place - Yet another ensemble](https://www.kaggle.com/competitions/playground-series-s5e8/writeups/2nd-place-yet-another-ensemble) (local: `data/writeups/playground-series-s5e8/2nd place - Yet another ensemble _ Kaggle.txt`)
- **Notebook (published):** [PG S5E8 - TabM - CV 0.976810 PB 0.97750](https://www.kaggle.com/code/mahoganybuttstrings/pg-s5e8-tabm-cv-0-976810-pb-0-97750) (local: `data/writeups/playground-series-s5e8/pg-s5e8-tabm-cv-0-976810-pb-0-97750.ipynb`) — single TabM model only; the 59-model CatBoost ensemble code isn't published. This notebook was later ported into cdeotte's s6e3 as `tabM-800.ipynb`.

## Dataset
Binary classification on a bank dataset, ROC AUC metric, 750,000 train rows. 17 features (mixed), max_cardinality=12. Synthetic data with public original ("orig" targets used for TE on bigrams alongside competition targets — `original_data_usage: concat_rows`). No distribution shift mentioned. Train/test CSVs not in `data/raw/`; schema inferred from writeup and notebook.

## What the spreadsheet currently records
- `primary_model: ensemble`, `best_single_model: tabm`, `dominant_base_model: neural_network`
- `ensemble_method: stacking` (single value — not `hill_climbing; stacking` like s5e10/s5e11)
- `cv_strategy: stratified_kfold`, `hyperparameter_tuning: none`, `original_data_usage: concat_rows`
- `models_used`: tabm, xgboost, lightgbm, catboost, neural_network (lumped), random_forest, bart (7 categories) — writeup actually shows 13 distinct architectures (also DeepTables, TabR, RealMLP, Gandalf, GRN, FTTransformer, CNN). Spreadsheet undercount again.
- `fe_techniques`: TE/CE on feature bigrams (competition + original targets), products of numerical bigrams, cyclical features
- All fields are individually accurate; the rank-2 framing is honestly captured.

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **1 itemized** + 6 broad thanks | Cyclical features from @yekenot (same source mahog ports in s6e1, 5 months later). Broad thanks: @cdeotte, @omidbaghchehsaraei, @yekenot, @itasps, @siukeitin, @tilii7. |
| Author cited *by* other winners | Yes | This notebook (`pg-s5e8-tabm-cv-0-976810-pb-0-97750`) was explicitly ported into cdeotte's s6e3 as `tabM-800.ipynb`. The same yekenot cyclical-features port shows up again in mahog's s6e1 (within-author technique persistence). |

## What's actually original to this author
- **Diversity-without-tuning strategy** (explicit): "not all models were fully optimized... ideally with different models rather than same model and different hyperparams/FE." Same family as s5e11 (3 months later), explicitly *opposite* of s6e1 (5 months later) where mahog switched to hyperparameter-sweep-as-diversity.
- **CatBoost as the final stacker — and a side-by-side test against Ridge, LightGBM, HC.** This is unusual: most writeups commit to one stacker; mahog reports all four with CV / Public LB / Private LB results (table reproduced below). CatBoost won, beating Ridge by 0.00010 on private LB.

  | Ensembler | CV | Public LB | Private LB |
  |---|---|---|---|
  | Ridge | 0.977207 | 0.97804 | 0.97786 |
  | LightGBM | 0.977408 | 0.97816 | 0.97796 |
  | **CatBoost** | **0.977432** | **0.97817** | **0.97796** |
  | HC | 0.97740 | 0.97807 | 0.97789 |

- **TE/CE on bigrams using BOTH competition targets AND original-dataset targets** — the alternative-target TE technique appears here in an earlier form than s5e11 (where it became more elaborated).
- **Products of numerical bigrams** as features.

## Dataset constraints that shaped this strategy
- **Binary + ROC AUC + moderate top-3 margin** (0.00011) + **public original dataset available** → standard "many models + ensemble" terrain. No exotic constraints to force novel meta-architectures.
- **Two months after the previous Mahog competition (s5e6, also placed top-3 per his TLDR)** → mahog is iterating on a stable diversity-without-tuning recipe; the strategy is *carry-over*, not invented for this dataset.
- **CatBoost beating Ridge by 0.00010 on private LB** → for *this* competition, the linear-stacker assumption was wrong by a tiny margin. Generalisable lesson is small.

## Code vs writeup check
- ✓ Published notebook is the TabM single-model only (CV 0.97681, PB 0.97750 — would have been ~4th by itself); confirms cyclical FE port from yekenot, TE on bigrams.
- ✓ Notebook is the same one cdeotte ported into s6e3's `tabM-800.ipynb` reference.
- ⚠ The 59-model ensemble code with the 4-way stacker comparison is **not** in the published notebook. The numeric stacker-comparison table is only in the writeup.
- ⚠ Spreadsheet `models_used` lists 7 categories; writeup shows 13 distinct architectures (DeepTables, TabR, RealMLP, Gandalf, GRN, FTTransformer, CNN are all lumped or missing).
- ⚠ Spreadsheet `ensemble_method: stacking` is correct in spirit but lossless — the writeup explicitly tested 4 stackers (Ridge / LGB / CatB / HC) and reports all results.

## Headline finding
Mahog's rank-2 s5e8 is the **counterexample** to the "linear stacker is universal" coupling: CatBoost beat Ridge by 0.00010 on private LB in a head-to-head test the author ran explicitly. Same author, 3 months later (s5e11), reports "non-linear stackers were much worse than linear" — showing that *even within-author the stacker family choice is competition-conditional, not a methodological constant*. This is the strongest evidence yet that constraint→strategy is the right unit of analysis: 3 Mahog competitions, 3 different stacker/training choices, all top-2 finishes.

## Surprising / unusual
- **Direct counter-evidence for the linear-stacker coupling.** Mahog ran the controlled comparison; CatBoost won. The margin is 0.00010 (tiny) but it's real and reported.
- **Same-author stacker reversal**: s5e8 → CatBoost (chosen) → s5e11 → "non-linear stackers were much worse" → Ridge (chosen) → s6e1 → Ridge again. The author's belief about stacker family flipped between Aug and Nov 2025.
- **Best single model (TabM, PB 0.97750) is ~4th-place-tier alone**, and the 59-model ensemble adds only 0.00044 on top to reach 2nd place. Echoes the consistent Mahog pattern: one near-podium single model + cheap ensemble, with everything else being margin.
- **Optimistix won this competition** but isn't in our writeup set. The community pattern from later writeups (Optimistix → 9th in s5e11, 4th in s6e4, 12th in s5e10) shows he's a regular podium-finisher whose s5e8 1st place is missing context.
- **Mahog's "I've been competing in this series for well over a year"** (per s6e2 self-description) — his strategy iterations between s5e8 → s5e11 → s6e1 are the strongest within-author timeseries evidence we have for constraint→strategy.
