# TPS Jun 2022 — Rank 1: Sebastian van Gerwen — first NN-primary winner

## Identifiers
- **Competition:** [tabular-playground-series-jun-2022](https://www.kaggle.com/competitions/tabular-playground-series-jun-2022) — *Tabular Playground Series - Jun 2022*
- **End date:** 2022-06-30. **Earliest entry now (Jun 2022)** — though same-era as TPS Feb 2022 (4 months later).
- **Rank / score:** 1 of 1,xxx · 0.83343 private LB (RMSE). 2nd: ArturRa 0.83379, 3rd: Patrick Chan 0.83390.
- **Team / Kaggle user:** Sebastian van Gerwen / [sebastianvangerwen](https://www.kaggle.com/sebastianvangerwen) — one-off author in our set.
- **Writeup:** [#1 Solution - Denoising Autoencoder](https://www.kaggle.com/competitions/tabular-playground-series-jun-2022/writeups/sebastian-van-gerwen-1-solution-denoising-autoenco) (local: `data/writeups/tabular-playground-series-jun-2022/#1 Solution - Denoising Autoencoder _ Kaggle.txt`)
- **Notebook:** Referenced but author flagged it scored poorly due to a submission dataframe bug. Not in local set.

## Dataset
Regression on F4 missing values (imputation problem), RMSE metric, 1,000,000 train rows. **81 features all numeric** (max_cardinality=0). 1.23% missing. **The main challenge: estimate conditional distribution of F4 where 2+ values are missing in the row.** Mean-imputable for F1/F3; F2 ignored entirely; F4 imputation is the actual prediction task.

## What the spreadsheet currently records
- **`primary_model: neural_network` (first NN-primary winner in set)**, **`best_single_model: DAE MLP (TensorFlow)`**, **`dominant_base_model: neural_network`**
- `ensemble_method: mean_blend`, `cv_strategy: not_described`, `hyperparameter_tuning: manual`
- `models_used: DAE MLP (PyTorch, TensorFlow)` — Denoising Autoencoder + MLP, two framework variants
- **`fe_techniques`: Feature-wise linear embeddings of values and null mask with additive fusion; conditional ensemble by F4 null count (single-null rows predicted separately); mean imputation for F1 and F3 groups**
- `original_data_usage: none`, `missing_data_strategy: imputation`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0** | Author's own architecture, not a fork. |
| Specific cites | @masatomurakawamm (masked autoencoder-like model), @ehekatlact (autoencoder + GAN discussion suggestion) | Cites community alternative implementations |
| Academic references | arxiv 2106.16057 (dot-product attention experiment), arxiv 2002.08338 (masked loss equivalent) | **Multiple academic paper citations** — author engages with research literature. |

## What's actually original to this author
- **Custom DAE architecture for tabular imputation**:
  - Input: zero-imputed data + null mask (concatenated source-null + random-binomial mask)
  - **Feature-wise linear embeddings of values AND mask, added together** (16-dim), then flattened
  - **7-layer MLP** with mish activation, layer norm, skip connections (hidden 2048)
  - Final dense layer to match input shape
  - **Conditional output**: if value masked → use prediction; else → use input (zeros gradients for non-masked positions)
  - **Masked MSE loss**: only computes loss at masked positions
- **Random masking strategy during training**: binomial 5% + "at least one value" constraint (to ensure non-zero gradient per row).
- **Author tested dot-product attention** (arxiv 2106.16057) instead of additive fusion → additive performed better.
- **Conditional ensemble by F4 null count**: 3 PyTorch + 3 TensorFlow DAE runs averaged (TF significantly better than PyTorch); single-null F4 rows used additional single-attribute prediction runs.
- **First NN-primary winner in set**: dominant_base_model = neural_network. All other winners have GBDT or "other" (kernel methods, GAM).

## Dataset constraints that shaped this strategy
- **Task IS missing-value imputation** (predict F4 given other features with various missingness patterns) → DAE is the natural model class. **NN-primary makes sense here because the problem itself is NN-friendly** (probabilistic imputation, conditional distribution).
- **81 features all numeric + no categoricals + 1M rows** → enough scale for a 7-layer MLP with 2048 hidden units to train; no categorical-encoding complexity.
- **Multiple-missingness-patterns** require single model that handles arbitrary null masks → autoencoder architecture handles this naturally vs iterating per missing column.

## Code vs writeup check
- ⚠ Author published a notebook but flagged that it scored poorly due to a "submission dataframe" bug. Notebook is referenced but not in local set.
- ✓ Writeup describes architecture in detail (random masking, embeddings, MLP, masked MSE, conditional output).
- ✓ Two academic paper citations + 2 community-implementation references.

## Headline finding
TPS Jun 2022 (Jun 2022) is **the first NN-primary winner in our set** (out of 43 entries). dominant_base_model = neural_network, primary_model = NN. **Earliest NN-primary winner**: predates s4e9 Mart Preusse's NN-stacker (Sept 2024) by 27 months, s3e26 Hardy Xu's NN-stacker (Dec 2023) by 18 months. **NN-primary only wins when the problem itself is NN-friendly** — here, the task IS missing-value imputation (estimate conditional distribution of F4 given partial features), and DAE is the natural model class. Author cites 2 academic papers and engages with research literature. Custom 7-layer MLP with feature-wise mask embeddings + masked MSE loss + conditional output. **The 4th lookup-/exploit-/specialized-architecture winner in set** (after s3e14 Sergey identity-lookup, s3e7 Hardy inversion-lookup, TPS Feb 2022 ambrosm distance-lookup) — here it's specialized-DAE-for-imputation-task.

## Surprising / unusual
- **First NN-primary winner in set** — all other 41 winners had GBDT, ensemble, or "other" (kernel/GAM) as primary. **NN-primary requires NN-friendly problem.**
- **DAE used for ACTUAL imputation task** (not as a base model for downstream prediction like s3e13 Umar's frozen-encoder-classifier or s6e2 masayakawamata's DVAE-for-diversity). Here DAE IS the model.
- **Custom architecture choices documented**: 7-layer MLP with mish + layer norm + skip connections + 16-dim embeddings + masked MSE loss. Most NN-stacker writeups don't go into this depth.
- **2 academic paper citations** (arxiv 2106.16057, arxiv 2002.08338) — author engages with research literature. **N=4 academic-paper-as-technique-source** cases now (PLE Gorishniy 2022 at s3e26, OpenFE Zhang 2022 at s4e4, AutoGluon Erickson 2020 at s3e1, **2 papers here**).
- **PyTorch vs TensorFlow comparison** within same architecture — TF performed significantly better. Empirical framework-choice data point. Author averaged across both.
- **NN-friendly problem family** hypothesis: imputation tasks (TPS Jun 2022), ranking/recommendation tasks, image-like tabular = NN-primary. Standard classification/regression = GBDT-primary. Worth tracking which task types favor which paradigm.
- **Pre-season-format entry (Jun 2022)** confirms NN-primary strategies existed BEFORE the season-format era; not a "new technique."
