# TPS Feb 2022 — Rank 1: AmbrosM (ambrosm) — THIRD ambrosm win

## Identifiers
- **Competition:** [tabular-playground-series-feb-2022](https://www.kaggle.com/competitions/tabular-playground-series-feb-2022) — *Tabular Playground Series - Feb 2022*
- **End date:** 2022-02-28 (1,255 teams) — **earliest entry now (Feb 2022, by 11 months over s3e1)**. First non-season-N entry (pre-S1 format).
- **Rank / score:** 1 of 1,255 · 0.99239 private LB (Categorization Accuracy). 2nd: JamieWallis 0.99228, 3rd: Ozzy 0.99098.
- **Team / Kaggle user:** AmbrosM / [ambrosm](https://www.kaggle.com/ambrosm) — **third ambrosm win in our set** (TPS Feb 2022 → s3e9 May 2023 → s3e11 Jun 2023). Wins span 16 months.
- **Writeup:** [#1 Solution: Exploiting the Flawed Random Generation](https://www.kaggle.com/competitions/tabular-playground-series-feb-2022/writeups/ambrosm-1-solution-exploiting-the-flawed-random-ge) (local: `data/writeups/tabular-playground-series-feb-2022/#1 Solution_ Exploiting the Flawed Random Generation _ Kaggle.txt`)
- **Notebook (published):** [tpsfeb22-exploiting-the-flawed-random-generation](https://www.kaggle.com/code/ambrosm/tpsfeb22-exploiting-the-flawed-random-generation) (local).

## Dataset
Multiclass classification of 10 bacteria, Categorization Accuracy metric, 200,000 train rows. **286 features all numeric** (LARGEST feature count in set — decamer counts). **`distribution_shift: TRUE`** — train was 10 bacteria, test was 10 *mutated* bacteria with different probability distributions but generated with SAME random seeds. **Generator-flaw-exploitable shift.**

## What the spreadsheet currently records
- **`primary_model: other` (RadiusNeighborsClassifier — single model!)**, **`best_single_model: RadiusNeighborsClassifier`**, **`dominant_base_model: other`**
- **`ensemble_method: none`** — single model wins
- `cv_strategy: none`, `hyperparameter_tuning: manual`
- `models_used: RadiusNeighborsClassifier` (single kNN variant)
- **`fe_techniques`: Custom reverse-transformation of decamer counts to 100-dimensional random index space for Manhattan distance matching of train/test pairs sharing generation seed**
- `original_data_usage: none`, `distribution_shift: TRUE`

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Specific technique cites | **@siukeitin** (documented the duplicates via "tps022022-what-is-causing-these-duplicates-csi" discussion notebook) | **siukeitin's earliest engagement** documented (Feb 2022) — pushes back from s3e7 (Apr 2023). siukeitin N=6 entries now. |
| Academic references | numpy source code (np.random.RandomState.choice) + **Knuth, Art of Computer Programming Vol 2, Algorithm K** | Source-code-level analysis. Author actually reads numpy source to understand the flaw. **Most technically deep writeup in set.** |

## What's actually original to this author
- **Generator-flaw discovery and exploitation**: discovered that `np.random.RandomState.choice()` with similar probability arrays + same seed produces nearly-identical outputs. Used this to identify train-test row pairs.
- **Reverse-transformation of feature space**: 286 decamer COUNTS → reconstructs the 100-element decamer SEQUENCE (the original output of `choice()`). Once reversed, Manhattan distance reveals seed-twin pairs.
- **RadiusNeighborsClassifier with Manhattan distance** in the reverse-transformed space → matches each test row to its train twin → predicts based on twin's label. **Single-model classification via leak-aware nearest-neighbor.**
- **Source-code-level numpy understanding**: author walked through numpy's `random_sample` and `cdf.searchsorted` implementation to explain the flaw mathematically. Knuth quote: *"random numbers should not be generated with a method chosen at random; some theory should be used."*
- **Single-model wins** without ensemble, FE-stacking, or HP optimization — just understanding the data generation process at code level.

## Dataset constraints that shaped this strategy
- **Distribution shift between train and test (mutated bacteria) but same random seeds** → **the shift IS the leak**. When generator preserves seed-based row-ordering across distribution shift, distance-lookup in reverse-transformed feature space works.
- **286 numeric features but interpretable as decamer counts** → reverse-transformable to the 100-element decamer sequence. Domain-specific reversibility.
- **Multiclass + accuracy + many duplicates (1/3 train, 1/4 test)** → nearest-neighbor approach is natural; @siukeitin already documented the duplicates as a separate phenomenon.
- **No public original** → can't exploit-original; must understand the generator itself.

## Code vs writeup check
- ✓ Notebook implements the reverse-transformation + RadiusNeighborsClassifier pipeline
- ✓ Writeup includes the 4-line code snippet demonstrating the np.random flaw with concrete output
- ✓ Author shows transformed data plot with paired train-test points

## Headline finding
TPS Feb 2022 (Feb 2022) is **the earliest entry now by 11 months over s3e1 (Jan 2023)**. **AmbrosM's THIRD documented win in our set** (TPS Feb 2022 → s3e9 May 2023 → s3e11 Jun 2023) — **N=6 ambrosm connections** (3 wins + 3 source citations) now surpasses arunklenin (N=5) and siukeitin (N=5) as most-recurring community contributor. **Third lookup-exploit family identified**: distance-lookup via generator-flaw reverse-engineering (Manhattan-distance-in-reverse-transformed-feature-space → match test to train seed-twins). Different from identity-lookup (s3e14 Sergey) and inversion-lookup (s3e7 Hardy Xu). **Source-code-level numpy understanding** as winning edge — author reads numpy's `RandomState.choice()` implementation to discover the flaw, cites Knuth. **siukeitin's earliest engagement now Feb 2022** (siukeitin N=6 entries now, ties ambrosm). **Single model wins** with 0 ensembling, 0 stacking, 0 HP tuning — pure data-generation-process understanding.

## Surprising / unusual
- **Earliest entry in set (Feb 2022)** — by 11 months over previous earliest (s3e1 Jan 2023). Pre-season-format TPS competition.
- **Generator-flaw exploit at code level**: author actually reads numpy source to understand `np.random.RandomState.choice()`'s behavior. **First source-code-level winning analysis in set.**
- **Third lookup-exploit family**: now have identity-lookup (s3e14), inversion-lookup (s3e7), **distance-lookup via reverse-transformed feature space (TPS Feb 2022)**. Lookup-exploits are dataset-property-specific.
- **Single model (RadiusNeighborsClassifier) wins** with NO ensembling, NO FE in the conventional sense (FE here is purely reversing the generator transformation). **Counter to dominant ensemble-heavy pattern.**
- **ambrosm N=6** (3 wins + 3 source citations): TPS Feb 2022, s3e9, s3e11 (wins) + s3e23, s4e5, s4e8 (cited). **Most-recurring community contributor in set, surpasses arunklenin and siukeitin (both N=5).**
- **siukeitin's earliest documented engagement is Feb 2022** (documented the duplicates phenomenon). siukeitin N=6 now (TPS Feb 2022, s3e7, s3e23, s4e5, s4e8, s4e10). **Ties ambrosm.**
- **Knuth citation** ("Algorithm K", Art of Computer Programming Vol 2) — first historical-CS-literature citation in set. Author engages with academic canon, not just modern Kaggle.
- **distribution_shift = TRUE but the shift IS the leak** — counter-intuitive. Usually distribution shift is a challenge; here, the way the shift was generated (same seeds, different probability arrays) made it exploitable.
- **Author's anti-ML-orthodoxy framing**: solved a classification problem by *understanding the data generation*, not by training a powerful model. **"Theory + source-code-reading > ensemble engineering"** as an alternative paradigm.
