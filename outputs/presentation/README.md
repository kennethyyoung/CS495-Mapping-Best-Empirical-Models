# Presentation deck — Overleaf upload instructions

## Files

- `slides.tex` — main Beamer source (Metropolis theme)
- `README.md` — this file
- Figures are referenced **by filename** (no subdirectory) so they must sit alongside `slides.tex` in the Overleaf project root.

## Steps to upload

1. Create a new blank project on Overleaf (https://www.overleaf.com).
2. Delete the auto-generated `main.tex` if Overleaf creates one.
3. Upload `slides.tex`.
4. Upload the following 7 PNG figures from `analysis/figures/phase5/` to the **project root** (same level as `slides.tex`):

   - `phase5_21_paradigm_distribution.png`
   - `phase5_22_paradigm_by_era.png`
   - `phase5_23_paradigm_photofinish.png`
   - `phase5_24_paradigm_n_rows.png`
   - `phase5_31_use_mode_paradigm.png`
   - `phase5_41_author_centrality.png`
   - `phase5_42_cdeotte_timeline.png`
   - `phase5_51_coupling_evidence.png`

   That's 8 PNGs total (counted again — 8 figure references in slides.tex).

5. In Overleaf's compiler menu, set the compiler to **XeLaTeX** or **LuaLaTeX**. The Metropolis theme requires one of these (not pdfLaTeX) for proper font rendering.

6. Click **Recompile**. First compile takes 20–60 seconds because Metropolis pulls fonts.

## Speaker notes

Each slide has a `\note{...}` block containing the verbal narration. To rehearse with notes visible:

- Uncomment `\setbeameroption{show notes on second screen=right}` in the preamble for a dual-monitor rehearsal view.
- Or uncomment `\setbeameroption{show only notes}` to produce a notes-only PDF for printing.

For the actual presentation, leave both lines commented (default) — notes won't appear on the projected slides.

## Slide count + timing

- **Main deck:** 14 content slides + 1 title + 1 thank-you = 16 slides
- **Appendix:** 4 slides (coupling table, n_rows scatter, photo-finish bar, use-mode heatmap)
- **Target talk length:** 5–7 minutes
- **Pacing:** roughly 25–30 seconds per content slide, faster for section dividers

## Customization notes

- Title block (author, institution, date) is in the preamble of `slides.tex`.
- Color accents (`kc-accent` gold, `kc-muted` gray) are defined in the preamble — adjust hex codes there if a different palette is preferred.
- All 8 figures use 88–95% of textwidth, leaving room for captions. If you swap in a wider/taller figure, adjust the `width=` argument on the corresponding `\includegraphics`.

## Known issues

- Metropolis on Overleaf occasionally complains about missing Fira Sans / Fira Mono fonts on the first compile. The compile usually still succeeds and the warning can be ignored. If it fails outright, add `\usepackage{fontspec}` and explicitly load the bundled fonts.
- The appendix section uses `\appendix` from the `appendixnumberbeamer` package, which resets the frame counter so the main deck's frame numbers don't include the appendix slides. Remove the package if undesired.
