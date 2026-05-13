# PlanV2.md

## Project Overview

**Title:** Meta-Analysis of Winning Solutions in Kaggle Tabular Competitions
**Author:** youngyken
**Updated:** May 13, 2026

### Description

A systematic meta-analysis of top-finishing solutions across Kaggle tabular competitions, focused on identifying the preprocessing and feature engineering decisions that separate winning solutions from the rest. The study collects structured data from winning notebooks and writeups, encodes key pipeline decisions into a dataset, and synthesizes findings into an empirically-grounded decision flowchart for tabular ML pipelines.

The unit of analysis is one solution per competition: whichever of the top-3 finishers has the most complete writeup (`writeup_detail` score). `finish_rank` (1/2/3) is tracked as a covariate. Competitions are sourced from Playground Series seasons 3–6 and Featured competitions from 2022 onward. `n_teams` is tracked as a covariate for competitive intensity.

### Objectives

- Build a structured dataset of top-finishing competition solutions — **achieved: 45 entries, 36 columns**
- Identify which preprocessing and feature engineering decisions are most consistently associated with winning, using frequency tables and conditional cross-tabulations
- Produce a decision flowchart covering 2–3 key decision nodes that maps dataset characteristics → recommended pipeline decisions, backed by empirical evidence
- Validate the flowchart retrospectively: apply it to 3–5 held-out competitions and check whether recommendations match what winners actually did

---

## Current State (as of May 13, 2026)

| Phase | Status |
|---|---|
| Phase 1: Competition Discovery & Dataset Design | Complete |
| Phase 2: Data Collection | Complete — 45 entries, 36 columns |
| Phase 3: EDA & Analysis | **In progress** (Week 3) |
| Phase 4: Flowchart Construction | Not started |
| Phase 5: Retrospective Validation | Not started |
| Phase 6: Writeup & Deliverables | Not started |

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
matplotlib
seaborn
jupyter
```

### Kaggle API Setup

Place `kaggle.json` credentials at `C:\Users\YourName\.kaggle\kaggle.json`. Used for competition metadata, leaderboard data, and notebook pulls via `api.kernels_pull()`.

---

## Architecture

```
CS495-Mapping-Best-Empirical-Models/
│
├── data/
│   ├── raw/                          # topics.json + leaderboard.json per competition
│   ├── writeups/                     # Downloaded .ipynb notebooks + .txt writeup scrapes
│   ├── kaggle_candidates_v2.xlsx     # Scraped competition shortlist (46 candidates)
│   ├── extracted_fields.csv          # Title-based model signal extraction output
│   └── kaggle_meta_analysis.xlsx     # Main dataset — 45 entries, 36 columns
│
├── scripts/
│   ├── kaggle_scraper_v2.py          # Competition discovery & pre-filtering via Kaggle API
│   ├── fetch_solutions.py            # Collects topics.json + leaderboard.json (no body text)
│   ├── fill_data_stats.py            # Auto-populates n_features + pct_missing from train.csv
│   ├── fill_extended_stats.py        # Auto-populates n_rows + max_cardinality from train.csv
│   ├── build_bar_plots.py            # Generates EDA bar plots
│   ├── _pull_notebook.py             # Pulls a Kaggle notebook by kernel ref into data/writeups/
│   ├── _update_entry.py              # Fills/force-updates fields for a single entry
│   ├── _add_entry.py                 # Inserts a new row into kaggle_meta_analysis.xlsx
│   ├── _scan_notebook.py             # Keyword search across notebook cells (for large .ipynb files)
│   └── _read_row.py                  # Reads back a single entry for verification
│
├── notebooks/
│   ├── 01_eda.ipynb                  # Exploratory analysis of collected dataset
│   ├── 02_analysis.ipynb             # Cross-tabulations, frequency analysis
│   ├── 03_flowchart_logic.ipynb      # Decision rule extraction
│   └── 04_validation.ipynb           # Retrospective flowchart validation
│
├── outputs/
│   ├── flowchart.png
│   ├── figures/                      # EDA and analysis plots
│   └── report/
│
├── private/                          # Gitignored — rubrics, grading materials
├── PlanV2.md
├── PLAN.md
├── pyproject.toml
└── README.md
```

### Dataset: `kaggle_meta_analysis.xlsx`

Sheet: `Competition Data`. 45 rows × 36 columns. Key fields:

| Category | Fields |
|---|---|
| Identity | `competition_ref`, `finish_rank`, `winner_1st/2nd/3rd`, `writeup_detail`, `code_url` |
| Dataset characteristics | `n_rows`, `n_features`, `pct_missing`, `max_cardinality`, `has_categorical`, `feature_type_dominant`, `target_type`, `metric`, `distribution_shift` |
| Model | `dominant_base_model`, `primary_model`, `models_used`, `best_single_model` |
| Preprocessing | `missing_data_strategy`, `encoding_strategy`, `scaling`, `outlier_treatment` |
| Pipeline | `cv_strategy`, `hyperparameter_tuning`, `ensemble_method`, `original_data_usage` |
| Feature engineering | `fe_techniques` |
| Context | `n_teams`, `is_monetized` |

---

## What We Learned in Phase 2

### Data Collection Reality vs. Plan

The planned automated pipeline (`fetch_solutions.py` → `extract_fields.py` regex + Claude API pass) did not work as designed:

1. **Kaggle REST API does not expose discussion body text.** The `firstMessage.message` field exists in the schema but returns empty for every topic. All `solution_text.txt` files are empty.

2. **Winners do not submit notebooks as Kaggle kernels.** `kernels_list(competition=slug)` returned 0 results for every competition. Winners share code via GitHub links or attached files in discussion posts — none of which is accessible via the API.

3. **Manual review was the actual collection method.** Writeups were scraped as `.txt` files by browsing and saving competition pages. Notebooks were pulled either via `api.kernels_pull()` (when the winner published a public Kaggle notebook) or downloaded from GitHub links manually.

### Dataset Characteristics

- **45 entries** across PS S3 (19), PS S4 (6), PS S5 (8), PS S6 (4), Featured/TPS (8)
- **Temporal range:** Feb 2022 – Apr 2026
- **Target type:** binary (21), regression (17), multiclass (7)
- **Dominant base model:** GBM (34), neural_network (8), other (2), linear (1)
- **GBM dominance (75%)** means NN and linear branches of the flowchart rest on 8 and 1 entries respectively — descriptive only, not inferential

### Field Completeness

| Field | Filled | Notes |
|---|---|---|
| `dominant_base_model` | 45/45 | 100% — derived field |
| `fe_techniques` | 45/45 | 100% |
| `cv_strategy` | ~44/45 | 97% |
| `ensemble_method` | ~43/45 | 95% |
| `original_data_usage` | ~43/45 | 95% |
| `encoding_strategy` | ~40/45 | 88% |
| `hyperparameter_tuning` | ~40/45 | 88% |
| `scaling` | ~27/45 | 60% — sparse; GBM entries rarely mention it |
| `missing_data_strategy` | ~24/45 | 53% — sparse; same reason |
| `distribution_shift` | ~13/45 | 28% — too sparse for use as decision node input |

### Known Limitations

- **`scaling` and `missing_data_strategy` are too sparse** (60% / 53%) to build reliable flowchart decision nodes. Root cause: tree-based model authors typically omit these because GBMs don't require them. The missing values are likely `none` in most cases, not truly unknown.
- **`distribution_shift` is too sparse (28%)** to use as a CV strategy decision node input as originally planned.
- **Monetized competitions: 1/45 (ICR only).** The monetized vs. playground comparison planned in Phase 3 is not viable.
- **`max_cardinality` inflated** for some entries by ID-like columns with non-standard naming (e.g., may-2022 = 741K). Treat these as data artifacts in analysis.
- **S6 entries (s6e1–s6e4) are methodologically distinct**: KGMON-style mega-stacks with 100+ models. Worth tracking as a temporal covariate.

### Key Finding from Phase 2

Ensemble methods dominate throughout PS S3–S5. Single-model wins are the exception. Blending and stacking (including AutoGluon's internal 3-level stacking) appear across nearly every winning solution. AutoGluon and RAPIDS cuML stacking emerge as dominant strategies in S4–S5.

---

## Tasks & Milestones

### Phase 1: Competition Discovery & Dataset Design ✓
- [x] Design dataset schema (36 variables, codebook)
- [x] Build `kaggle_scraper_v2.py` for competition discovery
- [x] Establish inclusion/exclusion criteria (tabular, no time series, cross-sectional only)
- [x] Build Excel template with codebook
- [x] Confirm competition scope: PS S3–S6 + Featured/TPS 2022+ (46 candidates)

### Phase 2: Data Collection ✓
- [x] Screen 46 candidates — 45 entries coded, 1 excluded (nov-2022 meta-competition)
- [x] Manual review of writeups and notebooks for all entries
- [x] Fill schema fields; mark `not_described` honestly
- [x] Auto-populate `n_features`, `pct_missing`, `n_rows`, `max_cardinality` from train.csv
- [x] Auto-populate `metric` from Kaggle API
- [x] Add `dominant_base_model` derived field
- [x] Normalize all field values (canonical separators, case, aliases)
- [x] Code-check pass: verify `code_url` for 10 entries lacking code; apply field corrections

### Phase 3: EDA & Analysis
- [ ] Summary statistics: field completeness, target type distribution, model distribution
- [ ] Frequency tables: encoding strategies by `feature_type_dominant`, `target_type`, `max_cardinality`
- [ ] Cross-tabulation: `dominant_base_model` × dataset size (`n_rows`) and cardinality
- [ ] CV strategy patterns by `target_type` (distribution_shift too sparse — drop from decision node)
- [ ] Ensemble method breakdown by competition era (S3 vs. S4–S5 vs. S6)
- [ ] FE technique clustering by domain / target type
- [ ] Flag sparse fields as known limitations (scaling, missing_data_strategy, distribution_shift)
- [ ] Note: monetized vs. playground comparison is not viable (n=1 monetized)

### Phase 4: Flowchart Construction
- [ ] Define 2–3 decision nodes based on what the data can actually support
  - Primary model selection: GBM vs. NN vs. ensemble — conditioned on `n_rows`, `has_categorical`
  - Encoding strategy: conditioned on `max_cardinality` + `feature_type_dominant` + `target_type`
  - CV strategy: conditioned on `target_type` (drop `distribution_shift` — too sparse)
- [ ] Extract rules from conditional frequency tables
- [ ] Draft flowchart: dataset characteristics → pipeline decisions
- [ ] Validate logic against collected entries (coverage + consistency tests)
- [ ] Export as clean visual (Graphviz or draw.io)

### Phase 5: Retrospective Validation
- [ ] Select 3–5 held-out competitions not in the training set
- [ ] Apply flowchart using only pre-modeling dataset characteristics as inputs
- [ ] Compare flowchart recommendations against winner's actual decisions per node
- [ ] Compute per-node agreement rate
- [ ] Document failure modes and diagnose causes

### Phase 6: Writeup & Deliverables
- [ ] Final dataset (cleaned, documented)
- [ ] EDA visualizations
- [ ] Decision flowchart (publication-ready)
- [ ] Validation results and interpretation
- [ ] Final report / paper draft

---

## Methods & Models

### Data Collection (Actual)

1. `kaggle_scraper_v2.py` — pulls competition metadata; outputs `kaggle_candidates_v2.xlsx`
2. `fetch_solutions.py` — collects `topics.json` (title + vote count) and `leaderboard.json` per competition. **Body text and notebook download do not work** via API.
3. Manual writeup review — browse winner's discussion post, read prose, extract field values
4. `_pull_notebook.py` — pulls Kaggle notebook by `user/kernel-slug` via `api.kernels_pull()` when winner published a public notebook
5. `_scan_notebook.py` — keyword search across cells for notebooks too large to read directly
6. `_update_entry.py` — applies field updates (UPDATES: fill-if-empty; FORCE_UPDATES: overwrite)
7. `fill_data_stats.py` / `fill_extended_stats.py` — auto-populate dataset-level statistics from train.csv

### Analysis Techniques
- Frequency tables and conditional cross-tabulations (pandas `groupby` / `crosstab`)
- Chi-square tests where cell counts allow (n ≥ 5 per cell)
- `finish_rank` and `n_teams` as covariates
- AutoML entries (`automated` fields) handled as a separate stratum; excluded from flowchart node derivation where not informative
- GBM / NN / linear strata analyzed separately where n allows; NN and linear are descriptive only

### Flowchart Decision Nodes (Revised)

Originally planned: encoding strategy, CV strategy, missing data handling.

**Revised based on data reality:**

| Node | Input features | Viable? |
|---|---|---|
| Primary model selection | `n_rows`, `has_categorical`, competition era | Yes — GBM vs. NN |
| Encoding strategy | `max_cardinality`, `feature_type_dominant`, `target_type` | Yes |
| CV strategy | `target_type` | Yes (drop `distribution_shift` — 28% filled) |
| Missing data handling | `pct_missing` | Marginal (53% filled) — document as limitation |

### Retrospective Validation

For each held-out competition, apply flowchart using only pre-modeling dataset characteristics. Compare against what the winner actually did. Target: ≥ 70% agreement per node. Document all failures.

---

## Data Sources

### Primary: Kaggle Competitions
- PS S3 (Jan–Dec 2023): 19 entries
- PS S4 (Jan–Dec 2024): 6 entries
- PS S5 (Jan–Dec 2025): 8 entries
- PS S6 (Jan–Apr 2026): 4 entries
- TPS / Featured (Feb 2022 – Aug 2023): 8 entries

### Competition Writeups & Notebooks
- Writeups scraped manually from `kaggle.com/competitions/{ref}/writeups/`
- Notebooks pulled via `api.kernels_pull()` (Kaggle-hosted notebooks only)
- GitHub repos linked from winning writeups (manual download)

### Inclusion Criteria
1. Data type is tabular (not image, audio, NLP, or pure graph)
2. Time series / forecasting competitions excluded
3. Multi-table competitions excluded unless winner joins all tables into one flat file
4. Winner uses tree-based model (XGB/LGBM/CatBoost) as primary or significant ensemble component, **OR** neural network as primary model (NN-winning entries inform the model-selection decision node)
5. PS S3–S6, or Featured/TPS ending 2022 or later
6. At least a partial writeup exists (`writeup_detail ≥ 1`)
7. Competition task involves actual feature data and model selection (excluded: nov-2022 TPS, which was a meta-blending task with no feature data)

---

## Timeline

| Week | Dates | Goals | Status |
|------|-------|-------|--------|
| **Week 1** | Apr 28 – May 4 | Scraper, candidate list, schema design | ✓ Complete |
| **Week 2** | May 5 – May 11 | Manual data collection, backfill, schema extension, normalization | ✓ Complete (45 entries, 36 cols) |
| **Week 3** | May 12 – May 18 | Phase 3 EDA — frequency tables, cross-tabs, field completeness audit | In progress |
| **Week 4** | May 19 – May 25 | Phase 4 — flowchart draft; extract decision rules from frequency tables |  |
| **Week 5** | May 26 – Jun 1 | Refine flowchart; validate logic against training entries; select held-out competitions |  |
| **Week 6** | Jun 2 – Jun 8 | Phase 5 retrospective validation — apply flowchart; compute agreement rates |  |
| **Week 7** | Jun 9 – Jun 15 | Final report, polish flowchart, all deliverables — **hard deadline Jun 16** |  |

---

## Key Risks & Mitigations

**Risk:** `scaling` and `missing_data_strategy` too sparse (53–60%) to support reliable flowchart nodes.
**Mitigation:** Exclude from primary flowchart nodes. Document as a known limitation. Note that sparse values in GBM-dominant entries likely mean "not applicable" rather than "unknown."

**Risk:** GBM dominance (75%) makes NN and linear branches of the flowchart statistically thin.
**Mitigation:** Treat NN branch as descriptive (n=8). Focus inferential analysis on GBM sub-sample. Label NN branch clearly as "based on limited evidence."

**Risk:** Flowchart too vague to be actionable ("it depends").
**Mitigation:** Scope to 2–3 well-supported decision nodes. Concrete thresholds (e.g., cardinality > X → target encoding) are the goal, not just directional findings.

**Risk:** Retrospective validation agreement rate is low.
**Mitigation:** Diagnose by decision node. A low rate on one node is informative and documentable. Low overall agreement signals dataset is too small or rules are too coarse — both are valid findings worth reporting.

**Risk:** S6 entries (KGMON mega-stacks) distort ensemble method distribution.
**Mitigation:** Track competition era as a covariate. Report S3–S5 and S6 distributions separately where relevant.
