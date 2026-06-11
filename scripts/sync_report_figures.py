"""Copy the 14 report figures into outputs/report/figures/ as fig01..fig14.

The figures are generated into their working location under analysis/figures/
(by make_fig3_4/5/6.py and notebooks/02_reanalysis.ipynb). This script folds the
final set into the deliverable tree so outputs/report/ is self-contained for PDF
assembly. It encodes the canonical Figure-number -> source mapping in one place.

Re-run after regenerating any figure:  python scripts/sync_report_figures.py
"""

import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "analysis" / "figures"
DST = ROOT / "outputs" / "report" / "figures"

# Figure number -> (source path relative to analysis/figures, deliverable stem)
FIGURES = [
    (1,  "phase5/phase5_21_paradigm_distribution.png",        "fig01_paradigm_distribution"),
    (2,  "phase5/phase5_51_coupling_evidence.png",            "fig02_coupling_evidence"),
    (3,  "report/fig3_technique_longtail_winners.png",        "fig03_technique_longtail"),
    (4,  "report/fig4_nfe_distribution_winners.png",          "fig04_nfe_distribution"),
    (5,  "report/fig5_fe_prevalence_winners_vs_controls.png", "fig05_fe_prevalence_winners_vs_controls"),
    (6,  "report/fig6_paired_winner_control.png",             "fig06_paired_winner_control"),
    (7,  "phase5/phase5_41_author_centrality.png",            "fig07_author_centrality"),
    (8,  "phase5/phase5_42_cdeotte_timeline.png",             "fig08_cdeotte_timeline"),
    (9,  "phase5/phase5_22_paradigm_by_era.png",              "fig09_paradigm_by_era"),
    (10, "phase5/phase5_24_paradigm_n_rows.png",              "fig10_n_rows_by_paradigm"),
    (11, "phase5/phase5_31_use_mode_paradigm.png",            "fig11_use_mode_by_paradigm"),
    (12, "phase5/phase5_23_paradigm_photofinish.png",         "fig12_photofinish_by_paradigm"),
    (13, "phase5/phase5_33_canonized_techniques.png",         "fig13_canonized_techniques"),
    (14, "phase5/phase5_34_citations_origination.png",        "fig14_citations_by_origination"),
]


def main():
    DST.mkdir(parents=True, exist_ok=True)
    missing = []
    for n, rel, stem in FIGURES:
        src = SRC / rel
        if not src.exists():
            missing.append(rel)
            continue
        dst = DST / f"{stem}.png"
        shutil.copy2(src, dst)
        print(f"  Figure {n:>2}: {rel}  ->  outputs/report/figures/{dst.name}")
    if missing:
        print("\nMISSING SOURCES:", *missing, sep="\n  ")
        sys.exit(1)
    print(f"\nSynced {len(FIGURES)} figures to {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
