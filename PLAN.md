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
- Validate the flowchart retrospectively: apply it to 3–5 held-out competitions not in the training set and check whether its recommendations match what those winners actually did

---

## Environment Setup

### Requirements

- Python 3.13
- Poetry for environment and dependency management

### Core Dependencies (`pyproject.toml`)

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
│   ├── classify_candidates.py      # Adds keep/exclude/verify labels to candidate shortlist
│   ├── fetch_solutions.py          # Scrapes writeup text & downloads top notebooks into data/raw/
│   ├── extract_fields.py           # Regex + Claude API pass to pre-fill schema fields from raw material
│   ├── write_entries.py            # Writes hand-coded entries into kaggle_meta_analysis.xlsx
│   └── build_bar_plots.py          # Generates EDA bar plots from dataset
│
├── notebooks/
│   ├── 01_eda.ipynb                # Exploratory analysis of collected dataset
│   ├── 02_analysis.ipynb           # Cross-tabulations, frequency analysis
│   ├── 03_flowchart_logic.ipynb    # Decision tree / rule extraction
│   └── 04_validation.ipynb         # Retrospective flowchart validation on held-out entries
│
├── outputs/
│   ├── flowchart.png               # Final decision flowchart (exported)
│   ├── figures/                    # All EDA and analysis plots
│   └── report/                     # Final writeup
│
├── PLAN.md
├── pyproject.toml
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
- [x] Finalize variable list (confirmed: `distribution_shift`, `feature_type_dominant`, `finish_rank`, `n_teams`, `models_used`, `best_single_model`, `hyperparameter_tuning`, `original_data_usage`)
- [x] Decide on cross-sectional only vs. mixed scope — **cross-sectional only confirmed**
- [x] Confirm competition scope: PS3–PS5 + Featured 2022+ (46 candidates after screening)

### Phase 2: Data Collection
- [x] Identify 30+ candidate competitions from shortlist — **46 candidates remain after tabular + time series screening**
- [x] Prioritize `writeup_detail = 3` entries (GitHub repo linked)
- [ ] Collect 10 monetized competition entries — **1 collected (ICR); Featured comps have sparse writeups; deprioritized**
- [x] Collect 20+ playground series entries — **33 Playground Series entries collected**
- [x] Fill all schema fields per entry; mark `not described` honestly — **35 entries coded**
- [x] Score `writeup_detail` (1/2/3) for each entry
- [x] Flag entries with `distribution_shift = TRUE`
- [ ] Run `extract_fields.py` regex pass on downloaded notebooks to auto-fill `cv_strategy`, `encoding_strategy`, `scaling`, `missing_data_strategy`, `hyperparameter_tuning`
- [ ] Run `extract_fields.py` Claude API pass on `solution_text.txt` to auto-fill `fe_techniques`, `original_data_usage`, `models_used`, `ensemble_method`
- [ ] Spot-check low-confidence extractions and manually fill remaining `not_described` fields for `writeup_detail = 3` entries (~14)

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

### Phase 5: Retrospective Validation
- [ ] Select 3–5 held-out competitions not in the training set
- [ ] Apply flowchart to each: given their dataset characteristics, what does the flowchart recommend?
- [ ] Compare flowchart recommendation against what the winner actually did for each decision node
- [ ] Compute agreement rate per decision node (encoding strategy, CV strategy, missing data handling)
- [ ] Document failure modes: cases where flowchart disagrees with winner and why

### Phase 6: Writeup & Deliverables
- [ ] Final dataset (cleaned, documented)
- [ ] EDA visualizations
- [ ] Decision flowchart (publication-ready)
- [ ] Replication results and interpretation
- [ ] Final report / paper draft

---

## Methods & Models

### Data Collection
1. `kaggle_scraper_v2.py` — pulls competition metadata via Kaggle API into `kaggle_candidates_v2.xlsx`
2. `classify_candidates.py` — labels each candidate keep/exclude/verify based on tabular + time-series screen
3. `fetch_solutions.py` — scrapes top-voted discussion topics for solution writeups (saves to `data/raw/{ref}/solution_text.txt`), downloads top-5 notebooks via Kaggle kernels API (saves to `data/raw/{ref}/notebooks/`)
4. `extract_fields.py` — two-pass automated field extraction:
   - **Pass 1 (regex/AST on notebook code):** scans `.ipynb` files for Python patterns that map directly to schema fields — `StratifiedKFold`/`KFold`/`GroupKFold` → `cv_strategy`; `get_dummies`/`TargetEncoder`/`OrdinalEncoder` → `encoding_strategy`; `StandardScaler`/`log1p`/RankGauss → `scaling`; `fillna`/`SimpleImputer`/`dropna` → `missing_data_strategy`; `optuna`/`RandomizedSearchCV` → `hyperparameter_tuning`
   - **Pass 2 (Claude API on writeup text):** sends `solution_text.txt` + notebook markdown cells to Claude with the codebook as context; extracts `fe_techniques`, `original_data_usage`, `ensemble_method`, `models_used`, `best_single_model`; outputs JSON with a `confidence` flag per field; low-confidence fields flagged for human review
5. Human spot-check — review flagged low-confidence extractions; manually fill remaining `not_described` fields; `writeup_detail = 1` entries with minimal text still require full manual review
6. `write_entries.py` — writes completed entries into `kaggle_meta_analysis.xlsx`

### Analysis Techniques
- Frequency tables and conditional cross-tabulations (pandas `groupby` / `crosstab`)
- Chi-square tests where cell counts allow (n ≥ 5 per cell)
- Sensitivity analysis: does the flowchart change with monetized-only entries?
- `finish_rank` and `n_teams` as covariates to check whether findings hold across competitive intensity

### Retrospective Validation
For each held-out competition, the flowchart is applied using only the competition's dataset characteristics (known before modeling) as inputs. The flowchart output — a set of recommended pipeline decisions — is then compared against what the winner actually did.

Decision nodes evaluated:
- `encoding_strategy` given `feature_type_dominant` + `target_type` + cardinality
- `cv_strategy` given `distribution_shift`
- `missing_data_strategy` given `pct_missing` + `data_type`
- `primary_model` / `best_single_model` given dataset characteristics

### Evaluation Metrics (Validation)
- Agreement rate per decision node: % of held-out entries where flowchart recommendation matches winner's actual choice
- Overall agreement rate across all nodes
- Failure mode analysis: which dataset characteristics cause the flowchart to disagree, and what did the winner do instead

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
4. The selected solution (best-documented of top-3 finishers) uses a tree-based model (XGBoost / LightGBM / CatBoost) as primary or significant ensemble component, OR uses a neural network as primary model — NN-winning solutions are in scope because model selection (tree vs. NN vs. ensemble) is itself a flowchart decision node
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

### Retrospective Validation
- For each held-out competition, apply the flowchart using only pre-modeling dataset characteristics as inputs
- Compare flowchart recommendations against the winner's actual pipeline decisions for each decision node
- Target: ≥ 70% agreement rate across decision nodes
- Document cases where the flowchart disagrees and diagnose whether the disagreement reflects a gap in the rules or a genuinely unusual competition

---

## Timeline

| Week | Dates | Goals |
|------|-------|-------|
| **Week 1** | Apr 28 – May 4 | Run scraper v2, review candidate list, finalize inclusion criteria and schema variables |
| **Week 2** | May 5 – May 11 | Build `extract_fields.py`; run regex + Claude API pass; spot-check extractions; complete Phase 2 backfill |
| **Week 3** | May 12 – May 18 | Phase 3 EDA — frequency tables, cross-tabs, monetized vs. playground comparison |
| **Week 4** | May 19 – May 25 | Phase 4 — flowchart draft; extract decision rules from conditional frequency tables |
| **Week 5** | May 26 – Jun 1 | Refine flowchart; validate logic against training entries; select 3–5 held-out competitions |
| **Week 6** | Jun 2 – Jun 8 | Phase 5 retrospective validation — apply flowchart to held-out entries; compute agreement rates |
| **Week 7** | Jun 9 – Jun 15 | Final report, polish flowchart, prepare all deliverables — **hard deadline Jun 16** |

### Key Risks & Mitigations

**Risk:** Not enough `writeup_detail = 3` entries to fill FE columns.  
**Mitigation:** Prioritize GitHub-linked entries from scraper; use KGMON playbook as FE reference for cdeotte competitions.

**Risk:** Flowchart too vague to be actionable ("it depends").  
**Mitigation:** Scope to 2–3 key decision nodes (encoding strategy, CV strategy) rather than trying to cover the full pipeline.

**Risk:** Retrospective validation agreement rate is low, undermining the flowchart's credibility.  
**Mitigation:** Diagnose failure modes by decision node — a low rate on one node (e.g., encoding) is informative and documentable; it doesn't invalidate the whole flowchart. Low overall agreement likely signals the dataset is too small or the rules are too coarse, both of which are valid findings.

**Risk:** Cross-sectional vs. non-cross-sectional split makes dataset too small per group.  
**Mitigation:** Keep both in one dataset with `data_type` as a covariate; analyze separately only if n ≥ 15 per group.
