# Project Session Log

Running log of decisions, attempts, failures, and pivots.
Intended as source material for a project writeup or reflection article.

---

## Session 1–2 — Project Setup & Competition Discovery

**What we did:**
- Designed the dataset schema: ~28 variables covering model choice, preprocessing decisions (encoding strategy, CV strategy, missing data handling, scaling), ensemble methods, and feature engineering techniques
- Built `kaggle_scraper_v2.py` to pull competition metadata via the Kaggle API and pre-filter to tabular competitions
- Established inclusion/exclusion criteria: Playground Series S3–S5 + Featured competitions from 2022 onward; excluded time series, NLP, image competitions
- Built `kaggle_candidates_v2.xlsx` with 46 candidates after screening
- Hand-coded 35 competition entries into `kaggle_meta_analysis.xlsx`

**What worked:**
- The Kaggle API's competition list endpoint (`/api/v1/competitions/list`) worked cleanly for discovery
- Manually coding entries from discussion posts was feasible for model-level fields (`models_used`, `ensemble_method`, `fe_techniques`) — most winning posts name the model family explicitly

**What didn't work / open gaps:**
- Preprocessing fields (`encoding_strategy`, `cv_strategy`, `missing_data_strategy`, `scaling`) require reading actual notebook code, not just the prose writeup — these ended up mostly blank in the initial coding pass
- No `writeup_url` was recorded during coding, so source URLs were lost

---

## Session 3 — Automated Scraping Attempt

**What we tried:**
Built `fetch_solutions.py` to automate three things:
1. Fetch solution writeup titles from the Kaggle discussion API
2. Scrape writeup body text from each topic
3. Download winner notebooks via the Kaggle kernels API

**What didn't work:**

**Problem 1 — Topic body text:**
The Kaggle REST API (`/api/v1/competitions/{slug}/topics/{id}`) returns topic metadata but not the post body. The `firstMessage.message` field exists in the schema but comes back empty. No public endpoint exposes the full discussion body text. Result: all `solution_text.txt` files are empty.

**Problem 2 — Winner notebook download:**
`kernels_list(competition=slug, user=winner_name)` returned 0 notebooks for every competition tested. Winners typically share code via GitHub links inside discussion posts, not as Kaggle notebook submissions tagged to the competition. The API can't find what isn't there.

**Problem 3 — Leaderboard API bug:**
`competition_leaderboard_view(slug, page=1, page_size=3)` — the `page=1` kwarg is invalid and silently caused the call to fail, returning empty arrays. All 42 `leaderboard.json` files were empty. Fixed by removing `page=1`.

**Outcome:**
Scraper successfully collected `topics.json` (discussion titles + vote counts) for all 42 competitions, and `leaderboard.json` (winner names) after the bug fix. But no writeup body text and no notebooks. The automated extraction pipeline (`extract_fields.py`) was built but couldn't run meaningfully without body text.

---

## Session 4 — Phase A: Manual Title-Based Extraction

**What we did:**
Since the scraper couldn't get writeup text, we pivoted to extracting model signals directly from solution topic *titles* — which the scraper did collect successfully.

Read all 42 `topics.json` files and inferred:
- `primary_model` (xgboost / catboost / ensemble_mixed / automl / unknown)
- `uses_ensemble`, `ensemble_type`, `uses_nn`
- `key_techniques`
- `confidence` (high / medium / low)

Wrote results to `data/extracted_fields.csv`.

**What worked:**
- Title-based inference is surprisingly effective. Titles like "1st Place — One CatBoost Is All You Need" or "1st Place — RAPIDS cuML Stack 3 Levels" give explicit model signal with high confidence.
- ~19/42 competitions yielded high-confidence extractions from titles alone.

**What didn't work:**
- ~11 competitions had 1st-place writeups present but the title gave no model info (e.g., "1st place. That was unexpected..."). Coded as `unknown`.
- Preprocessing fields (encoding, CV, scaling) are essentially never mentioned in titles. Title extraction only covers model-level signals.

**Key finding from title analysis:**
Ensemble approaches (blending, stacking, hill climbing) dominate across S3–S5. Single-model wins exist but are the exception. AutoGluon and RAPIDS cuML stacking emerge as dominant in S4–S5.

---

## Session 5 — Dataset Completeness Audit & Backfill Planning

**What we found:**
Running a completeness check on `kaggle_meta_analysis.xlsx` (35 hand-coded entries):

| Field | Filled |
|---|---|
| `fe_techniques` | 33/35 |
| `models_used` | 34/35 |
| `ensemble_method` | 30/35 |
| `original_data_usage` | 19/35 |
| `cv_strategy` | 18/35 |
| `encoding_strategy` | 12/35 |
| `hyperparameter_tuning` | 13/35 |
| `best_single_model` | 12/35 |
| `scaling` | 4/35 |
| `missing_data_strategy` | 2/35 |

The flowchart decision nodes (encoding strategy, CV strategy, missing data handling) are exactly the worst-filled fields — they require reading notebook code, not prose.

**Backfill plan:**
- 14 entries have `writeup_detail = 3` (GitHub repo linked) — these are worth manual backfill since code is explicit
- 17 entries have `writeup_detail = 2` (discussion post) — prose rarely mentions encoding/scaling, diminishing returns
- Manual process: open competition discussion page, find winner post, find code link, extract field values from code

**URL population attempt:**
Tried to auto-populate `writeup_url` by matching winner names (from `leaderboard.json`) to topic author names (from `topics.json`). Failed — `authorName` is always blank in the API response. Fell back to highest-voted solution topic as URL, but this is often not the winner's post (can be a tutorial, mid-place solution, or community compilation).

**Decision:**
Manual re-entry of writeup URLs. Set `writeup_url` to `kaggle.com/competitions/{slug}/discussion?sortBy=voteCount` as a consistent jump-off point. Added `code_url` column for the actual GitHub/notebook link. Added `winner_1st/2nd/3rd` columns directly in the Excel so winner names are visible while browsing.

---

## Session 6 — Backfill of Coded Fields (Notebook-Level Manual Review)

**What we did:**
Continued manual backfilling of `kaggle_meta_analysis.xlsx` for competitions that had notebook code available. Reviewed winner notebooks for s3e10, s3e9, s3e8, s3e6, s3e1, s3e7, s3e3, and s3e4, extracting: `missing_data_strategy`, `encoding_strategy`, `scaling`, `outlier_treatment`, `rare_class_handling`, `ensemble_method`, `cv_strategy`, `hyperparameter_tuning`, `original_data_usage`, `code_url`, `writeup_url`.

**Coding conventions established:**
- **Rank selection rule**: Use highest rank with a Kaggle notebook. If none, use highest rank with a writeup. All fields for an entry must come from the single rank recorded in `finish_rank` — never mix sources across ranks.
- **Ensemble distinctions**: Ridge/linear on OOF → `weighted_blend`; non-linear meta-learner on OOF → `stacking`; simple unweighted average → `mean_blend`.
- **CV distinctions**: `kfold` vs `stratified_kfold` vs `repeated_kfold` vs `repeated_stratified_kfold` coded separately based on actual class used.
- **AutoML**: When AutoGluon/H2O handles HPO and preprocessing internally → all relevant fields set to `automated`.

**Notable cases:**

*s3e1*: Winner writeup mentioned using another user's FE notebook (dmitryuarov's coordinate-based geographic features). Pulled that notebook and confirmed `original_data_usage = concat_rows` and `fe_techniques = Coordinate-based geographic features`. The source notebook, not just the winner's writeup, was the ground truth.

*s3e6*: Notebook (`ps-s-3-e-6.ipynb`) exceeded the ~25k token read limit. Created `_scan_notebook.py` to parse raw JSON and search cell source code for keywords. Used it to confirm `StandardScaler` was only called for an SVC model that wasn't in the final submission — so `scaling: none` was correct.

*s3e4*: Entry was missing from `kaggle_meta_analysis.xlsx` entirely — present in `kaggle_candidates_v2.xlsx` as `keep` but never added to the analysis sheet. No 1st or 2nd place source available (403 on data download, no writeup posted). Used 3rd place notebook (`olliekemp/3rd-place-solution-ensemble-catboost`). Wrote `_add_entry.py` to insert a new row with all fields in one pass.

**Tooling:**
- `_pull_notebook.py`: pulls a Kaggle notebook by kernel ref into `data/writeups/<slug>/`
- `_read_row.py`: reads back an entry from the Excel for verification
- `_update_entry.py`: fills empty fields via `UPDATES` dict, force-overwrites via `FORCE_UPDATES`
- `_add_entry.py`: creates a new row (used for s3e4)
- `_scan_notebook.py`: keyword search across cells for notebooks too large to read directly

**What didn't work:**
- Running multiline Python via `conda run ... python -c "..."` triggers conda's interactive error-report prompt and blocks indefinitely. Fix: always write code to a `.py` file and run that.

**Outcome:**
38 total entries coded (up from 35). 7 `keep` candidates from `kaggle_candidates_v2.xlsx` intentionally skipped due to no writeup or code available (s3e2, s3e12, s3e22, s3e25, s4e2, s4e6, s5e9). Phase 2 data collection declared complete.

---

## Session 7 — Population of n_features and pct_missing

**What we did:**
All 38 entries had `n_features = None` and `pct_missing = None` (or sparse manual fills). Wrote `fill_data_stats.py` to automate this: for each entry, download `train.csv` via `api.competition_download_file()`, compute column count minus id/target columns, compute `isnull().sum().sum() / size`, write both values to the Excel, and delete the downloaded file.

**What worked:**
- 34 of 38 entries filled in a single run (~4 min). The approach of downloading only `train.csv` (not the full competition zip) kept it fast.
- Already-filled entries are skipped via a guard, so the script is safe to re-run.

**What didn't work:**
- 4 competitions returned HTTP 403 (s3e4, s3e16, s3e26, s4e12) — these require accepting competition rules on kaggle.com before the API allows data download.
- s3e4 and s3e16 were resolved from notebook analysis: s3e4 = 30 features (V1–V28 + Time + Amount, 0% missing stated explicitly); s3e16 = 8 features (crab body measurements, 0% missing stated explicitly).
- After accepting rules, re-running the script filled s3e26 (19 features, 0% missing) and s4e12 (20 features, 5.02% missing). Note: s4e12 notebook describes "23 basic features" because it counts 5 date-derived columns added at load time; raw CSV has 20 input columns.

**Outcome:**
All 38 entries have `n_features` and `pct_missing` populated. Dataset is ready for Phase 3 analysis.

---

## Session 8 — Expansion Competitions (2022 TPS + S6E1–S6E4) + Schema Extension

**What we did:**

### Competition coding (7 new entries → 45 total)

Added six competitions across two sessions (prior session added may-2022 through s6e2; this session completed s6e3 and s6e4):

| Slug | Title | Outcome |
|---|---|---|
| tabular-playground-series-may-2022 | May 2022 TPS | Added (row 41) |
| tabular-playground-series-jun-2022 | Jun 2022 TPS | Added (row 42); data.csv not train.csv |
| tabular-playground-series-nov-2022 | Nov 2022 TPS | Dropped — meta-competition |
| playground-series-s6e1 | Students' Exam Score | Added (row 44) |
| playground-series-s6e2 | Predicting Heart Disease | Added (row 45) |
| playground-series-s6e3 | Predict Customer Churn | Added (row 46) |
| playground-series-s6e4 | Predicting Irrigation Need | Added (row 47) |

**nov-2022 drop rationale**: competition task was to blend a folder of other teams' prediction files against `train_labels.csv`. No raw feature data, no model selection decision, no FE — doesn't fit the research question.

**Notebook verification catches:**
- *s6e2*: writeup didn't name knowledge distillation explicitly; notebook showed `y_tr_soft = 0.5 * y_hard + 0.5 * teacher_preds`. Patched `fe_techniques` to include it.
- *s6e3*: `code_url` notebook is the level-4 meta-learner only (154 OOF predictions → cuML LogisticRegression). Revealed additional model types not named in writeup: SAINT, DCN, NAM, SNN, IFAN, RFF, Cox regression. Patched `models_used`.
- *s6e4*: `feature_type_dominant` coded as "numeric" initially; notebook Cell 5 showed 8 explicit `cat_cols` + 11 `num_cols`. Corrected to "mixed", `has_categorical=TRUE`, `encoding_strategy=target_encoding`, `scaling=none`, `original_data_usage=yes` (external irrigation CSV loaded). `fe_techniques` also populated from code: digit features, magnitude-based rounding, frequency encoding, pairwise interaction cross-features.

**KGMON-Playbook-2026 GitHub repo note**: the repo linked from the s6e3 writeup is an NVIDIA GTC26 educational resource (uses calorie prediction as demo data), not the competition solution. The actual s6e3 code is the Kaggle notebook at `code_url`.

### n_features / pct_missing

- `fill_data_stats.py` run for all new entries.
- jun-2022 returned 404 for `train.csv`; added `data.csv` as fallback in the script.
- nov-2022 had neither file accessible — moot since the entry was dropped.
- s6e1–s6e4 target columns (`exam_score`, `Heart Disease`, `Churn`, `Irrigation_Need`) aren't in the drop list, so the script overcounted by 1 each. Corrected manually: s6e1→11, s6e2→13, s6e3→19, s6e4→19.
- s5e7 had `pct_missing = "low"` — a data entry error (text landed in wrong column). Recomputed from data: 6.21%.

### New field: dominant_base_model

`primary_model` was coded as "ensemble" for 30/45 entries — the overall strategy, not the model type. Added `dominant_base_model` as a separate field capturing which model family actually drove the win.

**Derivation**: `_add_dominant_base_model.py` uses keyword matching on `best_single_model` first, falls back to `models_used`. Four entries needed manual judgment:
- s3e17 (AutoML stack: LightAutoML, H2O, FLAML) → `gbm` (all these default to GBMs internally)
- s5e3 (`best_single_model=SVC`) → `other`
- s3e10 (`best_single_model=GAM`) → `linear`
- feb-2022 (`best_single_model=RadiusNeighborsClassifier`) → `other`

**Distribution**: gbm=34, neural_network=8, other=2, linear=1.

### Normalization pass

59 changes in `_normalize_fields.py` + 7 cosmetic fixes in `_normalize_cosmetic.py`:

| Field | Fix |
|---|---|
| `has_categorical` | Unified to uppercase TRUE/FALSE |
| `primary_model` | XGBoost/lightgbm/catboost → gbm; NN → neural_network; ensemble_mixed → ensemble |
| `encoding_strategy` | target → target_encoding; OHE/one_hot → one_hot_encoding; label → label_encoding; ordinal → ordinal_encoding; catboost_encoding → target_encoding; comma → semicolon separator; canonical ordering (target first) |
| `scaling` | standard_scaler → standard |
| `ensemble_method` | blend/blending → mean_blend; weighted_blending → weighted_blend; ridge_stacking/ridge_ensemble/nn_ensemble → stacking; comma → semicolon separator |
| `original_data_usage` | True/yes unified to yes; False/not_used → none; comma → semicolon separator |
| `distribution_shift` | Lowercased TRUE/FALSE; "not described" → not_described; "low" → TRUE |
| Various | Stray "not described" (space) → "not_described" (underscore) in scaling, outlier_treatment, rare_class_handling, missing_data_strategy, writeup_detail |

---

## Session 9 — Dataset Evaluation & Schema Extension (n_rows, max_cardinality, metric)

### Dataset evaluation

Ran a structured evaluation of the 45-entry dataset against the Phase 3/4 research goals. Key findings:

**What's solid:**
- `dominant_base_model` and `fe_techniques` are 100% filled
- Core flowchart fields (cv_strategy, ensemble_method, encoding_strategy, hyperparameter_tuning, original_data_usage) all 88–97% filled
- Temporal spread is clean: 2022–2026 with no single year dominating
- Target type coverage: binary 21, regression 17, multiclass 7

**Structural gaps identified:**
- `scaling` (60%) and `missing_data_strategy` (53%) are too sparse to build reliable flowchart decision nodes. Root cause: GBM authors don't mention these because they're irrelevant to tree-based models — the missing values are almost certainly `none`, not truly unknown. Flagged as a known limitation.
- `best_single_model` missing for 20/45 entries — all the same S3-era competition entries with writeup_detail 1–2 where ensemble writeups didn't name individual model scores. `dominant_base_model` covers the type-level question but not the specific model.
- `distribution_shift` only 28% filled with actual TRUE/FALSE — too sparse to use as a CV strategy decision node input. Will likely need to drop this planned decision node or proxy it from other fields.
- Monetized competitions: 1/45 (ICR only). The monetized vs. playground comparison planned in Phase 3 is not viable with n=1.

**Missing schema fields identified:**
Three fields were missing that matter for the flowchart decision nodes:
1. `n_rows` — training set size. Critical for GBM vs. NN selection and pseudo-labeling decisions.
2. `max_cardinality` — highest cardinality among categorical features. The encoding strategy decision node was planned to use cardinality, but it wasn't in the schema.
3. `metric` — evaluation metric. Needed to condition analysis on what was being optimized.

**Robustness concerns noted:**
- GBM dominance (34/45 = 75%) means the NN and linear branches of any flowchart will rest on 8 and 1 entry respectively — descriptive only, not inferential.
- The 4 S6 entries (s6e1–s6e4) are methodologically distinct from S3 entries: KGMON-style mega-stacks with 100+ models and LLM-assisted coding. Worth tracking as a temporal covariate.
- `not_applicable` and `automated` values exist across several fields from AutoML entries — these entries may need to be handled as a separate stratum in analysis.

### Schema extension: n_rows, max_cardinality, metric

Added three columns (positions 34–36) via two scripts:

**`fill_extended_stats.py`** — downloads train.csv for each entry (same pattern as `fill_data_stats.py`), computes `n_rows = len(df)` and `max_cardinality = max(nunique()) across object/category columns`. Ran for all 45 entries in one pass.

**`_fill_metric.py`** — pulls evaluation metric from Kaggle API via `api.competitions_list(search=slug)`. Two bugs encountered and fixed:
- `ApiListCompetitionsResponse` is not directly iterable — must access `.competitions` attribute (changed in newer kagglesdk)
- Competition `ref` field is the full URL, not just the slug — fixed match to `slug in str(c.ref)`
- Attribute is `evaluation_metric` (snake_case), not `evaluationMetric`

**Results:**

| Field | Range / Notes |
|---|---|
| `n_rows` | 707 (s3e13) to 11.5M (s4e7); mean ~480K |
| `max_cardinality` | 0 (all-numeric) to 741K (may-2022 user IDs) |
| `metric` | 12 distinct values: Roc Auc Score (most common), RMSE, MSE, Log Loss, Balanced Accuracy, MAE, RMSLE, R2, Cohen Kappa, MCC, Accuracy, Weighted Multiclass Loss, MAP@{K}, MCOLAUROC |

**Known artifact:** several `max_cardinality` values are inflated by ID-like columns that weren't dropped (e.g., s4e12=167K, may-2022=741K). These are not true categorical feature cardinalities and should be treated as data artifacts in analysis. The script drops columns named id/Id/ID/target/Target/TARGET but not all competitions use standard naming conventions for non-feature columns.

---

## Session 10 — Phase 3 EDA Notebook

**Branch:** `phase3/eda` (created from `phase3/writeup`)

### What we did

Built `notebooks/01_eda.ipynb` — the full Phase 3 EDA — and retired `scripts/build_bar_plots.py` along with the four stale early-presentation plots (`plot1_model_frequency.png` through `plot4_best_single_model.png`).

**Why retire build_bar_plots.py:** The old plots were generated early for a presentation when the dataset had ~35 entries. After normalization passes and expansion to 45 entries, the numbers were wrong. More critically, the script had two structural bugs: (1) it used `blending` as a category name after the normalization pass renamed it to `mean_blend`/`weighted_blend`, so the ensemble chart would have shown zero counts for blending; (2) it didn't split semicolon-separated multi-value fields, so entries with `stacking;mean_blend` were counted as one string rather than two techniques.

**Notebook structure (9 sections, 7 figures):**
1. Setup & load
2. Helpers (era derivation, `explode_field`, row bins)
3. Field completeness audit — sortable table
4. Dataset overview — `eda_overview.png` (target type, dominant model, era)
5. Model family usage — `eda_model_families.png`
6. Ensemble methods — `eda_ensemble_overall.png` + `eda_ensemble_by_era.png`
7. Encoding strategy — `eda_encoding_overall.png` + cross-tabs (feature type, target type, cardinality)
8. CV strategy — `eda_cv_strategy.png` (overall + stratified vs non-stratified by target type)
9. Model selection — `eda_model_selection.png` (dominant model × dataset size and × has_categorical)
10. Sparse fields & limitations
11. Summary of key findings (markdown)

### Bug: Excel booleans read as Python bools

`has_categorical` and `is_monetized` are stored as Excel boolean cells. pandas reads these as Python `True`/`False`, not strings `'TRUE'`/`'FALSE'`. Three lookups were silently returning 0:
- `row.get('TRUE', 0)` in the model × categorical panel — entire right chart was blank
- `(x == 'TRUE').mean()` for `pct_has_categorical` — reported 0.0 for GBM and NN
- `(df['is_monetized'] == 'TRUE').sum()` — reported 0 instead of 1

**Fix:** `row.get(True, 0)`, `x.apply(bool).mean()`, `df['is_monetized'].apply(bool).sum()`.

Lesson: always check column dtypes after `pd.read_excel()`. Boolean Excel cells don't become strings.

### Decision: drop eda_fe_techniques

`fe_techniques` was recorded as free-text prose, not a controlled vocabulary. Splitting on semicolons produced 157 unique tags, 155 of them with count = 1. The bar chart was meaningless.

Two remediation options were evaluated:

**Option 1 — keyword taxonomy matching:** Define ~17 categories, keyword-match each entry's text, count by category. Prototype ran in ~30 minutes and produced defensible top counts (Interaction features: 18, Binning: 17, Target encoding: 15). Rejected: keyword matching on free-text prose is methodologically weak regardless of output quality. A paper would have to describe it as "classified by keyword matching against a researcher-defined taxonomy" — which is manual coding done imprecisely.

**Option 3 — re-code the field in Excel:** Revise `fe_techniques` to a controlled vocabulary for all 42 entries with data. Estimated 2–3 hours. Rejected on different grounds: even with clean coding, the FE chart would be purely descriptive and not connected to any decision node. FE is too dataset-specific to generalize — "interaction features appear in 18/42 entries" doesn't tell a practitioner anything actionable. The encoding_strategy cross-tabs already capture the structured FE signal that feeds the flowchart.

**Outcome:** Dropped the FE bar chart entirely. Replaced with one prose sentence in the summary: *"FE choices varied widely and were highly dataset-specific, consistent with the view that FE requires domain knowledge that resists generalization."* Two hours saved, paper tighter.

### Known issues flagged

The Methodology section (Section 3 of `research_report.md`) has two discrepancies introduced when it was written before data collection was finalized:
- 3.3 states multi-value fields use `|` as separator — actual data uses `;`
- 3.7 cites `missing_data_strategy` at 53% and `scaling` at 60% — notebook now shows 18% and 27% respectively (more entries coded after the methodology was written)

Both need to be corrected before the Results section is submitted.

### Current state (May 15, 2026)

Phase 3 EDA is complete. Section 4 (Results) of `research_report.md` is entirely placeholder and due May 18. All content needed to write it exists in the notebook. Phase 4 (flowchart) has not started.

---

## Session 11 — Contradiction Audit, Data Cleanup, Results Section

**Branch:** `phase3/methodology-fixes` (created from `phase3/eda`)

### Contradiction audit

Ran `scripts/_audit_contradictions.py` against all 45 entries, checking 8 contradiction types across fields. Found 24 initial flags. After two rounds of fixes, brought flags down to 14 — of which 5 are confirmed-correct behaviors, 3 are genuine data gaps, and 6 are uninvestigated soft warnings that cannot be verified from the available notebooks or writeups.

**Round 1 fixes (applied in previous session, confirmed this session):**
- ICR: `feature_type_dominant` numeric → mixed
- s5e5: `has_categorical` TRUE → FALSE
- s3e6: `has_categorical` FALSE → TRUE
- s4e5: `encoding_strategy` target_encoding → not_described
- s3e9: `encoding_strategy` target_encoding → not_described

**Round 2 fixes (this session, after reading writeups/notebooks):**
- s3e11: `max_cardinality` 0 → 20 (writeup says `store_sqft` has 20 unique values)
- s3e6: `max_cardinality` 0 → 2 (cat_cols confirmed as 5 binary features: hasYard, hasPool, isNewBuilt, hasStormProtector, hasStorageRoom; OHE applied)
- s3e7: `max_cardinality` 0 → None (has_categorical=TRUE but cardinality unknown from writeup)
- s3e13: `max_cardinality` 11 → None (the 11 was the number of target classes, not a feature cardinality; no categorical features used)
- s3e17: `feature_type_dominant` numeric → mixed (Binary Classification of Machine Failures; Machine Type is categorical)

**Two fixes applied then reverted (caused by _scan_notebook.py bug — see below):**
- s4e9: `cv_strategy` stratified_kfold → kfold → **reverted to stratified_kfold** (actual notebook Cell 86 confirms `StratifiedKFold` used)
- s3e3: `scaling` standard → not_described → **reverted to standard** (actual notebook Cell 25 confirms `StandardScaler().fit_transform()` used on full feature matrix)

**Root cause — _scan_notebook.py hardcoded path bug:**
`scripts/_scan_notebook.py` had the notebook path hardcoded to `s3e1`'s notebook on line 3. Every call to the script (passing s3e3, s4e9, s3e16, etc. as arguments) silently read the s3e1 California Housing notebook instead. This produced plausible-looking but completely wrong output ("no StandardScaler", "uses plain KFold") for all scanned notebooks. The bug was caught when the user asked about s3e6 — reading the notebook directly with Python revealed the correct content.

**Confirmed-correct flags (remain in audit, now 15 total):**
- s3e3, s3e4, s3e13: GBM+scaling=standard (all confirmed from actual notebooks/writeups)
- s3e16, s4e9: regression+stratified_kfold (confirmed: both use target binning for stratification)
- s3e11, s3e23: GBM+scaling=log (log1p target transform, not feature scaling)
- s5e2, s5e4, s4e8: genuine missing_data_strategy gaps

### Methodology section fixes

Two known discrepancies in `research_report.md` Section 3 corrected:
1. Section 3.3: separator `|` → `;`
2. Section 3.7: fill rates updated to actual values (missing_data_strategy 16%, scaling 27%, distribution_shift 29%); reframed explanation — low fill rates reflect structural property (80% of sample has no missing values) rather than collection gap

### Results section written

Wrote all 7 subsections of Section 4 (`research_report.md`):

**Key findings:**
- GBM dominant: 34/45 (76%)
- Ensembling near-universal: 40/45 (89%); stacking most common (21 mentions)
- Categorical features present in 30/45 (67%)
- Target encoding most frequent strategy (16/27 documented entries)
- CV strategy splits by task type: stratified KFold for classification (67%), plain KFold for regression (47%)
- Only statistically significant finding: task type vs. CV strategy, Fisher p = 0.03

**Unexpected findings documented:**
- GBM with standard scaling in 7/34 GBM entries (21%); confirmed intentional in 3 cases (s3e3, s3e4, s3e13)
- Regression entries using stratified CV via target binning (3/17 regression entries)
- Neural networks more prevalent in categorical-heavy datasets (23% vs 7%)
- Low pipeline heterogeneity in S3: LightGBM+CatBoost stack with target encoding was a de facto standard

### EDA notebook re-executed

Regenerated all 7 figures in `outputs/figures/` after data cleanup. All figures current as of this session.

### Current state (May 16, 2026)

Results section complete (numbers corrected after scan-bug reverts). Section 3 methodology discrepancies corrected. Data quality audit: 24 initial flags → 15 final (8 confirmed correct, 3 genuine gaps, 4 uninvestigated soft warnings). Phase 4 (flowchart construction) not yet started; scheduled for May 19–25. Next session: merge `phase3/methodology-fixes` into `phase3/writeup` (or main), then start flowchart.

---

## Session 12 — Pre-Phase 4 Viability Analysis, EDA Corrections, Blockers Report

**Branch:** `phase3/methodology-fixes` (no new branch; corrections applied to existing files)

### Pre-Phase 4 dataset viability discussion

Before starting Phase 4 (flowchart construction, scheduled May 19–25), conducted a structured analysis of whether the dataset can support the planned decision flowchart. Key findings:

**What the data can support (3–4 defensible branches):**
- Task type → CV strategy: the only statistically significant finding (Fisher's exact p = 0.03). Binary/multiclass → stratified k-fold; regression → k-fold.
- has_categorical → encoding approach: descriptive, n adequate. None → no encoding; TRUE → target encoding default.
- Model selection default: GBM ensemble (76% consensus). NN consideration for binary + categorical subgroup (23% vs 7%).
- Missing data: 78% of winners explicitly chose no treatment. "Don't impute by default" is itself an empirically grounded recommendation.

**What the data cannot support:**
- `distribution_shift` as an input node: 71% not_described — genuinely sparse (writeup culture gap).
- `outlier_treatment` as an input node: 67% not_described — same cause.
- Multi-variable conditioning: n=45 split across target type × has_categorical yields 3–16 entries per cell. Too thin for reliable conditional rules.
- Complex nested branches: dominant patterns (GBM 76%, ensembling 89%) leave insufficient variance to condition on.

**Conclusion:** Flowchart is viable but must be scoped to 3–4 shallow branches. Framed as empirically-grounded heuristic guide, not a statistically validated decision tree.

### EDA notebook correctness bug discovered and fixed

**Root cause:** `SKIP_VALS = {'not_described', 'not_applicable', 'automated', 'none', 'nan', ''}` was designed for multi-select technique fields (e.g., `fe_techniques`, `ensemble_method`) where `none` means "no technique used" and should not be counted. The same constant was used in the completeness audit (Cell 4), causing `none` and `not_applicable` to be treated as unknown for ALL fields — including `missing_data_strategy` and `scaling`, where `none` is a legitimate, meaningful answer (the winner explicitly did not impute / did not scale).

**Effect on reported numbers:**
| Field | Reported (wrong) | Correct |
|---|---|---|
| `missing_data_strategy` | 6/45 = 13% | 42/45 = 93% |
| `scaling` | 12/45 = 27% | 29/45 = 64% |
| `encoding_strategy` | 27/45 = 60% | 39/45 = 87% |
| `cv_strategy` | 39/45 = 87% | 41/45 = 91% |

**Distinction established:**
- `missing_data_strategy` at 93%: 35/45 explicitly "none/not_applicable" (structural — 80% of PS data has no missing values); only 3/45 genuinely not_described.
- `scaling` at 64%: 15/45 explicitly "none"; 16/45 genuinely not_described (authors didn't mention it). Excluded from flowchart nodes because 36% remains unknown.
- `distribution_shift` at 29%: genuinely sparse — 71% not_described. Actual documentation gap.

**Fixes applied:**
1. `notebooks/01_eda.ipynb` Cell 4: completeness audit now uses `NOT_KNOWN = {'not_described', 'nan', ''}` (narrower than `SKIP_VALS`). Added inline comment explaining the distinction.
2. `notebooks/01_eda.ipynb` Cell 22: print statements updated with correct numbers and "structurally omitted" framing. `distribution_shift` explicitly contrasted as a genuine gap.
3. `outputs/report/research_report.md` Section 3.7: split into two paragraphs — "Structurally omitted fields" (scaling, missing_data_strategy) and "Genuinely sparse field" (distribution_shift). Numbers corrected.
4. `outputs/report/research_report.md` Section 4.2: field completeness paragraph updated with corrected percentages.

**Notebook re-executed** via `conda run -n ds_env` (miniforge3). Standard `jupyter-nbconvert` failed with DeadKernelError (Windows proactor event loop issue with zmq); fixed by using `asyncio.WindowsSelectorEventLoopPolicy()` and running via `conda run` with a temp script. All 7 figures regenerated; outputs current.

### Blockers report for Prof. Albuquerque

Generated `private/phase4_blockers_report.md` documenting the three blockers and three supporting figures (`private/fig1_input_completeness.png`, `fig2_subgroup_sizes.png`, `fig3_outcome_concentration.png`). Report includes adjusted scope table and three questions for the professor. Updated to distinguish genuinely sparse fields from structurally omitted ones.

### Word cloud from solution writeups

Generated a word cloud from all 88 solution writeup `.txt` files in `data/writeups/` (43 competitions, ~456K chars of cleaned prose). Files are HTML-scraped Kaggle pages requiring two-stage cleaning:

1. **Nav truncation:** "Kaggle uses cookies" block is a consistent marker ~1900–2100 chars in; content starts after the following `\n\n`.
2. **Comment truncation:** Cut at first match of `Hotness\n` (comment editor toolbar) or `Posted (?:\d+|a|an) .* ago` — the Hotness pattern catches high-engagement posts where the toolbar precedes the first "Posted" line.
3. **Line-level boilerplate:** Regex strips Kaggle UI icon names (expand_more, content_copy, format_bold, insert_link, Hotness, etc.) and markdown link artifacts.

Three iterations needed to clean residual artifacts: "year ago" (regex missed "Posted a year ago"), editor toolbar (Hotness/undo/redo/format_bold block), and comment reaction labels.

**Outputs (all in `private/`, gitignored):**
- `gen_wordcloud.py` — generation script; walks `data/writeups/` dynamically, no hardcoded paths
- `writeup_corpus_clean.txt` — concatenated cleaned prose for inspection
- `fig_writeup_wordcloud.png` — final word cloud (1400×700, Blues colormap)

**Top terms:** feature, ensemble, OOF, fold, feature engineering, XGBoost, CatBoost, AutoGluon, Hill Climbing, LGBM, stacking, categorical, cross validation. Clean ML signal; a few borderline generics (different, time, work) retained as they appear legitimately in ML prose.

**Note:** `wordcloud` package installed into `ds_env` via `conda run pip install wordcloud`. Running via conda run + temp script (same pattern as notebook execution).

**Next:** Generated two additional subgroup word clouds (see below).

### Subgroup word clouds — GBM vs NN and Era

Built `private/gen_wordcloud_subgroups.py` to map each writeup folder to its competition entry via `competition_ref` in the Excel, then generate subgroup clouds using the same cleaning pipeline. No hardcoded paths.

**Figure A — GBM vs Neural Network** (`fig_wordcloud_gbm_vs_nn.png`, 1×2):
- GBM (n=32, Blues): `feature`, `ensemble`, `Hill Climbing`, `Regression`, `LGBM`, `combination`, `discussion`
- NN (n=8, Greens): `AutoGluon`, `RealMLP`, `TabM`, `interaction`, `categorical`, `Single`, `CatBoost`
- Contrast subtler than expected — both groups share `feature` and `ensemble` dominance. NN writers reference GBM tools as comparison baselines; GBM writers don't reciprocate.

**Figure B — Era** (`fig_wordcloud_era.png`, 1×5 horizontal strip):
- TPS/Featured (n=4, Purples): `mask`, `output`, `row`, `method`, `group` — earlier competitions had more diverse/unusual problem structures
- S3 (n=16, Blues): `original`, `ensemble`, `duplicate`, `level` — duplicate handling between train/test was a defining S3 theme
- S4 (n=10, Greens): `AutoGluon`, `OOF`, `XGBoost`, `fold`, `prediction` — AutoGluon dominance and OOF stacking becomes standard
- S5 (n=9, Oranges): `XGBoost`, `ensemble`, `single`, `original` — consolidation; less novelty vs S4
- S6 (n=4, Reds): `RealMLP`, `ipynb`, `categorical`, `XGBoost` — KGMON era, notebook-heavy, NN variety re-emerges

Layout iterated from 2×3 (cramped bottom row) to 1×5 horizontal strip.

**Note on S6 char count:** S6 has 122K chars despite only 4 competitions — the KGMON writeups are substantially longer than earlier-era posts, consistent with their more elaborate methodology.

### Current state (May 17, 2026)

EDA notebook corrected and re-executed. Research report Sections 3.7 and 4.2 corrected. Blockers report ready for professor meeting. Three word cloud figures generated (overall, GBM vs NN, era). Phase 4 (flowchart construction) starts May 19. Next: merge branch, then build flowchart from the 3–4 supported decision nodes.

---

## Session 13 — Branch Merge and Session Housekeeping

**Branch:** `phase3/methodology-fixes` → merged into `main` via GitHub website

### What we did

**Branch merge:** Answered the pending merge-to-main question from Session 12. `phase3/methodology-fixes` was 8 commits ahead of main with linear history — clean merge candidate. User merged via the GitHub website (no local merge command needed). Branch captures all Phase 3 work: Methodology section, EDA notebook, contradiction audit, Results section, EDA corrections, and blockers report prep.

**Journal gitignore discussion:** Considered whether `journal/session_log.md` should be gitignored. Decision: keep it tracked. Rationale — the journal is already in git history (removing it from tracking doesn't scrub history), it's low-stakes for a private repo, and it serves as an audit trail if methodology decisions need to be explained. Can revisit if the repo goes public.

### Current state (May 17, 2026)

`main` is now current with all Phase 3 deliverables. `private/` materials (blockers report + 7 figures) are gitignored and need manual transfer to laptop before the professor meeting. Phase 4 (flowchart construction) starts May 19 — create `phase4/flowchart` from updated `main`.

---

## Recurring Themes / Article Notes

- **The Kaggle API surface is shallower than it looks.** Competition list, leaderboard, topic titles — yes. Topic bodies, notebook code, author attribution on posts — no.
- **Winners don't submit notebooks to competitions.** They share GitHub repos in discussion posts. The kernels API finds nothing because the code isn't there.
- **Title-only signals are surprisingly strong at the model level** but completely silent on preprocessing. Two different layers of information requiring two different collection strategies.
- **Manual review is unavoidable** for preprocessing fields. The information simply isn't surfaced by any automated endpoint.
- **Ensemble methods dominate.** The clearest finding from even title-level data is that single-model wins are the exception, not the rule, in PS S3–S5.

---

## Session 14 — Phase 4 Writeup Re-evaluation (full sweep)

**Branch:** `phase4/writeup-reevaluation`

### What we did

Re-evaluated 45 curated writeups in reverse-chronological order using a 9-section per-writeup template (Identifiers, Dataset, What spreadsheet records, Public-notebook reuse, What's actually original, Dataset constraints, Code vs writeup check, Headline finding, Surprising/unusual). Built `analysis/writeup-reevaluation/INDEX.md` as the synthesis surface — status table + cross-cutting observations (constraint→strategy couplings, hypotheses on watch, methodology gaps, era patterns, community-graph hubs).

**Sweep order:** s6e4→s6e1, s5e12→s5e2 (skipping s5e9), s4e12→s4e1 (skipping s4e2, s4e6), s3e26→s3e1 (skipping gaps), then TPS Feb/May/Jun 2022, then ICR (first Featured/monetized entry, 6,430 teams). Two interim commits (425737f for s6 quartet, a62ba8c for s5 era); final commit bundles the rest.

### What worked

**The constraint→strategy framing held up.** Promoted couplings reached N≥2 (lookup-exploit families: identity, inversion, distance-via-generator-flaw; stacker families; validation-discipline variants). Hypotheses-on-watch list grew to ~133 single-case observations awaiting a second instance.

**Community-graph hubs surfaced:** ambrosm N=7 (4 wins + 3 source citations), siukeitin N=6, arunklenin N=5, paddykb N=4. cdeotte pre-dominance presence pushed back to Aug 2023 (ICR commenter, 806th).

**Cross-competition academic citation persistence:** TFT paper (Lim et al. 2019, arxiv 1912.09363) cited at ICR (Aug 2023, room722) and s6e1 (Jan 2026, mahog) — 29 months apart, two different authors. Academic techniques propagate across years.

**NN-primary winners cluster pre-2024:** TPS May 2022 (two-branch NN from xgbfir graph), TPS Jun 2022 (DAE for imputation), ICR Aug 2023 (Variable Selection Network at 617 rows). All three with custom architectures matching problem structure. Refined hypothesis: NN-primary requires (a) NN-friendly task, (b) discoverable interaction structure, or (c) tiny-data + heavy regularization + repeated training.

### What didn't work / friction

**Edit tool stale-string failures:** When sequentially editing INDEX.md (couplings/observations sections), wording from earlier edits sometimes invalidated later `old_string` matches. Fix: grep for current text before retrying.

**Windows PowerShell + UTF-8:** Python one-liners reading writeups with Chinese characters or em-dashes hit cp932 encoding errors. Workaround: prepend `sys.stdout.reconfigure(encoding='utf-8')`.

**Spreadsheet vs notebook discrepancies:** Found two cases where the user's notes ("no notebook") didn't match disk state. Noted and proceeded with both sources where available.

### Patterns rolled into INDEX

- Three lookup-exploit families (identity, inversion, distance-via-generator-flaw)
- Four "community pre-existed cdeotte canonization" techniques (HC, brute-force FE, Ridge-as-stacker, RAPIDS XGBoost)
- N=5 surprised-author wins, all at small-data or high-variance LB competitions
- N=5 academic-paper-as-technique-source cases (TFT paper, PLE Gorishniy, OpenFE Zhang, AutoGluon Erickson, masked-loss arxiv 2002.08338)
- First Featured/monetized competition (ICR) introduced new commenters: CPMP (Grandmaster of Grandmasters), pre-dominance cdeotte

### Current state (May 27, 2026)

44 per-writeup docs + ICR (45 total) sitting in `analysis/writeup-reevaluation/`. INDEX.md at 223 lines with 6 promoted couplings and ~133 hypotheses-on-watch. All work committed on `phase4/writeup-reevaluation`. Next: build the flowchart deliverable from promoted constraint→strategy couplings (Phase 4 main output).

### Session-14 continuation: pivot away from flowchart deliverable, build Pass 2 sheet

Discussion concluded that the evidence base doesn't support a prescriptive flowchart — only 6 couplings reached N≥2, ~133 single-case hypotheses can't justify decision nodes. Pivoted the deliverable framing from "flowchart" to **descriptive characterization (sociology-of-ML angle)**: typology of winning paradigms + attribution/canonization dynamics + community-graph analysis. Section outline drafted with new Discussion + Limitations + Implications sections (Methodology + Results-figures travel; Intro thesis and Prior Studies reframe).

Decided the original `kaggle_meta_analysis.xlsx` is **useful for distributional questions, flawed for origination/attribution questions** — added a new `Paradigm & Attribution` sheet rather than replacing the original (`scripts/build_pass2_sheet.py`). Schema designed and locked after 5 weigh-in questions:
- `lookup_exploit_subtype` strictly conditional on `paradigm=lookup-exploit`; separate `lookup_material_present` bool captures the pattern independently
- `origination_score` 0–3 ordinal with explicit anchor definitions in Codebook
- `uses_canonized_technique` list of 12 named techniques (HC, brute-force-FE, Ridge-as-stacker, RAPIDS-XGB, AG-as-ensembler, target-encoding-stack, LAD-as-stacker, original-as-columns, MLP-stacker, DAE-as-base-encoder, pseudo-labeling, adversarial-validation), with explicit exclusion list for universals
- `notable_commenters` threshold-gated (Grandmaster OR appears elsewhere in set)
- `winner_unique_edge` hard-capped at 200 chars

**Pass 2 sheet stats (45 rows):**
- Paradigm: ensemble-stacking 28, single-model-FE 6, lookup-exploit 4, problem-fit-NN 3, community-template-tweak 3, mixed 1
- Lookup material present in **13/45 (29%)** — material is often there even when not the winning move
- Origination: 0 entries at score 0 (pure fork), 5 at 1, 10 at 2, 30 at 3 — **even the most fork-heavy entries added some unique contribution**
- Surprised wins: 5; forked from public notebook: 8; academic paper cited: 6

Important meta-finding the sheet surfaced: **"pure fork" wins (origination=0) don't actually exist in our set.** Even Bill Cruise / Kirderf / Moonlit / kirill0212 (the heaviest fork cases) added something meaningfully original. The community-template-tweak paradigm is real but it's "fork+meaningful tweak," not "fork verbatim."

### Session-14 continuation: Pass 1 data quality audit + corrections in severity order

Built `Data Quality Audit` sheet catalogueing 24 issues from the re-eval (5 high / 14 medium / 5 low; 17 cell-level + 7 schema-wide). Applied corrections in severity order with full diff trail in a new `Corrections Log` sheet.

**Workbook now has 6 sheets and Competition Data has 40 columns:**

Corrections applied:
- **HIGH cell-level (4):** s5e2 `n_rows` 300000 → 4000000 (combined train.csv + training_extra.csv; misclassified the strategy-shaping constraint); s3e4 `winner_1st`/`winner_2nd` filled from leaderboard.json (was 'not described'); s6e2 `fe_techniques` removed 'knowledge distillation' (training-time, not FE).
- **MEDIUM cell-level (9):** `models_used` undercounts expanded for s5e11 (16→23), s5e8 (7→13), s5e10, s5e12, s4e7, s5e7; s6e3 `dominant_base_model` neural_network → gbm (90 trees vs 60 NN); s5e10 `original_data_usage` 'yes' → 'none' (no external original — internal data augmentation only); s4e11 `missing_data_strategy` imputation → leave_as_is (per author principle).

Two new columns added:
- **`top_3_margin`** (numeric, all 45 backfilled from leaderboard.json) — unblocks photo-finish → validation-discipline coupling analysis. Tightest margins surfaced: s6e2 (0.00001), s5e10 (0.00000 — 4-way tie at 0.05563), s5e5/s3e23/s3e11 (0.00002 each).
- **`distribution_shift_type`** (enum: temporal / covariate / label-noise / none / not-applicable) — disambiguates the 5 TRUE entries: s5e3 + s5e12 are temporal; s4e4 + tps-feb-2022 + ICR are covariate.

**`original_data_usage` split:** Replaced the conflated single-field encoding with two columns — `external_original_available` (TRUE/FALSE/unknown) and `external_original_use_mode` (rows-only/columns-only/both/features-derived/lookup/available-not-used/unavailable/unknown). All 45 rows mapped from re-eval docs. Old column preserved in place with deprecation note in Codebook. 90 backfill entries appended to Corrections Log.

**Distributions newly visible from the split:**
- External original available: TRUE 30 / FALSE 12 / unknown 3
- Use mode: rows-only 17, both 8, unavailable 12, **available-not-used 2** (cdeotte s3e5 + adaubas s4e5 — both CV-driven decisions to skip available original), lookup 2, columns-only 1, unknown 3

The `available-not-used` count (only 2) is a tiny but meaningful counter-pattern: most winners use available original; the explicit "don't use" decision based on CV evidence is rare.

**Codebook clarifications (11 new entries):** primary_model vs best_single_model vs dominant_base_model divergence rules; hyperparameter_tuning automated-vs-optuna distinction; models_used base-vs-stacker convention; the two new columns (top_3_margin, distribution_shift_type); the deprecation + split of original_data_usage.

### Current state (May 27, 2026)

Six-sheet workbook is the Pass 1 + Pass 2 + audit-and-corrections artifact. 103 cell-level corrections logged total (13 typed-as-corrections + 90 from the split backfill). All work committed on `phase4/writeup-reevaluation`. Re-analysis (new figures, paradigm-by-margin tables, updated research_report Results section) starts on a fresh branch using the corrected data.

---

## Session 15 — Phase 5 Reanalysis, Phase 6 Report Revision, Phase 7 Presentation Deck

**Branches:** `phase5/reanalysis` → `phase6/report-revision` → `phase7/presentation`

Three connected phases compressed into one extended session. Each got its own branch and built on the previous one. Notebook → report rewrite → presentation deck + glossary, ending with two systematic sweeps for numeric errors.

### Phase 5 — Reanalysis notebook + new figures

Built `notebooks/02_reanalysis.ipynb` from scratch on `phase5/reanalysis` to supersede the Phase 3 EDA notebook (`notebooks/01_eda.ipynb` left in place as the historical artifact, since the corrections changed several distributional counts).

Five-section structure: setup + load, distributional refresh, paradigm characterization, constraint cross-tabs, community + attribution, coupling evidence table.

**11 figures generated under `analysis/figures/phase5/`:**

| File | Section / purpose |
|---|---|
| phase5_21_paradigm_distribution.png | §2.1 — typology headline |
| phase5_22_paradigm_by_era.png | §2.2 — paradigm × era stacked bar |
| phase5_23_paradigm_photofinish.png | §2.3 — metric-aware photo-finish rate by paradigm |
| phase5_24_paradigm_n_rows.png | §2.4 — n_rows scatter by paradigm (log scale) |
| phase5_25_paradigm_origination.png | §2.5 — paradigm × origination_score heatmap |
| phase5_31_use_mode_paradigm.png | §3.1 — external_original_use_mode × paradigm |
| phase5_33_canonized_techniques.png | §3.3 — canonized-technique frequency bar |
| phase5_34_citations_origination.png | §3.4 — citations × origination_score boxplot |
| phase5_41_author_centrality.png | §4.1 — wins + citations + comments per top-15 |
| phase5_42_cdeotte_timeline.png | §4.2 — cdeotte observer-to-winner timeline |
| phase5_51_coupling_evidence.png | §5.1 — stacked-bar of supporting/contradicting/neutral per coupling |

Plus 4 additional figures generated specifically for the presentation (Phase 7) via `scripts/build_presentation_figures.py`: phase5_61 (FE tag frequency), phase5_62 (model family distribution), phase5_63 (origination score histogram), phase5_64 (use-mode breakdown).

**Coupling evidence outcome:** of 6 promoted couplings from INDEX, only 2 survive at strong-evidence threshold (≥75% support):
- C3 linear-stacker dominance: 32/40 (80%)
- C6 distribution-shift → custom CV: 4/5 (80%, small n)

Four contradicted (one detection-limited):
- C4 "use available original as columns": 11/30 (37%) — most striking, a direct contradiction of widely-cited cdeotte folk-knowledge
- C5 small-data → no-FE single-model: 3/13 (23%)
- C2 heavy-citations + recurring → fork-heavy: 3/8 (38%)
- C1 photo-finish → validation-discipline: 6/27 (22%) — flagged as detection-limited (strategy detector keys off 200-char `winner_unique_edge` summary)

**Output CSV:** `analysis/reanalysis/coupling_evidence.csv` for downstream paper use.

### Phase 6 — research_report.md rewrite

Branched `phase6/report-revision` from `phase5/reanalysis`. Rewrote `outputs/report/research_report.md` from 225 lines to 296 lines, pivoting framing from flowchart deliverable to typology + coupling-evidence.

**Sections written from scratch:**
- Abstract (~300 words, hits all four headlines)
- §1 Introduction (1.1–1.6, written for Kaggle-naive audience)
- §2 Background and Related Work (competition-as-method + knowledge-propagation framing)

**Sections substantially reframed:**
- §3 Methodology — added Pass 2 + audit + corrections workflow, replaced flowchart-rule extraction with coupling-evidence framework, expanded §3.7 Limitations
- §4 Results — restructured paradigm-first; new subsections for paradigm typology (4.2), coupling evidence (4.3), paradigm-by-era (4.4), constraint cross-tabs (4.5), community + attribution (4.6); existing field distributions moved to 4.7 as supporting evidence; new 4.8 for unexpected findings

**Sections removed per the no-Discussion presentation plan:**
- §5 Discussion (interpretation lives in verbal narration)
- §6 Conclusion (folded into 4.8)

**Sections corrected during rewrite:**
- §3.2 cohort sizes (previously inconsistent with §4.2) now matches: S3=17, S4=10, S5=10, S6=4, TPS=3, Featured=1
- §3.2 column count updated (was 36, now 40 after corrections + 2 new columns)

**Outstanding:** §5 References still a placeholder note. ~10 academic sources need formal APA 7th entries (Caruana, Erickson, Gorishniy, Borisov, Lim, Makridakis, Athey, von Krogh, Merton, plus inline NeurIPS/arXiv papers). Mechanical to fill in but not done.

### Phase 7 — Beamer presentation deck

Branched `phase7/presentation` from `phase6/report-revision`. Built Metropolis-themed Beamer deck targeting the May 4 capstone presentation (5–7 minutes, Kaggle-naive audience).

**Final structure (22 slides):**
- 1 title + 16 main content + 1 standout thank-you + 4 appendix
- 11 figure references from `analysis/figures/phase5/`
- 17 `\note{}` speaker-note blocks
- README documents Overleaf upload procedure (XeLaTeX/LuaLaTeX required for Metropolis fonts)
- 63-term glossary (`outputs/presentation/glossary.md`) added for Q&A reference

**Deck went through 4 iterations:**
1. Initial draft — 16 main slides
2. Restructuring after discussion: net +4 slides, -3 = +1 slide. Added "From flowchart to typology" pivot slide, "How winners actually build solutions", "Use as columns correction", "What each winner uniquely did" examples. Merged cdeotte timeline into community slide. Replaced three unexpected findings closer with "What this work contributes (beyond ensembles win)".
3. Word-wrap fixes — `\sloppy`, `\setlength{\emergencystretch}{3em}`, and `\raggedright` in every narrow column. Beamer's default justified text was overflowing narrow columns.
4. Numeric error sweep (see below).

**Adapted methodology framing for adaption note:** The Methodology guideline (and Results guideline) assumes a standard ML modeling project with baselines + RMSE/accuracy metrics. The report and deck explicitly adapt each subsection for a meta-analysis context. Captured in the report's §3.1 closing sentence.

### Numeric error sweep

The presentation prep surfaced a string of numeric errors propagated from earlier work into both slides and report. Caught and fixed in two sweeps; 12 errors total.

**Sweep 1 (provoked by user spotting slide 10 / slide 11):**
1. Slide 10 note: "96% / 4 paradigms" → 4 paradigms = 41/45 = 91%; 5 paradigms = 44/45 = 98%
2. Report §4.1: same "96% / 43 of 45" error
3. Slide 11 bullets: had inverted 67% / 33% (chart shows 67% are mostly-original, not 33%); also mixed in two metrics (`forked_from_public_notebook` flag and `community-template-tweak` paradigm count) that the audience couldn't map to chart bars — moved those to speaker note
4. Slide 17 (closer): "96% / 'three of the four'" → 91/98% + named the three (lookup-exploit / problem-fit-NN / single-model heavy-FE align with conditions; ensemble-stacking is the universal one)

**Sweep 2 (provoked by user spotting slide 16):**
5. Slide 16 cdeotte: said "4 wins + 6 citations", chart shows 6 + 6 (chart's "wins" axis counts all top-three appearances, not only rank-1 wins)
6. Slide 16 mahog: said "4 + 6", chart shows 3 + 4. Added paddykb (5+0) and ambrosm (4+3) to flesh out the archetypes.
7. Slide 17: "Dominant winners spent 12–22 months as observers" — 22 is cdeotte specifically; 12 was adaubas but adaubas has only 1 win, not a dominant winner. Narrowed to "cdeotte spent 22 months..."
8. Report §4.1: same author-count error, plus "From PS Season 4 onward" inconsistency (should be "From PS Season 3 onward" — S3 also has 65% ensemble-stacking)
9. Report §4.6: same author-count error in Dominant-competitor-also-cited bullet
10. Report §4.6: cdeotte timeline said "four entries in 14 months" — should be five top-three appearances in 15 months
11. Report §4.7: "five competition cohorts" but the list enumerates six
12. Report §4.7: external original use-mode breakdown omitted lookup=2

All twelve fixed across `outputs/presentation/slides.tex` (on `phase7/presentation`) and `outputs/report/research_report.md` (on `phase6/report-revision`).

### Methodology questions discussed but not fully resolved

Three methodology Q&A topics surfaced during prep and have notes/answers prepared but were not applied to the report or deck because we ran out of time on the presentation side:

**1. Why temporal scope 2022+?** Discussed two reasons: (a) tooling changes — RAPIDS cuML/cuDF, AutoGluon adoption, modern tabular NN architectures, A100 GPU access, and LLM-assisted coding all matured around 2021–2022; mixing earlier eras would conflate tool availability with strategy. (b) Technique propagation — Kaggle techniques migrate between competitions, so any era reflects what came before; including older competitions would mean characterizing a moving target. Possible future additions to report §1.5 Scope or §3.7 Limitations: explicit paragraph on the cutoff rationale.

**2. Cross-sectional vs time-series scope.** The corpus is implicitly cross-sectional tabular but the framing isn't explicit. Time-series exclusion rationale: different model families (ARIMA / Prophet / sequence models vs GBM / NN-for-tabular), different cross-validation (walk-forward vs k-fold), different metric vocabulary (MASE/sMAPE vs RMSE/AUC), different feature engineering vocabulary (lag features / rolling windows vs target encoding / groupby aggregates). Possible future addition: explicit positive framing in §1.5 Scope and slide 5 to say "cross-sectional tabular only" rather than just "no time series."

**3. FE-coding caveat for the pivot slide.** The "166 unique tags, 163 with count=1" stat is partly a coding artifact — `fe_techniques` was coded as free text, not normalized to a controlled vocabulary. The pivot rationale still holds (GBM dominance + decision-node field sparsity are coding-independent), but the FE chart is overstated supporting evidence. Honest Q&A answer drafted ("partly yes — but the underlying variance is real even after normalization, and the pivot rests on multiple legs"). Possible future addition: small footnote on slide 6 chart or one-sentence note in report §3.7 Limitations.

### Files added this session

- `notebooks/02_reanalysis.ipynb` (61 cells across 5 sections)
- `scripts/scaffold_reanalysis_notebook.py` (generator for above)
- `scripts/build_presentation_figures.py` (generator for phase5_61–64)
- `analysis/figures/phase5/` — 11 figures
- `analysis/reanalysis/coupling_evidence.csv`
- `outputs/presentation/slides.tex` (Beamer deck)
- `outputs/presentation/README.md` (Overleaf upload instructions)
- `outputs/presentation/glossary.md` (63 alphabetical terms for Q&A reference)

### Current state (May 27, 2026)

Presentation deck final and uploaded to Overleaf. Report is on `phase6/report-revision` with the typology rewrite complete; References section still needs APA-formatted entries before any formal submission. Three methodology answers prepared but not committed to either document — captured here in case they need to land later.

`phase4/writeup-reevaluation` → `phase5/reanalysis` → `phase6/report-revision` → `phase7/presentation` all pushed to origin. None merged to main yet. Branch decision (when ready): probably merge phase4 → main first since it's the longest-living, then merge phase5 → phase6 → phase7 → main sequentially, OR squash-merge phase7 to main as one final integrated state. To be decided.

---

## Session 16 — Project Retrospective + Pass 3 Design

**Branch:** `phase8/retrospective`

Reflective session after the presentation prep ended. Conducted a structured peer-review-style critique of the project, discussed strategic next steps, and clarified the Pass 1 vs Pass 2 methodological positions before designing Pass 3 (FE taxonomy).

### Critique conducted

Wrote a peer-review critique covering what works and what would need strengthening before publication outside the capstone. Findings:

**What works (kept):**
- Two-pass coding design is the strongest methodological contribution
- The pivot from flowchart to typology was the right call under data-supported framing
- "Use as columns" contradiction is a genuinely actionable finding for practitioners
- Audit + corrections workflow is unusually rigorous for capstone-scale work

**Major concerns identified:**
1. Selection bias on writeup-detail (overweights authors who write thoroughly — cdeotte overrepresented)
2. Author dependence not handled (5–6 entries are cdeotte; paradigm-by-era trends partly his recent activity)
3. Typology is partly circular — derived from the same data it's tested on; no held-out validation
4. Coupling-evidence verdict thresholds (75% / 50%) are intuitively chosen, not statistically grounded
5. Originator-vs-canonizer claim assumes participation; siukeitin's "0 wins" doesn't mean what it sounds like without entry data
6. Community-graph analysis is degree-counting, not actual graph analysis (no betweenness, no clustering)
7. FE-coding pivot evidence partly artifactual (163-of-166 unique-tags claim depends on free-text coding choice)
8. "No pure forks" is partly definitional artifact of the 0-3 scoring anchors

**Minor concerns:** typology × constraint alignments use the same 45 entries both for derivation and validation; deck appendix has redundancy; generalization to other modalities/domains not discussed.

**Net assessment:** Solid capstone work, above-average rigor for student-scale meta-research. Would need 4 specific strengthening passes before journal submission: held-out typology validation, author-removal robustness, selection-bias sensitivity, tighter originator-canonizer framing.

### Pass 1 vs Pass 2 methodological clarification

User pushed back on the framing of the two-pass methodology with a real question: *"the presentation mostly referenced findings from Pass 2; what makes the two-pass methodology useful? Pass 1 was just a less detailed, more rigid pass."*

Honest accounting: most analytical findings did come from Pass 2 (paradigm typology, origination, attribution, community archetypes). Pass 1's load-bearing contributions are infrastructure:
1. Cross-tabs requiring structured numerical/categorical fields (paradigm × n_rows etc.) need Pass 1
2. The audit + corrections workflow only works because Pass 1 and Pass 2 can disagree — without Pass 1, no audit
3. Pass 1 is replicable (a second researcher would get nearly identical results); Pass 2 is interpretive
4. Pass 1 forces recording of absence (`not_described`) that Pass 2 silently skips
5. Coupling-evidence strategy filters partly key off Pass 1 fields (ensemble_method for C3, cv_strategy for C6)

Reframing: Pass 1 is the table-stakes structured coding any meta-analysis needs; Pass 2 is the unique contribution. The methodological argument is that the **two-pass design surfaces its own scope limits** — Pass 1's distributional sparsity revealed the original FE-flowchart wasn't supportable, which forced the Pass 2 reframing. Most ML meta-analyses don't have a built-in pivot mechanism; this one did.

### Did Pass 2 capture FE techniques?

Confirmed: Pass 2 captured FE in prose (per-writeup MDs have "What's actually original" sections rich with FE detail), but **not as structured data**. The only Pass-2 fields that touch FE are `uses_canonized_technique` (only 12 named techniques) and `winner_unique_edge` (200-char headline summary). Cross-tabs like "target encoding × paradigm" are not possible from existing structured data.

### Pass 3 design decision

Proposed Pass 3 as a structured FE taxonomy: ~20–25 canonical boolean columns (uses_target_encoding, uses_brute_force_combinations, uses_groupby_aggregates, etc.) joined to existing sheets on (competition_ref, finish_rank).

**User's critical concern about Pass 3:** *"It's working off Pass 2, which means it's one generation away from the original writeups and notebooks."*

This is correct. Pass 2 MDs were never written to be comprehensive FE catalogs — they distill what mattered for the typology, not what mattered for FE counting. Building Pass 3 from Pass 2 MDs alone would systematically undercount FE techniques.

**Resolution: Pass 3 uses a layered source strategy.**

1. **Pass 2 MD as starting checklist** — gives the qualitative narrative and the techniques already noticed
2. **Original writeup in `data/writeups/<slug>/`** as the ground truth for what the winner *said* they did
3. **Notebook (`.ipynb`) in same folder** as the ground truth for what the code *did* — preferred where available since writeup and code often disagree
4. **`pass3_source_confidence` column** explicitly tracking each entry's source basis: `notebook+writeup` (highest) / `writeup+notes` / `writeup-only` / `notes-only` (lowest)

**Side effect of Pass 3:** acts as an audit pass for Pass 2 (techniques the MD missed get flagged), the same way Pass 2 acted as an audit pass for Pass 1.

**Expected effort:** ~2 days total. Stage 1 (half day): draft taxonomy from Pass 2 MDs as a first cut. Stage 2 (1–2 days): source-validate each entry against writeup + notebook; record additions. The delta between Stage 1 and Stage 2 is itself a methodological finding (how much Pass 2 undercounts).

### Sequencing decision

Discussed whether to:
- (A) Do more audit/correction work on Pass 1/Pass 2 before extending
- (B) Build Pass 3 first

Concluded (B) for three reasons:
1. The audit work has been thorough; continued auditing has diminishing returns
2. Pass 3 is self-contained — needs only join keys and the per-writeup MDs/writeups, doesn't depend on Pass 1 being any cleaner than it is
3. Pass 3 will surface more Pass 1/Pass 2 issues by side effect, same as the pattern that produced the audit in Session 14

### Outstanding methodology / critique items deferred

Not all critique items are addressable by Pass 3. The following remain on the post-Pass-3 roadmap if the project extends to journal-quality:
- Held-out typology validation (apply 4-paradigm definitions to 5–10 winning solutions not in original corpus)
- Author-removal robustness check (leave-cdeotte-out reanalysis of headline findings)
- Writeup-detail sensitivity analysis (does selecting rank-2 vs rank-1 by writeup-detail shift the paradigm distribution?)
- Originator-vs-canonizer claim needs either participation data or softer framing
- Community-graph analysis upgraded from degree-counting to actual DiGraph with centrality measures
- FE-coding caveat for slide 6 / report §3.7 (small fix, was deferred during presentation prep)

The three methodology questions from Session 15 (2022+ rationale, cross-sectional scope, FE-coding caveat) also remain available for application to the report if/when it's submitted formally.

### Current state (May 28, 2026)

Critique documented, Pass 1/Pass 2/Pass 3 methodological positions clarified, Pass 3 source strategy locked. Next branch starts the actual Pass 3 implementation.

`phase8/retrospective` pushed to origin. No code changes on this branch — pure reflection + planning.

---

## Session 17 — May 28-29, 2026

**Branch:** `phase9/fe-taxonomy` (continued from Session 16).
**Topic:** Pass 3 implementation — schema, pilot, full coding, Stage 2 source validation, aggregates, audit, fixes.

### Pass 3 schema design + pilot

Built a 53-column boolean taxonomy in `analysis/pass3-fe-taxonomy/SCHEMA.md` (v3, post-pilot). The schema is organized into 11 functional groups:

- A: categorical encoding (c01-c07) — TE basic, TE within-fold, TE multi-aggregations, TE alt targets, count enc, freq enc, missing indicator
- B: numeric transformations (c08-c12)
- C: interactions/combinatorial (c13-c18)
- D: aggregates/groupby (c19-c26)
- E: domain/temporal (c27-c31)
- F: external/original-derived (c32-c37)
- G: learned/advanced (c38-c41) — autoencoder latents, PCA/SVD, random projection, gplearn
- H: text/exotic (c42-c44)
- I: model-derived-as-features (c45-c47) — pseudo-labels, residual, outlier/aux classifier OOF
- J: feature selection (c48-c50)
- K: meta indicators (c51-c53) — explicit no-FE, adversarial validation for FE, forked uncatalogued FE

**User pushed for fine granularity:** "more detailed the better; can combine after but not split vague into detailed after the fact." Schema v1 (24 cols) → v2 (52 cols) → v3 (53 cols) after pilot revisions.

**3-entry pilot** (cdeotte s5e6, Sergey s3e14, Heitor s3e5) surfaced 6 schema issues:
1. Add c53 for forked-uncatalogued FE
2. Allow null for c02 (within-fold TE) when writeup ambiguous
3. Tighten c16 (brute-force) requires model-in-loop selection step
4. Clarify c18 (numerics-as-cats then combos)
5. Recalibrate expected n_fe ranges per paradigm
6. Document out-of-scope techniques (OptimizedRounder, target reversal, etc.)

All 6 applied as v3. Then extended pilot of 5 more entries (adaubas s4e5, greysky s5e4, room722 ICR, Bill Cruise s3e3, Mart Preusse s4e9) validated the schema works at scale.

### Stage 1 — code all 45 entries from Pass 2 MDs

Coded all remaining 37 entries against the v3 schema using their Pass 2 MDs (`pass3_source_confidence = notes-only`). Output: `stage1_data.csv` + `STAGE1_FULL.md`.

**Headline distribution:** median n_fe = 2, mean ~3.5. Bimodal — long left tail (1-3 techniques) and small right tail of heavyweight ensembles (cdeotte s5e2=15, s6e3=19, s6e2=10, s5e5=8). 64% of entries within paradigm-expected range; 36% below.

**v3.1 revisions** after full Stage 1 pass:
- c17 broadened from 3+ way to 2+ way categorical combos. Renamed `uses_higher_order_categorical_combos` → `uses_categorical_combos`. Affected s5e2 (all-pairs), s5e8 bigrams, s6e4 pairwise crosses.
- c53 relaxed from "multiple" to "one or more" forked sources with uncatalogued FE. Covered Kirderf s3e1 (single fork = all FE) and Cross Sellers s4e7 (proprietary feature store).

### Stage 2 — source-validate against writeups + notebooks

Six batches of source validation, 35 entries direct + 10 from pilot/extended pilot = 45/45 effectively covered:

1. **Batch 1** (5 high-priority below-range): s3e23 oscarm524, s4e10 omid, s4e3 Moonlit, s3e16 Ravi, s5e8 mahog. +5 flips. Pattern: TE granularity (within-fold) + bundled log transforms.
2. **Batch 2** (heavyweight + ambrosm): s4e12 cdeotte, s5e2 cdeotte, s6e2 masaya, s3e6 viktortaran, s3e9 ambrosm, s3e11 ambrosm. +7 flips. **ambrosm under-counting** was the big finding: s3e9 jumped 1→5 (concrete domain ratios, threshold-multiplicative interactions, has-component domain flags, custom TargetEncoder per-fold); s3e11 jumped 1→4. ambrosm's MDs emphasize methodology over per-feature FE detail.
3. **Batch 3** (fork-based + bundled): s3e1 Kirderf, s3e4 Ollie Kemp, s4e4 stopwhispering, s4e5 adaubas, s4e9 Mart Preusse, s6e4 kirill0212. +3 flips. **Kirderf's dmitryuarov coordinate notebook is heavy on geographic FE** (sin/cos lat/lon embeddings + PCA on coordinates + KMeans-haversine + UMAP + coordinate rotations). Three of these are schema gaps (singletons).
4. **Batch 4** (meta-only + TPS): s5e3 cdeotte starter, s5e7 Irfan, s5e11 mahog XGB, s6e1 mahog Ridge meta, TPS Feb/May 2022 ambrosm. +4 net flips. **TPS May 2022 re-coding**: Stage 1 mis-coded `i_02_21 = (f_21 + f_02 > 5.2).int - (f_21 + f_02 < -5.3).int` as multiplicative (c13). Notebook reveals it's additive sum + threshold flags (c14 + c15). Re-coded c13 FALSE, c14/c15 TRUE.
5. **Batch 5** (remaining notebook-available): s3e8 Craig Thomas, s4e1 Iqbal, s5e4 greysky, s6e3 cdeotte L4 meta, ICR room722. +1 flip (s4e1 Iqbal's Products_Per_Tenure banking domain ratio).
6. **Batch 6** (writeup-only): s3e7 Hardy Xu, s3e13 Umar, s3e17 ISoft, s3e24 Ravi, s4e7 Cross Sellers, s4e8 Optimistix, s5e5 cdeotte. +3 flips. **s3e7 explicit minimal-FE statement** was missed in MD ("I played around with creating additional features but did not find anything that improved my CV significantly"). **s5e5 cdeotte** had two granularity details glossed: cuML TargetEncoder per-fold (c02) and CatBoost 9-binned numerics combined pairwise = 81 unique cat values (c17 per v3.1).

**Cumulative: 23 net cell flips across 35 entries = 1.3% flip rate.** Higher than pilot's 0.6%; lower than batches 1-2 alone (~2%). Stage 1 from MDs systematically under-counts when authors' narratives dominate per-feature detail.

**Key methodology finding from Stage 2:** the flip pattern clusters in three predictable places:
- TE granularity (within-fold vs vanilla) - col 2 was null in Stage 1 for many; notebooks reveal Pipeline(TargetEncoder, ...) per-fold.
- Pipeline-bundled transformations - log/binning in cell-3 setup blocks that MDs skip.
- Domain-specific FE - ambrosm concrete-domain ratios, Kirderf's geo FE - hidden by author's narrative-style writeups.

**Technical fix during Stage 2:** `scripts/stage2_inspect.py` was silently crashing on a `–` en-dash character via Windows cp932 codec. Added `_safe()` helper to strip non-ASCII before printing. Re-ran s4e9 cells 80-150 (had been partially scanned); confirmed Stage 1 codings.

### Aggregates analysis

Computed schema-documented aggregations + paradigm summaries from `stage1_data.csv`:
- `uses_any_target_encoding` = c01 OR c02 OR c03 OR c04
- `uses_any_groupby` = c19 OR c20 OR c21 OR c22 OR c23 OR c24 OR c25
- `uses_any_combinatorial_search` = c16 OR (c17 AND c18)
- `uses_any_original_derived_feature` = c32 OR c33 OR c34 OR c35 OR c36 OR c37
- `uses_any_model_derived_feature` = c45 OR c46 OR c47
- `uses_any_explicit_selection` = c48 OR c49 OR c50

**CSV drift discovered.** `stage1_data.csv` accumulated unquoted-comma drift across many incremental edits. Rows have +1/+2/+7 extra fields from commas inside notes. Several attempts to write a clean parser; final approach: read 53 booleans positionally from cols 3-55, recompute n_fe by summing, accept ±1 imperfection in some rows.

### Audit (user request: "Audit the data as an expert data scientist")

Wrote `AUDIT.md` with three tiers of findings:

**Tier 1 (changes conclusions):** single-coder + self-designed schema (no Cohen's κ); paradigm × competition era × author confounded (heavyweight = all s5/s6 cdeotte; minimal-FE = mostly s3); sample sizes too small for percentages (Tilii s5e10 alone moves heavyweight TE% from 100→80); aggregation definitions arbitrary (c16 OR (c17 AND c18) — the AND is a choice); **Group G (autoencoder/PCA/random-projection/gplearn) was missing from any aggregate**; c51 (explicit no-FE) and c53 (forked uncatalogued) counted as +1 in n_fe — Heitor s3e5 gets n_fe=1 for declaring zero FE; c02 null-as-FALSE biases TE-within-fold downward.

**Tier 2 (specific errors):** Kirderf flipped c31+c39 but shows ALL ZEROS in aggregates because Group G isn't aggregated. Tilii has c38/c41/c44/c46 but all aggregate flags = 0. s3e7 Hardy Xu paradigm-assigned to lookup-exploit but his actual exploit is postprocessing not feature lookup.

**Tier 3 (bias and validity):** selection bias (winners only); cdeotte alone is 8 entries (18%) — "heavyweight uses TE" largely "cdeotte uses TE"; survivor bias on technique reporting; schema is analyst's mental model not nature.

### Fixes 1, 2, 5 implemented

User chose the three easy/important fixes:

**Fix 1 (Group G aggregate):** Added `uses_any_learned_derived_feature` = c38 OR c39 OR c40 OR c41. **Revealed: heavyweight 60% Learned%** (Tilii s5e10 autoencoder+GP, s5e6 cdeotte pseudo-labels, s6e2 masaya DVAE+gplearn, s6e3 cdeotte DAE+PCA+GRP — 4/5). Previously invisible. Major second dimension of the heavyweight paradigm beyond TE+Orig.

**Fix 2 (split n_fe):** `n_fe_techniques` (c01-c50, actual FE) vs `n_fe_meta` (c51-c53, meta-signals). Minimal-FE techniques mean dropped 1.86 → 0.86, meta mean = 1.0 — confirms the 1.0 was entirely c51 declarations. Heaviness gradient now **11× (9.6 vs 0.86)** instead of 5× — honest representation.

**Fix 5 (document single-coder limitation):** Added prominent "read first" section to STAGE2_AGGREGATES.md. User correction noted: this is a single human coder (Kenneth Young) working with Claude (Anthropic AI) as research collaborator. All schema/paradigm/flip decisions made by human in dialogue with Claude. Claude read writeups, scanned notebooks, proposed codings, surfaced gaps, ran scripts. Human reviewed each batch before commit. No inter-rater reliability computed (no Cohen's κ). Numbers are exploratory, not established facts.

### Current state (May 29, 2026)

**Pass 3 complete with audit and fixes.** Files in `analysis/pass3-fe-taxonomy/`:
- `SCHEMA.md` — v3.1 locked
- `PILOT.md` — 3-entry pilot
- `STAGE1_RESULTS.md` — extended pilot (5 entries)
- `STAGE1_FULL.md` — Stage 1 all 45 entries
- `STAGE2_LOG.md` — Stage 2 per-batch validation notes
- `stage1_data.csv` — canonical per-entry boolean data
- `stage2_aggregates.csv` — per-entry aggregates (with audit fixes)
- `STAGE2_AGGREGATES.md` — paradigm summary + per-column TRUE rates + per-entry table (with audit fixes)
- `AUDIT.md` — methodological audit

Plus `scripts/pass3_aggregates.py` and `scripts/stage2_inspect.py`.

**Headline (audit-fixed) per-paradigm summary:**

| Paradigm | n | tech mean | meta mean | TE% | Combo% | Orig% | Learned% |
|---|---|---|---|---|---|---|---|
| heavyweight | 5 | 9.6 | 0.0 | 80% | 20% | 60% | 60% |
| single-model-heavy | 3 | 9.67 | 0.0 | 100% | 100% | 33% | 0% |
| ensemble-standard | 19 | 4.0 | 0.11 | 53% | 16% | 11% | 5% |
| community-template | 4 | 3.5 | 0.5 | 25% | 0% | 0% | 25% |
| lookup-exploit | 4 | 1.0 | 0.25 | 0% | 0% | 75% | 0% |
| problem-fit-nn | 3 | 1.67 | 0.33 | 0% | 0% | 0% | 0% |
| minimal-fe | 7 | 0.86 | 1.0 | 0% | 0% | 0% | 14% |

**Audit-recommended next steps not yet done** (next branch will tackle robustness checks):
- Run 4 robustness checks: drop s6e3 outlier, subset to notebook+writeup confidence (n=22), subset to s4 era onward, drop cdeotte entries (n=37).
- Rescope claims in research report from "heavyweight paradigm" to "cdeotte/mahog/community heavyweight cluster."
- Independent second coder for inter-rater reliability (Cohen's κ) — likely out of scope for capstone.

**Lessons learned this session:**
1. **Fine-grained schema pays off.** v1 24 cols → v3 53 cols revealed structure (60% Learned% in heavyweight) that coarser coding would have missed.
2. **Single-coder + AI collaboration produces drift.** 23 cell flips across 35 Stage-2 entries (1.3% rate) is bounded below by what we measured; bounded above is unknown without inter-rater.
3. **Aggregation design matters more than coding precision.** Stage 1/2 codings were ~98% stable but the Group G omission hid a major dimension. Fixing aggregates surfaced more than fixing individual cells did.
4. **CSV-as-data-store is fragile for incremental coding.** Many small edits accumulated unquoted-comma drift. A structured editor + DB or even a strict-quoted CSV would have avoided ±1 n_fe errors.
5. **Meta-signals (c51/c53) should be separated from technique counts at the outset.** Conflating them made n_fe a misleading summary scalar until fix #2.

`phase9/fe-taxonomy` pushed to origin at commit 6de32c8. Next branch starts robustness checks.
