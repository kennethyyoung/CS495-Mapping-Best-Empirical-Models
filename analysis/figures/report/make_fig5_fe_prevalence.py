"""Fig 5 (report anchor): group-level FE prevalence, winners vs near-winning controls.
Reads the clean/adjudicated Pass 3 data. 2026-06-03."""
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
P3 = os.path.join(HERE, '..', '..', 'pass3-fe-taxonomy')

# 10 technique families (Group K = meta flags, excluded from the FE prevalence figure)
GROUPS = [
    ('Categorical encoding', range(1, 8)), ('Numeric transforms', range(8, 13)),
    ('Interactions / combos', range(13, 19)), ('Aggregates / groupby', range(19, 27)),
    ('Domain / temporal', range(27, 32)), ('External-original', range(32, 38)),
    ('Learned / advanced', range(38, 42)), ('Text / string', range(42, 45)),
    ('Model-derived', range(45, 48)), ('Feature selection', range(48, 51)),
]

def load(path, keyidx):
    r = list(csv.reader(open(path, encoding='utf-8'))); h = r[0]
    idx = [h.index(x) for x in h if x.startswith('c') and x[1:3].isdigit()]
    return [{('c%02d' % (j + 1)): row[idx[j]] for j in range(53)} for row in r[1:] if row]

W = load(os.path.join(P3, 'stage1_data.csv'), 0)
C = load(os.path.join(P3, 'controls_data.csv'), 1)

def rate(rows, rng):
    cs = ['c%02d' % i for i in rng]
    return 100 * sum(1 for r in rows if any(r[c] == '1' for c in cs)) / len(rows)

labels = [g[0] for g in GROUPS]
win = [rate(W, g[1]) for g in GROUPS]
ctl = [rate(C, g[1]) for g in GROUPS]

y = np.arange(len(labels)); bh = 0.38
fig, ax = plt.subplots(figsize=(9, 6.2))
b1 = ax.barh(y + bh / 2, win, bh, label=f'Winners (n={len(W)})', color='#2c6fbb')
b2 = ax.barh(y - bh / 2, ctl, bh, label=f'Near-winner controls (n={len(C)})', color='#e0922f')
ax.set_yticks(y); ax.set_yticklabels(labels); ax.invert_yaxis()
ax.set_xlabel('% of entries using ≥1 technique in the family')
ax.set_title('Feature-engineering family prevalence: winners vs near-winning controls', fontsize=12, fontweight='bold')
ax.legend(loc='lower right', frameon=False)
for b in (b1, b2):
    for r in b:
        ax.text(r.get_width() + 1, r.get_y() + r.get_height() / 2, f'{r.get_width():.0f}', va='center', fontsize=8, color='#444')
# highlight the one family where winners > controls
gi = labels.index('Learned / advanced')
ax.axhspan(gi - 0.5, gi + 0.5, color='#d8f0d8', alpha=0.5, zorder=0)
ax.annotate('only family where\nwinners > controls\n(Group G, heavyweight)',
            xy=(win[gi] + 1, gi), xytext=(44, gi), fontsize=8.5, color='#1a5e1a',
            ha='left', va='center',
            arrowprops=dict(arrowstyle='->', color='#1a5e1a', lw=1))
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.set_xlim(0, 75)
plt.tight_layout()
out = os.path.join(HERE, 'fig5_fe_prevalence_winners_vs_controls.png')
plt.savefig(out, dpi=150, bbox_inches='tight')
print('wrote', out)
print('group | winners% | controls%')
for l, w_, c_ in zip(labels, win, ctl):
    print(f'  {l:22s} {w_:5.0f} {c_:8.0f}')
