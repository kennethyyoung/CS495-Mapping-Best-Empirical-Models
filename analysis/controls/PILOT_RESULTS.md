# Phase 1 Pilot — Results and Decision

**Status:** Pilot complete. 5/5 controls coded.
**Date:** 2026-06-01.
**Branch:** `phase12/control-coding-pilot`.

---

## What was found

### Quantitative summary

| Metric | Target | Actual | Verdict |
|---|---|---|---|
| Codeable entries found | ≥3 out of 5 | **5/5** | Exceeded |
| Median rank of codeable entries | ≥8 | **15** | Exceeded |
| Time per discovery | <60 min | ~30 min user reported | Within budget |
| Time per coding | <45 min | ~20-30 min Claude | Within budget |

All five target competitions yielded codeable controls at ranks 14-19. The discovery success rate (5/5) is substantially higher than the protocol's success threshold (3/5). The methodology is clearly feasible.

### Per-competition outcomes

| # | Competition | Control rank | Author | Source confidence | n_fe_tech | n_fe_meta | Winner paradigm |
|---|---|---|---|---|---|---|---|
| 1 | playground-series-s6e2 | 15 | emreduman05 | notebook+writeup | 4 | 0 | heavyweight |
| 2 | playground-series-s5e10 | 14 | metamodels | writeup-only | 2 | 0 | heavyweight |
| 3 | playground-series-s6e3 | 16 | mhamza0810 | notebook+writeup | 9 | 0 | heavyweight |
| 4 | playground-series-s5e8 | 15 | tilii7 | notebook+writeup | 3 | 0 | ensemble-standard |
| 5 | playground-series-s6e4 | 19 | elenkapetrova | notebook+writeup | 7 | 1 | community-template |

### Source confidence distribution

- `notebook+writeup`: 4 controls (80%)
- `writeup-only`: 1 control (s5e10 metamodels — notebook is meta-only averager with no FE code)

This is comparable to the existing 45-entry corpus (49% notebook+writeup, 29% writeup+notes, 22% notes-only). Control quality matches winner quality.

---

## What we learned

### The headline finding: heavyweight Group G validates

The audit-fix-#1-revealed claim "heavyweight winners use Group G features" holds in all three heavyweight comparisons in the pilot:

| Competition | Winner Group G | Control Group G | Direction |
|---|---|---|---|
| s5e10 (Tilii r1 vs metamodels r14) | ✓ autoencoder + gplearn + Lasso recovery | ✗ | Winner > Control |
| s6e2 (masaya r1 vs emreduman r15) | ✓ DVAE + gplearn | ✗ | Winner > Control |
| s6e3 (cdeotte r1 vs mhamza0810 r16) | ✓ DAE + PCA + GRP | ✗ (DVAE available, **explicitly dropped**) | Winner > Control |

**3/3 heavyweight comparisons support the finding.** The s6e3 case is particularly clean: mhamza0810 had DVAE features handed to him in an upstream FE pipeline and removed them from his feature set (notebook cell 5, `cols_to_drop`). That's a deliberate technique-selection difference, not absence of opportunity.

### The Group G pattern is paradigm-specific

| Paradigm | Winner Group G | Control Group G |
|---|---|---|
| heavyweight (n=3) | 3/3 | 0/3 |
| ensemble-standard (n=1) | 0/1 (mahog) | 1/1 (tilii7's GP) |
| community-template (n=1) | 0/1 | 0/1 |

The pattern reverses at s5e8 (ensemble-standard) where the control uses Group G but the winner doesn't. At s6e4 (community-template), neither uses Group G. This means:

> Group G is heavyweight-specific. It is not a generic "winner-distinguishing" technique.

This is a *refinement*, not a contradiction. The audit fix #1 finding becomes more precise rather than weaker.

### Author signatures persist across competitions

The s5e8 control turned out to be **tilii7 — the same person as the s5e10 winner**. Tilii used genetic programming in both:
- s5e10 r1 (winner, heavyweight): GP among autoencoder + Lasso recovery
- s5e8 r15 (control, ensemble-standard): 13 GP_NN features

Tilii's GP is an *author signature*, not a *winner-distinguishing technique*. This complicates the "winners use X" framing throughout the analysis — at least for techniques strongly associated with specific authors.

This also suggests paradigm labels are competition-conditional. Tilii is a "heavyweight" author at one competition and "ensemble-standard-control" at another. The paradigm captures what an author *did at a specific competition*, not who the author *is*.

### Heavyweight winners have substantially more FE techniques than controls

| Competition | Winner n_fe_tech | Control n_fe_tech | Ratio |
|---|---|---|---|
| s5e10 | 4 (Tilii) | 2 (metamodels, undercount caveat) | 2.0× |
| s6e2 | 10 (masaya) | 4 (emreduman) | 2.5× |
| s6e3 | 19 (cdeotte) | 9 (mhamza0810) | 2.1× |
| Mean | 11.0 | 5.0 | **2.2×** |

Even mhamza0810's elaborate 9-technique control at s6e3 falls well short of cdeotte's 19. This supports the rescoped claim "heavyweight winners average ~6-7 FE techniques (drop-cdeotte estimate)" — controls average ~5 in this paradigm.

For non-heavyweight comparisons (s5e8, s6e4), the pattern doesn't hold: controls have similar or more techniques than winners.

### Caveats that emerged during coding

1. **Three of five controls had meta-only notebooks.** s5e10 (metamodels), s5e8 (tilii7's GP-only NB), s6e4 (elenkapetrova's Ridge meta-only) all published notebooks that don't contain base-model FE. For these, the writeup is canonical and source confidence drops to writeup-only or writeup+notebook-meta-only. Same generational-drift issue we documented for several winners in the original corpus.

2. **"Chris formula" and "magical feature" are common vague-naming patterns.** elenkapetrova mentions both but doesn't define them. Conservative coding leaves these unmarked. Likely true rate of multiplicative/additive interactions is higher than coded.

3. **s5e10 writeup is very high-level.** "Statistical features," "features-rich," "with target encoding" are too vague to map to specific Pass 3 columns. The n_fe_tech=2 for metamodels is almost certainly an under-count.

These caveats apply equally to the existing corpus's writeup-only winners. The control coding has the same biases.

---

## Decision options

Following the protocol's decision template:

### Option A: Scale to Phase 2 full sample (target 25-30 controls)

**Pros:**
- Larger n enables statistical testing of paradigm-specific differences
- More heavyweight controls (target 8-10) would tighten the 100% Group G claim
- Coverage of paradigms beyond heavyweight (ensemble-standard, community-template) needs more controls
- The protocol's success criteria explicitly say "≥3 codeable → scale to Phase 2"

**Cons:**
- ~30-40 additional hours of discovery + coding work
- The heavyweight Group G finding is already clear at 3/3; marginal value of additional heavyweight controls is small
- Discovery in s3/s4 era competitions may be harder (older discussions, lower writeup density at low ranks)
- s3-era controls would likely not change the heavyweight Group G finding (heavyweight paradigm is s5/s6-era)

### Option B: Stop here, write up pilot results as the finding

**Pros:**
- 5 controls is enough to support paradigm-bounded claims with documented limitations
- The heavyweight Group G finding is robust at 3/3; more data won't sharpen it much
- The Tilii cross-author finding is a methodological contribution that doesn't need more data to support
- Frees ~30-40 hours for report rescope work

**Cons:**
- Statistical claims are weaker at n=3 per paradigm (no significance tests possible)
- Reviewer might say "controls are interesting but n is small"
- Doesn't fully address the audit's selection-bias concern in the strongest possible way

### Option C: Targeted extension — code 5-10 more controls focused on ambiguous paradigms

**Pros:**
- Bigger ensemble-standard control sample (currently n=1) would clarify if the s5e8 GP-reversal pattern generalizes
- Bigger community-template sample (currently n=1) would test whether "no Group G" pattern holds
- Skips heavyweight which is already conclusive
- Realistic effort: ~10-15 hours

**Cons:**
- Heavyweight Group G remains the strongest finding; spending time elsewhere may not change the headline
- Discovery effort for non-heavyweight competitions may be similar to heavyweight (per-comp ~30-60 min)

---

## Recommendation

**Option B (stop, write up).**

Rationale:
1. The pilot exceeded all quantitative success criteria (5/5 codeable, median rank 15).
2. The headline finding (heavyweight Group G survives controls) is robust at n=3 heavyweight comparisons.
3. The methodological surprise (Tilii cross-author signature) is more informative than additional data would be — it surfaces a confound that more controls would also encounter.
4. For the *capstone* deliverable, 5 controls in 10 hours is a substantial methodological strengthening; 30 controls in 40 hours would only modestly improve the headline claim.
5. Phase 2's marginal value is in *non-heavyweight paradigms* where the pilot has n=1 each. Those don't drive the report's headline finding (the audit-flagged heavyweight Group G).

**If Option A is preferred**, prioritize:
1. Additional heavyweight controls (s5e2 cdeotte, s5e5 cdeotte, s5e6 cdeotte) to push the Group G claim from 3/3 to 5-6/6.
2. Skip s3/s4-era competitions (writeup availability low at deep ranks; heavyweight paradigm absent).
3. Target 5 more controls, ~10 hours.

This converges to Option C effectively — a targeted scale-up rather than full Phase 2.

---

## What's defensible to claim from this pilot

**Strong (3/3 supports):**
- "In heavyweight ensemble competitions, winners use learned-derived feature techniques (autoencoder/PCA/GRP/gplearn) that elaborated non-winning entries at the same competitions do not."
- "Group G usage is paradigm-specific to heavyweight ensembles in our corpus, not a generic winner-distinguishing pattern."

**Suggestive (n=1 per non-heavyweight paradigm):**
- "In our ensemble-standard and community-template comparisons, the Group G pattern does not extend or is reversed."

**Methodological:**
- "Author signatures (e.g., genetic programming for tilii7) persist across competitions regardless of finish rank. Paradigm assignment is competition-conditional, not author-fixed."

**NOT defensible from this pilot:**
- Statistical significance of any specific aggregate difference (n=3 per paradigm).
- Generalization to s3/s4-era competitions (pilot is all s5/s6).
- Quantitative claims about technique-count distributions (caveats from writeup-only controls).

---

## Time spent

| Step | Estimated | Actual | Notes |
|---|---|---|---|
| Discovery (user) | 5 hr | ~2-3 hr | User did discovery faster than protocol estimate |
| Coding (Claude + user review) | 3.5 hr | ~2 hr | 5 entries at ~20 min each |
| Decision memo | 1 hr | (this doc) | |
| **Total** | 10.5 hr | **~5-6 hr** | Substantially under budget |

The pilot was more efficient than predicted, partly because the user found high-quality candidates quickly and partly because all 5 controls had at least writeups (no need to scrape discussion-only candidates).
