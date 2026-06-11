"""Fig 6: within-competition PAIRED winner-vs-control comparison (dumbbell). 2026-06-03."""
import csv, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
P3 = os.path.join(HERE, '..', '..', 'pass3-fe-taxonomy')

def load(path, k):
    r = list(csv.reader(open(path, encoding='utf-8'))); h = r[0]
    ni = h.index('n_fe_techniques_used')
    gcols = {('c%02d' % i): h.index([c for c in h if c.startswith('c%02d' % i)][0]) for i in range(38, 42)}
    out = {}
    for row in r[1:]:
        if row:
            out[row[k]] = {'nfe': int(row[ni]), 'G': any(row[gcols['c%02d' % i]] == '1' for i in range(38, 42))}
    return out

W = load(os.path.join(P3, 'stage1_data.csv'), 0)
C = load(os.path.join(P3, 'controls_data.csv'), 1)
pairs = sorted(set(W) & set(C), key=lambda c: W[c]['nfe'])  # ascending -> highest at top after invert
labels = [c.replace('playground-series-', '') for c in pairs]

fig, ax = plt.subplots(figsize=(8.5, 6))
for i, comp in enumerate(pairs):
    w, c = W[comp]['nfe'], C[comp]['nfe']
    up = w > c
    ax.plot([c, w], [i, i], color=('#2c6fbb' if up else '#e0922f'), lw=2, zorder=1, alpha=0.7)
    ax.scatter(c, i, color='#e0922f', s=70, zorder=2, edgecolor='white', linewidth=0.8)
    g = W[comp]['G']
    ax.scatter(w, i, color='#2c6fbb', s=(170 if g else 70), zorder=3,
               edgecolor=('#1a5e1a' if g else 'white'), linewidth=(1.4 if g else 0.8),
               marker=('*' if g else 'o'))
ax.set_yticks(range(len(pairs))); ax.set_yticklabels(labels, fontsize=9)
ax.set_xlabel('own feature-engineering techniques (n_fe)')
nW = sum(1 for c in pairs if W[c]['nfe'] > C[c]['nfe'])
nC = sum(1 for c in pairs if C[c]['nfe'] > W[c]['nfe'])
ax.set_title(f'Paired within-competition: winner vs near-winning control\n'
             f'winner higher in {nW}/{len(pairs)} pairs (control higher in {nC}); medians 6 vs 3',
             fontsize=11.5, fontweight='bold')
from matplotlib.lines import Line2D
leg = [Line2D([0],[0], marker='o', color='w', markerfacecolor='#2c6fbb', markersize=9, label='Winner'),
       Line2D([0],[0], marker='o', color='w', markerfacecolor='#e0922f', markersize=9, label='Control'),
       Line2D([0],[0], marker='*', color='w', markerfacecolor='#2c6fbb', markeredgecolor='#1a5e1a', markersize=14, label='Winner uses Group G (learned)'),
       Line2D([0],[0], color='#2c6fbb', lw=2, label='winner > control'),
       Line2D([0],[0], color='#e0922f', lw=2, label='control > winner')]
ax.legend(handles=leg, loc='lower right', frameon=False, fontsize=8.5)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
ax.set_xlim(-0.5, 20)
ax.margins(y=0.04)
plt.tight_layout()
out = os.path.join(HERE, 'fig6_paired_winner_control.png')
plt.savefig(out, dpi=150, bbox_inches='tight')
print('wrote', out, f'| winner>control {nW}, control>winner {nC}')
