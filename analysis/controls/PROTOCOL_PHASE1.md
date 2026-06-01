# Phase 1 — Non-Winning Controls Feasibility Pilot

**Status:** Draft protocol. Not yet executed.
**Goal:** Test whether rank 4-20 non-winning entries can be found and coded against the Pass 3 schema with enough density to support a full Phase 2 study.
**Estimated effort:** 5-8 hours total.

---

## What this pilot tests

1. **Discovery feasibility:** Can codeable rank 4-20 entries be found in ≥1 of every 2-3 competitions?
2. **Data quality at lower ranks:** Is the detail in rank 4-20 posts sufficient to fill 53 boolean columns, or are they too brief?
3. **Realistic time per entry:** How long does discovery + coding actually take?

**Decision criteria after pilot:**
- ≥3 codeable entries found across 5 pilot competitions → scale to Phase 2 full sample
- 1-2 codeable entries found → reconsider scope (maybe rank 4-10 only, or pivot to Path 2 internal-top-3 variation)
- 0 codeable entries found → methodology infeasible; document and pivot to Path 1 (skip controls, lean on rescope)

---

## Target competitions for the pilot

Five competitions chosen for high community engagement (more likely to have rank 4-20 posts):

| Competition | Coded winner | Why selected |
|---|---|---|
| **playground-series-s4e8** (Mushrooms) | Optimistix r1 | Optimistix acknowledged 14+ contributors; community very engaged this month |
| **playground-series-s4e10** (Loan Approval) | omid r2 | Hardy Xu won, omid 2nd, nadavcherry 3rd — multiple top finishers active |
| **playground-series-s5e11** (Loan Payback) | mahog r1 | mahog wrote up, masaya cited, 23+ model families discussed in forum |
| **playground-series-s6e3** (Customer Churn) | cdeotte r1 | KGMON references 39 public notebooks — should have abundant rank 4-20 content |
| **playground-series-s4e7** (Cross Sellers) | Ravi+arunklenin r1 | Optimistix at 4th, tilii at 3rd, Cross Sellers acknowledged 5 specific competitors |

If discovery fails badly in 2+ of these, the methodology likely fails everywhere.

---

## Per-competition discovery protocol

For each of the 5 target competitions, allocate **~60 minutes**. Steps:

### Step 1 — Pull the private LB ranks 4-20 (10 min)

1. Navigate to `https://www.kaggle.com/competitions/<slug>/leaderboard`
2. Sort by private LB (default view)
3. Record the top 20 entries: rank, team/user name, private LB score
4. Note the rank-1 / rank-4 / rank-20 spread (margin matters for interpretation)

### Step 2 — Check each rank 4-20 entry for posted content (35 min)

Go through ranks 4-20 in order. For each:

1. **Check the competition's "Discussion" tab** filtered to that user — look for posts by that user
2. **Check the competition's "Code" tab** filtered to that user — look for published notebooks
3. **Check the competition's "Writeups" tab** — look for any formal writeup posts from rank 4-20

Categorize each rank's content as:

- **A — Full writeup + notebook** (best, ~5 competitions in our existing corpus have this)
- **B — Writeup only** (no published notebook)
- **C — Notebook only** (no formal writeup but a documented public notebook)
- **D — Discussion post only** (informal thread post describing approach)
- **E — Brief comment only** ("nice work, I came 7th with XGB") — not codeable
- **F — Nothing posted**

### Step 3 — Select the lowest-rank codeable entry (5 min)

Among ranks 4-20, identify the **lowest rank** (largest distance from rank 1) with content in categories A, B, C, or D. That's your control candidate.

Rationale for "lowest rank with codeable content":
- Maximizes distance from rank 1 (more meaningful comparison)
- Tests feasibility ceiling — if we can find rank 18-20 with codeable content, methodology scales
- Deterministic rule (no per-competition judgment)
- Acceptable bias for pilot (self-selection toward community-engaged lower-rank competitors is fine for feasibility testing; revisit in Phase 2 sampling design)

If no rank 4-20 has codeable content (only E/F): mark competition as "no control available" and move on. Don't fall back to ranks 2-3 (those are the existing on-disk writeups we already discussed — they don't address the actual selection-bias question).

### Step 4 — Save content locally (10 min)

For the selected candidate:
- Copy the writeup text into `data/writeups/<slug>/control_<author>_rank<N>.txt`
- Save the notebook (if any) to `data/writeups/<slug>/control_<author>_rank<N>.ipynb`
- Save any relevant discussion thread excerpt similarly

This keeps the control data alongside the existing winners' data, with `control_` prefix to distinguish.

---

## Pass 3 coding template for controls

After all 5 candidates are gathered, code each one. Estimated ~40 minutes per entry.

### Coding rules

- **Use the existing v3.1 schema (SCHEMA.md).** No new columns.
- **Set `pass3_source_confidence` honestly** based on what you found:
  - `notebook+writeup` if both available
  - `writeup+notes` if writeup but no notebook (note: there's no "Pass 2 notes" for controls, so substitute `writeup-only`)
  - `notebook-only` if only notebook available
  - `discussion-only` if only a discussion thread post (NEW value — flag this as lower confidence than even writeup-only)
- **Do NOT assign a paradigm.** Controls are "non-winning" by definition; the paradigm typology was developed from winners and circular to apply.
- **Do NOT code Pass 1 or Pass 2 fields.** Only Pass 3 booleans + admin columns.

### Data storage

Add control entries to a NEW file: `analysis/pass3-fe-taxonomy/controls_data.csv`

Same column structure as `stage1_data.csv`, with these differences:
- `competition_ref` is the same as the winner's competition (matched-on-competition design)
- `finish_rank` is the actual rank (e.g., 12 for rank 12)
- Add a new column at the start: `entry_type` = "control"
- The same 53 boolean columns
- Same admin columns (n_fe_techniques_used, pass3_notes, pass3_date_coded)

Keep controls in a separate CSV so the existing winners' analyses don't have to handle a mixed dataset.

---

## Success metrics for the pilot

After 5 competitions are processed and 5 candidates (or fewer) are coded:

### Quantitative metrics

| Metric | Target | If lower, implication |
|---|---|---|
| Codeable entries found | ≥3 out of 5 | Methodology feasible |
| Time per discovery | <60 min | Phase 2 scope realistic |
| Time per coding | <45 min | Phase 2 scope realistic |
| Median rank of codeable entries | ≥8 | True non-winning distance achieved |

### Qualitative checks

After coding each control, ask:
1. Did the content clearly describe enough FE technique detail to fill the 53 booleans, or did most columns end up at 0 by absence-of-information?
2. What was the source confidence distribution? (If most controls are `discussion-only`, the data is much weaker than winners' `notebook+writeup`.)
3. Did the control's techniques look qualitatively similar to the winner's, or different?

If most controls came in at 0-2 TRUE columns by absence-of-information (because brief discussion posts don't enumerate FE), the comparison won't be valid even with adequate sample size. The signal-to-noise ratio matters more than the count.

---

## Estimated time budget for pilot

| Step | Time |
|---|---|
| Setup (read this protocol, set up CSV) | 0.5 hours |
| Discovery × 5 competitions | 5 hours |
| Pass 3 coding × 5 entries | 3.5 hours |
| Write pilot summary + decision memo | 1 hour |
| **Total** | **~10 hours** |

Slightly more than the 5-8 I estimated initially. Plan for 10.

---

## Decision memo template (write after pilot)

After the pilot, document the results in `analysis/controls/PILOT_RESULTS.md`:

```markdown
# Phase 1 Pilot — Results and Decision

## What was found

- Competitions attempted: 5
- Codeable controls found: N out of 5
- Median rank of codeable entries: X
- Source confidence distribution: {nb+wu: a, wu-only: b, nb-only: c, discussion: d}

## Per-competition outcomes

| Competition | Lowest codeable rank | Source | Took (min) |
|---|---|---|---|
| s4e8 | 7 | nb+wu | 90 |
| ... | | | |

## What we learned

- [Honest assessment of feasibility]
- [Time-per-entry breakdown matches/differs from estimate]
- [Quality of content at lower ranks]

## Decision

- [ ] Scale to Phase 2 full sample (target 25-30 controls across 45 competitions)
- [ ] Reduce scope to ranks 4-10 only (if rank 11+ data was too thin)
- [ ] Pivot to Path 2 (internal-top-3 variation using on-disk writeups)
- [ ] Pivot to Path 1 (skip controls, focus on report rescope)

## Justification

[1-paragraph reasoning for the decision]
```

---

## Phase 2 design considerations (for after pilot)

If pilot succeeds, Phase 2 sampling should adjust to avoid the pilot's intentional bias:

- **Stratified by rank band**: split rank 4-20 into bands {4-7, 8-12, 13-20} and sample one codeable entry per band per competition where possible. Avoids "always-rank-18 self-selection."
- **Target n=20-25** across remaining 40 competitions (some won't yield any controls; aim for ~50% yield rate).
- **Pre-register the comparison tests** before running them: which aggregates will be compared, what proportion-difference threshold counts as "significantly different," whether multiple-testing correction is applied.

These design choices matter for Phase 2 reporting but don't need to be settled during Phase 1.

---

## Quick reference: what NOT to do during the pilot

- **Don't fall back to rank 2-3** if rank 4-20 yields nothing. Rank 2-3 are the on-disk writeups we already discussed; they don't address selection bias.
- **Don't try to code paradigms** for controls. The typology was developed from winners; applying it back is circular.
- **Don't combine the controls CSV into stage1_data.csv** during the pilot. Keep separate so existing analyses aren't disturbed.
- **Don't run statistical tests on n=5 pilot data.** It's feasibility validation, not findings.
- **Don't commit to Phase 2 before reviewing the pilot's decision memo.** The whole point of the pilot is to inform the scope decision.
