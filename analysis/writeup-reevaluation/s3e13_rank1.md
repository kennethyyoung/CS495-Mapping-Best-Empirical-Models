# s3e13 — Rank 1: Umar (mufathurrohman)

> **Caveat:** No notebook published — author explicit: *"My notebook is a mess and clearly lacks any explanation, so I am sorry that I could not post the notebook publicly."*

## Identifiers
- **Competition:** [playground-series-s3e13](https://www.kaggle.com/competitions/playground-series-s3e13) — *Classification with a Tabular Vector Borne Disease Dataset*
- **End date:** 2023-07-15 (mid-month finish, 934 teams — smallest field in set) — **earliest entry now (early Jul 2023)**.
- **Rank / score:** 1 of 934 · **0.53179 private LB (MAP@K)** vs Public LB **0.37196** (delta 0.16 — **largest public-private gap in set**). 2nd: rjZhang97 0.52521, 3rd: Unworried1686 0.52302.
- **Team / Kaggle user:** Umar / [mufathurrohman](https://www.kaggle.com/mufathurrohman) — **self-described "competition beginner."** Doesn't appear elsewhere in our set.
- **Writeup:** [Surprisingly #1, Public LB: 0.37196 | Private LB: 0.53179](https://www.kaggle.com/competitions/playground-series-s3e13/writeups/umar-surprisingly-1-public-lb-0-37196-private-lb-0) (local: `data/writeups/playground-series-s3e13/Surprisingly #1, Public LB_ 0.37196 _ Private LB_ 0.53179 _ Kaggle.txt`)
- **Notebook:** **none** (author's "mess").

## Dataset
Multiclass classification of vector-borne disease (11 classes), MAP@K metric, **707 train rows (TINIEST in set — smaller even than s3e26's 7,905)**. **65 features all numeric** (max_cardinality blank). Curse-of-dimensionality regime: 65 features / 707 rows ≈ 9% feature density. No missing data.

## What the spreadsheet currently records
- `primary_model: ensemble` (3 models), `dominant_base_model: gbm`, `ensemble_method: mean_blend`
- `cv_strategy: not_described`, **`hyperparameter_tuning: none`**, `scaling: standard`
- `models_used`: lightgbm, nn, **autoencoder** (3 models — **first autoencoder-as-base-model in set**)
- **`fe_techniques: None`**, `original_data_usage: none`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **0 itemized** | Author cites the **"legendary Porto Seguro autoencoder thread"** (Kaggle discussion 44629) — older competition (~2017-2018) as autoencoder-ensemble inspiration. |
| Acknowledgments | @belati, @mpwolke ("being very active") | mpwolke also commented on s4e5 (aldparis) — recurring community member. |
| Cross-author lineage | None — first-time competitor, one-off win | |

## What's actually original to this author
- **Autoencoder-as-base-model with frozen-encoder + classification head** — first time we see this in the set:
  - Bottleneck architecture 64-64relu-32relu-**16relu**-32relu-64linear
  - Take encoder portion (up to 16relu), freeze it
  - Add 16relu-11softmax classification head on top
  - **Semi-supervised pretraining variant** — autoencoder learns unsupervised representation, then frozen for classification.
  - Best individual model on public LB: 0.37196.
- **Pure averaging ensemble** of 3 models (LGBM, NN, autoencoder-classifier) — no learned weights, no stacking. **Simplest possible ensembling.** Private LB jump: best single 0.46 → ensemble 0.53.
- **Default hyperparameters** for everything. Author motivation explicitly was *learning* autoencoders (he cited Porto Seguro thread), not winning.

## Dataset constraints that shaped this strategy
- **TINIEST dataset (707 rows) + 65 features (curse-of-dimensionality, ~9% feature density)** → autoencoder for *representation learning* under data scarcity is well-matched (semi-supervised pretraining). Heavy ensembling or FE would overfit.
- **MAP@K metric** → ensemble probability averaging directly improves K-best ranking; simple mean blend works.
- **First-time competitor + "learning autoencoder" motivation** → minimalist setup (default params, no FE, no tuning). Author's goal was educational, not competition-winning.

## Code vs writeup check
- ✗ **No notebook published.** Pipeline reconstructed from writeup only.
- ✓ Author provides per-model architectures and per-model CV/Public/Private LB scores in a clean table.
- ⚠ Cannot verify autoencoder training details (loss, epochs, freezing implementation) without code.

## Headline finding
s3e13 (early Jul 2023) is the **earliest entry now** and the **tiniest dataset (707 rows / 65 features)** — extreme curse-of-dimensionality regime. Won by a **self-described first-time competitor** using a **3-model mean-blend ensemble** (LightGBM + NN + **frozen-encoder Autoencoder-as-classifier**), all default hyperparameters, no FE, no original data, no learned stacker. **Pure averaging beat any single model by 0.06+ private LB** (best single 0.46 → ensemble 0.53). **Largest public-private gap in set (0.16)** validates "trust-CV-not-public-LB" pattern. Author's primary motivation was *learning autoencoders*, not winning — accidental win with minimalist setup demonstrates **simple ensembling + autoencoder semi-supervised pretraining can win in very-tiny-data regimes**.

## Surprising / unusual
- **TINIEST dataset in set** (707 rows) — even smaller than s3e26 (7,905) and s5e3 (2,190).
- **Largest public-private gap in set** (0.16 delta — Public 0.37, Private 0.53). Validates trust-CV ethos by example: any author who relied on public LB tuning would have lost massively.
- **First-time competitor wins 1st place** — even more extreme than Moonlit's s4e3 first-competition-2nd-place case.
- **Autoencoder-as-base-model** — first time in set. Semi-supervised pretraining with frozen encoder + classification head. The technique is decades-old but rarely appears in modern Kaggle ensembles.
- **"Porto Seguro autoencoder thread"** cited — *7-year-old competition (~2017-2018) discussion still informing 2023 strategy*. Community knowledge persistence is impressive.
- **Pure averaging ensemble (no learned weights)** wins. **Simplest possible meta-ensembling** — validates that in very-small-data regimes, simple averaging may outperform learned stackers (which would overfit on 707 rows).
- **Default hyperparameters across all models** — counter-pattern to most other winners' Optuna-heavy approaches. **In very-small-data, hyperparameter tuning may not help** (or could hurt).
- **Author's educational motivation** — joined to *learn autoencoders*, not to win. Accidental wins show competition outcomes are partly luck × technique.
- **mpwolke recurring** — also commented in s4e5 (aldparis). Another minor recurring community member.
