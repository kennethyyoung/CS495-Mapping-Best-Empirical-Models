"""Fig 3 (technique long-tail) and Fig 4 (n_fe distribution) for winners. 2026-06-03."""
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', '..', 'pass3-fe-taxonomy', 'stage1_data.csv')
r = list(csv.reader(open(SRC, encoding='utf-8'))); h = r[0]
cidx = [(i, h[i]) for i in range(len(h)) if h[i].startswith('c') and h[i][1:3].isdigit()]
rows = [row for row in r[1:] if row]
nfe = [int(row[h.index('n_fe_techniques_used')]) for row in rows]
N = len(rows)

# ---- Fig 3: technique-level prevalence, sorted (small core + long tail) ----
counts = sorted(((sum(1 for row in rows if row[i] == '1'), name) for i, name in cidx), reverse=True)
vals = [c for c, _ in counts]
fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(vals))
ax.bar(x, vals, color=['#2c6fbb' if v >= 5 else '#9bb8d6' for v in vals], width=0.85)
# label the two clear leaders individually; bracket the rest of the core
ax.annotate('target encoding', xy=(0, vals[0]), xytext=(2.5, 17.2), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#555', lw=0.8))
ax.annotate('within-fold TE', xy=(1, vals[1]), xytext=(3.2, 13.6), fontsize=9,
            arrowprops=dict(arrowstyle='->', color='#555', lw=0.8))
ax.annotate('rest of shared core\n(interactions, freq, combos,\ndigits, ratios, ...)',
            xy=(5, vals[5]), xytext=(8.5, 11), fontsize=8.5, color='#333',
            arrowprops=dict(arrowstyle='->', color='#888', lw=0.8))
tail = sum(1 for v in vals if v <= 2)
ax.annotate(f'long bespoke tail:\n{tail} of 53 techniques used by ≤2 winners',
            xy=(len(vals) - 12, 1.6), xytext=(len(vals) - 27, 8.5), fontsize=9, color='#444',
            arrowprops=dict(arrowstyle='->', color='#888', lw=0.8))
ax.set_xlabel('feature-engineering technique (53 columns, ranked by prevalence)')
ax.set_ylabel(f'# of winners using it (of {N})')
ax.set_title('Winning FE is a small shared core plus a long bespoke tail', fontsize=12, fontweight='bold')
for s in ('top', 'right'): ax.spines[s].set_visible(False)
plt.tight_layout()
out3 = os.path.join(HERE, 'fig3_technique_longtail_winners.png')
plt.savefig(out3, dpi=150, bbox_inches='tight'); print('wrote', out3)

# ---- Fig 4: n_fe distribution ----
fig, ax = plt.subplots(figsize=(8, 4.6))
mx = max(nfe)
bins = np.arange(0, mx + 2) - 0.5
ax.hist(nfe, bins=bins, color='#2c6fbb', edgecolor='white')
med = st.median(nfe); mean = st.mean(nfe)
ax.axvline(med, color='#c0392b', lw=1.6, ls='--', label=f'median = {med}')
ax.set_xticks(range(0, mx + 1))
ax.set_xlabel('number of own FE techniques (n_fe, excl. meta flags)')
ax.set_ylabel('# of winners')
ax.set_title(f'Most winners use few of their own FE techniques (median {med}, mean {mean:.1f})', fontsize=12, fontweight='bold')
z = sum(1 for v in nfe if v == 0)
ax.annotate(f'{z} winners: forked/\nminimal-only (n_fe=0)', xy=(0, nfe.count(0)), xytext=(1.5, max(nfe.count(0), 1) + 4),
            fontsize=8.5, color='#444', arrowprops=dict(arrowstyle='->', color='#888', lw=0.8))
ax.annotate('heavyweight tail\n(cdeotte s6e3 = 19)', xy=(mx, 1), xytext=(mx - 8, 5), fontsize=8.5, color='#444',
            arrowprops=dict(arrowstyle='->', color='#888', lw=0.8))
ax.legend(frameon=False)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
plt.tight_layout()
out4 = os.path.join(HERE, 'fig4_nfe_distribution_winners.png')
plt.savefig(out4, dpi=150, bbox_inches='tight'); print('wrote', out4)
print(f'N={N} | n_fe median={med} mean={mean:.1f} max={mx} | zeros={z} | tail(<=2 techs)={tail}/53')
