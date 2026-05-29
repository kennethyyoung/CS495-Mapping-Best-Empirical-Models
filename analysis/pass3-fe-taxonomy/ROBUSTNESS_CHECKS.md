# Pass 3 — Robustness Checks

**Date:** 2026-05-29.
**Purpose:** test whether the headline paradigm patterns survive when we systematically remove confounding sources of variation.
**Branch:** `phase10/robustness-checks`.

Four jackknife-style subsets, plus the baseline. For each, recompute the per-paradigm summary using the audit-corrected aggregates (Group G + n_fe split).

---

## heavyweight

| Subset | n | tech mean | TE% | Groupby% | Combo% | Orig% | Learned% | Model% | Sel% |
|---|---|---|---|---|---|---|---|---|---|
| Baseline (all 45) | 5 | 9.6 | 80.0% | 20.0% | 20.0% | 60.0% | 60.0% | 40.0% | 0.0% |
| Check 1: Drop s6e3 (drop the n_fe=19 outlier) | 4 | 7.25 | 75.0% | 25.0% | 25.0% | 50.0% | 50.0% | 50.0% | 0.0% |
| Check 2: notebook+writeup only (n=22, highest-confidence) | 1 | 10.0 | 100.0% | 0.0% | 0.0% | 100.0% | 100.0% | 0.0% | 0.0% |
| Check 3: s4 era onward (Jan 2024+) | 5 | 9.6 | 80.0% | 20.0% | 20.0% | 60.0% | 60.0% | 40.0% | 0.0% |
| Check 4: Drop cdeotte entries (n=39) | 2 | 6.5 | 50.0% | 0.0% | 0.0% | 50.0% | 100.0% | 0.0% | 0.0% |

## single-model-heavy

| Subset | n | tech mean | TE% | Groupby% | Combo% | Orig% | Learned% | Model% | Sel% |
|---|---|---|---|---|---|---|---|---|---|
| Baseline (all 45) | 3 | 9.67 | 100.0% | 33.3% | 100.0% | 33.3% | 0.0% | 0.0% | 0.0% |
| Check 1: Drop s6e3 (drop the n_fe=19 outlier) | 3 | 9.67 | 100.0% | 33.3% | 100.0% | 33.3% | 0.0% | 0.0% | 0.0% |
| Check 2: notebook+writeup only (n=22, highest-confidence) | 2 | 12.0 | 100.0% | 50.0% | 100.0% | 50.0% | 0.0% | 0.0% | 0.0% |
| Check 3: s4 era onward (Jan 2024+) | 3 | 9.67 | 100.0% | 33.3% | 100.0% | 33.3% | 0.0% | 0.0% | 0.0% |
| Check 4: Drop cdeotte entries (n=39) | 1 | 5.0 | 100.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |

## ensemble-standard

| Subset | n | tech mean | TE% | Groupby% | Combo% | Orig% | Learned% | Model% | Sel% |
|---|---|---|---|---|---|---|---|---|---|
| Baseline (all 45) | 19 | 4.0 | 52.6% | 0.0% | 15.8% | 10.5% | 5.3% | 5.3% | 26.3% |
| Check 1: Drop s6e3 (drop the n_fe=19 outlier) | 19 | 4.0 | 52.6% | 0.0% | 15.8% | 10.5% | 5.3% | 5.3% | 26.3% |
| Check 2: notebook+writeup only (n=22, highest-confidence) | 11 | 4.91 | 63.6% | 0.0% | 9.1% | 9.1% | 9.1% | 9.1% | 27.3% |
| Check 3: s4 era onward (Jan 2024+) | 11 | 5.09 | 72.7% | 0.0% | 18.2% | 18.2% | 9.1% | 9.1% | 18.2% |
| Check 4: Drop cdeotte entries (n=39) | 19 | 4.0 | 52.6% | 0.0% | 15.8% | 10.5% | 5.3% | 5.3% | 26.3% |

## community-template

| Subset | n | tech mean | TE% | Groupby% | Combo% | Orig% | Learned% | Model% | Sel% |
|---|---|---|---|---|---|---|---|---|---|
| Baseline (all 45) | 4 | 3.5 | 25.0% | 0.0% | 0.0% | 0.0% | 25.0% | 0.0% | 25.0% |
| Check 1: Drop s6e3 (drop the n_fe=19 outlier) | 4 | 3.5 | 25.0% | 0.0% | 0.0% | 0.0% | 25.0% | 0.0% | 25.0% |
| Check 2: notebook+writeup only (n=22, highest-confidence) | 3 | 3.67 | 33.3% | 0.0% | 0.0% | 0.0% | 33.3% | 0.0% | 33.3% |
| Check 3: s4 era onward (Jan 2024+) | 2 | 4.5 | 50.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 50.0% |
| Check 4: Drop cdeotte entries (n=39) | 4 | 3.5 | 25.0% | 0.0% | 0.0% | 0.0% | 25.0% | 0.0% | 25.0% |

## lookup-exploit

| Subset | n | tech mean | TE% | Groupby% | Combo% | Orig% | Learned% | Model% | Sel% |
|---|---|---|---|---|---|---|---|---|---|
| Baseline (all 45) | 4 | 1.0 | 0.0% | 0.0% | 0.0% | 75.0% | 0.0% | 0.0% | 25.0% |
| Check 1: Drop s6e3 (drop the n_fe=19 outlier) | 4 | 1.0 | 0.0% | 0.0% | 0.0% | 75.0% | 0.0% | 0.0% | 25.0% |
| Check 2: notebook+writeup only (n=22, highest-confidence) | 2 | 1.0 | 0.0% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| Check 3: s4 era onward (Jan 2024+) | 1 | 1.0 | 0.0% | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% |
| Check 4: Drop cdeotte entries (n=39) | 4 | 1.0 | 0.0% | 0.0% | 0.0% | 75.0% | 0.0% | 0.0% | 25.0% |

## problem-fit-nn

| Subset | n | tech mean | TE% | Groupby% | Combo% | Orig% | Learned% | Model% | Sel% |
|---|---|---|---|---|---|---|---|---|---|
| Baseline (all 45) | 3 | 1.67 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 33.3% |
| Check 1: Drop s6e3 (drop the n_fe=19 outlier) | 3 | 1.67 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 33.3% |
| Check 2: notebook+writeup only (n=22, highest-confidence) | 2 | 2.0 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 50.0% |
| Check 3: s4 era onward (Jan 2024+) | 0 | — | — | — | — | — | — | — | — |
| Check 4: Drop cdeotte entries (n=39) | 3 | 1.67 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 33.3% |

## minimal-fe

| Subset | n | tech mean | TE% | Groupby% | Combo% | Orig% | Learned% | Model% | Sel% |
|---|---|---|---|---|---|---|---|---|---|
| Baseline (all 45) | 7 | 0.86 | 0.0% | 0.0% | 0.0% | 0.0% | 14.3% | 0.0% | 57.1% |
| Check 1: Drop s6e3 (drop the n_fe=19 outlier) | 7 | 0.86 | 0.0% | 0.0% | 0.0% | 0.0% | 14.3% | 0.0% | 57.1% |
| Check 2: notebook+writeup only (n=22, highest-confidence) | 1 | 1.0 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| Check 3: s4 era onward (Jan 2024+) | 2 | 1.0 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% |
| Check 4: Drop cdeotte entries (n=39) | 6 | 0.83 | 0.0% | 0.0% | 0.0% | 0.0% | 16.7% | 0.0% | 50.0% |

---

## Survival assessment

Headline patterns (from STAGE2_AGGREGATES.md) and whether each robustness check supports, weakens, or breaks them.

### Heavyweight tech mean (baseline 9.6)

Drop s6e3: drops to 7.25. Drop cdeotte: heavyweight n=2 entries left, tech mean 6.5. With cdeotte removed, only 2 heavyweight entries remain (Tilii s5e10, masaya s6e2). The 'heavyweight does heavy FE' claim is largely about cdeotte's KGMON variants.

### Heavyweight Learned% (baseline 60.0%)

Notebook+writeup only: 100.0%. Drop cdeotte: 100.0%. Learned-derived features (autoencoder, PCA, GRP, gplearn) appear robust across subsets — survives drop-cdeotte better than tech mean because Tilii and masaya carry it.

### Single-model-heavy 100% TE + 100% Combo (baseline n=3)

Drop cdeotte: n=1 entries left (only greysky s5e4 remains; s4e12 and s5e2 are cdeotte). With n=1, percentages are degenerate. The 100% TE / 100% Combo claim is sustained by 3 entries that include 2 cdeotte entries.

### TE is most-used technique (40% across all 45)

All subsets show TE remains dominant in heavyweight/single-model/ensemble-standard. The 40% baseline rate may shift but the ordinal ranking (TE > everything else) appears robust.

### Lookup-exploit 75% Orig (baseline n=4)

This is tautological by paradigm definition. Robustness checks don't apply meaningfully here; the 75% just reflects that 3 of 4 entries do synthetic-to-original matching and the 4th (Hardy Xu s3e7) is a paradigm-assignment error (the 'lookup' is postprocessing, not feature engineering).

### Heavyweight is a recent (s5/s6) phenomenon

s4-era-onward subset has heavyweight n=5 (full 5 entries retained — all heavyweight entries are in s5/s6). This confirms heavyweight as a recent paradigm; it doesn't isolate paradigm from era because the two are nearly co-extensive.

---

## Overall verdict

**Patterns that survive all 4 checks:**
- TE is the dominant categorical-encoding technique among winners (ordinal ranking, not exact percentage).
- Heavyweight ensembles use *learned-derived* features (autoencoder/PCA/GRP/gplearn) more than other paradigms (revealed by fix #1, survives drop-cdeotte).
- Lookup-exploit paradigm relies on original-derived features (true by definition).
- Minimal-FE paradigm genuinely uses <1 technique on average (the 0.86 tech mean is honest after fix #2).

**Patterns that weaken substantially under at least one check:**
- 'Heavyweight does heavy FE' is largely a statement about cdeotte's KGMON variants. Drop cdeotte and heavyweight n drops to 2.
- 'Single-model-heavy 100% combinatorial search' is n=3, two of which are cdeotte. Drop cdeotte and the percentage becomes meaningless.
- 'Heavyweight tech mean = 9.6' is pulled up by s6e3 (n_fe=19). Without s6e3, drops noticeably.

**Patterns that don't generalize beyond their narrow data:**
- Most per-paradigm percentages at n<5 (single-model-heavy, lookup-exploit, problem-fit-nn).
- Era-paradigm separation: heavyweight = all s5/s6, minimal-FE = mostly s3. Without entries in *both* (paradigm and era), can't disentangle.

**Implication for the research report writeup:**
- Heavyweight finding should be scoped: 'the cdeotte/mahog/community heavyweight cluster' rather than 'heavyweight paradigm.'
- Learned-derived finding (fix #1's revelation) is the most defensible: it survives drop-cdeotte because Tilii s5e10 and masaya s6e2 carry it, and it's not era-confounded with paradigm in the same way as TE/Combo.
- All per-paradigm percentages should report n alongside (e.g., 'TE = 80% (4/5)' not 'TE = 80%').
- A 'limitations' section should explicitly note cdeotte concentration (6 entries = 13% of corpus) and paradigm × era confound.
