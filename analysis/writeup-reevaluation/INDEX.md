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

## Cross-cutting observations

Patterns that show up across **multiple** writeups (N ≥ 2). Single-case observations stay in the per-writeup doc's *Surprising / unusual* section until a second case promotes them here. Cite the writeups each entry rests on.

### Constraint → viable strategies

Datasets and competition structures don't have a single "winning strategy" — but specific *constraints* appear to make specific *strategy families* viable (or even forced). A coupling enters this table when the same constraint→strategy pairing is observed in ≥2 cases. This table is the intended spine of the flowchart deliverable.

| Dataset / competition constraint | Viable strategy | Cases (N) |
|---|---|---|
| Synthetic data with known public original | Exploit-original toolkit: snap features, KDTree nearest-neighbor lookup, external target statistics (mean, smoothed, WoE, entropy), drift ratios | s6e4_rank1, s6e3_rank1, s6e2_rank1 (N=3 of 3 applicable cases; s6e1 had no public original and the toolkit is absent there — consistent) |
| Heavy public-notebook coverage of competition (and prior PS series) | Fork-heavy OOF ensembling; cross-season porting from earlier seasons | s6e4_rank1, s6e3_rank1 (N=2; s6e2 and s6e1 acknowledge community but itemize fewer ports) |
| Small base feature set + mature public-notebook ecosystem | Ridge stacker on many strong/diverse OOFs (anti-overfit choice over nonlinear stackers) | s6e2_rank1 (Ridge on ~150 OOFs), s6e1_rank1 (Ridge on 190 OOFs), s6e4_rank1 (LogisticRegressionCV on 61 OOFs — same linear-stacker family) (N=3) |

### Hypotheses awaiting a second case

Constraint→strategy couplings with N=1 evidence. Promote to the table above when a second case appears.

- **Multiclass + rare class + balanced-accuracy metric → binary reframe** (split into one-vs-rest dichotomies). Observed: s6e4_rank1. Test on: future multiclass/imbalanced competitions, especially those with non-standard metrics.
- **Tight top-N margin (≤ CV noise floor) + ROC AUC → validation discipline as primary strategy** (anti-greedy submission selection based on CV–LB tracking). Observed: s6e2_rank1. Test on: other photo-finish competitions; s6e3 was also tight (0.00007 spread top 3) but cdeotte didn't write CV–LB analysis as a primary lever.
- **No public original + strong CV/LB correlation + long signal tail → strength-over-diversity** (focus on stronger individual models + hyperparameter-sweep-as-diversity, not just many-weak-models). Observed: s6e1_rank1. This is *contradictory* to the validation-discipline hypothesis above; the constraint set differs. Test on: other regression / no-original competitions.
- **Different model families want different feature representations → maintain separate FE sets (NN-friendly vs GBDT-friendly)**. Observed: s6e1_rank1 (explicit two-feature-set design). Test on: other writeups — most authors use one FE pipeline; mahog is unusual in articulating this split.
- **Regression + RMSE + miscalibrated base model predictions → isotonic-regression post-processing at two stages** (per-OOF before stacker, and on stacker output). Observed: s6e1_rank1. Test on: other regression competitions.

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
- **All four s6 winners participate in one tight cross-citation network.** cdeotte cites mahog 5× + masayakawamata 2× in s6e3; masayakawamata cites cdeotte + mahog in s6e2; mahog cites cdeotte + yekenot + others in s6e1; kirill0212 cites multiple public contributors in s6e4. The "community" is ~10 named contributors who repeatedly cite each other across competitions. (all four)
- **"Stronger models" vs "diverse weak models" is a competition-conditional choice, not an author identity.** s6e1 mahog explicitly chose strength; s6e2 masayakawamata explicitly chose diversity. Both won 1st. The competition profile (signal-tail length, CV–LB tightness) determines which is correct. Evidence for the *constraint→strategy* framing being the right unit of analysis. (s6e2_rank1, s6e1_rank1)
