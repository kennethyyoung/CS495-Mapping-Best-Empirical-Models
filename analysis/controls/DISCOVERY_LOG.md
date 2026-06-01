# Phase 1 Pilot — Discovery Log

**Pilot status:** Discovery complete (5/5 target).
**Started:** 2026-06-01.

## Discovery results

| # | Competition | Control rank | Author | Content type | Local files | Winner (coded) | Winner's paradigm | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | playground-series-s6e4 | 19 | ? | ? | ? | kirill0212 r1 | community-template | |
| 2 | playground-series-s6e3 | 16 | ? | ? | ? | cdeotte r1 | heavyweight | |
| 3 | playground-series-s6e2 | 15 | ? | 2 notebooks | ? | masaya r1 | heavyweight | High data quality (2 NBs) |
| 4 | playground-series-s5e10 | 14 | ? | ? | ? | Tilii r1 | heavyweight | |
| 5 | playground-series-s5e8 | 15 | ? | ? | ? | mahog r2 | ensemble-standard | |

(Author handle / content type / filenames to be filled in as we process each entry.)

## Paradigm coverage

- **Heavyweight:** 3 controls (s5e10, s6e2, s6e3) — directly tests the audit-flagged heavyweight finding
- **Community-template:** 1 control (s6e4)
- **Ensemble-standard:** 1 control (s5e8)
- **Single-model-heavy / lookup / problem-fit / minimal:** 0 controls (pilot didn't target these)

## Era coverage

- **s5 era (2025):** 2 controls (s5e8, s5e10)
- **s6 era (2026):** 3 controls (s6e2, s6e3, s6e4)
- **s3/s4 era:** 0 controls

This concentration is fine for the pilot — it matches where heavyweight as a paradigm is observed in our corpus. Phase 2 would need to broaden to s3/s4 if we want era-stable claims.

## Rank distribution

- Ranks: 14, 15, 15, 16, 19. Median 15.
- All five are clearly outside top 3. **True non-winning controls.**
- Median rank 15 satisfies the "≥8" pilot success criterion.

## Next steps for Phase 1

1. Save each control's content to `data/writeups/<slug>/control_<author>_rank<N>.{txt,ipynb}`
2. Code Pass 3 booleans for each (writes to `analysis/pass3-fe-taxonomy/controls_data.csv`)
3. Write `analysis/controls/PILOT_RESULTS.md` decision memo
4. Decide: scale to Phase 2 (target 25-30 controls) OR finalize comparison from pilot data alone

## Time tracking

| Step | Estimated | Actual |
|---|---|---|
| Discovery | 5 hr | (TBD) |
| Save content locally | 1 hr | (TBD) |
| Pass 3 coding × 5 entries | 3.5 hr | (TBD) |
| Decision memo | 1 hr | (TBD) |
| **Total** | 10.5 hr | (TBD) |
