# Mapping Best Empirical Models: A Meta-Analysis of Winning Kaggle Solutions

## Project Description

A systematic meta-analysis of top-finishing solutions across Kaggle tabular competitions, focused on identifying which preprocessing and feature engineering decisions separate winning solutions from the rest.

The study collects structured data from 35 winning competition writeups and notebooks, encodes key pipeline decisions into a dataset, and synthesizes findings into an empirically-grounded decision flowchart for tabular ML pipelines. Competitions are scoped to Playground Series seasons 3–5 and Featured competitions from 2022 onward, restricted to cross-sectional tabular data with tree-based models as the primary or significant ensemble component.

## Objectives

- Build a structured dataset of 30+ top-finishing competition solutions with one entry per competition (best-documented of top-3 finishers)
- Identify which preprocessing and feature engineering decisions are most consistently associated with winning, using frequency tables and conditional cross-tabulations
- Produce a decision flowchart covering key decision nodes (encoding strategy, CV strategy, missing data handling) that maps dataset characteristics to recommended pipeline decisions
- Validate the flowchart by replicating its recommendations on a held-out competition

## Tools & Technologies

- **Language:** Python 3.13
- **Environment:** Poetry (dependency management)
- **Data:** openpyxl, pandas
- **Modeling:** XGBoost, LightGBM, CatBoost, scikit-learn
- **Visualization:** matplotlib, seaborn
- **Data source:** Kaggle API (`kaggle` Python package)

## Project Structure

```
├── data/
│   ├── kaggle_candidates_v2.xlsx   # Scraped competition shortlist (49 candidates)
│   └── kaggle_meta_analysis.xlsx   # Main dataset — 35 hand-coded entries
├── scripts/
│   ├── kaggle_scraper_v2.py        # Competition discovery & pre-filtering
│   ├── write_entries.py            # Writes coded entries to Excel dataset
│   └── build_bar_plots.py          # Generates EDA bar plots from dataset
├── notebooks/                      # Analysis notebooks (Phase 3+)
├── outputs/
│   ├── figures/                    # EDA and analysis plots
│   └── report/                     # Final writeup
└── PLAN.md                         # Full project plan with tasks and timeline
```

## How to Run

**Install dependencies:**
```bash
poetry install
```

**Run Kaggle scraper** (requires `~/.kaggle/kaggle.json`):
```bash
python scripts/kaggle_scraper_v2.py
```

**Write dataset entries to Excel:**
```bash
python scripts/write_entries.py
```

**Generate bar plots:**
```bash
python scripts/build_bar_plots.py
```

## Current Status

- Phase 1 (competition discovery & schema design): complete
- Phase 2 (data collection): 35 entries coded; code exploration pass for `writeup_detail=3` entries pending
- Phase 3 (EDA & analysis): pending
- Phase 4 (flowchart construction): pending
- Phase 5 (replication & validation): pending

## Team

- Kenneth Young (kenneth.young@bellevuecollege.edu)

## Timeline

April 28 – June 24, 2026. See [PLAN.md](PLAN.md) for full milestone breakdown.
