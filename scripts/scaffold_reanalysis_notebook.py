"""Generate scaffold for notebooks/02_reanalysis.ipynb.

Section headers + load/sanity-check cells + minimal placeholder cells per
analysis section. User fills in the substantive analysis cells iteratively.
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

OUT = Path("notebooks/02_reanalysis.ipynb")


def md(src: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}


def code(src: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": src.splitlines(keepends=True),
    }


cells = []

# ============== Title + intro ==============
cells.append(md("""# Phase 5 Re-analysis — Paradigm Characterization on Corrected Data

**Branch:** `phase5/reanalysis` · **Date:** 2026-05-27 · **Supersedes:** `notebooks/01_eda.ipynb`

This notebook re-runs the meta-analysis on the corrected/extended Pass 1 sheet and the new Pass 2 (Paradigm & Attribution) sheet. Unlike `01_eda.ipynb` which was organized around field distributions for the flowchart deliverable, this notebook is organized around **paradigms** (the new unit of analysis) and around the cross-tabs the audit unblocks.

**Data sources:**
- `data/kaggle_meta_analysis.xlsx` — 6 sheets (Competition Data, Codebook, Example (icr), Paradigm & Attribution, Data Quality Audit, Corrections Log)
- `data/raw/<competition>/leaderboard.json` — used to verify `top_3_margin` derivations

**Outputs:**
- Figures to `analysis/figures/phase5/`
- Coupling evidence table (CSV) to `analysis/reanalysis/coupling_evidence.csv`

**Sections:**
1. Setup + data load + sanity checks
2. Distributional refresh (diff vs Phase 3 figures)
3. Paradigm characterization (paradigm × era, n_rows, top_3_margin)
4. Constraint → strategy cross-tabs (external_original, distribution_shift, data-size)
5. Community / attribution (author centrality, cdeotte timeline)
6. Coupling evidence table — N supporting / contradicting / neutral per coupling
"""))

# ============== Section 0: Setup ==============
cells.append(md("""## 0. Setup
"""))

cells.append(code("""import json
from collections import Counter
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# Repo paths (relative to repo root, assuming notebook run from there)
ROOT = Path.cwd() if Path('data').exists() else Path('..')
XLSX = ROOT / 'data' / 'kaggle_meta_analysis.xlsx'
LB_DIR = ROOT / 'data' / 'raw'
FIG_DIR = ROOT / 'analysis' / 'figures' / 'phase5'
OUT_DIR = ROOT / 'analysis' / 'reanalysis'
FIG_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

pd.set_option('display.max_columns', 60)
pd.set_option('display.width', 200)
print(f'ROOT = {ROOT.resolve()}')
print(f'XLSX exists: {XLSX.exists()}')
"""))

cells.append(code("""# ---- Helpers ----
def get_era(ref):
    \"\"\"Derive era label from competition_ref.\"\"\"
    if pd.isna(ref):
        return 'unknown'
    if ref.startswith('tabular-playground-series'):
        return 'TPS'
    if ref == 'icr-identify-age-related-conditions':
        return 'Featured'
    for s in ('s3', 's4', 's5', 's6'):
        if f'playground-series-{s}' in ref:
            return s.upper()
    return 'unknown'

def split_semicolons(val):
    \"\"\"Split a semicolon-separated string into a clean list (preserves order).\"\"\"
    if pd.isna(val) or not str(val).strip():
        return []
    return [s.strip() for s in str(val).split(';') if s.strip()]
"""))

# ============== Data load ==============
cells.append(md("""### Load Pass 1, Pass 2, Corrections Log
"""))

cells.append(code("""# Pass 1: Competition Data (40 columns post-correction)
pass1 = pd.read_excel(XLSX, sheet_name='Competition Data')
pass1['era'] = pass1['competition_ref'].apply(get_era)
print(f'Pass 1: {pass1.shape}')
print('Columns:', list(pass1.columns))
"""))

cells.append(code("""# Pass 2: Paradigm & Attribution (18 columns)
pass2 = pd.read_excel(XLSX, sheet_name='Paradigm & Attribution')
print(f'Pass 2: {pass2.shape}')
print('Columns:', list(pass2.columns))
"""))

cells.append(code("""# Corrections Log (for reference; not for joining)
corrections = pd.read_excel(XLSX, sheet_name='Corrections Log')
print(f'Corrections Log: {corrections.shape}')
print('By severity:')
print(corrections['severity'].value_counts())
"""))

cells.append(code("""# Join Pass 1 + Pass 2 on (competition_ref, finish_rank)
merged = pass1.merge(
    pass2,
    on=['competition_ref', 'finish_rank'],
    how='outer',
    suffixes=('_p1', '_p2'),
    indicator=True,
)
print(f'Merged: {merged.shape}')
print('Merge indicator:')
print(merged['_merge'].value_counts())
assert (merged['_merge'] == 'both').all(), 'Pass 1 and Pass 2 should have identical (comp_ref, rank) keys'
merged = merged.drop(columns=['_merge'])
"""))

# ============== Sanity checks ==============
cells.append(md("""### Sanity checks
"""))

cells.append(code("""# Expected: 45 rows, all paradigms present, all eras present
print(f'Rows: {len(merged)} (expect 45)')
print(f'Eras: {merged[\"era\"].value_counts().to_dict()}')
print(f'Paradigms: {merged[\"paradigm\"].value_counts().to_dict()}')
print(f'\\ntop_3_margin range: {merged[\"top_3_margin\"].min()} - {merged[\"top_3_margin\"].max()}')
print(f'distribution_shift_type: {merged[\"distribution_shift_type\"].value_counts().to_dict()}')
print(f'external_original_available: {merged[\"external_original_available\"].value_counts().to_dict()}')
"""))

cells.append(code("""# Verify top_3_margin against leaderboard.json directly (spot-check 5 entries)
def lb_margin(comp_ref):
    lb = LB_DIR / comp_ref / 'leaderboard.json'
    if not lb.exists():
        return None
    data = json.load(open(lb))
    if len(data) < 3:
        return None
    return round(abs(float(data[0]['score']) - float(data[2]['score'])), 6)

sample = merged.sample(5, random_state=42)[['competition_ref', 'finish_rank', 'top_3_margin']]
sample['recomputed'] = sample['competition_ref'].apply(lb_margin)
sample['ok'] = (sample['top_3_margin'] - sample['recomputed']).abs() < 1e-5
print(sample.to_string(index=False))
"""))

# ============== Section 1: Distributional Refresh ==============
cells.append(md("""## 1. Distributional Refresh (vs Phase 3 EDA)

Goal: identify which Section 4 figures shift post-corrections so we know what to regenerate.

**Fields most affected by corrections:**
- `models_used` (6 entries had undercounts expanded: s5e11, s5e8, s5e10, s5e12, s4e7, s5e7)
- `n_rows` (s5e2: 300K → 4M)
- `original_data_usage` → split into `external_original_available` + `external_original_use_mode`
- `missing_data_strategy` (s4e11 corrected)
- `dominant_base_model` (s6e3 corrected)
"""))

cells.append(code("""# TODO: regenerate the Phase 3 distributional figures here using corrected data
# Compare to outputs of notebooks/01_eda.ipynb for diffing
# Suggested figures to refresh:
#   - models_used family count distribution
#   - n_rows distribution (log-scale histogram or violin)
#   - dominant_base_model breakdown
#   - ensemble_method breakdown
#   - missing_data_strategy breakdown

# Quick first look:
print('dominant_base_model distribution (post-correction):')
print(pass1['dominant_base_model'].value_counts())
print('\\nensemble_method distribution:')
print(pass1['ensemble_method'].value_counts())
"""))

# ============== Section 2: Paradigm Characterization ==============
cells.append(md("""## 2. Paradigm Characterization

Headline finding: what does \"winning\" look like across paradigms?

**Paradigm × constraint cross-tabs to build:**
- Paradigm × era (stacked bar)
- Paradigm × n_rows (scatter or binned bar)
- Paradigm × top_3_margin (violin or boxplot per paradigm)
- Paradigm × origination_score (heatmap)
"""))

cells.append(code("""# Paradigm distribution
print('Paradigm counts:')
print(merged['paradigm'].value_counts())
print(f'\\nTotal: {len(merged)}')
"""))

cells.append(code("""# Paradigm × era cross-tab
xt_paradigm_era = pd.crosstab(merged['paradigm'], merged['era'])
xt_paradigm_era = xt_paradigm_era.reindex(columns=['TPS', 'S3', 'S4', 'S5', 'S6', 'Featured'], fill_value=0)
print(xt_paradigm_era)
# TODO: stacked bar plot
"""))

cells.append(code("""# Paradigm × top_3_margin
print(merged.groupby('paradigm')['top_3_margin'].describe())
# TODO: violin/boxplot grouped by paradigm
"""))

cells.append(code("""# Paradigm × n_rows (log-scale relevant)
print(merged.groupby('paradigm')['n_rows'].describe())
# TODO: scatter plot of n_rows (log scale) colored by paradigm
"""))

# ============== Section 3: Constraint Cross-Tabs ==============
cells.append(md("""## 3. Constraint → Strategy Cross-Tabs

Test specific couplings the re-eval flagged as N≥2 promotable:

| Cross-tab | Tests coupling |
|---|---|
| `external_original_available` × `paradigm` | Does lookup-exploit require external original? |
| `external_original_use_mode` × `paradigm` | Is "columns-only" mainly a cdeotte/single-model-FE pattern? |
| `distribution_shift_type` × `cv_strategy` | Custom-CV-when-shifted coupling |
| `n_rows` (binned) × `paradigm` | cdeotte's "small data → no FE / single model" rule |
| `top_3_margin` (binned: photo-finish vs not) × `paradigm` | Photo-finish → ensemble-stacking? |
"""))

cells.append(code("""# external_original × paradigm
xt = pd.crosstab(merged['external_original_use_mode'], merged['paradigm'])
print(xt)
"""))

cells.append(code("""# distribution_shift_type × cv_strategy (for the 5 TRUE entries)
shifted = merged[merged['distribution_shift_type'].isin(['temporal', 'covariate', 'label-noise'])]
print(shifted[['competition_ref', 'distribution_shift_type', 'cv_strategy', 'paradigm']].to_string(index=False))
"""))

cells.append(code("""# n_rows binned × paradigm (cdeotte's small-data rule)
bins = [0, 5_000, 50_000, 500_000, 5_000_000, 20_000_000]
labels = ['<5K', '5K-50K', '50K-500K', '500K-5M', '5M+']
merged['n_rows_bin'] = pd.cut(merged['n_rows'], bins=bins, labels=labels)
xt = pd.crosstab(merged['n_rows_bin'], merged['paradigm'], observed=False)
print(xt)
"""))

cells.append(code("""# top_3_margin classified as photo-finish (<0.0005) or not
merged['photo_finish'] = merged['top_3_margin'] < 0.0005
print('Photo-finish entries (top_3_margin < 0.0005):')
print(f'  count: {merged[\"photo_finish\"].sum()} / {len(merged)}')
print()
print(pd.crosstab(merged['photo_finish'], merged['paradigm']))
"""))

# ============== Section 4: Community / attribution ==============
cells.append(md("""## 4. Community / Attribution

- Author centrality (appearance count, cross-referencing)
- cdeotte timeline (pre-dominance Feb 2023 → first win Dec 2024 → dominant from there)
- Cross-author citation graph (degree distribution per recurring contributor)
- `available-not-used` cases (cdeotte s3e5, adaubas s4e5 — CV-driven decisions)
"""))

cells.append(code("""# Author appearance counts (from Pass 2 author_appearance_count)
# Note: same author may appear in multiple rows (mahog wins s5e11, s6e1, s5e8 rank2)
authors = merged[['author', 'author_appearance_count']].drop_duplicates(subset=['author'])
print('Top authors by appearance count (Pass 2):')
print(authors.sort_values('author_appearance_count', ascending=False).head(15).to_string(index=False))
"""))

cells.append(code("""# Cited-community-members flattened — count citations per handle
all_citations = []
for cited in merged['cited_community_members'].fillna(''):
    for handle in split_semicolons(cited):
        all_citations.append(handle.lower())
top_cited = Counter(all_citations).most_common(20)
print('Top cited community members (across all writeups):')
for handle, n in top_cited:
    print(f'  {handle:40s} {n}')
"""))

cells.append(code("""# 'Available but not used' counter-pattern — both should be CV-driven decisions
not_used = merged[merged['external_original_use_mode'] == 'available-not-used']
print('available-not-used entries:')
print(not_used[['competition_ref', 'finish_rank', 'author', 'paradigm', 'winner_unique_edge']].to_string(index=False))
"""))

# ============== Section 5: Coupling Evidence Table ==============
cells.append(md("""## 5. Coupling Evidence Table

For each of the 6 promoted couplings in `analysis/writeup-reevaluation/INDEX.md`, derive:
- N supporting (cases that fit the coupling)
- N contradicting (cases that violate it)
- N neutral (not testable in this case)

Output: single CSV `analysis/reanalysis/coupling_evidence.csv` for use in Discussion §5.1.

**Promoted couplings to score:**
1. Photo-finish → validation-discipline (anti-greedy submission selection)
2. Heavy public-notebook + author with framework → KGMON-style fork-heavy win
3. Linear stacker dominance (Ridge / mean / LR)
4. Available original → "use as columns" (or "use as features-derived") pattern
5. Small data (<50K rows) → no FE / single-model
6. Distribution shift → custom CV strategy
"""))

cells.append(code("""# Skeleton: build evidence rows incrementally
evidence_rows = []

# --- Coupling 1: Photo-finish → validation-discipline ---
# Supporting: top_3_margin < 0.0005 AND Pass 2 winner_unique_edge mentions anti-greedy/CV-trust
# Contradicting: top_3_margin < 0.0005 AND no validation-discipline framing
# TODO: implement check on winner_unique_edge text

# --- Coupling 2: Heavy citations + author has framework ---
# Supporting: n_cited_members >= 5 AND author_recurring_in_set
# TODO

# --- Coupling 3: Linear stacker dominance ---
# Supporting: uses_canonized_technique contains Ridge-as-stacker / LAD-as-stacker
# OR ensemble_method == mean_blend / weighted_blend
# TODO

# --- Couplings 4-6: TODO ---

# evidence_df = pd.DataFrame(evidence_rows)
# evidence_df.to_csv(OUT_DIR / 'coupling_evidence.csv', index=False)
# print(evidence_df.to_string(index=False))
print('Skeleton — fill in per-coupling checks')
"""))

# ============== End ==============
cells.append(md("""## End of scaffold

**Next steps to fill in:**
1. Section 1: regenerate Phase 3 figures, save side-by-side comparison
2. Section 2: plot paradigm × era stacked bar, paradigm × top_3_margin boxplot
3. Section 3: same cross-tabs but with figures
4. Section 4: cdeotte-mention timeline figure, citation-graph degree plot
5. Section 5: implement each coupling-check, write CSV

Once filled, the outputs feed:
- `research_report.md` §4 (revised Results) — figures from §§2-4
- `research_report.md` §5 (new Discussion) — coupling evidence table from §5
"""))

# ============== Build notebook ==============
notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.13"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

OUT.parent.mkdir(parents=True, exist_ok=True)
with open(OUT, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

md_count = sum(1 for c in cells if c["cell_type"] == "markdown")
code_count = sum(1 for c in cells if c["cell_type"] == "code")
print(f'OK: wrote {OUT} ({len(cells)} cells)')
print(f'  Markdown cells: {md_count}')
print(f'  Code cells:     {code_count}')
