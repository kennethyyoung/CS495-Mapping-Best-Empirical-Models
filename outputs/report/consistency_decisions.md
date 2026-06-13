# Doc-wide Consistency Decisions — research_report_v2.md

Decisions made during the prose/mechanics walkthrough (2026-06-12) that apply across the
whole document, recorded so each is made once rather than re-litigated per section.

## 1. constraint-to-strategy compound → spelled-out, hyphenated (DECIDED — REVISED 2026-06-12)
Use `constraint-to-strategy` (e.g. "constraint-to-strategy patterns/couplings") as the
compound modifier in prose. This REVERSES the initial en-dash call: the spelled-out form is
the dominant existing usage (was 4 vs 2) and is directionally accurate for the tested
"when constraint X holds, winners do Y" patterns. The 2 en-dash instances (lines 49, 56)
were converted to constraint-to-strategy. The arrow form `→` is still allowed only in
tables/code/quoted coupling labels (see Decision 2), never in prose.
Status: standardized doc-wide.

## 2. Arrows `→` — keep as notation only (DECIDED)
`→` is allowed ONLY in tables, code spans, and quoted coupling labels (e.g. coupling-table
cells, `` `TargetEncoder` → `target_encoding` ``, `"small data → no-FE single model"`),
where it denotes a directional constraint→strategy coupling. It must NOT appear in running
prose (the one prose instance, line 49, was converted to the en-dash noun).

## 3. `non-` prefix → closed, per APA 7th (LEANING; confirm rollout)
Close `non-` prefixes: nonwinners, nonwinner, nonwinning, nonmonetized, nonrandom,
nonparadoxical, nonsignificant.
EXCEPTIONS (keep hyphen): before a capital/numeral/abbreviation (none currently, e.g. `no-FE`
is unaffected), and `non-writeup` (closed form "nonwriteup" reads awkwardly).
Status: nonsignificant done (1.4); remaining ~14 instances closed doc-wide 2026-06-12.

## 4. Section cross-references → spelled out (DECIDED)
Write "Section X" / "Sections X–Y" in text, not the `§`/`§§` symbol (APA spells "Section";
matches usage everywhere else in the doc). The lone `§§4.1–4.9` was fixed in 1.6.

## 5. Comparison-group terminology → near-winner(s) (DECIDED)
Always call the rank 4–25 comparison group "near-winners" / "near-winning controls" (the
latter especially in figures). Do NOT use "(strong) nonwinners". "strong" dropped because
near-winners already implies strength. Applied doc-wide 2026-06-12 (8 instances).

## 7. APA stat-symbol italics — pending dedicated sweep
Italicize Latin stat symbols (*n*, *N*, *p*, *M*, *SD*, *t*, *F*, *df*); Greek (κ) stays roman.
~34 `n = ` instances doc-wide, of which 9 are INSIDE code spans/backticks (must NOT be
italicized). Done so far inline: 1.4 (*n* = 11), 3.2 line 98 (6 cohort *n*). Remaining prose
instances to be done in a final careful sweep that skips code spans and verifies table rendering.
Also: "winner corpus" (not "winners corpus") standardized doc-wide; "rank 4–25" open (not hyphenated).

## 11. Number style — APA (DECIDED 2026-06-12)
Statistical values use NUMERALS even below 10 (medians, means, n, percentages, ratios,
sample sizes): e.g. "a median of 4". General narrative counts below 10 stay SPELLED OUT
("four winning paradigms", "three entries"). Ordinals below 10 spelled ("first-place");
ordinals 10+ numeral ("23rd", "806th"). Fixed: "median of four" → "median of 4" (abstract +
Contributions); 1st/2nd/3rd → first/second/third.

## 10. Bold usage — structural + topic-anchors kept (DECIDED 2026-06-12)
KEEP bold for: headings/run-in headings, list labels (paradigm names, etc.), table captions,
the group-level reporting rule (3.6), and INLINE CONCEPT-NAMES that open a discussion paragraph
in Results (e.g. **Linear-stacker dominance**, coupling/finding topic-anchors). REMOVE bold used
as bare inline emphasis (e.g. former **Pass 3**, **both**/**and**, **highest-placing**).
Refinement (Results): KEEP bold key-finding STATEMENTS that anchor a point (e.g. **Target
encoding is the single most common technique**); DE-BOLD emphasized NUMBERS in prose (e.g.
**4**/**1** medians — redundant with tables). Table-cell highlight bold stays.

## 8. winner–control (en-dash) is the standard for the comparison (DECIDED)
Use `winner–control` (en-dash) for the comparison/pairs, not `winner-versus-control`.
Dominant form (9 vs 2); the 2 versus-forms were converted 2026-06-12.

## 9. APA prefix closure — extended to ALL prefixes (DECIDED 2026-06-12)
Full APA closure, not just non-. Closed doc-wide: intercoder, interrater, intrarater,
multipass, multitable, multivalue, preadjudication, prebuilt, reevaluation, reread,
recode/recoded, recoding, subgroup, cowinners. EXCEPTIONS kept hyphenated: before a
capital/numeral/abbreviation (e.g. `no-FE`, none currently broken), base word already
hyphenated, and `non-writeup` (awkward closed). Compound MODIFIERS (feature-engineering,
field-level, gradient-boosted, etc.) are NOT prefixes — leave hyphenated.
Closed so far also: overcorrect, oversamples, overrepresent, miscoded, postprocessing,
midfield, autopopulated. KEPT-HYPHENATED EXCEPTIONS (readability/established): the entire
`meta-` family (meta-analysis, meta-dataset, meta-blending, meta-research, meta-indicator(s),
meta-learner, meta-architecture), `non-writeup`, `out-engineered`/`out-of-fold` (phrasal/nonce).
Note `meta-indicators` standardized (was once open "meta indicators").

## 6. -ly adverb + adjective → never hyphenated (DECIDED)
APA/Chicago rule. Fixed doc-wide: widely adopted, sufficiently documented, jointly absent,
mostly original, differently composed. NOTE false positive to keep: "family-level" ("family"
is a noun, not an -ly adverb). User wants hyphenation/en-dash issues flagged AGGRESSIVELY
going forward — scan each section for compound-modifier hyphenation and en-dash correctness.
