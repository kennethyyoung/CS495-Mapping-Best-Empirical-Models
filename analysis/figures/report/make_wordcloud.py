"""Word cloud of "what winning looks like": models + ensemble methods + FE techniques,
sized by how many of the 45 winners used each (from the coded data, not raw writeup text),
colored by category. 2026-06."""
import csv, os
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from wordcloud import WordCloud
import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
P3 = os.path.join(ROOT, 'analysis', 'pass3-fe-taxonomy', 'stage1_data.csv')
XLSX = os.path.join(ROOT, 'data', 'kaggle_meta_analysis.xlsx')

MODEL_C, ENS_C, FE_C = '#1f4e79', '#c0392b', '#2e8b57'   # blue / red / green

# ---------- 1. FE techniques from the Pass-3 taxonomy ----------
FE_LABELS = {
    'te_basic': 'Target Encoding', 'te_within_fold': 'Within-fold TE',
    'te_multi_aggs': 'Multi-agg TE', 'te_alt_targets': 'Alt-target TE',
    'count_encoding': 'Count Encoding', 'frequency_encoding': 'Frequency Encoding',
    'pairwise_mult': 'Pairwise Products', 'pairwise_add': 'Pairwise Sums',
    'higher_order_combos': 'Higher-order Combos', 'binning': 'Binning',
    'numerics_as_cats': 'Numerics as Categories', 'digit_features': 'Digit Features',
    'rounding_multi': 'Rounding', 'log_transform': 'Log Transform',
    'cyclical_encoding': 'Cyclical Encoding', 'rowwise_stats': 'Row-wise Stats',
    'domain_ratios': 'Domain Ratios', 'orig_target_mean': 'Original Target Mean',
    'autoencoder_latents': 'Autoencoder Latents', 'pca_svd': 'PCA / SVD',
    'genetic_programming': 'Genetic Programming', 'residual_features': 'Residual Features',
    'permutation_importance': 'Permutation Importance', 'brute_force': 'Brute-force Search',
    'brute_force_interactions': 'Brute-force Interactions',
}
SKIP_FE = {'minimal_no_fe', 'forked_base_uncatalogued'}  # meta flags, not techniques

rows = list(csv.reader(open(P3, encoding='utf-8'))); hdr = rows[0]
data = [r for r in rows[1:] if r]
freq, category = {}, {}
for i, h in enumerate(hdr):
    if not (h[:1] == 'c' and h[1:3].isdigit()):
        continue
    suffix = h[4:]
    if suffix in SKIP_FE:
        continue
    cnt = sum(1 for r in data if r[i] == '1')
    if cnt >= 3:
        label = FE_LABELS.get(suffix, suffix.replace('_', ' ').title())
        freq[label] = cnt
        category[label] = 'fe'

# ---------- 2. Models + ensemble from the workbook ----------
wb = openpyxl.load_workbook(XLSX, data_only=True); ws = wb['Competition Data']
wr = list(ws.iter_rows(values_only=True)); wh = list(wr[0])
def col(name): i = wh.index(name); return [r[i] for r in wr[1:] if r[i] is not None]
def tokens(field):
    c = Counter()
    for v in col(field):
        for t in str(v).replace(',', ';').split(';'):
            t = t.strip().lower()
            if t and t not in ('not_described', 'not_applicable', 'none', 'nan'):
                c[t] += 1
    return c

MODEL_MERGE = {'nn': 'neural_network', 'randomforest': 'random_forest'}
MODEL_LABELS = {
    'xgboost': 'XGBoost', 'lightgbm': 'LightGBM', 'catboost': 'CatBoost',
    'neural_network': 'Neural Network', 'autogluon': 'AutoGluon', 'tabm': 'TabM',
    'realmlp': 'RealMLP', 'random_forest': 'Random Forest', 'ridge': 'Ridge',
    'resnet': 'ResNet', 'mlp': 'MLP', 'deeptables': 'DeepTables',
    'logistic_regression': 'Logistic Regression',
}
mc = Counter()
for t, n in tokens('models_used').items():
    mc[MODEL_MERGE.get(t, t)] += n
for t, n in mc.items():
    if n >= 3 and t in MODEL_LABELS:
        freq[MODEL_LABELS[t]] = n; category[MODEL_LABELS[t]] = 'model'

ENS_LABELS = {'stacking': 'Stacking', 'hill_climbing': 'Hill Climbing',
              'weighted_blend': 'Weighted Blend', 'mean_blend': 'Mean Blend'}
for t, n in tokens('ensemble_method').items():
    if t in ENS_LABELS:
        freq[ENS_LABELS[t]] = n; category[ENS_LABELS[t]] = 'ens'

# ---------- 3. Render ----------
colors = {'model': MODEL_C, 'ens': ENS_C, 'fe': FE_C}
def color_func(word, **kw): return colors[category[word]]

def render(rel_scaling, suffix):
    wc = WordCloud(width=1600, height=850, background_color='white',
                   prefer_horizontal=1.0, color_func=color_func, max_words=100,
                   relative_scaling=rel_scaling, margin=6, collocations=False,
                   random_state=42).generate_from_frequencies(freq)
    fig, ax = plt.subplots(figsize=(12, 6.8))
    ax.imshow(wc, interpolation='bilinear'); ax.axis('off')
    ax.set_title('What winning looks like: models, ensembling, and feature engineering\n'
                 '(word size = number of the 45 winners using it)', fontsize=13, fontweight='bold')
    ax.legend(handles=[Patch(color=MODEL_C, label='Models'),
                       Patch(color=ENS_C, label='Ensembling'),
                       Patch(color=FE_C, label='Feature engineering')],
              loc='lower center', bbox_to_anchor=(0.5, -0.06), ncol=3, frameon=False, fontsize=11)
    plt.tight_layout()
    out = os.path.join(HERE, f'wordcloud_winning{suffix}.png')
    plt.savefig(out, dpi=150, bbox_inches='tight'); plt.close(fig)
    print('wrote', out)

render(0.20, '')        # flat (rel_scaling 0.20): mid-size terms read; GBM dominance still clear
print(f'{len(freq)} terms')
