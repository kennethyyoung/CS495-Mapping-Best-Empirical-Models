# Mapping Best Empirical Models: A Meta-Analysis of Winning Solutions in Kaggle Tabular Competitions

**Author:** Kenneth Young  
**Course:** CS495 Capstone in Data Science — Bellevue College  
**Instructor:** Pedro Albuquerque, PhD  
**Date:** May 2026

---

## Abstract

*[To be written after Results and Discussion are complete.]*

---

## 1. Introduction

*[To be written.]*

---

## 2. Background and Related Work

*[To be written.]*

---

## 3. Methodology

### 3.1 Research Design

This study employed a quantitative observational meta-analysis design. Rather than collecting new experimental data, the research systematically aggregated and analyzed publicly available solution writeups and notebooks from completed Kaggle tabular machine learning competitions. The goal was to identify which preprocessing and feature engineering decisions are most consistently associated with winning solutions, and to synthesize those patterns into an empirically grounded decision flowchart.

The unit of analysis was one competition solution per competition: whichever of the top-three finishers had the most complete publicly available writeup, scored on a three-point `writeup_detail` scale (1 = discussion post only, 2 = notebook without full explanation, 3 = GitHub repository with detailed documentation). The finishing rank of the selected solution (1st, 2nd, or 3rd) was recorded as a covariate (`finish_rank`) to account for any systematic differences across rank positions. This selection rule reduced writeup-availability bias without increasing data collection effort. The analysis was cross-sectional: each competition contributed one entry to the dataset regardless of the number of active seasons or competitors.

The research was exploratory and descriptive rather than confirmatory. The primary outputs were frequency distributions, conditional cross-tabulations, and a derived decision flowchart — not hypothesis tests of a predefined causal model. Chi-square tests were applied post hoc where cell counts permitted to assess whether observed associations were statistically distinguishable from chance.

### 3.2 Data Collection

**Source and scope.** Competition solutions were drawn from the Kaggle platform (kaggle.com), a public competitive machine learning environment. The study covered Playground Series seasons 3 through 6 (January 2023 – April 2026) and Featured and Tabular Playground Series (TPS) competitions that concluded in February 2022 or later. The resulting dataset comprised 45 entries across five competition cohorts: PS S3 (n = 19), PS S4 (n = 6), PS S5 (n = 8), PS S6 (n = 4), and Featured/TPS (n = 8). The temporal range spanned from February 2022 to April 2026.

**Inclusion and exclusion criteria.** A competition was included if (1) the competition data type was tabular (image, audio, NLP, and pure graph competitions were excluded); (2) the task was not a time series or forecasting problem; (3) the competition was not a multi-table join task unless the winning solution collapsed all tables into a single flat file before modeling; (4) at least a partial writeup existed for one of the top-three finishers (`writeup_detail ≥ 1`); and (5) the selected solution used a tree-based model (XGBoost, LightGBM, or CatBoost) as a primary or significant ensemble component, or a neural network as the primary model. Neural network-winning solutions were retained in scope because model selection between tree-based and neural approaches is itself a flowchart decision node. One competition was excluded: the November 2022 TPS meta-blending competition, which involved no feature data and no model selection task.

**Data format and size.** The final dataset was stored as a single Excel workbook (`data/kaggle_meta_analysis.xlsx`), sheet `Competition Data`, with 45 rows and 36 columns. Column categories included competition identity fields (`competition_ref`, `finish_rank`, `writeup_detail`, `code_url`), dataset characteristics (`n_rows`, `n_features`, `pct_missing`, `max_cardinality`, `has_categorical`, `feature_type_dominant`, `target_type`, `metric`, `distribution_shift`), model fields (`dominant_base_model`, `primary_model`, `models_used`, `best_single_model`), preprocessing fields (`missing_data_strategy`, `encoding_strategy`, `scaling`, `outlier_treatment`), pipeline fields (`cv_strategy`, `hyperparameter_tuning`, `ensemble_method`, `original_data_usage`), feature engineering (`fe_techniques`), and context covariates (`n_teams`, `is_monetized`). A companion `Codebook` sheet defined the allowed canonical values for every categorical field.

**Access method.** Competition metadata (competition name, slug, evaluation metric, and leaderboard) was collected via the Kaggle REST API (Python package `kaggle` v1.6) using a registered Kaggle account. Discussion post titles and vote counts were retrieved via `api.competitions_list()` and `api.kernel_list()`; however, the Kaggle REST API does not expose the body text of discussion posts, and `kernels_list()` returned zero results for every competition slug, because most winning solutions were shared via GitHub links or file attachments rather than as published Kaggle kernels. As a result, the actual collection of solution content required extensive manual review: writeups were read directly from competition discussion pages and writeup tabs on Kaggle, and notebooks were either pulled via `api.kernels_pull()` when the winner had published a public Kaggle kernel, or downloaded manually from GitHub links provided in winning writeups. Dataset-level statistics (`n_rows`, `n_features`, `pct_missing`, `max_cardinality`) were auto-populated by downloading each competition's `train.csv` file via the Kaggle API and computing summary statistics in Python.

**Licensing.** All competition writeups, notebooks, and solution discussions are public submissions on Kaggle, freely viewable without authentication. Competition datasets are provided under each competition's own data terms; the study used only metadata computed from those datasets (row counts, column counts, missing value rates) rather than the raw data itself.

### 3.3 Data Preprocessing

Preprocessing in this study referred to the cleaning and normalization steps applied to `kaggle_meta_analysis.xlsx` — the meta-dataset of collected competition solutions — rather than to any machine learning input data.

**Value normalization.** All multi-value categorical fields (for example, `fe_techniques`, `models_used`, `ensemble_method`) used a pipe character (`|`) as a canonical separator. Values were normalized to lowercase with underscores (for example, `TargetEncoder` → `target_encoding`; `One Hot` → `one_hot_encoding`). Common aliases encountered across writeups were mapped to their canonical equivalents using a manually maintained alias table defined in the collection codebook.

**Sentinel coding.** Fields that a solution did not describe at all were coded as `not_described`. Fields that were genuinely inapplicable for a given solution (for example, `scaling` for a gradient-boosted tree model that explicitly stated no scaling was used) were coded as `not_applicable`. These two values were distinguished to avoid conflating missing data with a meaningful absence.

**Derived field.** The field `dominant_base_model` was derived automatically from `primary_model` and `models_used`. If the primary model was one of XGBoost, LightGBM, or CatBoost, or if GBM variants comprised the majority of models listed in `models_used`, the entry was assigned `dominant_base_model = GBM`. Entries where a neural network was the primary or dominant model were assigned `dominant_base_model = neural_network`. Entries using linear models as the primary approach were assigned `dominant_base_model = linear`. This derived field drove the primary stratification used in the analysis.

**Field completeness audit.** After collection was complete, each field was audited for the proportion of entries that contained a substantive value (anything other than `not_described`, `not_applicable`, or a null). Fields with fill rates below 60% were flagged as too sparse to serve as reliable flowchart decision node inputs. Three fields were flagged: `distribution_shift` (28% fill rate), `missing_data_strategy` (53%), and `scaling` (60%). These fields were excluded from primary flowchart node derivation and documented as known limitations.

**Outlier annotation.** The `max_cardinality` field was found to be inflated in several entries because ID-like columns with non-standard naming conventions (for example, a row-identifier encoded as a date string with high cardinality, up to 741,000 unique values in one case) were included in the cardinality scan. These values were annotated as data artifacts rather than imputed or removed, to preserve the raw provenance of each entry.

**Exclusion of one entry.** The November 2022 TPS competition was excluded from the final dataset because its task involved blending pre-generated model predictions rather than training on feature data — making all preprocessing and feature engineering fields inapplicable. This exclusion reduced the candidate pool from 46 to 45 entries.

**Train/test split.** No train/test split was applied to the meta-dataset itself. Instead, 3–5 held-out competitions — not included in the 45-entry analysis set — were reserved for retrospective validation of the derived decision flowchart in Phase 5.

### 3.4 Analytical Methods

The analytical strategy consisted of three sequential stages: descriptive frequency analysis, conditional cross-tabulation, and retrospective flowchart validation.

**Frequency analysis.** Summary statistics were computed for all categorical and continuous fields using `pandas` `DataFrame.value_counts()` and `DataFrame.describe()`. Frequency tables reported the count and proportion of each canonical value per field, with `not_described` and `not_applicable` tallied separately so that fill rates were transparent.

**Conditional cross-tabulation.** The primary analytical technique was `pandas.crosstab()` applied to pairs of fields hypothesized to be associated based on domain knowledge of machine learning practice. Key cross-tabulations included: `encoding_strategy` grouped by `feature_type_dominant`, `max_cardinality` binned to low/medium/high, and `target_type`; `cv_strategy` grouped by `target_type`; `dominant_base_model` grouped by `n_rows` quartile and `has_categorical`; and `ensemble_method` grouped by competition era (PS S3, PS S4–S5, PS S6). The `finish_rank` and `n_teams` covariates were examined to check whether findings were stable across competitive intensity and rank position.

**Statistical significance.** Chi-square tests of independence (`scipy.stats.chi2_contingency`) were applied to cross-tabulations where all cells had expected counts of at least 5. Where cell counts were below this threshold — which was common given N = 45 — Fisher's exact test or descriptive language only were used, and the finding was flagged as exploratory.

**Decision rule extraction.** Flowchart decision rules were extracted by inspection of conditional frequency distributions rather than by fitting a formal classification model on the meta-dataset. For each proposed decision node, the modal value of the output field within each stratum of the conditioning variable was taken as the flowchart recommendation. Nodes were accepted only where the modal value accounted for at least 60% of substantive (non-missing) entries within a stratum, providing a clear empirical basis for the recommendation.

**Retrospective validation.** To evaluate the generalizability of the derived flowchart, it was applied to 3–5 held-out competition solutions not included in the 45-entry analysis set. For each held-out entry, only pre-modeling dataset characteristics (those knowable before model training begins, such as `n_rows`, `n_features`, `target_type`, `max_cardinality`) were used as flowchart inputs. The flowchart output — a set of recommended pipeline decisions per node — was compared against the winner's actual recorded decisions. The primary evaluation metric was the per-node agreement rate: the proportion of held-out entries for which the flowchart recommendation matched the winner's actual choice at that node. A target agreement rate of 70% or higher was established as the threshold for treating a node's rule as empirically supported.

### 3.5 Evaluation Metrics

**Primary metric.** The primary evaluation metric was the per-node agreement rate in retrospective validation, defined as the number of held-out entries where the flowchart recommendation matched the winner's recorded decision, divided by the total number of held-out entries for that node. A target of ≥ 70% per node was set a priori as the threshold for treating a flowchart rule as actionable. Agreement rates below this threshold were interpreted as evidence that the rule was too coarse or that the underlying dataset characteristics were insufficient to discriminate between approaches.

**Secondary metrics.** Secondary metrics included: (1) the overall field completeness rate per column, reported as the proportion of entries with a substantive value, to characterize the reliability of the dataset; (2) chi-square test statistics and p-values for association tests between conditioning variables and pipeline decision variables, reported as supporting evidence for frequency-based decision rules; and (3) flowchart coverage — the proportion of entries in the analysis set for which the flowchart produced a recommendation at each node without encountering a missing or ambiguous conditioning value.

**Visualizations.** The following visualizations were planned to accompany the results: (1) bar plots of frequency distributions for each major categorical field; (2) cross-tabulation heatmaps showing the conditional distribution of each pipeline decision field across conditioning variable strata; (3) a field completeness chart showing fill rates across all 36 schema fields; and (4) the final decision flowchart as a directed graph, exported as a PNG via Graphviz or Matplotlib.

**Statistical significance threshold.** A significance level of α = 0.05 was used for all chi-square tests. Given the exploratory nature of the analysis and the small sample size, p-values were reported as supporting evidence rather than as definitive tests of hypotheses.

### 3.6 Tools and Technologies

The following tools and technologies were used throughout the project:

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.13 | Primary programming language |
| Poetry | 1.x | Dependency and environment management |
| pandas | 2.2 | Data manipulation, cross-tabulations, frequency tables |
| numpy | 2.0 | Numerical operations |
| openpyxl | 3.1 | Reading and writing the Excel dataset |
| matplotlib | 3.9 | Visualization (bar plots, flowchart export) |
| seaborn | 0.13 | Statistical visualization (heatmaps) |
| scikit-learn | 1.5 | Chi-square test utilities; future flowchart visualization |
| kaggle (API) | 1.6 | Competition metadata retrieval, notebook downloads |
| requests | 2.32 | HTTP requests for supplemental data fetching |
| beautifulsoup4 | 4.12 | HTML parsing for supplemental page scraping |
| Jupyter | 1.1 | Exploratory analysis notebooks |
| Git / GitHub | — | Version control and submission |
| Claude Code CLI | claude-sonnet-4-6 | AI assistant for development support throughout the project |

All Python dependencies were managed through Poetry and are specified in `pyproject.toml` at the project root. The project was developed on Windows 11 Pro using PowerShell as the primary shell environment.

### 3.7 Limitations

**Data sparsity in key fields.** Three fields had fill rates too low to support reliable flowchart decision node derivation: `distribution_shift` (28%), `missing_data_strategy` (53%), and `scaling` (60%). For tree-based model entries, the most common base model family in the dataset, low fill rates in preprocessing fields are likely attributable to authors omitting steps that gradient-boosted tree models do not require rather than to true data absence. However, this ambiguity between "not applicable" and "not described" could not always be resolved from the available writeups, limiting the reliability of these fields.

**Small sample size.** With N = 45 entries, the dataset was underpowered for sub-group analyses. GBM-dominant entries (n = 34) permitted more reliable frequency analysis than the neural network stratum (n = 8) or linear model stratum (n = 1). All findings from the NN and linear strata were treated as descriptive only and were not used to derive flowchart rules.

**Single-researcher coding.** All schema field values were coded by a single researcher. No formal inter-rater reliability check was performed. To partially mitigate this, a self-audit was conducted on a random 20% sample of entries (approximately 9 rows) after a one-week gap from initial coding, checking for internal consistency.

**Writeup availability bias.** The study required at least a partial writeup for inclusion. Competitions where no top-three finisher published any solution documentation were excluded from the candidate pool before screening. If solutions with published writeups differ systematically from those without — for example, if winners who publish tend to use more standard or reproducible techniques — the resulting dataset may not be fully representative of all winning approaches on the platform.

**Limited monetized competition coverage.** The original study design planned to compare monetized (Featured) competitions against playground (non-monetized) competitions as a covariate. Only one monetized competition entry was collected (ICR — Identify Age-Related Conditions), making this comparison infeasible. All comparative analyses were conducted on the combined dataset.

**Temporal scope and generalizability.** The dataset covers February 2022 through April 2026. Kaggle Playground Series Season 6 entries (n = 4) were characterized by KGMON-style mega-stacks with more than 100 base models — a methodology qualitatively different from the solutions observed in earlier seasons. Flowchart rules derived primarily from PS S3–S5 entries may not generalize to this emerging competitive paradigm.

---

## 4. Results

*[To be written. Due May 18, 2026.]*

### 4.1 Summary of Findings

*[Placeholder.]*

### 4.2 Descriptive Statistics and Field Completeness

*[Placeholder.]*

### 4.3 Frequency Analysis: Model and Pipeline Decisions

*[Placeholder.]*

### 4.4 Comparative Analysis: Cross-Tabulations

*[Placeholder.]*

### 4.5 Key Visualizations

*[Figures to be referenced here from `outputs/figures/`.]*

### 4.6 Statistical Validation

*[Placeholder.]*

### 4.7 Unexpected Findings

*[Placeholder.]*

---

## 5. Discussion

*[To be written after Results.]*

---

## 6. Conclusion

*[To be written.]*

---

## 7. References

*[To be completed.]*
