# s6e3 — Rank 1: cdeotte (Chris Deotte)

## Identifiers
- **Competition:** [playground-series-s6e3](https://www.kaggle.com/competitions/playground-series-s6e3) — *Predict Customer Churn*
- **End date:** 2026-03-31
- **Rank / score:** 1 of ~3,000+ teams · 0.91856 ROC AUC (final ensemble OOF: 0.91985)
- **Team / Kaggle user:** Chris Deotte / [cdeotte](https://www.kaggle.com/cdeotte) (NVIDIA KGMON)
- **Writeup:** [1st Place - GPT5.4, Gemini3.1, ClaudeOpus4.6 - KGMON Playbook!](https://www.kaggle.com/competitions/playground-series-s6e3/writeups/1st-place-gpt5-4-gemini3-1-claudeopus4-6-kgm) (local: `data/writeups/playground-series-s6e3/1st Place - GPT5.4, Gemini3.1, ClaudeOpus4.6 - KGMON Playbook! _ Kaggle.txt`)
- **Notebook (published):** [1st Place - Nvidia cuML Logistic Regression](https://www.kaggle.com/code/cdeotte/1st-place-nvidia-cuml-logistic-regression) (local: `data/writeups/playground-series-s6e3/1st-place-nvidia-cuml-logistic-regression.ipynb`) — *meta-learner only*
- **OOF/test dataset:** [cdeotte/s6e3-oof-and-test-pred-v2](https://www.kaggle.com/datasets/cdeotte/s6e3-oof-and-test-pred-v2) — 154 base model OOFs and predictions

## Dataset
Binary classification of `Churn` ∈ {0, 1}, ROC AUC metric, 594,194 train rows. 19 features (mixed): 3 numeric (`tenure`, `MonthlyCharges`, `TotalCharges`) and 16 categorical (`gender`, `Contract`, `InternetService`, `PaymentMethod`, service flags, etc.). **Synthetic data generated from the public IBM Telco Customer Churn dataset (7,032 original rows)** — this duality is central to the winning strategy. Train/test CSVs not in `data/raw/`; schema recovered from writeup and notebook.

## What the spreadsheet currently records
- `primary_model: gbm`, `ensemble_method: stacking`, `best_single_model: TabM`
- `dominant_base_model: neural_network` — *but writeup gives 90 tree models vs 60 NNs, so trees dominate by count*
- `hyperparameter_tuning: optuna`, `cv_strategy: stratified_kfold`, `original_data_usage: yes`
- `models_used`: 31 distinct architectures listed (XGBoost, LightGBM, CatBoost, YDF, cuML RF, LR, Embedding MLP, RealMLP, TabM, TabICL, FT-Transformer, TabTransformer, GraphSAGE GNN, GANDALF, ResNet, FFM, FM, DeepFM, DCN, NAM, SAINT, SNN, IFAN, RFF, Cox regression, Liquid NN, DAE, TabNet, Trompt, TabPFN, VSN)
- `fe_techniques`: 12+ techniques listed (snap features, decimal digits, nested TE, bigrams/trigrams, binned numerics, arithmetic interactions, multi-scale binning, categorical crosses, frequency/count encoding, service aggregations, cKDTree lookup, radix interactions, Benford's Law deviation, TF-IDF on numeric strings, PCA/GRP, cyclical tenure)
- Spreadsheet fields are individually accurate as a catalogue of components, but conceal that the framework (KGMON Playbook) and most components are pre-published.

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| **KGMON Playbook framework** (author co-authored at NVIDIA) | 1 (whole framework) | 7-step playbook: EDA → Baselines → GPU FE → GPU Hill Climbing → Stacking → Pseudo Labeling → GPU Extra Training. Has public blog, slides, GitHub, GTC training. |
| Public Kaggle notebooks ported / adapted | 39 unique | Writeup section 8 lists each with URL + adapted-in local filename. Authors: angelosmar1, azzamradman, badalkrsharma (×3), blamerx (×5), cdeotte (×1, prior comp), furqonaryadana, greysky, include4eto (×3), johnnyhyland, lightningv08, mahoganybuttstrings (×5), masayakawamata (×2), mikhailnaumov, nalgirayergn, omidbaghchehsaraei (×2), ozermehmet, rawashishsin, siukeitin, tsunamazda, yekenot (×4), yunsuxiaozi (×2) |
| Cross-season ports (from prior PS comps) | ~15 of the 39 | Significant share are S5E11, S5E8, S5E10, S5E5, S5E4, S6E1 solutions ported to S6E3 |
| Total candidate models trained | 850 | Selected down to ~150 via greedy forward hill climbing |
| Models in final stacker | 154 (per notebook FILES list) | Writeup says 150; close |

Two "secret sauce" techniques called out by author (snap features, decimal digit extraction) are present in multiple public-notebook references that pre-date this solution (e.g., nalgirayergn already used snap features).

## What's actually original to this author
- **Systematic application of KGMON Playbook to this specific dataset** at unprecedented scale — 850 candidate models, hill-climbing selection to 150, 4-level stack
- **Synthetic-data exploitation toolkit specifically wired for IBM Telco generator artifacts:** snap features mapping to nearest IBM row, cKDTree nearest-neighbor lookup on standardized `(MonthlyCharges, TotalCharges, tenure)`, PCA + GRP projection fitted on the 7,032 original rows, drift-ratio and Benford's-law features
- **The 4-level stack design:** L1 feature extraction (cuML KNN, DAE, PCA, TE) → L2 GBDT+NN on nested OOFs → L3 GBDT+NN on L2 OOFs → L4 cuML L2 LogisticRegression
- **The LLM "AI Council" workflow** — using GPT5.4 / Gemini3.1 / ClaudeOpus4.6 in role-specialized fashion (GPT brainstorm → Claude code → Gemini critique) to generate ~600K LOC and 850 models. NVIDIA-documented elsewhere; novel as competition methodology.
- **Specific architectural choices within the playbook:** L2-penalized cuML LR meta-learner (with explicit anti-domination rationale), fold-wise OOF calibration before stacking, `_stk` suffix convention for L3 models

## Dataset constraints that shaped this strategy
- **Synthetic data with known public original** (IBM Telco Customer Churn, 7,032 rows) → enables the entire generator-artifact toolkit: snap features, cKDTree nearest-neighbor lookup, drift ratios, target priors from original, PCA/GRP projection fitted on original. Without a known original, this whole strategy disappears.
- **ROC AUC metric** → ranking-based, robust to per-model probability calibration differences. Makes fork-and-stack viable because heterogeneous public OOFs do not need a common calibration to combine well.
- **Large train (594K rows) + author's hardware** (4×A100 GPUs, NVIDIA RAPIDS) → supports 850-model scale and 60 neural network architectures that would be infeasible on a smaller budget.
- **Heavy public-notebook coverage** of this competition and prior PS series → made the cross-season porting strategy (~15 of 39 refs from S5/S6E1) cheap relative to building from scratch.

## Code vs writeup check
- ✓ Published notebook contains only the L4 cuML LogisticRegression meta-learner (3 cells, ~5KB) — by design; base models are externalized to a Kaggle Dataset
- ✓ Notebook FILES list confirms 154 entries with prefixes matching writeup model families: xgb_*, lgbm_*, cat_*, nn_*, realmlp_*, gnn_*, tabm_*, ydf_*, etc.
- ✓ Meta-learner uses cuML `LogisticRegression(penalty='l2', C=1e-2, solver='qn')` with fold-wise OOF calibration before stacking, as writeup describes
- ✓ References section (writeup §8) lists 39 public Kaggle notebooks with author handles + adapted-in local filenames
- ⚠ Spreadsheet `dominant_base_model: neural_network` conflicts with writeup count of 90 trees vs 60 NNs (trees dominate by count, though best single model is the NN TabM)
- ⚠ Base-model training code is not in the published notebook — full reproducibility would require the KGMON Playbook GitHub repo + 850 model configs that are not public

## Headline finding
The KGMON Playbook itself is a pre-published, NVIDIA-branded methodology (blog, slides, GitHub, GTC training) — cdeotte's "winning approach" is the framework applied at industrial scale (850 models from 39 public notebook ports + LLM-generated code, hill-climbed to 150, stacked four levels deep). What's distinctive to *this competition* is the synthetic-data exploitation toolkit (snap, KDTree on IBM, Benford, drift ratios) and the LLM agent workflow.

## Surprising / unusual
- **Even more explicit attribution than s6e4** — 39 numbered references with URLs, author handles, and adapted-in filenames. Some references are this author's *own* prior-competition solutions (cdeotte ports his own S6E2 work).
- **LLM-generated code at unprecedented scale**: ~600,000 lines, 850 models, agent-orchestrated. The winning "playbook" is partly a prompt-engineering playbook.
- **The published notebook is intentionally incomplete** — it's only the L4 meta-learner; the 850 model training scripts are external and not all public. Verifying the full pipeline against the writeup is not possible from the local notebook alone.
- **Cross-season recycling is heavy**: ~15 of 39 references are ports from S5 series competitions, suggesting playbook continuity across seasons rather than per-competition novelty.
