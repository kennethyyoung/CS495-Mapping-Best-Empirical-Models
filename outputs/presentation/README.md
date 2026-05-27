# Presentation deck — Overleaf upload instructions

## Files

- `slides.tex` — main Beamer source (Metropolis theme)
- `README.md` — this file
- Figures are referenced **by filename** (no subdirectory) so they must sit alongside `slides.tex` in the Overleaf project root.

## Steps to upload

1. Create a new blank project on Overleaf (https://www.overleaf.com).
2. Delete the auto-generated `main.tex` if Overleaf creates one.
3. Upload `slides.tex`.
4. Upload the following **11 PNG figures** from `analysis/figures/phase5/` to the **project root** (same level as `slides.tex`):

   Main deck figures:
   - `phase5_21_paradigm_distribution.png` — slide 10 (four paradigms)
   - `phase5_22_paradigm_by_era.png` — slide 14 (paradigm by era)
   - `phase5_41_author_centrality.png` — slide 16 (community centrality)
   - `phase5_51_coupling_evidence.png` — slide 12 (coupling evidence)
   - `phase5_61_fe_tag_frequency.png` — slide 6 (pivot, FE tag histogram)
   - `phase5_62_model_family.png` — slide 6 (pivot, model family bar)
   - `phase5_63_origination_score.png` — slide 11 (how winners build)
   - `phase5_64_use_mode_breakdown.png` — slide 13 (use-as-columns correction)

   Appendix figures:
   - `phase5_23_paradigm_photofinish.png` — appendix
   - `phase5_24_paradigm_n_rows.png` — appendix
   - `phase5_31_use_mode_paradigm.png` — appendix

5. In Overleaf's compiler menu, set the compiler to **XeLaTeX** or **LuaLaTeX**. The Metropolis theme requires one of these (not pdfLaTeX) for proper font rendering.

6. Click **Recompile**. First compile takes 20–60 seconds because Metropolis pulls fonts.

## Speaker notes

Each slide has a `\note{...}` block containing the verbal narration. To rehearse with notes visible:

- Uncomment `\setbeameroption{show notes on second screen=right}` in the preamble for a dual-monitor rehearsal view.
- Or uncomment `\setbeameroption{show only notes}` to produce a notes-only PDF for printing.

For the actual presentation, leave both lines commented (default) — notes won't appear on the projected slides.

## Slide count + timing

- **Main deck:** 15 content slides + 1 title + 1 thank-you = 17 slides
- **Appendix:** 4 slides (coupling table, n_rows scatter, photo-finish bar, use-mode heatmap)
- **Target talk length:** 5–7 minutes
- **Pacing:** roughly 22–28 seconds per content slide, faster for section dividers

## Slide order (current version)

1. Title
2. What is Kaggle?
3. The research arc (original FE question → pivot to typology)
4. What's been done — and what hasn't (related work + gap)
5. Data: 45 winning solutions (with manual-reading caveat)
6. **From flowchart to typology: a pivot** (explains why we did Pass 2)
7. Two-pass coding design
8. Double-checking our own work (audit + corrections)
9. Limitations
10. Four winning paradigms
11. **How winners actually build solutions** (67% inheritance, 0% pure forks)
12. Coupling evidence (the headline)
13. **The "use as columns" correction**
14. Paradigm composition by era
15. **What each winner uniquely did (examples)**
16. Who wins vs. who's cited (community centrality + cdeotte timeline merged)
17. **What this work contributes** (closer)
18. Thank you / Questions?

**Bold** = new slides added in this revision (vs. the original draft).

## Customization notes

- Title block (author, institution, date) is in the preamble of `slides.tex`.
- Color accents (`kc-accent` gold, `kc-muted` gray) are defined in the preamble — adjust hex codes there if a different palette is preferred.
- All 8 figures use 88–95% of textwidth, leaving room for captions. If you swap in a wider/taller figure, adjust the `width=` argument on the corresponding `\includegraphics`.

## Known issues

- Metropolis on Overleaf occasionally complains about missing Fira Sans / Fira Mono fonts on the first compile. The compile usually still succeeds and the warning can be ignored. If it fails outright, add `\usepackage{fontspec}` and explicitly load the bundled fonts.
- The appendix section uses `\appendix` from the `appendixnumberbeamer` package, which resets the frame counter so the main deck's frame numbers don't include the appendix slides. Remove the package if undesired.
