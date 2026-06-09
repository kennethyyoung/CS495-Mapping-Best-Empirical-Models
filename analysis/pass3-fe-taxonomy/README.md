# Pass 3 — Feature-Engineering Taxonomy: data files

Guide to the data files in this directory. The prose write-ups (`SCHEMA.md`,
`AUDIT.md`, `STAGE1_*.md`, `STAGE2_*.md`, `PILOT.md`, `ROBUSTNESS_CHECKS.md`)
document the taxonomy and the coding process; this note covers the CSVs and how
to use them safely.

## Canonical data — use these

| File | What it is |
|---|---|
| `stage1_data.csv` | **Live winners coding** (45 entries), post-repair and post-adjudication. The current source of truth for winners. |
| `controls_data.csv` | **Live controls coding** (11 near-winning controls), post-repair. |
| `stage1_data_preadjudication.csv` | Clean **pre-adjudication** snapshot of the winners coding, materialized from git commit `6bd2092`. **Reliability is computed from this file** (adjudication moves primary→blind, so agreement against the live file would be circular). |
| `stage2_aggregates.csv` | Group-level (Group A–K) aggregates derived from the above. |
| `blind_recode_sheet.csv`, `blind_v2.csv` | The 12-entry blind intra-rater re-code used for the reliability check. |

`stats.py` reproduces the reliability figures (Cohen's κ, Gwet's AC1, positive
agreement) from `stage1_data_preadjudication.csv`. `validate_pass3.py` gates the
structural integrity of the live CSVs.

## ⚠️ The `.bak` files are the corrupt pre-repair source — do NOT use for analysis

`stage1_data.csv.bak` and `controls_data.csv.bak` are the **pre-repair backups**
that still contain the structural corruption fixed on 2026-06-02 (column-shifted
rows; e.g. s3e8). They are kept only as the **input of record** to the one-shot
rebuild scripts (`_rebuild_winners.py`, `_rebuild_controls.py`,
`_make_blind_sample.py`, `_winners_worktable.py`), which read the
position-intact booleans from them to reconstruct the clean live CSVs above.

Never compute statistics, reliability, or aggregates from a `.bak` file, and
never "restore" a live CSV from one. For analysis use `stage1_data.csv` /
`controls_data.csv`; for reliability use `stage1_data_preadjudication.csv`.
