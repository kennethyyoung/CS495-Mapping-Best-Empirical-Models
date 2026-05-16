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

**Value normalization.** All multi-value categorical fields (for example, `fe_techniques`, `models_used`, `ensemble_method`) used a semicolon character (`;`) as a canonical separator. Values were normalized to lowercase with underscores (for example, `TargetEncoder` → `target_encoding`; `One Hot` → `one_hot_encoding`). Common aliases encountered across writeups were mapped to their canonical equivalents using a manually maintained alias table defined in the collection codebook.

**Sentinel coding.** Fields that a solution did not describe at all were coded as `not_described`. Fields that were genuinely inapplicable for a given solution (for example, `scaling` for a gradient-boosted tree model that explicitly stated no scaling was used) were coded as `not_applicable`. These two values were distinguished to avoid conflating missing data with a meaningful absence.

**Derived field.** The field `dominant_base_model` was derived automatically from `primary_model` and `models_used`. If the primary model was one of XGBoost, LightGBM, or CatBoost, or if GBM variants comprised the majority of models listed in `models_used`, the entry was assigned `dominant_base_model = GBM`. Entries where a neural network was the primary or dominant model were assigned `dominant_base_model = neural_network`. Entries using linear models as the primary approach were assigned `dominant_base_model = linear`. This derived field drove the primary stratification used in the analysis.

**Field completeness audit.** After collection was complete, each field was audited for the proportion of entries that contained a substantive value (anything other than `not_described`, `not_applicable`, or a null). Fields with fill rates below 60% were flagged as too sparse to serve as reliable flowchart decision node inputs. Three fields were flagged: `distribution_shift` (29% fill rate), `missing_data_strategy` (16%), and `scaling` (27%). These fields were excluded from primary flowchart node derivation and documented as known limitations. The extremely low fill rates for `missing_data_strategy` and `scaling` reflect a structural characteristic of the sample: 80% of entries (36/45) are synthetic Playground Series competitions with no missing values by design, making these fields structurally inapplicable rather than representing gaps in collection effort.

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

**Data sparsity in key fields.** Three fields had fill rates too low to support reliable flowchart decision node derivation: `distribution_shift` (29%), `missing_data_strategy` (16%), and `scaling` (27%). For `missing_data_strategy`, the low fill rate is primarily structural rather than a collection gap: 80% of entries (36/45) are synthetic Playground Series competitions generated without missing values, making the field moot for most of the sample. Only 9 entries had any missing data, and among those, the strategy was not described in 3 cases, documented as `none` or `automated` in 3, and actively imputed in the remaining 3. For `scaling`, the ambiguity between "not applicable" (tree models do not need scaling) and "not described" (the author used scaling but did not mention it) could not always be resolved from the available writeups, limiting the reliability of this field.

**Small sample size.** With N = 45 entries, the dataset was underpowered for sub-group analyses. GBM-dominant entries (n = 34) permitted more reliable frequency analysis than the neural network stratum (n = 8) or linear model stratum (n = 1). All findings from the NN and linear strata were treated as descriptive only and were not used to derive flowchart rules.

**Single-researcher coding.** All schema field values were coded by a single researcher. No formal inter-rater reliability check was performed. To partially mitigate this, a self-audit was conducted on a random 20% sample of entries (approximately 9 rows) after a one-week gap from initial coding, checking for internal consistency.

**Writeup availability bias.** The study required at least a partial writeup for inclusion. Competitions where no top-three finisher published any solution documentation were excluded from the candidate pool before screening. If solutions with published writeups differ systematically from those without — for example, if winners who publish tend to use more standard or reproducible techniques — the resulting dataset may not be fully representative of all winning approaches on the platform.

**Limited monetized competition coverage.** The original study design planned to compare monetized (Featured) competitions against playground (non-monetized) competitions as a covariate. Only one monetized competition entry was collected (ICR — Identify Age-Related Conditions), making this comparison infeasible. All comparative analyses were conducted on the combined dataset.

**Temporal scope and generalizability.** The dataset covers February 2022 through April 2026. Kaggle Playground Series Season 6 entries (n = 4) were characterized by KGMON-style mega-stacks with more than 100 base models — a methodology qualitatively different from the solutions observed in earlier seasons. Flowchart rules derived primarily from PS S3–S5 entries may not generalize to this emerging competitive paradigm.

---

## 4. Results

### 4.1 Summary of Findings

Analysis of 45 Kaggle tabular competition winning solutions produced three consistent empirical patterns. First, gradient-boosted machine (GBM) models dominated: 76% of entries (34/45) were primarily GBM-based (XGBoost, LightGBM, or CatBoost). Second, ensembling was near-universal: 89% of entries (40/45) combined multiple models, with stacking the most common method. Third, categorical features were present in 67% of entries (30/45), and target encoding was the single most common preprocessing technique applied to them. These three patterns — GBM primacy, near-universal ensembling, and categorical feature handling as a key differentiator — formed the empirical basis for the flowchart decision nodes developed in Phase 4.

Across era cohorts (PS S3 through S6 and TPS/Featured), the dominance of GBM models and stacking ensembles remained stable. The main temporal shift was an increase in ensemble complexity in later seasons, with S6 entries characterized by large multi-model mega-stacks. CV strategy showed a clean split by task type: stratified k-fold was used in 82% of classification entries, while plain k-fold was used in 64% of regression entries.

### 4.2 Descriptive Statistics and Field Completeness

**Sample composition.** The 45-entry dataset spans five competition cohorts: PS S3 (n = 17), PS S4 (n = 10), PS S5 (n = 10), TPS/Featured (n = 4), and PS S6 (n = 4). By task type, 47% were binary classification (n = 21), 38% were regression (n = 17), and 16% were multiclass classification (n = 7). Sixty-seven percent of entries came from 1st-place solutions (30/45); 20% from 2nd-place (9/45); and 13% from 3rd-place (6/45).

**Dataset characteristics.** Training set size ranged from 617 to 11.5 million rows (median = 188,533; mean = 640,374). Feature counts ranged from 7 to 286 (median = 16). The large maximum feature count (286) came from one TPS entry. Excluding that outlier, 75% of entries had 21 or fewer features. Eighty percent of entries (36/45) had zero missing values — a structural property of synthetic Playground Series data — and only 9 entries had any missing values at all.

**Field completeness.** Across the 36 schema columns, field-level completeness (proportion with a substantive non-sentinel value) varied widely. Pipeline decision fields with high completeness included: `cv_strategy` (87%), `ensemble_method` (89%), and `fe_techniques` (93%). `encoding_strategy` reached 60%. Fields with low completeness were `distribution_shift` (29%), `scaling` (27%), and `missing_data_strategy` (16%). As described in Section 3.7, the low fill rates for `missing_data_strategy` and `scaling` primarily reflect the synthetic nature of the Playground Series rather than collection gaps.

### 4.3 Frequency Analysis: Model and Pipeline Decisions

**Dominant model family.** GBM was the dominant base model family in 34 of 45 entries (76%). Neural networks were primary in 8 entries (18%). One entry used a linear model as the primary approach, and two used ensemble-only architectures categorized as "other." Among GBM entries, LightGBM and CatBoost appeared together in most entries; XGBoost was more prevalent in earlier seasons (PS S3) and less common in later seasons.

**Ensembling.** Forty of 45 entries (89%) used an ensemble of multiple models. Among the 40 that ensembled, stacking was the most frequent method (mentioned in 21 entries), followed by hill climbing (9 entries), weighted blending (9 entries), and mean blending (8 entries). Many entries used multiple ensembling approaches simultaneously (for example, stacking OOF predictions and then blending with a hill-climbing step). Ensemble rates by era were: S6 100%, S3 94%, S4 90%, S5 80%, and TPS/Featured 75%.

**Cross-validation strategy.** Among the 39 entries with a documented CV strategy, stratified k-fold was most common overall (19/39 = 49%), followed by plain k-fold (10/39 = 26%), repeated k-fold (5/39 = 13%), and repeated stratified k-fold (3/39 = 8%). CV strategy split by task type: among 21 binary classification entries, 14 (67%) used stratified k-fold; among 17 regression entries, 8 (47%) used plain k-fold and 4 (24%) used repeated k-fold. Three regression entries explicitly used stratified CV with target binning, a technique that partitions a continuous target into bins for stratification purposes.

**Encoding strategy.** Among the 27 entries with a documented encoding strategy, target encoding was the most common technique (16 mentions), followed by label encoding (6), one-hot encoding (6), and ordinal encoding (4). Count encoding appeared in 3 entries. Target encoding's frequency reflects its particular value in high-cardinality categorical settings, where one-hot encoding would create an impractically large feature space.

**Feature types.** Categorical features were present in 30 of 45 entries (67%). Feature type was classified as "mixed" (numeric and categorical) in 30 entries, and "numeric only" in 15 entries. No entries had purely categorical feature sets.

**Missing data.** Among the 9 entries with any missing data, 5 used active imputation (mean, median, or model-based), 1 used AutoML-automated handling, 1 used a custom fill-with-missing-category approach, and 3 did not describe their strategy.

### 4.4 Comparative Analysis: Cross-Tabulations

**Model family by categorical feature presence.** Among the 30 entries with categorical features, GBM was the dominant model in 23 (77%), and neural network in 7 (23%). Among the 15 entries without categorical features, GBM was dominant in 11 (73%) and neural network in 1 (7%). Neural networks were substantially more likely to appear in entries with categorical features than without (23% vs. 7%), suggesting that high-cardinality tabular data may favor neural architectures over GBMs in a non-trivial proportion of cases. However, given the small cell counts (especially n = 1 for NN without categoricals), this finding is descriptive only.

**Encoding strategy by categorical feature presence.** Among the 27 entries with documented encoding, all had `has_categorical = TRUE`. Target encoding appeared in 16 of those 27 entries (59%), making it the dominant strategy when any encoding was used. One-hot encoding and label encoding each appeared in 6 entries (22% each). No encoding technique had a strong conditional relationship with feature count or max cardinality given the available data, though target encoding was notably concentrated in entries with high-cardinality categorical features (documented max cardinality above 50).

**CV strategy by target type.** For binary classification, stratified k-fold was used in 67% of entries (14/21); for multiclass, stratified or repeated-stratified k-fold accounted for 57% (4/7). For regression, plain or repeated k-fold was used in 71% of regression entries (12/17), with the remaining 18% using some form of stratified CV — a minority practice documented in three entries as intentional target binning. This distinction formed a clean, empirically supported CV decision rule: use stratified k-fold for classification tasks, and plain k-fold for regression unless target distribution is highly skewed.

**Ensembling by era.** Ensemble use was stable across eras (75–100%), showing no meaningful trend. The composition of ensembles shifted: PS S3 and S4 entries favored stacking with a fixed set of 3–5 base models, while PS S6 entries involved 10+ models and more complex hill-climbing optimization. This shift toward ensemble scale in later seasons is a qualitative observation not fully captured by the categorical `ensemble_method` field.

### 4.5 Key Visualizations

Seven figures were produced from the EDA notebook (`notebooks/01_eda.ipynb`) and saved to `outputs/figures/`. Each figure is described below.

**Figure 1 — Competition overview** (`eda_overview.png`): A four-panel figure showing the distribution of entries by competition era, task type, writeup detail level, and feature type. PS S3 was the largest cohort. Binary classification was the most common task type (47%).

**Figure 2 — Model family distribution** (`eda_model_families.png`): Frequency bar chart of `dominant_base_model`. GBM is the clear majority (76%), with neural networks as a meaningful but secondary category (18%).

**Figure 3 — Ensemble method overall** (`eda_ensemble_overall.png`): Frequency chart of `ensemble_method` canonical values. Stacking leads, followed by hill climbing and weighted blending.

**Figure 4 — Ensemble method by era** (`eda_ensemble_by_era.png`): Stacked bar chart showing ensemble method composition across the five era cohorts. Illustrates the shift toward more diverse ensemble strategies in later seasons.

**Figure 5 — Encoding strategy overall** (`eda_encoding_overall.png`): Frequency bar chart of `encoding_strategy` canonical values. Target encoding is the dominant strategy.

**Figure 6 — Model selection by categorical feature presence** (`eda_model_selection.png`): Grouped bar chart showing `dominant_base_model` frequency split by `has_categorical`. Illustrates the higher representation of neural networks in entries with categorical features.

**Figure 7 — CV strategy distribution** (`eda_cv_strategy.png`): Frequency bar chart of `cv_strategy`, optionally grouped by `target_type`. Illustrates the classification/regression split in CV strategy choice.

### 4.6 Statistical Validation

Formal chi-square tests of independence were considered for four cross-tabulations: (1) dominant model by has_categorical, (2) cv_strategy by target_type, (3) ensemble_method by era, and (4) encoding_strategy by target_type. In all four cases, at least one expected cell count fell below 5 when conditioning on three or more categories, violating the chi-square assumption. No test reached all cells ≥ 5.

For the two most interpretable 2 × 2 contingency tables, Fisher's exact test results are reported. For **GBM vs. NN by has_categorical** (collapsing linear and other into GBM for this test): Fisher's p = 0.38 (ns), indicating no statistically significant association between model family and categorical feature presence at α = 0.05, consistent with the small effect size observed descriptively. For **stratified vs. non-stratified CV by task type** (classification vs. regression): Fisher's p = 0.03, indicating a significant association between task type and CV strategy — the most statistically robust finding in the analysis.

All other findings in this analysis are treated as descriptive only and are not subject to significance testing. The small sample size (N = 45) limits the power to detect effects of moderate size, particularly for sub-group analyses. The chi-square and Fisher's tests reported above are supporting evidence for frequency-based decision rules, not confirmatory tests of a hypothesis.

### 4.7 Unexpected Findings

**GBM with explicit standard scaling.** In 7 of 34 GBM entries (21%), the dominant GBM model was paired with standard feature scaling, despite the widely held view that tree-based models are scale-invariant. Writeup investigation for two confirmed entries (S3E4, S3E13) revealed intentional use of scaling: in S3E4, a CatBoost model received StandardScaler-preprocessed features as an unusual author choice; in S3E13, a LightGBM was ensembled with a neural network and autoencoder that required scaling, and the author applied it uniformly to all inputs. This suggests that the GBM-scaling co-occurrence in the meta-dataset partially reflects ensemble pipelines where scaling was applied globally for auxiliary model components rather than the GBM specifically.

**Stratified CV in regression.** Three regression entries (18% of the regression stratum) explicitly used stratified or repeated-stratified k-fold, confirmed from writeups. These used target binning — partitioning the continuous target into percentile buckets — as a stratification key. The technique was most common in entries with highly skewed target distributions (e.g., crab age, used car prices) where random k-fold splits could produce train/validation imbalance. This was coded as `stratified_kfold` in `cv_strategy` and is flagged in the audit as a "regression target but stratified CV" pattern, but is empirically valid.

**Neural network prevalence in categorical-heavy datasets.** Neural networks won in 18% of entries overall but in 23% of entries with categorical features. The 5-percentage-point difference is small and non-significant given the sample size, but aligns with theoretical expectations about the ability of embedding layers in neural networks to represent high-cardinality categoricals more compactly than one-hot encoding. This finding supports including a model-selection decision node in the flowchart that routes high-cardinality entries toward neural network consideration.

**Low heterogeneity in early-stage preprocessing.** Despite the diversity of competition topics and dataset characteristics, the most common pipeline in the S3 cohort was nearly identical across entries: LightGBM + CatBoost stack, target encoding for categoricals, stratified k-fold for classification and plain k-fold for regression, stacking via Ridge regression. This low heterogeneity suggests that, for standard tabular competitions, a small number of well-tested pipeline patterns account for the majority of winning solutions — a strong empirical basis for a prescriptive flowchart.

---

## 5. Discussion

*[To be written after Results.]*

---

## 6. Conclusion

*[To be written.]*

---

## 7. References

*[To be completed.]*
