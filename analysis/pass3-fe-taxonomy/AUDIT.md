# Pass 3 FE Taxonomy — Data Audit

**Auditor's role:** expert data scientist reviewing this Pass 3 analysis for methodological soundness, coding validity, and the strength of the headline claims.

**Verdict in one line:** the per-column TRUE rates are usable; the per-paradigm summaries are *suggestive* but not strong enough to defend as paper-grade findings without addressing the issues below.

---

## Tier 1 — Issues that change the conclusions

### A1. Single-coder, single-author-designed schema (no inter-rater reliability)

**The biggest issue.** Both the schema and every coded cell came from one source. There is no Cohen's kappa, no second coder, no audit trail of disagreement and resolution.

The schema docs claim "any second coder could replicate." This is unverified. The genuine v3.1 schema revisions (col 17 broadened, col 53 relaxed) plus the documented mid-coding judgment calls (median TE in col 1, paddykb's all-as-categorical coded as col 10, fork-based FE judgments) suggest replicability would have flaws.

**Fix needed before publication:** ≥10 entries double-coded by an independent coder. Compute κ. Resolve disagreements with a documented protocol.

### A2. Paradigm × competition era are confounded

Heavyweight paradigm: s5e5, s5e6, s5e10, s6e2, s6e3 — **all in May 2025 – Mar 2026**.
Minimal-FE: s3e5 / s3e10 / s3e13 / s3e17 / s4e11 / s5e3 — mostly s3 era (Feb 2023 – early 2024).
Single-model-heavy: s4e12 / s5e2 / s5e4 — Dec 2024 – Apr 2025.

When we report "heavyweight uses 80% TE," it could mean any of:
- Heavyweight winners use more TE
- s5/s6 era uses more TE regardless of paradigm
- cdeotte's signature pulls heavyweight up (3 of 5 heavyweight entries are cdeotte)

**No way to disentangle paradigm from era from author** with n=5. The "constraint→strategy" framing in the report assumes paradigm causes technique choice; the data is consistent with era or author causing both.

### A3. Sample sizes per paradigm are too small for percentages

| Paradigm | n | 1 entry = |
|---|---|---|
| heavyweight | 5 | 20% |
| single-model-heavy | 3 | 33% |
| community-template | 4 | 25% |
| lookup-exploit | 4 | 25% |
| problem-fit-nn | 3 | 33% |

Single-model-heavy "100% Combo%" means *all 3 entries* do combinatorial search. With n=3, 95% CI is roughly [29%, 100%] — almost no inference power. Reporting "100%" is statistically dishonest at this n.

**Tilii s5e10 in heavyweight has TE=0, Groupby=0, Combo=0, Orig=0** — a heavyweight that does no TE, no groupby, no combos. This single entry pulls heavyweight TE% from 100% (4/4) to 80% (4/5). The "80% TE for heavyweight" number is one entry away from "100%."

### A4. Aggregation definitions are arbitrary choices, not derived

The schema doc declares:
```
uses_any_combinatorial_search = c16 OR (c17 AND c18)
```

Why `c17 AND c18`? If I used `c17 OR c18`:
- Single-model-heavy Combo% drops from 100% to 100% (unchanged — all 3 have both)
- Heavyweight Combo% goes from 20% to 40%
- Ensemble-standard goes from 16% to ~26%

The "100% combo% for single-model-heavy" is partly a definition artifact: all 3 single-model winners do c17 AND c18 because that's what cdeotte's recipe is.

**Group G (autoencoder, PCA, random projection, gplearn) is missing from any aggregate** — Kirderf s3e1's PCA flip and the autoencoder flips for s5e10 / s5e6 / s6e3 / s6e2 don't appear in *any* aggregate flag. They're "invisible" at the paradigm-summary level.

### A5. `c51` (explicit minimal/no FE) and `c53` (forked uncatalogued) are anti-FE meta-signals counted as +1 in n_fe

This is conceptually wrong. n_fe is computed as `sum of TRUE booleans`. But:
- `c51` = "author explicitly did NO FE." Heitor s3e5 gets n_fe=1 (or 2 in current CSV) because c51=TRUE. But Heitor did 0 FE techniques.
- `c53` = "FE happened in a forked notebook that isn't catalogued." Sergey s3e14 gets n_fe=1 from c34 (lookup) plus possibly c53. Counts as +1 even though it represents *missing* coding.

Sanity check: minimal-FE paradigm mean n_fe = 1.86, range 1-2. This is entirely from c51 TRUE values, not from actual FE. The mean conflates "did no FE explicitly" with "did some FE."

**Recommended fix:** publish two n_fe metrics:
- `n_fe_techniques` = sum of cols 1-50 (actual FE techniques)
- `n_fe_meta` = sum of cols 51, 52, 53 (meta-signals)

### A6. `c02` (within-fold TE) null-handling biases the result downward

c02 is documented as three-valued: TRUE, FALSE, null. The Python aggregate parser treats null/empty as 0 (FALSE). So "TE within-fold" rate is systematically *under-counted* — entries with ambiguous TE handling get coded as "no within-fold TE" rather than "unknown."

Current count: c02 TRUE = 13/45 = 29%. Real rate is higher (probably 40-50%) because most cdeotte / mahog / masaya entries use cuML TargetEncoder per-fold even when not explicitly stated.

---

## Tier 2 — Specific coding errors caught in audit

### B1. s3e1 Kirderf flipped to col 31 (cyclical) and col 39 (PCA) but disappears from aggregate flags

Stage 2 flipped col 31 and col 39. The aggregate flags show **ALL ZEROS** for Kirderf. Reason: col 31 is in Group E (domain/temporal/structural) and col 39 is in Group G (learned/advanced). Neither is in any aggregate. Kirderf's 3 FE techniques are invisible at the paradigm-summary level.

This isn't a coding error — it's an **aggregate-design error**. Group G should have its own aggregate (`uses_any_learned_derived_feature` = c38 OR c39 OR c40 OR c41).

### B2. Tilii s5e10 in "heavyweight" paradigm has n_fe=3 and all-zero aggregates

Tilii's TRUE columns: c38 (autoencoder), c41 (gplearn), c44 (Lasso generator recovery), c46 (residual). None of these are in any aggregate flag (autoencoder/GP are Group G; Lasso recovery is Group H; residual is Group I).

So Tilii's heavyweight entry shows TE=0 Groupby=0 Combo=0 Orig=0 Model=0 Sel=0 even though it has 3-4 distinct techniques. The aggregate misrepresents this entry.

### B3. s3e7 Hardy Xu coded as "lookup-exploit" but his exploit is postprocessing

s3e7's "opposite-label assignment for train-test duplicates" is a **prediction override**, not a feature. Stage 1 correctly coded c52 (adversarial validation) and Stage 2 added c51 (explicit no FE).

But the **paradigm assignment** to "lookup-exploit" reflects the lookup *narrative*, not the FE *substance*. Hardy Xu uses no lookup features at all. The aggregate shows Orig=0 for him, correctly. But then the "75% Orig-derived for lookup-exploit" headline only reflects 3 of 4 entries because the 4th paradigm-member doesn't fit.

This means the paradigm assignment for s3e7 is **wrong for FE-analysis purposes**. Should probably be "minimal-FE" or its own category "postprocessing-exploit."

### B4. The `c01` broadening to "single-statistic TE (mean OR median)" wasn't applied to all entries that use median TE

v3.1 changed col 1 to include median TE. Mart Preusse s4e9 was flipped. But other entries (mahog's TE work) may also use median TE — was every entry rechecked? Audit says: probably not.

### B5. csv data integrity has known drift

7+ entries have stored n_fe that disagrees with the sum-of-booleans. The aggregation script recomputes n_fe to handle this, but downstream consumers reading the CSV directly will see inconsistent values. This is a data engineering problem documented but not fixed.

---

## Tier 3 — Bias and validity concerns

### C1. Selection bias: winners only

The corpus is 45 1st-3rd place winners. The implicit hypothesis is "what wins?" but we're observing *what winners did*, not *what works on average*.

A 4th-place entry might use the same techniques as a 1st-place entry. Without non-winning entries to compare against, we can't distinguish "this technique correlates with winning" from "this technique is common."

**Counterfactual question we can't answer:** if a winner had used a different technique, would they still have won?

### C2. Author concentration

cdeotte alone is **8 entries** (s4e12, s5e2, s5e3, s5e5, s5e6, s6e3, plus ICR + s5e4-comment) — ~18% of the corpus. mahog is 4 entries. ambrosm is 4. Three authors = 16/45 = 35% of the corpus.

The "heavyweight uses TE" pattern is **mostly the cdeotte pattern**. Without the cdeotte cluster, heavyweight n drops to 2 (s6e2 masaya, s5e10 Tilii) and the percentages become meaningless.

### C3. Survivor bias on FE techniques

We code techniques that authors *report*. Authors:
- Report techniques they think helped (selection effect on technique → reporting)
- Don't report techniques they tried and discarded (selection effect on success → reporting)

So "X% used TE" actually means "X% reported using TE in a way that justified mention." Could be higher or lower than actual usage. Stage 2 partially addresses this by reading notebook code, but only 22/45 entries have full code.

### C4. The schema is the analyst's mental model, not nature

Every column is a category I invented. The choice of 53 columns vs 30 or 100 is itself a coding decision. The schema is "true" only to the extent it carves nature at its joints.

Some columns are clearly real techniques (TE basic, log transform, pairwise multiplicative). Others are author-specific signatures (c22 groupby histogram bins = cdeotte's invention with n=1). The aggregates don't distinguish "broadly-recognized FE technique" from "single-author idiosyncrasy."

### C5. The TPS entries are different from the season-N PS entries

TPS Feb 2022 (generator-flaw exploit), TPS May 2022 (two-branch NN), TPS Jun 2022 (DAE-for-imputation), ICR (Featured competition). These have substantially different competition mechanics than the PS season format. Including them in the same corpus and computing paradigm percentages mixes the populations.

---

## Tier 4 — Robustness checks (recommended but not done)

The following SHOULD be done before claiming any pattern:

1. **Drop s6e3 cdeotte (the n_fe=19 outlier)** and recompute heavyweight stats. If patterns survive, they're robust. If they evaporate, the heavyweight finding is "cdeotte wrote KGMON."

2. **Subset to entries with `notebook+writeup` confidence** (n=22) and recompute. If the high-confidence subset shows the same patterns as the full set, the patterns are robust to notes-only entries' uncertainty. If they shift, the headline numbers are partly notes-only noise.

3. **Subset to s4 era onward** (Dec 2024+). If the patterns hold there, they're not just the s3 era's minimal-FE drag.

4. **Drop cdeotte entries** (n=37 remaining). If "heavyweight TE = 80%" survives, the pattern isn't cdeotte-driven.

5. **Independent paradigm assignment.** Have a second person assign paradigms before coding. Compute paradigm-assignment agreement. Re-run aggregates with the agreed assignments only.

None of these have been done. The headline numbers in STAGE2_AGGREGATES.md are best read as "first-pass exploratory" — not "publication-grade findings."

---

## What's defensible to claim from this data

**Defensible (with caveats):**

- TE is the single most-used FE technique in the winning-solutions corpus (40% of 45 entries).
- Heavyweight ensemble paradigm uses qualitatively more FE techniques than lookup/minimal-FE paradigms.
- A core cdeotte recipe — within-fold TE, multi-aggregation groupby, original-derived snap/KDTree — is present across his entries.
- Lookup-exploit paradigm relies on original-derived features by construction.

**Not defensible from this data alone:**

- Specific percentages by paradigm at n<5.
- "Single-model-heavy uses 100% combinatorial search" — n=3.
- Causal claims (X paradigm causes Y technique).
- Era-controlled comparisons.
- Rankings of techniques by importance (we measure use, not impact).

**Should not be claimed without further work:**

- Inter-paradigm differences are statistically significant.
- Authors converge on the same techniques.
- These percentages reflect the broader Kaggle community, not just our 45.

---

## Recommendations

**Before the project ends:**

1. Add a `uses_any_learned_derived_feature` aggregate (c38 OR c39 OR c40 OR c41) so Kirderf's PCA, Tilii's GP+autoencoder, and masaya's DVAE appear in the summary.
2. Split `n_fe` into `n_fe_techniques` (c01-c50) and `n_fe_meta` (c51, c52, c53). Anti-FE signals shouldn't add to a "uses many techniques" count.
3. Run the 4 robustness checks above. Report which patterns survive each.
4. In the research report, scope claims to "the cdeotte / mahog / community heavyweight cluster" rather than the more sweeping "heavyweight paradigm."
5. Add a paragraph documenting the single-coder limitation and the auditor's recommendations.

**Tier-2 fixes (only if a second pass is in scope):**

6. Independent paradigm re-assignment, with κ.
7. Independent coding of ≥10 entries (Cohen's κ on the bool columns).
8. CSV data integrity pass: rewrite stage1_data.csv with proper quoting so stored n_fe matches sum-of-booleans.

**Tier-3 fixes (probably out of scope):**

9. Code 10-20 non-winning entries (4th-10th place) as a control.
10. Multivariate analysis: paradigm vs era vs author as predictors of technique use.
