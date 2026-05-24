# s6e2 — Rank 1: masayakawamata (Masaya Kawamata)

## Identifiers
- **Competition:** [playground-series-s6e2](https://www.kaggle.com/competitions/playground-series-s6e2) — *Predicting Heart Disease*
- **End date:** 2026-02-28
- **Rank / score:** 1 of ~3,000+ teams · 0.95535 private LB (ROC AUC) · 0.9557801 final-submission CV. Top 3 separated by 0.00001 — decided in the 5th decimal place.
- **Team / Kaggle user:** Masaya Kawamata / [masayakawamata](https://www.kaggle.com/masayakawamata)
- **Writeup:** [1st Place Solution — Diversity, Selection, and Trusting the CV–LB Relation](https://www.kaggle.com/competitions/playground-series-s6e2/writeups/1st-place-solution-diversity-selection-and-t) (local: `data/writeups/playground-series-s6e2/1st Place Solution — Diversity, Selection, and Trusting the CV–LB Relation _ Kaggle.txt`)
- **Notebook (published):** [S6E2 | Single RealMLP](https://www.kaggle.com/code/masayakawamata/s6e2-single-realmlp) (local: `data/writeups/playground-series-s6e2/s6e2-single-realmlp.ipynb`) — *single distilled RealMLP, not the final ensemble*

## Dataset
Binary classification of `Heart Disease` ∈ {Absence, Presence}, ROC AUC metric, 630K train rows. 13 features (mixed): numeric (`Age`, `BP`, `Cholesterol`, `Max HR`, `ST depression`, etc.) + categorical. Synthetic data with an original heart-disease dataset available — author exploited the original via target statistics (target mean, smoothed mean, WoE, entropy) as external TE. Train/test CSVs not in `data/raw/`; schema recovered from notebook.

## What the spreadsheet currently records
- `primary_model: neural_network`, `best_single_model: RealMLP`, `dominant_base_model: neural_network`, `ensemble_method: stacking`, `hyperparameter_tuning: optuna`, `cv_strategy: stratified_kfold`, `original_data_usage: yes`
- `models_used`: XGBoost, LightGBM, CatBoost, RealMLP, RGF, TabICL, AutoGluon (7 families)
- `fe_techniques`: binning, digit features, all-as-categorical, within-fold TE (cuML), gplearn nonlinear features, original-data target stats (mean/smoothed/WoE/entropy), DVAE latents, knowledge distillation (0.5 hard + 0.5 teacher OOF)
- Caveat: `knowledge distillation` is listed as FE but is a training-time technique; also, the writeup explicitly lists distillation under *what did not work* — though distillation IS wired into the published single-model notebook (see Code vs writeup check).

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0 itemized** | Writeup gives broad thanks to @cdeotte, @tilii, @mahoganybuttstrings, @optimistix and "the community" — no numbered reference list. Author noted he was rushed and used an LLM to organize the writeup, so attribution may be condensed. |
| External Kaggle datasets used as input | 1 | The published RealMLP notebook loads `masayakawamata/s6e2-realmlpdistil/oof_realmlp_distil.csv` — author's *own* dataset with the teacher OOF for distillation. No third-party OOF datasets referenced. |
| Author cited *by* other winners | Yes | masayakawamata is named in cdeotte's s6e3 references twice (S5E11 LGBM, S5E5 ResMLP). Tight cross-author community. |

Cannot quantify reuse the way s6e4 (90% public OOFs) or s6e3 (39 numbered refs) allowed. Either masayakawamata did most pipeline work himself, or his writeup deliberately doesn't itemize. The detailed model+feature-set CV table in §4 (14 distinct combinations evaluated, each with specific OOF scores) suggests substantial original engineering, not just port-and-ensemble.

## What's actually original to this author
- **CV–LB relation discipline** (the headline): chose a 0.9557801-CV submission over the 0.955865-CV one because he tracked LB behavior across multiple stopped-ensemble submissions and found the CV–LB relation degrading above ~0.95578. Hindsight confirmed: had he picked highest-CV, he'd have come 3rd (0.95534) instead of 1st (0.95535).
- **Diversity-first generation:** ~150 OOFs from 7 model families × multiple feature representations (BASE / BIN / DIGIT / ALL_CATS / FREQ / GP_FEAT / DVAE / ORIG combinations). Explicitly chose "many slightly different models" over chasing one dominant model.
- **DVAE (Denoising Variational Autoencoder)** trained on base features for latent representations as a *diversity tool*, not for single-model performance.
- **gplearn genetic programming features** for nonlinear interaction discovery.
- **Original-dataset target statistics** (target mean, smoothed mean, WoE, entropy) as external TE, exploiting that the synthetic data was generated from a public original.
- **Optuna OOF subset search:** 2500 trials, only ~10% of the 150 OOFs were consistently selected. Selection treated as equal-importance to generation.
- **Ridge regression meta-learner** over nonlinear stackers (explicit anti-overfitting choice — nonlinear stackers overfit in his experiments).
- **20-seed full-data retraining** with `n_estimators = 1.25 × CV's best iteration`, averaged across seeds.
- **Explicit "what did not work" section** (rare): pseudo-labeling, knowledge distillation, deep GBDTs, high-order interaction expansion, other autoencoders, nonlinear stacking, averaging-without-selection, public-LB chasing.
- **Methodological rigor** (§10): full discussion of nested K-fold as theoretically correct, early stopping as subtle leakage, and the practical trade-offs he accepted.

## Dataset constraints that shaped this strategy
- **Synthetic data with original heart-disease dataset available** → enables external target statistics (mean, smoothed, WoE, entropy) as features. Universal pattern in the s6 era (see INDEX).
- **ROC AUC + extremely tight top-3 margin (0.00001 spread)** → makes single-model CV gains misleading; "highest CV" becomes high-variance gambling. Drives the validation-discipline strategy: deliberately sub-greedy submission selection based on CV–LB tracking.
- **Small base feature set (13 features)** → makes diversity-via-feature-representation cheap. Binning × digit × all-as-categorical × frequency × gplearn × DVAE × ORIG combinations are all feasible to enumerate. Larger feature spaces would force pruning.
- **Synthetic-data noise floor** → caps the marginal gain from per-model tweaks, which shifts the optimization frontier from "best single model" to "many slightly-different-mistakes models combined carefully."

## Code vs writeup check
- ✓ Published notebook implements digit features (cell 10), quantile+uniform+rounding binning (cell 12), all-as-categorical (cell 14, 17) — matching writeup §2.1–2.3
- ✓ RealMLP (pytabkit `RealMLP_TD_Regressor`) with 3-config top-3 hyperparam ensemble inside the notebook (cell 19) — `n_ens=8`, mish activation, PBLD num embeddings, no early stopping
- ⚠ **Distillation is wired in the published notebook** (cell 19 loads `oof_realmlp_distil.csv` as `teacher_pred` and uses it during training), but the writeup §8 lists "Knowledge distillation" under *what did not work*. Reconciliation: distillation likely was used in *some* of the 150 OOFs for diversity even though it didn't improve single-model CV — consistent with the diversity-over-individual-strength philosophy.
- ⚠ Final 150-OOF Ridge ensemble notebook is **not published** — only the single distilled RealMLP is. The Optuna subset search and Ridge meta-learner code are not available.
- ⚠ Spreadsheet lists `knowledge distillation` under `fe_techniques`; it's actually a training-time loss/label technique, not feature engineering.

## Headline finding
The winning edge for s6e2 was **validation discipline**, not bigger models or more compute. masayakawamata built ~150 OOFs across 7 families, used Optuna to select ~15 of them, stacked with Ridge, and then made a deliberate non-greedy final choice — picking a submission ~0.0001 below his best CV because the CV–LB relation degraded past 0.95578. The top 3 were separated by 0.00001; this discipline is what put him on top.

## Surprising / unusual
- **Far less explicit public-notebook attribution than s6e3 or s6e4** — no numbered references, just broad thanks. May reflect either genuinely more original work or writeup compression (author noted he used an LLM to organize and was rushed).
- **Distillation listed as "did not work" but actually used in the published single-model notebook.** Could indicate that techniques discarded for *single-model performance* are still kept in the ensemble for diversity — a subtle but important distinction not captured by the writeup's framing.
- **Explicit "what didn't work" section is rare and valuable** — for the meta-analysis, this is one of the few writeups likely to give us negative-result evidence we can compare across competitions.
- **The competition was decided in the 5th decimal place** (top 3 within 0.00001). The winning move was specifically *not* chasing the highest CV — an anti-pattern relative to what most Kaggle write-ups celebrate.
