"""Generate four new presentation figures from corrected Pass 1 + Pass 2 data.

Outputs to analysis/figures/phase5/:
  - phase5_61_fe_tag_frequency.png    -> pivot slide (slide 6)
  - phase5_62_model_family.png         -> pivot slide (slide 6)
  - phase5_63_origination_score.png    -> "how winners build" slide (slide 11)
  - phase5_64_use_mode_breakdown.png   -> "use as columns" slide (slide 13)
"""

import sys
from collections import Counter
from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding="utf-8")

XLSX = Path("data/kaggle_meta_analysis.xlsx")
FIG_DIR = Path("analysis/figures/phase5")
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 150,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})


def load_data():
    p1 = pd.read_excel(XLSX, sheet_name="Competition Data")
    p2 = pd.read_excel(XLSX, sheet_name="Paradigm & Attribution")
    merged = p1.merge(p2, on=["competition_ref", "finish_rank"],
                      how="outer", suffixes=("_p1", "_p2"))
    return p1, p2, merged


def split_semicolons(val):
    if pd.isna(val) or not str(val).strip():
        return []
    return [s.strip().lower() for s in str(val).split(";") if s.strip()]


# =====================================================================
# Figure 1: FE tag frequency histogram (pivot slide evidence #1)
# =====================================================================
def fig_fe_tag_frequency(p1):
    """Shows that fe_techniques is unbucketable: most tags appear once."""
    # Split fe_techniques across all entries; count tag occurrences
    all_tags = []
    for val in p1["fe_techniques"].fillna(""):
        # fe_techniques is free-text; split on common separators
        # First try semicolons, then commas, then take whole string
        if ";" in str(val):
            tags = [t.strip().lower() for t in str(val).split(";") if t.strip()]
        elif "," in str(val):
            tags = [t.strip().lower() for t in str(val).split(",") if t.strip()]
        else:
            tags = [str(val).strip().lower()] if str(val).strip() else []
        # Skip placeholder sentinels
        tags = [t for t in tags if t not in
                ("not_described", "not_applicable", "none", "nan", "")]
        all_tags.extend(tags)

    tag_counts = Counter(all_tags)
    n_unique_tags = len(tag_counts)
    # Histogram of count-of-count: how many tags appear N times?
    appearance_counts = Counter(tag_counts.values())

    max_appearances = max(appearance_counts) if appearance_counts else 1
    # Bin into: 1, 2, 3, 4-5, 6-10, 11+
    bins = {"1": 0, "2": 0, "3": 0, "4-5": 0, "6-10": 0, "11+": 0}
    for n_app, n_tags in appearance_counts.items():
        if n_app == 1:
            bins["1"] += n_tags
        elif n_app == 2:
            bins["2"] += n_tags
        elif n_app == 3:
            bins["3"] += n_tags
        elif n_app <= 5:
            bins["4-5"] += n_tags
        elif n_app <= 10:
            bins["6-10"] += n_tags
        else:
            bins["11+"] += n_tags

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    bin_labels = list(bins.keys())
    bin_values = [bins[k] for k in bin_labels]
    colors = ["#d62728" if k == "1" else "#1f77b4" for k in bin_labels]
    ax.bar(bin_labels, bin_values, color=colors, edgecolor="white")
    ax.set_xlabel("Number of writeups a tag appears in")
    ax.set_ylabel("Number of unique FE tags")
    ax.set_title(f"FE tag frequency distribution ({n_unique_tags} unique tags total)")
    for i, v in enumerate(bin_values):
        if v > 0:
            ax.text(i, v + max(bin_values) * 0.02, str(v),
                    ha="center", fontsize=10, fontweight="bold")
    ax.set_ylim(0, max(bin_values) * 1.15)
    plt.tight_layout()
    out = FIG_DIR / "phase5_61_fe_tag_frequency.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")
    print(f"    total unique tags: {n_unique_tags}")
    print(f"    appearing exactly once: {bins['1']} "
          f"({100*bins['1']/n_unique_tags:.0f}%)")
    return n_unique_tags, bins["1"]


# =====================================================================
# Figure 2: Model family distribution (pivot slide evidence #2)
# =====================================================================
def fig_model_family(p1):
    """Shows GBM dominance -- visual support for 'no which-model branch'."""
    counts = p1["dominant_base_model"].value_counts()
    # Order: GBM, neural_network, linear, other (descending)
    order = ["gbm", "neural_network", "other", "linear"]
    counts = counts.reindex(order, fill_value=0)
    total = counts.sum()

    fig, ax = plt.subplots(figsize=(7.5, 3.2))
    colors = ["#1f77b4", "#2ca02c", "#7f7f7f", "#9467bd"]
    labels = ["GBM\n(XGBoost/LGBM/CatBoost)", "Neural network",
              "Other (kernel methods)", "Linear"]
    ax.barh(range(len(counts)), counts.values, color=colors, edgecolor="white")
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel(f"Number of winning entries (n = {total})")
    ax.set_title("Dominant model family across winners")
    for i, v in enumerate(counts.values):
        pct = 100 * v / total
        ax.text(v + 0.5, i, f"{v}  ({pct:.0f}%)", va="center", fontsize=10)
    ax.set_xlim(0, counts.max() * 1.22)
    plt.tight_layout()
    out = FIG_DIR / "phase5_62_model_family.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")
    print(f"    counts: {dict(counts)}")


# =====================================================================
# Figure 3: Origination score histogram ("how winners build")
# =====================================================================
def fig_origination_score(p2):
    """Shows the score distribution; key is the empty bar at score 0."""
    counts = p2["origination_score"].value_counts().reindex([0, 1, 2, 3], fill_value=0)
    total = counts.sum()

    fig, ax = plt.subplots(figsize=(7.5, 3.8))
    # Score 0 colored red (the "empty" / striking bar)
    colors = ["#d62728", "#ff7f0e", "#1f77b4", "#2ca02c"]
    labels = [f"0\n(pure fork)", f"1\n(fork + tweak)",
              f"2\n(significant\noriginal)", f"3\n(mostly\noriginal)"]
    ax.bar(range(4), counts.values, color=colors, edgecolor="white", width=0.62)
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels)
    ax.set_ylabel(f"Number of winners (n = {total})")
    ax.set_title("Origination score distribution: no pure forks among winners")
    for i, v in enumerate(counts.values):
        pct = 100 * v / total
        label_text = f"{v}  ({pct:.0f}%)" if v > 0 else f"{v}  (0%)"
        ax.text(i, v + max(counts.values) * 0.03 if v > 0 else 0.3,
                label_text, ha="center", fontsize=10, fontweight="bold")
    # Special annotation for the empty bar
    if counts[0] == 0:
        ax.annotate("no pure-fork wins\nin the entire corpus",
                    xy=(0, max(counts.values) * 0.07 + 1.7), xytext=(0.35, max(counts.values) * 0.42),
                    fontsize=9, color="#d62728",
                    arrowprops=dict(arrowstyle="->", color="#d62728", lw=1))
    ax.set_ylim(0, max(counts.values) * 1.18)
    plt.tight_layout()
    out = FIG_DIR / "phase5_63_origination_score.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")
    print(f"    counts by score: {dict(counts)}")


# =====================================================================
# Figure 4: External original use-mode breakdown
# (filtered to entries with available original)
# =====================================================================
def fig_use_mode_breakdown(p1):
    """Shows the 'use as columns' contradiction visually."""
    # Filter to entries where external_original_available is TRUE
    available_mask = p1["external_original_available"].astype(str).str.upper() == "TRUE"
    subset = p1[available_mask]
    counts = subset["external_original_use_mode"].value_counts()
    # Order: rows-only, both, available-not-used, lookup, columns-only, features-derived
    order = ["rows-only", "both", "available-not-used", "lookup",
             "columns-only", "features-derived"]
    counts = counts.reindex(order, fill_value=0)
    # Drop zero-count categories that don't exist
    counts = counts[counts > 0]
    total = counts.sum()

    fig, ax = plt.subplots(figsize=(8, 3.8))
    # Highlight columns-only in gold (it's the "famous trick" everyone supposedly does)
    colors = []
    for mode in counts.index:
        if mode == "columns-only":
            colors.append("#C8932A")  # gold accent
        elif mode == "rows-only":
            colors.append("#1f77b4")  # blue (dominant)
        else:
            colors.append("#7f7f7f")  # gray
    ax.barh(range(len(counts)), counts.values, color=colors, edgecolor="white")
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels(counts.index)
    ax.invert_yaxis()
    ax.set_xlabel(f"Number of winners (n = {total} with available original)")
    ax.set_title('How winners use available external original datasets')
    for i, v in enumerate(counts.values):
        pct = 100 * v / total
        ax.text(v + 0.2, i, f"{v}  ({pct:.0f}%)", va="center", fontsize=10)
    ax.set_xlim(0, counts.max() * 1.22)
    plt.tight_layout()
    out = FIG_DIR / "phase5_64_use_mode_breakdown.png"
    plt.savefig(out, bbox_inches="tight")
    plt.close()
    print(f"  saved {out}")
    print(f"    counts: {dict(counts)}")


def main():
    p1, p2, merged = load_data()
    print(f"loaded: pass1={p1.shape}, pass2={p2.shape}")
    print()
    print("Fig 1: FE tag frequency")
    fig_fe_tag_frequency(p1)
    print()
    print("Fig 2: Model family distribution")
    fig_model_family(p1)
    print()
    print("Fig 3: Origination score histogram")
    fig_origination_score(p2)
    print()
    print("Fig 4: External original use-mode breakdown")
    fig_use_mode_breakdown(p1)
    print()
    print("All figures saved to", FIG_DIR)


if __name__ == "__main__":
    main()
