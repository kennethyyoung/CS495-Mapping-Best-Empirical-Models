"""Slide-native coupling figure: one bar per coupling (support rate), colored by
verdict, big fonts for projection. Companion to the dense report fig02. 2026-06."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))

# coupling, support %, n, verdict  (listed most -> least supported)
rows = [
    ("Linear stacker dominance",                80, 40, "STRONG"),
    ("Distribution shift → custom CV",      80,  5, "DIRECTIONAL"),
    ("Recurring author → fork-heavy win",   38,  8, "CONTRADICTED"),
    ("Recover original → use as columns",   37, 30, "CONTRADICTED"),
    ("Small data → skip FE",                23, 13, "CONTRADICTED"),
    ("Photo-finish → trust own CV",         22, 27, "INCONCLUSIVE"),
]
COLOR = {"STRONG": "#2e8b57", "DIRECTIONAL": "#e0922f",
         "CONTRADICTED": "#c0392b", "INCONCLUSIVE": "#8a8a8a"}

rows = rows[::-1]                       # barh draws first item at the bottom
labels = [f"{r[0]}  (n={r[2]})" for r in rows]
vals   = [r[1] for r in rows]
colors = [COLOR[r[3]] for r in rows]

fig, ax = plt.subplots(figsize=(11, 5.4))
y = list(range(len(rows)))
ax.barh(y, vals, color=colors, height=0.6, zorder=3)
ax.axvline(50, color="#555", ls="--", lw=1.3, zorder=2)
ax.text(50, len(rows) - 0.35, "50%", color="#555", fontsize=11, ha="center", va="bottom")

ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=14)
ax.set_xlim(0, 100)
ax.set_xlabel("Support rate (% of testable cases)", fontsize=13)
for i, v in enumerate(vals):
    ax.text(v + 1.5, i, f"{v}%", va="center", fontsize=13, fontweight="bold", color="#222")

ax.legend(handles=[Patch(color=COLOR["STRONG"],       label="Strong"),
                   Patch(color=COLOR["DIRECTIONAL"],  label="Directional (thin n)"),
                   Patch(color=COLOR["CONTRADICTED"], label="Contradicted"),
                   Patch(color=COLOR["INCONCLUSIVE"], label="Inconclusive")],
          loc="lower right", fontsize=11, frameon=False)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.tick_params(axis="x", labelsize=12)
plt.tight_layout()
out = os.path.join(HERE, "coupling_slide.png")
plt.savefig(out, dpi=150, bbox_inches="tight")
print("wrote", out)
