# s3e14 — Rank 1: Sergey Saharovskiy (sergiosaharovskiy)

## Identifiers
- **Competition:** [playground-series-s3e14](https://www.kaggle.com/competitions/playground-series-s3e14) — *Regression with a Wild Blueberry Yield Dataset*
- **End date:** 2023-07-31 (1,875 teams) — **earliest entry now (Jul 2023)**.
- **Rank / score:** 1 of 1,875 · 327.38765 private LB (MAE). 1st-2nd gap: 0.657 (largest in set, due to lookup-exploit).
- **Team / Kaggle user:** Sergey Saharovskiy / [sergiosaharovskiy](https://www.kaggle.com/sergiosaharovskiy) — appears later commenting on aldparis's s4e5 writeup ("the man from France predicts floods 0.00007 more accurately than anybody else").
- **Writeup:** [1# Winning solution](https://www.kaggle.com/competitions/playground-series-s3e14/writeups/sergey-saharovskiy-1-winning-solution) (local: `data/writeups/playground-series-s3e14/1# Winning solution _ Kaggle.txt`)
- **Notebook (published):** [ps-s3e14-2023-first-place-winning-solution](https://www.kaggle.com/code/sergiosaharovskiy/ps-s3e14-2023-first-place-winning-solution) (local).

## Dataset
Regression on `yield`, MAE metric, 15,289 train rows (small). 17 features all numeric (max_cardinality=0). Public original Wild Blueberry dataset.

## What the spreadsheet currently records
- `primary_model: ensemble`, `dominant_base_model: gbm`, `ensemble_method: stacking`
- `cv_strategy: repeated_kfold`, `hyperparameter_tuning: manual`
- `models_used: lightgbm` (LightGBM family with multiple variants)
- **`fe_techniques: Post-processing: match test rows to original dataset by fruitset+fruitmass key -> assign original yield values; automated matching script (2073 test samples x 776 unique yields)`**
- **`original_data_usage: concat_rows; feature_lookup`** — NEW: `feature_lookup` value (assign original target by key-match)

## Public-notebook reuse
| Source | Count | Notes |
|---|---|---|
| Public notebooks explicitly forked / ported | **5+ itemized** | (1) @zhukovoleksiy's EDA+ensemble (p1); (2) @paddykb's FLAML-BFI notebook (p2, p5); (3) @yzokulu's simple LightGBM regressor (p3, p6); (4) @tetsutani's various models ensemble (p4); (5) **@adaubas's "ps-s3e14-stacking-leastabsolutedeviation-reg"** notebook (p7/p8/p9 — Sergey explicit: *"adaubas's config and work helped me jump to 2nd place"*); (6) @mattop's post-processing discussion. **All 8 base OOFs in Sergey's stack are from public notebooks.** |
| **adaubas as recurring author** | Yes (Jul 2023 → May 2024) | adaubas helped Sergey at s3e14 (Jul 2023) with stacking + LAD regression code; **adaubas later wins s4e5 himself (May 2024) with similar techniques**. Recurring community contributor — Sergey here cites adaubas, then adaubas wins s4e5 10 months later. Earliest adaubas appearance is at s3e14 (as a contributor, not a winner). |
| Cross-author cameo | @naganohikaru (competitor Sergey was racing); @mattop (post-processing source). | |

## What's actually original to this author
- **Lookup-exploit post-processing** (the headline): match test rows to original dataset by (fruitset, fruitmass) keys → assign exact `yield` values from original. Out of 2073 test samples, 776 unique yields exist; matches automated across train + test + origin. **The synthetic generator preserves enough (X, y) pairs verbatim that direct key-matching predicts perfectly.** Original contribution: discovering and operationalizing this leak.
- **Discovery story**: noticed model struggled on `fruitset=0.335339, fruitmass=0.233554` rows where yield was *always* 1945.53061. Assigned this value → big OOF improvement. Generalized to all (fruitset, fruitmass) keys present in train+test+origin. Automated script ran through 776 unique yields iteratively.
- **Risk-tiered submission strategy** (humorously named after International Nuclear Event Scale): "Anomaly" (only the 1945.53061 fix) → "Serious Incident" (train>4, test>3) → "Zone With Consequences" (train>3, test>2) → "Dangerous Zone" (train>2, test>1, what he submitted) → "Ground Zero" (train>1, test>0, didn't submit). **Author chose mid-tier risk; left a more aggressive submission unmade.**
- **LAD regression for ensemble weights** (from adaubas) — matches MAE loss function.
- **All-public-notebook OOFs** — Sergey's *only* original contribution is the post-processing. Base models are entirely community.

## Dataset constraints that shaped this strategy
- **Synthetic data preserving exact (X, y) pairs from original** → enables direct test-row-to-original-row matching. **A unique exploitable property of this competition** — not universally available.
- **Small dataset (15K rows) + all-numeric features + MAE metric** → ensemble gains are modest (Sergey explicit: model side hits a ceiling). The lookup exploit is the only path to a winning edge.
- **Original dataset publicly available with overlap** → enables the lookup.
- **Public notebook ecosystem mature for this comp** → 8 OOFs available to port → no need to build own base models.

## Code vs writeup check
- ✓ Notebook (presumably) implements the lookup matching script — writeup walks through the logic; code snippet shown for the matching condition (`if len(dsp_train) > 2 and len(dsp_test) > 1`)
- ✓ Spreadsheet `fe_techniques` and `original_data_usage` accurately captures the lookup-exploit nature
- ⚠ The 8 specific public-notebook OOF sources are all listed in writeup; pipeline assembly code is in the published notebook

## Headline finding
s3e14 (Jul 2023) is the **earliest entry now** and **the most lookup-exploit-driven winner in the set**: Sergey ported 8 public-notebook OOFs and stacked with adaubas's LAD regression, then *won via pure post-processing* — matching test rows to original-dataset rows by (fruitset, fruitmass) keys and assigning exact original `yield` values. **Synthetic data preserving exact (X, y) pairs from original is an EXPLOITABLE LEAK** when present; Sergey's contribution was discovering and operationalizing it across 776 unique yields / 2073 test samples. The 1st-2nd gap (0.657 MAE) is the largest in the set, reflecting how big this exploit was. **adaubas appears as a contributor here** (Jul 2023) 10 months before his own s4e5 win — pre-existing community member with iterative trajectory.

## Surprising / unusual
- **Largest 1st-2nd gap in set (0.657 MAE)** — driven entirely by lookup exploit.
- **Lookup-exploit as primary strategy** — first time we see a winner whose ENTIRE original contribution is post-processing via direct test-to-original key matching. Conceptually similar to s5e7 Irfan's `match_p` row-merge but used as the WINNING move, not just one FE among many.
- **Risk-tiered submission strategy with nuclear-event-scale naming** — humorous and methodical. "Dangerous Zone" was submitted; "Ground Zero" left in reserve. **Explicit submission strategy beyond just "trust your CV"** — author calibrates risk per-submission.
- **All 8 base OOFs from public notebooks** — Sergey's stack is entirely community-sourced. His only original work is the lookup exploit. **Forks + 1 original trick = win** pattern.
- **adaubas's earliest appearance in set is as a TECHNIQUE CONTRIBUTOR here (Jul 2023)** — not as winner. Trajectory: contributor at s3e14 → 1st at s4e5 (May 2024). **Community pre-formation visible 10+ months before adaubas's own win.**
- **Sergey's 5-month learning curve** (explicit in writeup) — *"It took me almost 5 months of polishing tabular competition pipelines."* Matches s4e1 Iqbal's 11-month wait and s4e8 Optimistix's 6-month timeline. **Multi-month learning curve is normal for first podium.**
- **Synthetic data preserving original (X, y) pairs verbatim** — generator-property exploit that's competition-specific. Won't transfer to all competitions but when present, it's a dominant strategy.
- **Sergey racing @naganohikaru explicitly in the writeup** — author waited for competitor's next move, then "sent the bomb" (made aggressive submission). Real-time strategic interaction visible.
