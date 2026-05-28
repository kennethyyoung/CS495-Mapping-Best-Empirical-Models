# Pass 3 FE Taxonomy — Pilot Results (3 entries)

**Status:** Pilot complete. Schema revisions proposed.
**Branch:** `phase9/fe-taxonomy`.
**Author:** Kenneth Young.
**Date:** 2026-05-28.

This document codes three representative entries against the 52-column schema in `SCHEMA.md`, in two stages, to validate the schema before the full 45-entry pass.

## Pilot entries

| Entry | Paradigm | Expected TRUE count | Sources consulted |
|---|---|---|---|
| cdeotte s5e6 | ensemble-stacking, heavyweight | 15–25 (expected) | Pass 2 MD + original writeup (no notebook published) |
| Sergey s3e14 | lookup-exploit | 1–3 (expected) | Pass 2 MD + original writeup + notebook |
| Heitor s3e5 | minimal-FE | 0–2 (expected) | Pass 2 MD + original writeup + notebook |

## Pilot results — coded boolean cells (TRUE only listed)

### Entry 1: cdeotte s5e6 (Predicting Optimal Fertilizers)

**Stage 1 — from Pass 2 MD only (`pass3_source_confidence = notes-only`):**

| # | Column | Justification (from MD) |
|---|---|---|
| 1 | `uses_target_encoding_basic` | MD: "TE of 162 combos × 7 binary targets" |
| 4 | `uses_te_alternative_targets` | MD: "7 binary targets" = 7 derived alternative targets per class |
| 17 | `uses_higher_order_categorical_combos` | MD: "all pairs/triples/quadruples of 8 features (162 combos)" |
| 32 | `uses_original_target_mean_as_feature` | MD: "TE using original dataset" |
| 45 | `uses_pseudo_labels_as_features` | MD: "Stacking XGB with pseudo-label COLUMNS" |
| 46 | `uses_residual_features` | MD: "residual boosting (XGB over LR base margin)" |

**Stage 1 TRUE count: 6**

**Stage 2 — after reading original writeup (`pass3_source_confidence = writeup+notes`):**

Added columns (Stage 1 missed → Stage 2 caught):

| # | Column | Justification (from writeup) |
|---|---|---|
| 2 | `uses_target_encoding_within_fold` | Writeup TE formula shown; cdeotte signature is within-fold for leakage-safety. **Tentative TRUE** — would be confirmed if notebook were available. |

Removed columns: none.

**Stage 2 TRUE count: 7**

**Stage 1 → Stage 2 delta: +1 (within-fold TE was implicit; not explicitly stated in MD).**

**Surprise:** Expected 15–25; got 7. The "monster model" produces 2,268 features but from only ~7 distinct techniques. **Feature-count is not feature-diversity.** This is itself a useful schema-level finding — the schema captures technique diversity (which is bounded ~5–10 even for heavyweight wins) rather than feature-count (which can be in the thousands).

### Entry 2: Sergey s3e14 (Wild Blueberry Yield)

**Stage 1 — from Pass 2 MD only:**

| # | Column | Justification (from MD) |
|---|---|---|
| 34 | `uses_exact_key_match_lookup` | MD: "match test rows to original dataset by (fruitset, fruitmass) keys; assign exact original yield values" |

**Stage 1 TRUE count: 1**

**Stage 2 — after reading writeup + notebook:**

Added columns: **none**. Writeup confirms only the exact-key-match lookup as the winning move. Sergey's contribution was *only* the postprocessing lookup. The 8 base OOFs come from public notebooks (paddykb, adaubas, yzokulu, tetsutani, zhukovoleksiy); their internal FE is *not documented in Sergey's writeup*.

Removed columns: none.

**Stage 2 TRUE count: 1**

**Stage 1 → Stage 2 delta: 0**

**Schema issue surfaced:** This entry is a *fork-heavy* solution where the base-model FE techniques are technically part of the winning ensemble but are inherited from forked public notebooks. The schema undercounts FE for fork-heavy entries unless we read each base notebook (impractical at scale). **Coding decision for full pass: accept the undercount and flag it in `pass3_notes`.** (Alternative: add a single boolean `uses_forked_base_model_fe` to mark this case explicitly.)

### Entry 3: Heitor s3e5 (Wine Quality, Ordinal Regression)

**Stage 1 — from Pass 2 MD only:**

| # | Column | Justification (from MD) |
|---|---|---|
| 51 | `explicit_minimal_or_no_fe` | MD: "fe_techniques: None — FE tried but worsened CV" |

**Stage 1 TRUE count: 1**

**Stage 2 — after reading writeup + notebook:**

Writeup confirms: *"I tried different FE and the ones available in some public notebooks, but my local CV was doing worse, so I removed it. In the end, my final model did not have a special FE."*

Added columns: **none**.
Removed columns: none.

**Stage 2 TRUE count: 1**

**Stage 1 → Stage 2 delta: 0**

This is the cleanest pilot entry. Author explicitly states no FE. Single XGBoost with Optuna + OptimizedRounder (post-processing, out of scope) + StratifiedKFold (CV, out of scope).

## Aggregate pilot statistics

| Entry | Expected TRUE | Stage 1 TRUE | Stage 2 TRUE | Delta | In expected range? |
|---|---|---|---|---|---|
| cdeotte s5e6 | 15–25 | 6 | 7 | +1 | **No** (much lower than expected) |
| Sergey s3e14 | 1–3 | 1 | 1 | 0 | Yes |
| Heitor s3e5 | 0–2 | 1 | 1 | 0 | Yes |

**Stage 1 → Stage 2 delta total: +1 column across 3 entries (1 / 156 cells = 0.6% flip rate).**

This is much smaller than I expected. Two possible reasons:
1. The pilot entries all have *focused* FE recipes (cdeotte's KGMON proto is tightly scoped; Sergey is single-trick; Heitor is no-FE). Less-focused winners might show a higher delta.
2. The Pass 2 MDs for these three entries are unusually thorough on FE because all three are paradigm-defining cases.

The 156-cell low delta is *not* representative of what we'd see on the broader 45. Expect higher deltas on entries with diverse FE recipes.

## Schema issues surfaced during pilot

### Issue 1: Expected ranges were overestimated

I expected the heavyweight (s5e6) to hit 15–25 TRUE columns. It hit 7. The schema captures **FE technique diversity**, not **FE feature count**. cdeotte's 2,268-feature monster uses 7 distinct techniques; mahog's later 100+-model stacks would probably hit ~10–15.

**Revised expected ranges for the full 45-entry pass:**

| Paradigm | Expected n_fe_techniques_used |
|---|---|
| Ensemble-stacking heavyweight (cdeotte s4e12, s5e2, s5e6, s6e3) | 6–12 |
| Ensemble-stacking standard (most s3/s4/s5 winners) | 4–9 |
| Single-model heavy-FE | 8–15 |
| Lookup-exploit | 1–4 |
| Problem-fit NN | 2–6 |
| Community-template-tweak | 3–7 |
| Minimal-FE (explicit) | 0–3 |

These ranges reflect what the schema actually measures (diversity not count). Will update the SCHEMA.md once locked.

### Issue 2: Fork-heavy entries undercount their inherited FE

Sergey s3e14's "winning solution" includes 8 forked base notebooks. Each presumably uses target encoding, possibly groupby aggregates, etc. — but Sergey's writeup doesn't document those, and reading 8 base notebooks per entry is impractical at scale.

**Proposed fix:** add one column `uses_forked_base_model_fe_uncatalogued` (boolean) to explicitly flag entries where significant base-model FE exists but wasn't documented in the winner's writeup. Set TRUE when winner cites multiple forked base notebooks without enumerating their FE. Lets us distinguish "winner did minimal FE" from "winner inherited FE but didn't document."

This adds a 53rd boolean technique column.

### Issue 3: Brute-force vs enumeration boundary needs clarification

cdeotte s5e6: enumerates ALL 162 combos, uses ALL. Per my schema, this is NOT `uses_brute_force_combinatorial_search` (no "search and keep best" step).
cdeotte s4e12: searches 145K combos, keeps 170 that move CV. This IS `uses_brute_force_combinatorial_search`.

The boundary is: **search + selection step** is required for `uses_brute_force_combinatorial_search` to be TRUE. Pure enumeration without selection goes in `uses_higher_order_categorical_combos`.

**Proposed schema clarification:** add to the inclusion/exclusion criteria of column 16 (brute force) the explicit "must include model-in-the-loop selection step." Add to column 17 (higher-order combos) the explicit "applies to enumeration without selection."

### Issue 4: Within-fold TE is hard to determine from writeups alone

Most writeups don't explicitly state whether TE is within-fold (leakage-safe) or applied globally. Notebooks reveal this. For writeup-only entries, this column will often be ambiguous.

**Proposed fix:** allow a `null` / `unknown` value alongside TRUE/FALSE for column 2 specifically. Code TRUE only when explicitly stated within-fold; code FALSE only when explicitly stated globally-applied; code `null` when ambiguous. Most cells will be `null` for writeup-only entries.

This may extend to other columns where notebooks are the canonical source.

### Issue 5: "Treating as categorical" — preexisting vs converted

cdeotte s5e6 says "8 features which can each be treated as categorical." Are those features (Soil Type, Crop Type) already categorical (string-typed), or were they numeric and converted? Affects whether `uses_numerics_as_categoricals_then_combos` is TRUE.

For s5e6 my judgment is FALSE (features are already string-typed categoricals from the schema). But this requires checking the dataset schema, which the writeup doesn't always state.

**Proposed fix:** clarify inclusion criteria for column 18 — "originally numeric (int/float) converted to categorical via binning OR direct conversion." Not applicable if features were originally categorical-typed.

### Issue 6: A modest schema gap

Heitor s3e5 used OptimizedRounder for ordinal class cutoffs. This is **post-processing** per my out-of-scope list (correctly excluded). But it's a distinctive technique tied to ordinal regression problems. Worth noting that some interesting techniques in the corpus are out-of-scope for an FE-focused taxonomy. Not a schema fix, but a documentation note: the schema is FE-specific by design and won't capture some distinctive non-FE techniques (OptimizedRounder, target reversal, knowledge distillation, etc.).

## Schema revisions recommended before full pass

Based on the pilot:

1. **Add column 53 `uses_forked_base_model_fe_uncatalogued`** — flag fork-heavy entries.
2. **Clarify columns 2 (within-fold TE)** — allow `null` for ambiguous cases.
3. **Clarify column 16 vs 17 boundary** — brute force requires selection step; pure enumeration goes in higher-order combos.
4. **Clarify column 18** — only applies when numeric originally + converted.
5. **Update expected n_fe_techniques_used ranges per paradigm** (per Issue 1 table above).

**Net schema after revisions: 53 boolean technique columns + 1 source-confidence + 5 admin = 59 columns × 45 rows = 2,655 cells for the full pass.**

## Verdict: proceed with full pass

The schema **works**, with the caveats above. The pilot results match expectations except for cdeotte's lower-than-expected count, which the revised range table resolves. The Stage 1 → Stage 2 delta is small for these three entries but probably underrepresents what we'll see across all 45.

**Recommendation:** apply the 6 schema revisions, then proceed with the full 45-entry pass on a separate pilot-extension session. Estimated effort: 6–10 hours (Stage 1 ~half day, Stage 2 ~1–2 days).

## Open question for next decision

Should the full pass code Stage 1 first across all 45 (then Stage 2 separately), or do Stage 1 + Stage 2 sequentially per entry?

- **Stage 1 batch then Stage 2 batch:** lets us measure the global Stage 1 → Stage 2 delta cleanly. Easier to manage.
- **Stage 1 + Stage 2 per entry:** less context-switching per entry; faster overall. Harder to measure delta cleanly without separate snapshots.

Recommendation: **Stage 1 batch first** so the delta measurement is methodologically clean. Then Stage 2 batch.
