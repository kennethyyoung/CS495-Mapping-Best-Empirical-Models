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

Five views of paradigm structure across the 45-entry set:
- 2.1 Paradigm distribution (headline figure)
- 2.2 Paradigm × era (stacked bar) — are paradigms era-stable or era-shifting?
- 2.3 Paradigm × photo-finish — does photo-finish coupling hold?
- 2.4 Paradigm × n_rows (log scale) — does single-model-FE require large data?
- 2.5 Paradigm × origination_score — do some paradigms inherit more than others?

**Note on top_3_margin:** raw margin is metric-confounded (AUC ~0.0001 vs RMSE ~2335). We use the `photo_finish` boolean (margin < 0.0005) for AUC/Accuracy/MAP@K entries and a normalized per-metric photo-finish flag elsewhere.
"""))

cells.append(code("""# ----- Shared style + paradigm color map -----
PARADIGM_ORDER = ['ensemble-stacking', 'single-model-FE', 'lookup-exploit',
                  'problem-fit-NN', 'community-template-tweak', 'mixed']
PARADIGM_COLORS = {
    'ensemble-stacking':         '#1f77b4',  # blue (dominant)
    'single-model-FE':           '#ff7f0e',  # orange (cdeotte-flavored)
    'lookup-exploit':            '#d62728',  # red (exploit family)
    'problem-fit-NN':            '#2ca02c',  # green (NN clusters)
    'community-template-tweak':  '#9467bd',  # purple (high-inheritance)
    'mixed':                     '#7f7f7f',  # grey
}
ERA_ORDER = ['TPS', 'S3', 'S4', 'S5', 'S6', 'Featured']

plt.rcParams.update({'figure.dpi': 110, 'savefig.dpi': 150,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'font.size': 10})
"""))

cells.append(md("""### 2.1 Paradigm distribution"""))

cells.append(code("""# Horizontal bar of paradigm counts
counts = merged['paradigm'].value_counts().reindex(PARADIGM_ORDER, fill_value=0)
fig, ax = plt.subplots(figsize=(8, 3.5))
colors = [PARADIGM_COLORS[p] for p in counts.index]
ax.barh(range(len(counts)), counts.values, color=colors, edgecolor='white')
ax.set_yticks(range(len(counts)))
ax.set_yticklabels(counts.index)
ax.invert_yaxis()
ax.set_xlabel('Number of winning entries (n=45)')
ax.set_title('Paradigm distribution across winners')
for i, v in enumerate(counts.values):
    pct = v / len(merged) * 100
    ax.text(v + 0.3, i, f'{v} ({pct:.0f}%)', va='center', fontsize=9)
ax.set_xlim(0, counts.max() * 1.18)
plt.tight_layout()
plt.savefig(FIG_DIR / 'phase5_21_paradigm_distribution.png', bbox_inches='tight')
plt.show()
print('Headline: ensemble-stacking is 62% of wins; lookup-exploit + problem-fit-NN are tail paradigms but not negligible (16% combined).')
"""))

cells.append(md("""### 2.2 Paradigm × era (stacked bar)"""))

cells.append(code("""# Stacked bar: era on x, paradigm composition stacked
xt = pd.crosstab(merged['era'], merged['paradigm'])
xt = xt.reindex(index=ERA_ORDER, columns=PARADIGM_ORDER, fill_value=0)

fig, ax = plt.subplots(figsize=(9, 4))
bottom = np.zeros(len(xt))
for paradigm in PARADIGM_ORDER:
    vals = xt[paradigm].values
    ax.bar(xt.index, vals, bottom=bottom, label=paradigm,
           color=PARADIGM_COLORS[paradigm], edgecolor='white', linewidth=0.5)
    bottom += vals
ax.set_ylabel('Winning entries')
ax.set_xlabel('Era')
ax.set_title('Paradigm composition by era')
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1.0), frameon=False, fontsize=9)
# annotate totals
totals = xt.sum(axis=1).values
for i, t in enumerate(totals):
    ax.text(i, t + 0.2, f'n={t}', ha='center', fontsize=9, color='dimgray')
ax.set_ylim(0, totals.max() * 1.18)
plt.tight_layout()
plt.savefig(FIG_DIR / 'phase5_22_paradigm_by_era.png', bbox_inches='tight')
plt.show()
print('Counts:')
print(xt)
print('\\nObservation: problem-fit-NN concentrates in TPS+Featured era (pre-2024). lookup-exploit')
print('appears in every era except S4 and Featured. ensemble-stacking dominates every era.')
"""))

cells.append(md("""### 2.3 Paradigm × photo-finish

We define photo-finish as top_3_margin < 0.0005 for AUC/Accuracy/probability-based metrics, and use a metric-relative threshold for RMSE/MSE/MAE/RMSLE entries (margin < 0.1% of 1st-place score).
"""))

cells.append(code("""# Metric-aware photo-finish flag
def is_photo_finish(row):
    metric = str(row.get('metric', '')).lower()
    margin = row['top_3_margin']
    if pd.isna(margin):
        return None
    # AUC, accuracy, probability-based metrics: absolute threshold
    if any(k in metric for k in ['auc', 'accuracy', 'map', 'log loss', 'kappa', 'matthews', 'multiclass loss']):
        return margin < 0.0005
    # Regression metrics (RMSE/MSE/MAE/RMSLE): relative threshold
    # Need 1st-place score for relative comparison
    lb_path = LB_DIR / row['competition_ref'] / 'leaderboard.json'
    if lb_path.exists():
        data = json.load(open(lb_path))
        if data:
            s1 = abs(float(data[0]['score'])) or 1.0
            return margin / s1 < 0.001  # 0.1% of 1st score
    return None

merged['photo_finish_aware'] = merged.apply(is_photo_finish, axis=1)
print('Photo-finish (metric-aware): {}/{} entries'.format(
    int(merged['photo_finish_aware'].sum()), merged['photo_finish_aware'].notna().sum()))
"""))

cells.append(code("""# Photo-finish rate per paradigm
photo_xt = pd.crosstab(merged['paradigm'], merged['photo_finish_aware'])
photo_xt = photo_xt.reindex(index=PARADIGM_ORDER, fill_value=0)
if True not in photo_xt.columns: photo_xt[True] = 0
if False not in photo_xt.columns: photo_xt[False] = 0
photo_xt['total'] = photo_xt[True] + photo_xt[False]
photo_xt['photo_finish_rate'] = (photo_xt[True] / photo_xt['total']).fillna(0)
photo_xt = photo_xt.sort_values('photo_finish_rate', ascending=False)
print(photo_xt[[True, False, 'total', 'photo_finish_rate']].rename(
    columns={True: 'photo_finish', False: 'wider'}))

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.barh(range(len(photo_xt)), photo_xt['photo_finish_rate'] * 100,
        color=[PARADIGM_COLORS[p] for p in photo_xt.index], edgecolor='white')
ax.set_yticks(range(len(photo_xt)))
ax.set_yticklabels(photo_xt.index)
ax.invert_yaxis()
ax.set_xlabel('% of paradigm wins that are photo-finish (margin < 0.0005 or <0.1% relative)')
ax.set_title('Photo-finish rate by paradigm')
for i, (rate, total) in enumerate(zip(photo_xt['photo_finish_rate'], photo_xt['total'])):
    ax.text(rate * 100 + 1, i, f'{int(rate * total)}/{int(total)}', va='center', fontsize=9)
ax.set_xlim(0, 100)
plt.tight_layout()
plt.savefig(FIG_DIR / 'phase5_23_paradigm_photofinish.png', bbox_inches='tight')
plt.show()
"""))

cells.append(md("""### 2.4 Paradigm × n_rows (log scale strip plot)"""))

cells.append(code("""# Strip plot: n_rows on log x-axis, y = paradigm, color = paradigm
fig, ax = plt.subplots(figsize=(9, 3.8))
np.random.seed(0)
for i, paradigm in enumerate(PARADIGM_ORDER):
    sub = merged[merged['paradigm'] == paradigm]['n_rows'].dropna()
    if len(sub) == 0:
        continue
    # jitter on y
    y_jitter = np.full(len(sub), i) + (np.random.rand(len(sub)) - 0.5) * 0.3
    ax.scatter(sub, y_jitter, s=70, color=PARADIGM_COLORS[paradigm],
               edgecolor='white', linewidth=0.8, alpha=0.85, zorder=3)
ax.set_xscale('log')
ax.set_yticks(range(len(PARADIGM_ORDER)))
ax.set_yticklabels(PARADIGM_ORDER)
ax.invert_yaxis()
ax.set_xlabel('Training rows (log scale)')
ax.set_title('Dataset size (n_rows) per winning entry, grouped by paradigm')
ax.xaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f'{int(x/1e6)}M' if x >= 1e6 else (f'{int(x/1e3)}K' if x >= 1e3 else str(int(x)))))
ax.grid(axis='x', alpha=0.3)
# Vertical reference line at 50K (cdeotte's 'small data' threshold)
ax.axvline(50_000, linestyle='--', color='gray', alpha=0.5)
ax.text(55_000, len(PARADIGM_ORDER) - 0.3, 'cdeotte 50K threshold', fontsize=8, color='gray')
plt.tight_layout()
plt.savefig(FIG_DIR / 'phase5_24_paradigm_n_rows.png', bbox_inches='tight')
plt.show()

# Summary stats per paradigm
size_by_paradigm = merged.groupby('paradigm')['n_rows'].agg(['min', 'median', 'max', 'count'])
size_by_paradigm = size_by_paradigm.reindex(PARADIGM_ORDER)
print('n_rows per paradigm:')
print(size_by_paradigm)
"""))

cells.append(md("""### 2.5 Paradigm × origination_score (heatmap)"""))

cells.append(code("""# Heatmap: paradigm (y) × origination_score (x), counts as cells
xt = pd.crosstab(merged['paradigm'], merged['origination_score'])
xt = xt.reindex(index=PARADIGM_ORDER, fill_value=0)
# Ensure all 4 score columns present
for s in [0, 1, 2, 3]:
    if s not in xt.columns:
        xt[s] = 0
xt = xt[[0, 1, 2, 3]]

fig, ax = plt.subplots(figsize=(7, 3.5))
im = ax.imshow(xt.values, cmap='Blues', aspect='auto')
ax.set_xticks(range(4))
ax.set_xticklabels(['0\\n(pure fork)', '1\\n(fork+tweak)', '2\\n(significant)', '3\\n(mostly original)'])
ax.set_yticks(range(len(PARADIGM_ORDER)))
ax.set_yticklabels(PARADIGM_ORDER)
ax.set_xlabel('origination_score')
ax.set_title('Paradigm × origination_score (counts)')
# Annotate cells
for i in range(len(xt)):
    for j in range(4):
        val = xt.iloc[i, j]
        if val > 0:
            color = 'white' if val > xt.values.max() / 2 else 'black'
            ax.text(j, i, str(val), ha='center', va='center', color=color, fontsize=10)
plt.colorbar(im, ax=ax, fraction=0.04, pad=0.02, label='count')
plt.tight_layout()
plt.savefig(FIG_DIR / 'phase5_25_paradigm_origination.png', bbox_inches='tight')
plt.show()
print('Observation: no paradigm has any score-0 entries (no pure forks anywhere).')
print('community-template-tweak and lookup-exploit skew toward score 1 (fork+tweak); single-model-FE,')
print('problem-fit-NN, and ensemble-stacking skew toward score 3 (mostly original).')
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
xt = pd.crosstab(merged['n_rows_bin'].astype(str), merged['paradigm'])
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
