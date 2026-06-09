# Report Improvement Plan (from expert critique)

**Drafted 2026-06-03.** Remediation plan for `research_report_v2.md` based on the expert-reviewer critique. Tags: 📊 needs new analysis (computable from existing data) · ✍️ prose-only · ⚠️ integrity/defensibility.

**Sequencing principle:** run the Tier-2 analyses first; their outputs feed the Tier-1 prose. Then Tier-3 polish.

---

## Tier 1 — Defensibility (must-fix before submission)

The headline comparison is the exposure. The goal is to make §4.5 the *most-caveated* section, not the most-confident.

1. **Recast §4.5 (volume-vs-learned) as caveated.** ✍️⚠️
   - Report Group G as **exact raw counts** (≈7 winners vs ≈1 control), not just "16% vs 9%."
   - Soften "the only differentiator is learned features" → "the only family showing a winner-favoring gap, on thin counts."
   - Add the **selection-on-codeability** bias note (controls chosen partly for writeup detail → biased toward *more* documented FE).
   - Depends on item 5 (paired analysis) and the exact-count pull.

2. **Add a synthetic-data external-validity paragraph (§5.4).** ✍️
   - State plainly: the corpus is overwhelmingly Playground Series (synthetic data); TE dominance, lookup-exploit, and external-original use are partly synthetic-generation artifacts. Generalization to real-world tabular ML or Featured competitions (n=1) is unestablished.

3. **Caveat the "median 2 / small core" as a possible measurement floor (§4.4).** ✍️📊
   - `n_fe` is bounded by writeup detail; terse writeups → low counts by construction.
   - Back it with item 6 (n_fe by source-confidence): if notebook+writeup entries don't show higher n_fe, the finding strengthens; if they do, it qualifies.

4. **Tighten reliability claims (Abstract + §3.6).** ✍️⚠️
   - Abstract "validates" → "substantial family-level agreement (κ=0.65), with lower technique-level agreement (58%)."
   - Note the reliability sample is **n=12**.
   - Make the **AI-assisted-coding integrity framing airtight**: specify concretely what "AI assistance under researcher direction" meant and the human's role (a committee will ask).

---

## Tier 2 — Strengthening (new analyses, computable from existing data)

5. **Within-competition PAIRED winner-vs-control comparison.** 📊 *(highest-leverage upgrade)*
   - For each of the 11 control competitions, pair the control's FE-group vector against *that same competition's winner* in `stage1_data.csv`.
   - Report per-pair deltas (winner groups − control groups) and Group-G presence per pair.
   - Controls for competition difficulty/type; replaces the confounded aggregate comparison. Becomes the new core of §4.5.

6. **`n_fe` by source-confidence.** 📊
   - Group winners by `pass3_source_confidence` (notebook+writeup / writeup-only / notes-only); show n_fe distribution per group.
   - Small table or figure; feeds item 3.

7. **Guild base-rate / chance baseline (§4.6).** 📊
   - Report the number of distinct authors across winners + controls and an expected-overlap-under-chance figure (hypergeometric/permutation).
   - *Dependency:* winners' author handles are not in `stage1_data.csv` (only controls have `author_handle`); may require extracting winner handles from the Pass-2 / writeup-reevaluation docs first.

---

## Tier 3 — Polish

8. **Trim Discussion redundancy.** ✍️ §5.1–5.3 re-report §4.4–4.6 numbers; cut to interpretation only.
9. **Reframe or demote §4.3 Coupling.** ✍️ It reads as legacy against the new thesis — either tie it to "what distinguishes winners" or move detail to an appendix.
10. **Downgrade §5.2 "frontier has shifted."** ✍️ → "may be shifting" (thin evidence + n=4 Season-6).
11. **Coupling "Strong" at n_testable=5.** ✍️ Don't let the abstract/§4.1 lean on the small-n strong verdict (C6).
12. **Housekeeping.** ✍️ Title-page date (still "May 2026"); **§6 References** in APA 7.
    - §2 carries the densest unanchored citations (~8 author groups, no years): Caruana & Niculescu-Mizil, Gijsbers et al., Erickson et al./AutoGluon, Gorishniy et al., Borisov et al., Athey et al., Makridakis/Spiliotis/Assimakopoulos (M5), von Krogh & von Hippel, Merton 1968 (Matthew Effect). Every one needs an APA entry; add years inline during the §6 pass.

---

## Suggested execution order

1. Tier-2 analyses (5 → 6 → 7) — produce the numbers/figures.
2. Tier-1 prose (1, 3, 4) using those outputs; then 2.
3. Tier-3 polish (8–12).

**Net:** items 1–4 make the report defensible; item 5 makes it materially stronger; the rest are credibility polish. None require new data collection except possibly item 7's author handles.
