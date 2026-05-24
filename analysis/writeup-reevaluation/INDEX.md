# Writeup Re-evaluation — Index

Per-writeup deep re-reads of the curated entries in `data/kaggle_meta_analysis.xlsx`.

**Goal:** for each winning entry, determine what the author *actually originated* (vs. inherited from public notebooks, discussions, or earlier baselines), and identify the technique(s) that plausibly delivered the winning edge.

**Where things live:**
- Per-writeup docs stay focused on their subject (this folder)
- Project-level reflection / methodology decisions live in `journal/session_log.md`
- Cross-writeup patterns roll up below under *Cross-cutting observations*

## Status

| Doc | Competition | Rank | Author / Team | Status | Headline finding |
|---|---|---|---|---|---|
| [s6e4_rank1.md](s6e4_rank1.md) | playground-series-s6e4 (Predicting Irrigation Need) | 1 | cstdy / kirill0212 | done | ~90% of final ensemble's OOFs from public notebooks; winning edge is two-binary-classifier reframing + logit blending + threshold search |
| [s6e3_rank1.md](s6e3_rank1.md) | playground-series-s6e3 (Predict Customer Churn) | 1 | cdeotte (Chris Deotte) | done | KGMON Playbook (pre-published NVIDIA framework) applied at scale via 39 public-notebook ports + LLM-generated code; original work is synthetic-data exploitation toolkit + LLM agent workflow |
| [s6e2_rank1.md](s6e2_rank1.md) | playground-series-s6e2 (Predicting Heart Disease) | 1 | masayakawamata (Masaya Kawamata) | done | Won by *validation discipline*: ~150 OOFs across 7 families, Optuna subset selection, Ridge stacker, and a deliberate non-greedy final-submission choice based on CV–LB relation analysis |
| [s6e1_rank1.md](s6e1_rank1.md) | playground-series-s6e1 (Predicting Student Test Scores) | 1 | mahoganybuttstrings (Mahog) | done | Won by *strength-over-diversity* (opposite of s6e2): 190 hyperparameter-tuning-trial OOFs of 10 strong models, Ridge stacker, Centered Isotonic Regression post-processing applied twice. Regression + no public original. |
| [s5e12_rank1.md](s5e12_rank1.md) | playground-series-s5e12 (Diabetes Prediction Challenge) | 1 | wind1234it | done | First **distribution-shift** case: post-cutoff CV (credited to @masayakawamata) + two-stage HC selection → Ridge stacking on top-36. Photo-finish margin (0.00007), weak signal (~0.70 AUC). |
| [s5e11_rank1.md](s5e11_rank1.md) | playground-series-s5e11 (Predicting Loan Payback) | 1 | mahoganybuttstrings (Mahog) | done | Same author as s6e1 but **opposite strategy**: 23 model families × heavy FE combinatorics × no hyperparameter tuning + Ridge/HC stacker. Notebook explicitly ported into cdeotte's s6e3 (`mahog-700.ipynb`). |
| [s5e10_rank1.md](s5e10_rank1.md) | playground-series-s5e10 (Predicting Road Accident Risk) | 1 | Tilii (tilii7) | done | Won most extreme photo-finish (4-way tie at 0.05563) via **ensemble-stage engineering**: GP features added at second-level stacker, CatBoost residual booster on Keras ensemble, HC of two-level ensembles. cdeotte cited these techniques for use in s6e3 4 months later. |
| [s5e8_rank2.md](s5e8_rank2.md) | playground-series-s5e8 (Binary Classification with a Bank Dataset) | **2** | mahoganybuttstrings (Mahog) | done | *Rank-2 entry per spreadsheet* (rank-1 writeup not in set). Third Mahog entry: 59-model diversity ensemble with **CatBoost as stacker** — direct head-to-head test had CatBoost beating Ridge by 0.00010 on private LB. Counterexample to the linear-stacker coupling. |
| [s5e7_rank2.md](s5e7_rank2.md) | playground-series-s5e7 (Predict the Introverts from the Extroverts) | **2** | Irfan Ahmad | done | *Rank-2 + no writeup* (notebook-only evaluation). Simplest pipeline in set: single FE trick (`match_p` row-merge with public original), 5 GBDT variants, Optuna-tuned weighted blend with threshold search. Tiny dataset (18K) + accuracy metric constrain the strategy. |

## Cross-cutting observations

Patterns that show up across **multiple** writeups (N ≥ 2). Single-case observations stay in the per-writeup doc's *Surprising / unusual* section until a second case promotes them here. Cite the writeups each entry rests on.

### Constraint → viable strategies

Datasets and competition structures don't have a single "winning strategy" — but specific *constraints* appear to make specific *strategy families* viable (or even forced). A coupling enters this table when the same constraint→strategy pairing is observed in ≥2 cases. This table is the intended spine of the flowchart deliverable.

| Dataset / competition constraint | Viable strategy | Cases (N) |
|---|---|---|
| Synthetic data with known public original | Exploit-original toolkit: snap features (s6e3), KDTree nearest-neighbor lookup (s6e3), **exact row-match join** (s5e7 `match_p` — enabled by small discrete feature space), external target statistics (mean, smoothed, WoE, entropy), drift ratios, "original_as_columns" feature concat, **TE with alternative targets from original columns** (s5e11) | s6e4_rank1, s6e3_rank1, s6e2_rank1, s5e12_rank1, s5e11_rank1, s5e8_rank2, s5e7_rank2 (N=7 of 7 applicable cases; s6e1 had no public original and the toolkit is absent there — consistent) |
| Heavy public-notebook coverage of competition (and prior PS series) | Fork-heavy OOF ensembling; cross-season porting from earlier seasons | s6e4_rank1, s6e3_rank1 (N=2; s6e2 and s6e1 acknowledge community but itemize fewer ports) |
| Many OOFs at linear-stacker scale (>~50) | Linear stacker (Ridge / LogisticRegressionCV / cuML L2 LR / HC rank-blend) as **final** meta-learner is the *common* choice — anti-overfit choice over nonlinear stackers (s5e11 explicit: "stacking with non-linear models... much worse than linear"). **But not universal:** s5e8 (Mahog) ran the head-to-head and chose CatBoost over Ridge (won by 0.00010 on private LB). Linear preference holds in 6 of 7 cases; the exception was the *same author* who later switched back to linear. | Linear: s6e4_rank1, s6e3_rank1, s6e2_rank1, s6e1_rank1, s5e12_rank1, s5e11_rank1, s5e10_rank1 (final layer only) (N=7). Counter: s5e8_rank2 (CatBoost, +0.00010 over Ridge in author's own test). |
| Tight top-N margin (≤ CV noise floor) | Validation discipline as primary strategy — deliberately sub-greedy submission selection, CV–LB gap monitoring, sometimes ≠ highest-CV submission | s6e2_rank1 (chose 0.9558-CV over 0.9559 best), s5e12_rank1 (chose Ridge top-36/α=10 over top-34/α=5 due to public LB gap) (N=2; s5e10 had even tighter margin but Tilii used meta-ensemble engineering instead — a second viable response to the same constraint) |
| Late-comp plateau + extremely tight top-N margin | Meta-architecture engineering at the ensemble layer — GP features at ensemble stage, residual-boost ensembler, ensembles-of-ensembles | s5e12_rank1 (HC of HC), s5e10_rank1 (GP-at-ensemble + Keras→CatBoost residual + HC of 2-level ensembles) (N=2) |

### Hypotheses awaiting a second case

Constraint→strategy couplings with N=1 evidence. Promote to the table above when a second case appears.

- **Multiclass + rare class + balanced-accuracy metric → binary reframe** (split into one-vs-rest dichotomies). Observed: s6e4_rank1. Test on: future multiclass/imbalanced competitions, especially those with non-standard metrics.
- **No public original + strong CV/LB correlation + long signal tail → strength-over-diversity** (focus on stronger individual models + hyperparameter-sweep-as-diversity, not just many-weak-models). Observed: s6e1_rank1. This is *contradictory* to the validation-discipline strategy; the constraint set differs. Test on: other regression / no-original competitions.
- **Different model families want different feature representations → maintain separate FE sets (NN-friendly vs GBDT-friendly)**. Observed: s6e1_rank1 (explicit two-feature-set design). Test on: other writeups — most authors use one FE pipeline; mahog is unusual in articulating this split.
- **Regression + RMSE + miscalibrated base model predictions → isotonic-regression post-processing at two stages** (per-OOF before stacker, and on stacker output). Observed: s6e1_rank1. Test on: other regression competitions.
- **Distribution shift + identifiable train/test cutoff → post-cutoff CV optimization + rank-blend HC with negative weights + Ridge stacker on top-N** (validation restricted to the train region that matches test). Observed: s5e12_rank1. Test on: other competitions flagged `distribution_shift: TRUE`.
- **Weak per-feature signal + low absolute score (~0.70 ROC AUC) → ensembles-of-ensembles** (feed prior HC/Ridge stacks back in as base models for a meta-HC). Observed: s5e12_rank1. Test on: other low-signal competitions.
- **Synthetic data with no external original + nearly-linear underlying target → Lasso as diagnostic / generator-formula reverse-engineering**. Observed: s5e10_rank1 (Tilii recovered the target formula via Lasso coefficients, then independently confirmed it with constrained GP). Test on: other no-original synthetic competitions.
- **Engineered features that fail as base inputs may succeed at the ensemble layer**. Observed: s5e10_rank1 (11 GP features added to stacker, not to base models). Test on: other writeups that distinguish base-feature vs ensemble-feature placement.
- **Small dataset (<50K rows) + non-AUC metric + public original mergeable on feature tuple → row-match join + 5-GBDT weighted blend (no stacking, no NNs)**. Observed: s5e7_rank2. The s6-era heavy-ensemble toolkit isn't viable here (overfits at this scale). Test on: other small-dataset entries if any exist in the curated set.
- **Negative ensemble weights** as a deliberate diversity-and-cancellation mechanism. Observed: s5e7_rank2 (Optuna weights in [−1, +1] normalized), s5e12_rank1 (wind1234it HC weights −0.3 to +0.5). N=2 — could be promoted but the technique is implementation-detail-level rather than constraint→strategy, so leaving here for now.

### Notebook-only evaluations

Some entries have no discussion writeup in the local set (only the published notebook). For these, the "Public-notebook reuse" and "What's actually original" analyses are code-only inferences — we cannot distinguish what the author originated vs inherited without authorial narrative. Treat findings as weaker evidence.

- s5e7_rank2 (Irfan Ahmad — Introverts/Extroverts) — notebook is pedagogical/beginner-facing style.

### Methodology / schema gaps
- **Component vs origination is invisible in the spreadsheet.** `fe_techniques` and `models_used` list what was *used*, not what was *originated*. In s6e4 and s6e3 the lists are accurate but credit the winner for FE/models that are overwhelmingly inherited; in s6e2 we can't even tell because attribution isn't itemized in the writeup. (s6e4_rank1, s6e3_rank1, s6e2_rank1)
- **Architectural-level contributions are unrecorded.** s6e4's two-binary-classifier reframing, s6e3's 4-level KGMON stack, and s6e2's Optuna-subset + Ridge + CV–LB-discipline pipeline don't fit `primary_model`, `ensemble_method`, or any other current field. (s6e4_rank1, s6e3_rank1, s6e2_rank1)
- **Spreadsheet `dominant_base_model` is ambiguous and inconsistently coded.** s6e3 says `neural_network` despite 90 trees vs 60 NNs (trees dominate by count); s6e2 says `neural_network` for a 7-family mix where best single is RealMLP. Codebook needs to clarify whether this is "best single" or "count majority". (s6e3_rank1, s6e2_rank1)
- **Training-time techniques are sometimes coded as FE.** s6e2 lists `knowledge distillation` under `fe_techniques`; it's a training-loss technique. (s6e2_rank1)

### Cross-season patterns
- **Cross-author / cross-season community is tight.** Top winners cite each other across seasons: cdeotte cites masayakawamata twice in s6e3 (S5E11 LGBM, S5E5 ResMLP); kirill0212 (s6e4 winner) is one of the public-OOF contributors for s6e3 implicitly via the broader community network. (s6e3_rank1, s6e2_rank1; watch in s6e1)
- **Cross-season porting of public notebooks is a winner strategy.** s6e3 winner explicitly ports ~15 prior PS-series solutions (S5E11, S5E8, S5E10, S5E5, S5E4, S6E1) into the s6e3 ensemble. (s6e3_rank1; not present in s6e2, watch in s6e1)

### Public-notebook reuse patterns
- **Reuse-attribution explicitness varies wildly.** s6e4 gives a 30/25/6 OOF breakdown; s6e3 gives 39 numbered URLs with adapted-in filenames; s6e2 gives broad thanks to ~4 names and "the community" — no itemized references. The earlier hypothesis "Grandmaster winners explicitly attribute" is contradicted by s6e2 (also a strong contributor, cited by cdeotte). May be a *competition culture* signal (winner choice) rather than a Grandmaster norm. (s6e4_rank1, s6e3_rank1, s6e2_rank1)
- **The "winning edge" lives one layer above the components.** s6e4 = meta-architecture (two-binary-classifier reframing). s6e3 = framework-application + LLM workflow + 4-level stack. s6e2 = validation discipline + selection-as-important-as-generation + Ridge-over-nonlinear stacker. None of these are at the FE or base-model layer. (s6e4_rank1, s6e3_rank1, s6e2_rank1)
- **Distinct "win profiles" are emerging:** (1) clever-reframing (s6e4), (2) industrial-scale-ensemble-from-forks (s6e3), (3) validation-discipline (s6e2). All three are at the meta-architecture layer — different *kinds* of meta-architecture. Worth tracking whether s6e1 fits one of these or introduces a fourth. (s6e4_rank1, s6e3_rank1, s6e2_rank1)

### Other recurring patterns
- **Synthetic-data exploitation is universal *when a public original exists*.** s6e4, s6e3, s6e2 all use the original; s6e1 has no public original and the toolkit is correspondingly absent — confirming the coupling is dataset-driven, not author-driven. Spreadsheet's `original_data_usage: yes/no` captures the availability but not the technique. (s6e4_rank1, s6e3_rank1, s6e2_rank1, s6e1_rank1)
- **The cross-citation network spans seasons.** cdeotte cites mahog 5× + masayakawamata 2× in s6e3; masayakawamata cites cdeotte + mahog in s6e2; mahog cites cdeotte + yekenot + others in s6e1; kirill0212 cites multiple public contributors in s6e4; wind1234it cites masayakawamata (post-cutoff CV) and 5 others in s5e12. The community is ~10 named contributors propagating techniques across at least s5–s6 (≈6+ months). **Techniques cross competition boundaries faster than people do** — masayakawamata's post-cutoff CV idea informed s5e12's winner before masayakawamata himself won s6e2 with related validation-discipline framing. (all five)
- **"Stronger models" vs "diverse weak models" is a competition-conditional choice, not an author identity.** Same author (Mahog) across 3 competitions: s5e8 = diversity-no-tuning (CatBoost stacker, 2nd); s5e11 = diversity-no-tuning (Ridge/HC stacker, 1st); s6e1 = strength-with-tuning (Ridge stacker, 1st). Plus masayakawamata s6e2 = diversity (Ridge stacker, 1st). The same-author **stacker family** also flipped: Mahog Aug 2025 → CatBoost; Nov 2025 → "non-linear stackers much worse than linear" → Ridge/HC; Jan 2026 → Ridge. Strongest evidence so far that strategy is competition-conditional even at the stacker-family level. (s6e2_rank1, s6e1_rank1, s5e11_rank1, s5e8_rank2)
