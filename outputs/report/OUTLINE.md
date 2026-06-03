# Report Re-Architecture Outline (v2)

**Drafted:** 2026-06-03. Re-architecture of `research_report.md` (the May-27, N=45 winners-only version) around the post-controls / post-reliability findings.

**Thesis (one sentence):** *We expected winning tabular solutions to be distinguished by sophisticated feature engineering; instead, winning FE is a small shared core, technique volume does not separate winners from near-winners (only learned/advanced FE does), and the documented top is a small recurring guild — established with a reliability-validated taxonomy and honestly scoped by a documentation-self-selection limit.*

Tags: **[REUSE]** survives ~as-is · **[REVISE]** reframe existing · **[NEW]** write fresh · 📊 figure slot

---

## Abstract **[REWRITE]**
~150 words: typology → small-FE-core → Group-G discriminator → guild → reliability → documentation-self-selection.

## 1. Introduction
- 1.1 Background — Kaggle as a venue, tabular ML **[REUSE]**
- 1.2 Problem & gap — no systematic FE taxonomy; no winner-vs-non-winner check **[REVISE]**
- 1.3 Research questions **[NEW]** — RQ1 what winning solutions look like; RQ2 what FE winners use; RQ3 does FE distinguish winners from near-winners; RQ4 community structure
- 1.4 Contributions **[NEW]** — typology · reliability-validated 53-col taxonomy · small-core finding · Group-G discriminator · guild finding · honest scoping
- 1.5 Scope **[REVISE]** — tabular PS, Feb 2022–Apr 2026, 45 winners + 11 near-winner controls

## 2. Background & Related Work **[REUSE]**
2.1 Tabular ML benchmarking · 2.2 Competition-as-method · 2.3 Knowledge propagation *(feeds the guild story)* · 2.4 Gap **[REVISE]**

## 3. Methodology
- 3.1 Design — descriptive/taxonomic meta-analysis **[REVISE]**
- 3.2 Data collection — winners + **controls (new)** **[REVISE]**
- 3.3 Preprocessing **[REUSE]**
- 3.4 Coding scheme — two-pass + **the 53-column Pass 3 FE taxonomy / 11 groups (the instrument)** **[EXPAND]**
- 3.5 Analytical methods — paradigm assignment, coupling evidence, community graph, **group-level FE prevalence, winner-vs-control** **[REVISE]**
- 3.6 **Reliability [NEW]** — blind re-code, κ=0.65 / AC1=0.78, human-vs-AI-assisted, group-level justification
- 3.7 Tools **[REUSE]**
- 3.8 Limitations **[EXPAND]** — single-coder (mitigated by 3.6) · **documentation self-selection [NEW]** · near-winner ≠ typical · small-n strata · era confound

## 4. Results **[MAJOR RESTRUCTURE]**
- 4.1 The central surprise **[NEW]** — expected sophisticated FE; found a small core + a guild
- 4.2 A typology of winning solutions **[REUSE]** + coupling evidence — 📊 Fig 1 paradigm distribution, 📊 Fig 2 paradigm-by-era *(both exist)*
- 4.3 Winning FE is a small shared core **[NEW]** — group prevalence, median 2 techniques, long tail — 📊 Fig 3 FE group prevalence (winners), 📊 Fig 4 n_fe distribution
- 4.4 Volume doesn't distinguish winners; learned FE does **[NEW]** — winners vs controls null contrast; Group G the only discriminator (heavyweight-specific) — 📊 **Fig 5 winners-vs-controls grouped bar (anchor)**
- 4.5 The documented top is a recurring guild **[NEW]** — 45% author overlap; skill persistence; cdeotte/KGMON propagation — 📊 Fig 6 community/attribution graph
- 4.6 Era shift **[REUSE]** — Season 6 LLM-agents / 100+ model ensembles

## 5. Discussion **[NEW]**
What the small-core + guild findings mean; documentation-self-selection scoping; what this says about "winning"; practical implications.

## 6. Limitations & Future Work **[REVISE]** — Option C (non-writeup controls) as the future move

## 7. References **[REUSE]**

---

## Figure inventory
| # | Figure | Source | Status |
|---|---|---|---|
| 1 | Paradigm distribution | phase5 | reuse |
| 2 | Paradigm by era | phase5 | reuse |
| 3 | FE group prevalence (winners) | stage1_data.csv | new |
| 4 | n_fe distribution | stage1_data.csv | new |
| 5 | **Winners vs controls FE prevalence (anchor)** | stage1 + controls | **new — generating** |
| 6 | Community/attribution graph | phase5 / regen | reuse |

## Effort split
~60% reframe-and-reorder of solid material (typology, coupling framework, community graph, methods, §2); ~40% new writing concentrated in §4.3–4.5 + §3.6 + the abstract/intro reframe.
