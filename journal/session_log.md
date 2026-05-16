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

## Recurring Themes / Article Notes

- **The Kaggle API surface is shallower than it looks.** Competition list, leaderboard, topic titles — yes. Topic bodies, notebook code, author attribution on posts — no.
- **Winners don't submit notebooks to competitions.** They share GitHub repos in discussion posts. The kernels API finds nothing because the code isn't there.
- **Title-only signals are surprisingly strong at the model level** but completely silent on preprocessing. Two different layers of information requiring two different collection strategies.
- **Manual review is unavoidable** for preprocessing fields. The information simply isn't surfaced by any automated endpoint.
- **Ensemble methods dominate.** The clearest finding from even title-level data is that single-model wins are the exception, not the rule, in PS S3–S5.
