# PLAN.md

## Project Overview

**Title:** Meta-Analysis of Winning Solutions in Kaggle Tabular Competitions
**Author:** youngyken
**Date:** April 27, 2026

### Description

A systematic meta-analysis of top-finishing solutions across Kaggle tabular competitions, focused on identifying the preprocessing and feature engineering decisions that separate winning solutions from the rest. The study collects structured data from winning notebooks and writeups, encodes key pipeline decisions into a dataset, and synthesizes findings into an empirically-grounded decision flowchart for tabular ML pipelines.

The unit of analysis is one solution per competition: whichever of the top-3 finishers has the most complete writeup (`writeup_detail` score). `finish_rank` (1/2/3) is tracked as a covariate. This reduces selection bias from writeup availability without increasing data collection workload.

The analysis is scoped to Playground Series seasons 3–5 (Jan 2023–present) and Featured competitions from 2022 onward, where tree-based models (XGBoost, LightGBM, CatBoost) are the primary or dominant model family. Competitions are sourced from both monetized (Featured) and non-monetized (Playground Series) categories on Kaggle, with `is_monetized` tracked as a covariate so both pools can be analyzed separately or together. `n_teams` (number of competing teams) is tracked as a covariate to account for differences in competitive intensity.

### Objectives

- Build a structured dataset of top-finishing competition solutions with ~30+ entries (one per competition, best-documented of top-3)
- Identify which preprocessing and feature engineering decisions (encoding strategy, missing data handling, outlier treatment, etc.) are most consistently associated with winning, using frequency tables and conditional cross-tabulations
- Produce a decision flowchart covering 2–3 key decision nodes (encoding strategy, CV strategy, missing data handling) that maps dataset characteristics → recommended pipeline decisions, backed by empirical evidence
- Validate the flowchart by replicating it on a held-out competition and measuring performance

---

## Environment Setup

### Requirements

- Python 3.13
- Miniforge (conda) for environment management
- Virtual environment or conda env


### Core Dependencies (`requirements.txt`)

```
kaggle
pandas
numpy
openpyxl
requests
beautifulsoup4
scikit-learn
xgboost
lightgbm
catboost
matplotlib
seaborn
jupyter
```

### Kaggle API Setup

Place your `kaggle.json` credentials at:
- **Windows:** `C:\Users\YourName\.kaggle\kaggle.json`
- **Mac/Linux:** `~/.kaggle/kaggle.json`

```powershell
# Windows — copy from project folder
mkdir %USERPROFILE%\.kaggle
copy kaggle.json %USERPROFILE%\.kaggle\kaggle.json
```

---

## Architecture

```
kaggle-meta-analysis/
│
├── data/
│   ├── raw/                        # Downloaded notebooks and writeups
│   ├── kaggle_candidates_v2.xlsx   # Scraped competition shortlist
│   └── kaggle_meta_analysis.xlsx   # Main dataset (hand-coded entries)
│
├── scripts/
│   ├── kaggle_scraper_v2.py        # Competition discovery & pre-filtering
│   ├── parse_notebook.py           # Extract schema fields from .ipynb files
│   └── build_dataset.py            # Compile all entries into final dataset
│
├── notebooks/
│   ├── 01_eda.ipynb                # Exploratory analysis of collected dataset
│   ├── 02_analysis.ipynb           # Cross-tabulations, frequency analysis
│   ├── 03_flowchart_logic.ipynb    # Decision tree / rule extraction
│   └── 04_replication.ipynb        # Flowchart validation on held-out competition
│
├── outputs/
│   ├── flowchart.png               # Final decision flowchart (exported)
│   ├── figures/                    # All EDA and analysis plots
│   └── report/                     # Final writeup
│
├── PLAN.md
├── requirements.txt
└── README.md
```

### Key Components


**`kaggle_meta_analysis.xlsx`** — The core dataset. Three sheets: `Competition Data` (entry form), `Codebook` (allowed values), `Example (s5e12)` (reference row). Each row is one competition, each column is a schema variable.

**`03_flowchart_logic.ipynb`** — Reads the completed dataset and derives decision rules via conditional frequency tables and cross-tabulations (e.g., encoding choice grouped by cardinality + target type). Flowchart rules are extracted by inspection of these distributions, not by fitting a model on the dataset.

---

## Tasks & Milestones

### Phase 1: Competition Discovery & Dataset Design
- [x] Design dataset schema (variables, codebook)
- [x] Build Kaggle API scraper to pre-filter tabular competitions
- [x] Create Excel data collection template with codebook
- [x] Establish inclusion/exclusion criteria (tree-based primary model, no time series)
- [ ] Finalize variable list (confirm `distribution_shift`, `feature_type_dominant`, `rare_class_handling`, `finish_rank`, `n_teams`)
- [x] Decide on cross-sectional only vs. mixed scope — **cross-sectional only confirmed**
- [ ] Confirm competition scope: PS3–PS5 + Featured 2022+ (update scraper filter accordingly)

### Phase 2: Data Collection
- [x] Identify 30+ candidate competitions from shortlist — **46 candidates remain after tabular + time series screening**
- [ ] Prioritize `writeup_detail = 3` entries (GitHub repo linked)
- [ ] Collect 10 monetized competition entries
- [ ] Collect 20+ playground series entries
- [ ] Fill all schema fields per entry; mark `not described` honestly
- [ ] Score `writeup_detail` (1/2/3) for each entry
- [ ] Flag entries with `distribution_shift = TRUE`

### Phase 3: EDA & Analysis
- [ ] Summary statistics on collected dataset
- [ ] Frequency tables: encoding strategies by `target_type`, `feature_type_dominant`
- [ ] Cross-tabulation: `data_type` × preprocessing decisions
- [ ] Compare monetized vs. playground pipeline patterns
- [ ] Identify most common FE techniques by domain
- [ ] Correlation analysis: `writeup_detail` vs. completeness of fields

### Phase 4: Flowchart Construction
- [ ] Define 2–3 decision nodes (encoding strategy, CV strategy, missing data handling)
- [ ] Extract rules from conditional frequency tables (e.g., encoding choice given cardinality + target type)
- [ ] Draft flowchart covering: missing data → encoding → CV strategy
- [ ] Validate logic against collected entries (does the flowchart match what winners did?)
- [ ] Export as clean visual (Graphviz or draw.io)

### Phase 5: Replication & Validation
- [ ] Select a held-out competition (not in training set)
- [ ] Follow flowchart recommendations to build a pipeline
- [ ] Submit to Kaggle and record leaderboard position
- [ ] Compare performance vs. baseline (no flowchart guidance)
- [ ] Document discrepancies and failure modes

### Phase 6: Writeup & Deliverables
- [ ] Final dataset (cleaned, documented)
- [ ] EDA visualizations
- [ ] Decision flowchart (publication-ready)
- [ ] Replication results and interpretation
- [ ] Final report / paper draft

---

## Methods & Models

### Data Collection
- Kaggle API (`kaggle` Python package) for competition metadata
- Manual extraction from `.ipynb` notebooks and GitHub repos
- Structured coding schema with controlled vocabularies (see Codebook sheet)

### Analysis Techniques
- Frequency tables and conditional cross-tabulations (pandas `groupby` / `crosstab`)
- Chi-square tests where cell counts allow (n ≥ 5 per cell)
- Sensitivity analysis: does the flowchart change with monetized-only entries?
- `finish_rank` and `n_teams` as covariates to check whether findings hold across competitive intensity

### Replication Pipeline (Flowchart Validation)
Following the empirically-derived flowchart:
- **Missing data:** strategy determined by `data_type` and `pct_missing`
- **Encoding:** OHE vs. target encoding vs. embeddings determined by cardinality and `feature_type_dominant`
- **Rare class handling:** frequency threshold (e.g., < 200 observations → `rare_class`)
- **Scaling:** rank transform for tree-based models, standard for linear
- **CV strategy:** stratified k-fold baseline; post-cutoff if distribution shift detected
- **Primary model:** LightGBM or XGBoost baseline; CatBoost if high-cardinality categoricals
- **Ensemble:** hill climbing → stacking (Ridge or Logistic Regression on OOF)

### Evaluation Metrics (Replication)
- Leaderboard rank percentile (primary)
- Score delta vs. 2nd place
- Score delta vs. no-flowchart baseline

### Visualization
- Matplotlib / Seaborn for EDA
- scikit-learn `plot_tree` or Graphviz for flowchart
- Pandas styling for dataset summary tables

---

## Data Sources

### Primary: Kaggle Competitions
- **API endpoint:** `https://www.kaggle.com/api/v1/competitions/list`
- **Categories:** featured, research, playground, masters
- **Auth:** `~/.kaggle/kaggle.json`
- **Scraper:** `scripts/kaggle_scraper_v2.py` — outputs ranked shortlist with GitHub link detection

### Competition Writeups & Notebooks
- Kaggle Discussion pages (`/competitions/{ref}/discussion`)
- Kaggle Writeups pages (`/competitions/{ref}/writeups`)
- GitHub repos linked from winning writeups (primary source for `writeup_detail = 3`)
- Direct `.ipynb` uploads for manual parsing

### Reference Pipelines
- **KGMON Playbook 2026** (cdeotte) — `github.com/cdeotte/KGMON-Playbook-2026`  
  Template for full pipeline steps: EDA → FE → baselines → stacking → hill climbing → pseudo-label
- **s5e12 ensemble notebook** — hill climbing + Ridge stacking, distribution shift exploit
- **s6e3 ensemble notebook** — 4-level stacking, cuML logistic regression, 154 base models

### Inclusion Criteria
A competition is included if:
1. Data type is tabular (not image, audio, NLP, or pure graph)
2. Time series / forecasting competitions are **excluded**
3. Multi-table competitions are **excluded** unless the winning solution joins all tables into a single flat file before modeling
4. The selected solution (best-documented of top-3 finishers) uses a tree-based model (XGBoost / LightGBM / CatBoost) as primary or significant ensemble component
5. Competition is Playground Series season 3–5, or a Featured/Research competition that ended 2022 or later
6. At least a partial writeup exists (`writeup_detail ≥ 1`)

---

## Testing Strategy

### Dataset Validity
- **Codebook compliance:** all categorical fields use only allowed values; script flags violations
- **Completeness check:** flag any entry with > 40% `not described` fields — deprioritize in analysis
- **Inter-rater check:** solo project — use Claude as second reviewer for candidate curation; for dataset coding, self-audit a random 20% sample after a 1-week gap to check consistency

### Flowchart Logic
- **Coverage test:** does the flowchart produce a recommendation for every entry in the dataset?
- **Consistency test:** do entries with the same `data_type` + `feature_type_dominant` + `target_type` receive the same flowchart recommendation?
- **Accuracy test:** for entries where we know the winner's actual choice, does the flowchart agree?

### Replication Validation
- Submit flowchart-guided pipeline to a held-out Kaggle competition
- Target: finish in top 25% of leaderboard
- Compare against a naive baseline (default LightGBM, no FE, no encoding strategy)

---

## Timeline

| Week | Dates | Goals |
|------|-------|-------|
| **Week 1** | Apr 28 – May 4 | Run scraper v2, review candidate list, finalize inclusion criteria and schema variables |
| **Week 2** | May 5 – May 11 | Collect 15 entries (mix monetized + playground); fill dataset |
| **Week 3** | May 12 – May 18 | Collect remaining 15+ entries; reach 30 total; begin EDA notebook |
| **Week 4** | May 19 – May 25 | Complete EDA; frequency tables; cross-tabulations; first flowchart draft |
| **Week 5** | May 26 – Jun 1 | Refine flowchart; fit decision tree; validate logic against dataset |
| **Week 6** | Jun 2 – Jun 8 | Select held-out competition; run replication pipeline following flowchart |
| **Week 7** | Jun 9 – Jun 15 | Analyze replication results; write findings; produce final visualizations |
| **Week 8** | Jun 16 – Jun 22 | Final report draft; polish flowchart; prepare deliverables |
| **Buffer** | Jun 23 – Jun 24 | Final review and submission |

### Key Risks & Mitigations

**Risk:** Not enough `writeup_detail = 3` entries to fill FE columns.  
**Mitigation:** Prioritize GitHub-linked entries from scraper; use KGMON playbook as FE reference for cdeotte competitions.

**Risk:** Flowchart too vague to be actionable ("it depends").  
**Mitigation:** Scope to 2–3 key decision nodes (encoding strategy, CV strategy) rather than trying to cover the full pipeline.

**Risk:** Replication doesn't finish in time.  
**Mitigation:** Choose a currently-active Playground Series competition so submission is always open; replication is a deliverable goal, not a hard requirement.

**Risk:** Cross-sectional vs. non-cross-sectional split makes dataset too small per group.  
**Mitigation:** Keep both in one dataset with `data_type` as a covariate; analyze separately only if n ≥ 15 per group.
