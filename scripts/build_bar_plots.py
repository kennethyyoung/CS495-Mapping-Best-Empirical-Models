import sys, openpyxl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

# ── Load data ──────────────────────────────────────────────────────────────────
wb = openpyxl.load_workbook('data/kaggle_meta_analysis.xlsx')
ws = wb['Competition Data']
headers = [cell.value for cell in ws[1]]
rows = list(ws.iter_rows(min_row=2, values_only=True))
N = len(rows)

def col(name):
    idx = headers.index(name)
    return [r[idx] for r in rows]

# ── Shared style ───────────────────────────────────────────────────────────────
BLUE   = '#2563EB'
GRAY   = '#6B7280'
BG     = 'white'
plt.rcParams.update({
    'font.family': 'sans-serif',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.grid': True,
    'axes.grid.axis': 'x',
    'grid.color': '#E5E7EB',
    'grid.linewidth': 0.8,
})

# ── Plot 1: Model family frequency in models_used ─────────────────────────────
MODEL_FAMILIES = {
    'XGBoost':             ['XGBoost'],
    'LightGBM':            ['LightGBM'],
    'CatBoost':            ['CatBoost'],
    'Neural Network':      ['NN', 'TabPFN', 'TabNet', 'TabM', 'RealMLP', 'FastAI', 'MLP', 'Autoencoder'],
    'AutoGluon / AutoML':  ['AutoGluon', 'AutoML'],
    'RF / ExtraTrees':     ['RandomForest', 'ExtraTrees', 'HistGB', 'GradientBoosting'],
    'Linear models':       ['LinearRegression', 'Lasso', 'Ridge', 'LogisticRegression'],
    'Other':               ['SVR', 'SVC', 'KNN', 'GAM'],
}

model_counts = Counter()
for val in col('models_used'):
    if not val or val == 'not_described':
        continue
    for family, aliases in MODEL_FAMILIES.items():
        if any(a in val for a in aliases):
            model_counts[family] += 1

# Sort descending
families = [f for f, _ in model_counts.most_common()]
counts   = [model_counts[f] for f in families]

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.barh(families[::-1], counts[::-1], color=BLUE, height=0.55)
ax.set_xlabel(f'Number of winning solutions (n = {N})')
ax.set_title('Model families used in winning solutions', fontweight='bold', pad=10)
ax.set_xlim(0, N + 2)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
for bar, count in zip(bars, counts[::-1]):
    ax.text(bar.get_width() + 0.4, bar.get_y() + bar.get_height() / 2,
            str(count), va='center', fontsize=9, color=GRAY)
plt.tight_layout()
plt.savefig('outputs/figures/plot1_model_frequency.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved plot1_model_frequency.png')

# ── Plot 2: Target type breakdown ──────────────────────────────────────────────
target_counts = Counter(col('target_type'))
order  = ['binary', 'regression', 'multiclass']
labels = ['Binary', 'Regression', 'Multiclass']
vals   = [target_counts.get(k, 0) for k in order]
colors = [BLUE, '#059669', '#D97706']

fig, ax = plt.subplots(figsize=(5, 3.5))
bars = ax.bar(labels, vals, color=colors, width=0.5)
ax.set_ylabel(f'Number of competitions (n = {N})')
ax.set_title('Dataset breakdown by target type', fontweight='bold', pad=10)
ax.set_ylim(0, max(vals) + 3)
ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
for bar, v in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.4,
            str(v), ha='center', fontsize=10, color=GRAY)
ax.grid(axis='y')
ax.grid(axis='x', visible=False)
plt.tight_layout()
plt.savefig('outputs/figures/plot2_target_type.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved plot2_target_type.png')

# ── Plot 3: Ensemble method distribution ──────────────────────────────────────
em_raw = col('ensemble_method')
em_filtered = [v for v in em_raw if v and v != 'not_described']
em_counts = Counter(em_filtered)
n_em = len(em_filtered)

order_em  = ['stacking', 'blending', 'hill_climbing', 'none']
labels_em = ['Stacking', 'Blending', 'Hill climbing', 'None (single model)']
vals_em   = [em_counts.get(k, 0) for k in order_em]

fig, ax = plt.subplots(figsize=(6, 3.8))
bars = ax.barh(labels_em[::-1], vals_em[::-1], color=BLUE, height=0.5)
ax.set_xlabel(f'Number of solutions (n = {n_em} with known method)')
ax.set_title('Ensemble method used by winning solutions', fontweight='bold', pad=10)
ax.set_xlim(0, max(vals_em) + 4)
ax.xaxis.set_major_locator(ticker.MultipleLocator(5))
for bar, v in zip(bars, vals_em[::-1]):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
            str(v), va='center', fontsize=9, color=GRAY)
plt.tight_layout()
plt.savefig('outputs/figures/plot3_ensemble_method.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved plot3_ensemble_method.png')

# ── Plot 4: Best single model (when explicitly stated) ────────────────────────
bsm_raw = col('best_single_model')
bsm = [v for v in bsm_raw if v and v not in ('not_described', '')]
bsm_counts = Counter(bsm)
n_bsm = len(bsm)

# Collapse AutoGluon variants
bsm_label_map = {
    'AutoGluon': 'AutoGluon',
}
bsm_display = Counter()
for k, v in bsm_counts.items():
    bsm_display[k] += v

bsm_families = [f for f, _ in bsm_display.most_common()]
bsm_vals     = [bsm_display[f] for f in bsm_families]

fig, ax = plt.subplots(figsize=(6, 3.5))
bars = ax.barh(bsm_families[::-1], bsm_vals[::-1], color=BLUE, height=0.5)
ax.set_xlabel(f'Number of solutions (n = {n_bsm} of {N} entries stated a best model)')
ax.set_title('Best single model (when explicitly stated)', fontweight='bold', pad=10)
ax.set_xlim(0, max(bsm_vals) + 2)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
for bar, v in zip(bars, bsm_vals[::-1]):
    ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height() / 2,
            str(v), va='center', fontsize=9, color=GRAY)
plt.tight_layout()
plt.savefig('outputs/figures/plot4_best_single_model.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved plot4_best_single_model.png')

print('\nAll 4 plots saved to outputs/figures/')
