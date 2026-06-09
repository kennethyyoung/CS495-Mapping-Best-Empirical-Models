# Draft sections for the re-architected report

**Drafted 2026-06-03.** Drop-in prose for three new/expanded sections, matching `research_report.md` voice. Splice during the §4 restructure. Placement + renumbering notes in each header.

> **Renumbering note:** inserting §3.6 *Coding Reliability* pushes current §3.6 *Tools* → §3.7 and §3.7 *Limitations* → §3.8. The §3.8 "single-researcher coding … no formal inter-rater reliability check was performed" sentence must be revised to cross-reference §3.6 (see end of this file).

---

## 3.6 Coding Reliability
*(new subsection — insert before Tools and Technologies)*

The primary Pass 3 feature-engineering codings were produced with AI assistance under researcher direction. Because the 53-column taxonomy involves fine-grained judgments, a reliability check was performed on a stratified subsample to quantify how reproducibly the scheme can be applied.

**Design.** An independent blind re-code was conducted on a stratified 12-entry sample (≈ 21% of the combined 56-entry winners-plus-controls corpus), drawn to span eras (one each from the 2022 Tabular Playground series, Seasons 3–6) and source-confidence levels, and mixing eight winners with four controls. The re-coder worked from the original notebooks and writeups plus the schema definitions only, blind to the primary codings, the coding notes, and the data sheets. Agreement was then computed between the blind re-code and the primary codings.

**Results.** Raw per-cell agreement was high (94.5% at the 53-column level), but this figure is inflated by the large number of jointly-absent techniques and is reported only for completeness. Chance-corrected agreement gives the interpretable picture, and it depends strongly on resolution:

| Resolution | Cohen's κ | Gwet's AC1 | Positive agreement |
|---|---|---|---|
| 53-column | 0.59 (moderate) | 0.94 | 45% |
| 11-group | **0.65 (substantial)** | **0.78** | 58% |

At the full 53-column resolution Cohen's κ is only moderate (0.59); Gwet's AC1 (0.94) is reported but is known to over-correct under extreme prevalence skew and is not relied upon. Collapsing the 53 columns into the 11 technique families (Section 3.4) raises κ to 0.65 — *substantial* on the Landis–Koch scale — and brings κ and AC1 into agreement (0.65 and 0.78), indicating a non-paradoxical estimate. Because reliability is substantial only at the family level, **all quantitative feature-engineering results are reported at the group level** (Sections 4.3–4.4); the 53-column resolution is used for qualitative description only.

**Adjudication.** Disagreements were adjudicated against source materials. The disagreements were bidirectional: the primary codings had missed techniques the blind re-code caught (e.g., a `carat³` polynomial and a per-row max/min feature in one entry; an original-target-mean feature in another), while the blind re-code had missed techniques the primary codings caught (e.g., frequency encoding and pairwise interactions a "no-FE" reading overlooked). Four winner entries received source-verified corrections (most substantially a Sequential-Feature-Selection/OpenFE pipeline that had been mis-coded), which were applied to the dataset with provenance notes. A single coding rule was fixed for the `forked-uncatalogued` indicator (it applies to forked *feature pipelines*, not to ensembling another model's out-of-fold predictions). The "positive agreement" column above (45% at column level, 58% at group level) is reported as an honest reminder that even at the family level the two coders converged on which technique families were present only ~58% of the time; fine-grained feature-engineering coding is sensitive to coder thoroughness, which is a limitation the group-level reporting is designed to absorb.

---

## 4.3 Winning Feature Engineering Is a Small Shared Core
*(new subsection)*

The feature-engineering taxonomy reveals that winning solutions concentrate on a small shared set of techniques rather than an elaborate or idiosyncratic craft. **Target encoding is the single most common technique**, used by 18 of 45 winners (40%), with its leak-safe within-fold variant used by 14 (31%); the next tier — multiplicative and additive interactions, higher-order categorical combinations, frequency encoding, and digit features — is used by roughly 9–13% of winners each. Beyond this core, technique usage falls off sharply into a long tail: **29 of the 53 catalogued techniques are each used by two or fewer winners** (Figure 3). Winning feature engineering is thus better described as a small shared core plus a long bespoke tail than as a uniformly sophisticated practice.

The *amount* of feature engineering per winner is correspondingly modest. The median winner uses just **2** of their own catalogued techniques (mean 3.9), and 6 of 45 winners do none at all — relying entirely on forked public features or an explicit no-feature-engineering strategy (Figure 4). The distribution is right-skewed: a small heavyweight tail of ensemble-stacking entries reaches 10–19 techniques (the maximum, 19, belonging to a six-time winner's stacking solution), but these are the exception. This bimodality — most winners doing little feature engineering, a few doing a great deal — is itself a substantive finding: it indicates that elaborate feature engineering is neither typical of nor necessary for a winning tabular solution.

> *Figure 3.* `analysis/figures/report/fig3_technique_longtail_winners.png` — technique-level prevalence among winners, ranked, showing the small core and the long bespoke tail.
> *Figure 4.* `analysis/figures/report/fig4_nfe_distribution_winners.png` — distribution of own-technique counts (`n_fe`) across winners.

---

## 4.4 Technique Volume Does Not Distinguish Winners; Learned Features Do
*(new subsection — depends on the controls introduced in §3.2)*

To test whether feature engineering distinguishes winners from strong non-winners, winning entries were compared against the near-winning controls (rank 4–25 finishers; Section 3.2) at the technique-family level (Figure 5). The comparison yields a counter-intuitive result: **the controls use as much or more feature engineering than the winners across nearly every family.** Controls exceed winners in categorical encoding (64% vs 44%), numeric transforms (55% vs 38%), interactions (45% vs 42%), external-original features (36% vs 18%), and model-derived features (18% vs 11%); the median control uses 3 own techniques to the median winner's 2. Feature-engineering *volume*, in other words, does not separate winners from the near-winning field.

The one exception is decisive in its narrowness. **Learned and advanced feature techniques (Group G — autoencoder latents, genetic programming, PCA/SVD components) are the only family in which winners exceed controls** (16% vs 9%), and this difference is concentrated in heavyweight ensemble-stacking entries, where every heavyweight winner examined used at least one Group G technique while its rank-matched control used none. What distinguishes a winning tabular solution from a near-winning one is thus not *more* feature engineering but a *qualitatively different kind* — learned, derived features rather than additional hand-crafted ones.

This null contrast on volume should be read together with the composition of the control pool (Section 4.5) and the documentation-self-selection limitation (Section 3.8): because the controls are themselves a documented near-winning elite — and in 5 of 11 cases share an author with the winners corpus — the comparison establishes that feature-engineering intensity does not separate winners from *near-winners*, not that it fails to separate them from typical competitors. The finding is consistent with, and reinforces, the report's broader observation that the documented top of these leaderboards is distinguished less by technique inventory than by a small recurring pool of highly skilled competitors.

> *Figure 5.* `analysis/figures/report/fig5_fe_prevalence_winners_vs_controls.png` — feature-engineering family prevalence, winners (n=45) vs near-winning controls (n=11). Group G (Learned/advanced) is the only family where winners exceed controls.

---

## §3.8 Limitations — revision note

Replace the **"Single-researcher coding for both passes"** limitation's closing claim ("No formal inter-rater reliability check was performed.") with a cross-reference: *"For the Pass 3 feature-engineering taxonomy, a formal reliability check against an independent blind re-code of a stratified subsample was performed (Section 3.6); agreement was substantial at the family level (κ = 0.65) and moderate at full resolution (κ = 0.59), motivating group-level reporting."* The single-coder concern remains for Pass 1 and Pass 2, which were not independently re-coded.

---

## Abstract
*(rewrite of existing abstract)*

This study is a meta-analysis of winning solutions in Kaggle tabular machine-learning competitions, asking what actually distinguishes a winning approach. We coded 45 top-place solutions from competitions spanning February 2022 to April 2026 across a structured field schema, a qualitative origination-and-attribution pass, and a 53-technique feature-engineering taxonomy, and compared them against 11 near-winning (rank 4–25) controls. Four findings emerge. First, winning solutions cluster into a small set of recurring paradigms dominated by ensemble stacking. Second, winning feature engineering is a small shared core — target encoding plus a handful of interaction and encoding techniques — atop a long bespoke tail, with the median winner using just two of their own techniques. Third, feature-engineering *volume* does not distinguish winners from near-winners (the controls use as much or more); the only differentiator is learned/advanced features, concentrated in heavyweight ensembles. Fourth, the documented top is a small recurring guild: 5 of 11 near-winning controls share an author with the winners corpus, and technique knowledge propagates through a few central figures. A blind-re-code reliability check (family-level Cohen's κ = 0.65) validates the feature-engineering coding. All claims are scoped by a documentation-self-selection limitation: the corpus represents the *documented* elite, not the typical competitor.

---

## 1.3 Research Questions
*(new subsection)*

The analysis is organized around four questions:

- **RQ1.** What forms do winning tabular solutions take? *(typology — Section 4.2)*
- **RQ2.** Which feature-engineering techniques do winners use, and how much? *(prevalence — Section 4.3)*
- **RQ3.** Does feature engineering distinguish winners from strong non-winners? *(winner–control comparison — Section 4.4)*
- **RQ4.** How is the winning population structured, and how does knowledge move through it? *(community and attribution — Section 4.5)*

## 1.4 Contributions
*(new subsection)*

This work contributes:

1. a four-paradigm typology of winning tabular solutions, with a coupling-evidence framework linking dataset constraints to chosen strategies;
2. a 53-technique feature-engineering taxonomy (organized into 11 families), reliability-validated at the family level (κ = 0.65) — a reusable coding instrument;
3. the empirical finding that winning feature engineering is a small shared core (median 2 own techniques), not a uniformly elaborate craft;
4. the finding that feature-engineering volume does not separate winners from near-winners, whereas learned/advanced features do;
5. a characterization of the documented top as a small recurring guild (45% author overlap with the controls) with traceable knowledge propagation; and
6. an explicit documentation-self-selection scoping of all claims.

---

## 4.1 Overview: The Central Surprise
*(new subsection — opens Results)*

Feature engineering is widely held to be the decisive craft in tabular machine learning, so one might expect the winners of tabular competitions to be distinguished by especially extensive or sophisticated feature work. The corpus does not bear this out. The results below establish, in turn, what winning solutions look like structurally (Section 4.2, a four-paradigm typology dominated by ensemble stacking); that their feature engineering is a small shared core rather than an elaborate practice (Section 4.3); that feature-engineering volume does not separate them from strong non-winners — only learned features do (Section 4.4); that the documented top is a small recurring guild distinguished more by who competes than by technique inventory (Section 4.5); and how the field has shifted toward very large ensembles and LLM-assisted workflows in the most recent season (Section 4.6). The recurring theme is that *winning is less about feature-engineering volume than the folklore suggests, and more about paradigm fit, a small set of high-leverage techniques, and membership in a small skilled community.*

---

## 4.5 The Documented Top Is a Recurring Guild
*(new subsection — merges and reframes the existing Community and Attribution material with the new author-overlap finding)*

The winner–control comparison (Section 4.4) showed that technique inventory does not separate winners from near-winners. What does the data suggest separates them? The composition of the corpus points to a structural answer: the documented top of these leaderboards is a small, recurring pool of highly skilled competitors.

**Author recurrence.** Of the 11 near-winning controls, **5 share an author with an entry in the 45-winner corpus** — a 45% overlap. The recurring names include a multiple playground winner who is also a cited community hub and who additionally appears as a rank-25 control, and four other competitors who appear as both winners (in one competition) and near-winners (in another): a genetic-programming specialist, a stacking-ensemble specialist, a permutation-importance specialist, and a high-volume "diverse-blend" competitor. Because both the winners and the controls are documented top finishers, this overlap indicates that placing first versus placing fourth-to-twenty-fifth in a given month is, to a substantial degree, an outcome drawn from the same small pool — the "winner" label captures a single month's result within a recurring elite rather than a categorically distinct group.

**Knowledge propagation.** The community-and-attribution analysis (Section 4.6) shows that this guild has internal structure, organized into three centrality roles. A handful of *pure technique-sources* — most prominently `siukeitin` (the single most-cited handle, appearing in 12 writeups) and `paddykb` (5) — supply techniques that propagate widely through winning solutions yet never themselves place top-three in the corpus; they are, in effect, the guild's armorers. A second tier *occasionally wins while being heavily cited* (`tilii7`: one win, eight citations; `masayakawamata`: one win, five). A third tier are *dominant competitors who are also cited sources* (`cdeotte`: four wins, six citations; `mahoganybuttstrings`: four wins; `AmbrosM` and partner: four wins). The trajectory of the most central figure illustrates how membership forms: `cdeotte` first appears in February 2023 merely commenting on another competitor's winning writeup, then spends nearly two years as a commenter, cited source, and non-winning entrant (placing 81st and 806th in two competitions) before accelerating, from December 2024, into four wins in fourteen months (Section 4.6, Figure 8). Technique knowledge moves through these hubs — canonized techniques show measurable adoption across the corpus (Figure 9), and in the most recent season an explicitly named LLM-assisted "playbook" methodology propagated from a single entry into the broader workflow (Sections 4.6, 3.8). The guild is thus not merely a set of recurring names but a connected community with identifiable hubs and roles through which techniques are originated, canonized, and spread.

**Scope.** This finding must be read with the documentation-self-selection limitation (Section 3.8). Both the winners and the controls are *documented* top finishers — they published a writeup — and writeup publication is itself concentrated among habitual, brand-conscious competitors. The recurring-guild result therefore characterizes the *documented* elite of these competitions; it does not establish that the broader competitor population is similarly concentrated. What it does establish, robustly, is that the population from which documented winning solutions are drawn is small and recurring, and that this — more than any difference in feature-engineering inventory — is what the "winner" label tracks.

> *Figure 6.* community/attribution graph (reuse `analysis/figures/phase5/`) — competitor co-citation / origination network with the dominant hub highlighted.

---

## 5. Discussion
*(new section — interprets the Section 4 results)*

### 5.1 Winning is not what the feature-engineering folklore predicts

The prevailing folklore of tabular machine learning holds that feature engineering is the decisive craft and that the strongest competitors win by out-engineering the field. The corpus contradicts the simple form of this claim in two ways: the median winner applies only two of their own catalogued feature-engineering techniques (Section 4.3), and feature-engineering volume does not separate winners from near-winning controls — if anything the controls do slightly more (Section 4.4). The most parsimonious interpretation is that the techniques that *matter* for winning tabular competitions have already been canonized and diffused through the community (Section 4.5), so that the high-leverage core — target encoding and its leak-safe within-fold form, a few interaction and encoding moves, and disciplined cross-validation — has become *table stakes* rather than a differentiator. Once a technique is common to most strong entrants, it can no longer distinguish them; what remains to separate first place from fourth is execution quality, paradigm fit, ensemble craft, and the small residual edges examined below. This reading is consistent with the broader knowledge-propagation literature (Section 2.3): in an open community with fast, public diffusion, today's edge becomes tomorrow's baseline.

### 5.2 The frontier of feature differentiation has shifted from hand-crafted to learned features

The one feature-engineering family in which winners do exceed near-winners is learned/advanced features — autoencoder latents, genetic-programming features, and dimensionality-reduction components — and the gap is concentrated in heavyweight ensemble entries (Section 4.4). This suggests that the *frontier* of feature differentiation has moved: hand-crafted features (ratios, digit features, domain flags) are now broadly shared and no longer separating, while the remaining feature-level edge comes from learned, derived representations that are harder to copy from a public notebook. The trend coheres with the Season-6 shift toward very large ensembles and learned components (Section 4.6): as the hand-crafted layer commoditizes, the competitive margin migrates to the parts of the pipeline that are most expensive to reproduce.

### 5.3 Winning is, in part, a community phenomenon

The recurring-guild finding (Section 4.5) reframes the question from *what winners do* to *who wins*. With 45% author overlap between winners and near-winning controls, a connected centrality structure (technique-sources, occasional-winners, dominant-also-cited), and a documented trajectory by which a competitor moves from commenter to cited source to dominant winner over roughly two years, the data indicate that documented winning is partly an outcome drawn from a small, skilled, and socially connected pool. This does not diminish the technical findings; it contextualizes them. If the differentiating techniques are largely shared, then membership in the community that originates and canonizes those techniques — and the skill and persistence that membership reflects — is itself a substantial part of what the "winner" label tracks.

### 5.4 What these findings do and do not establish

The strength of these conclusions rests on an honest boundary (Section 3.8). Because inclusion required a published writeup, and writeup publication is concentrated among habitual, brand-conscious competitors, *both* the winners and the near-winning controls are drawn from the **documented elite** of these competitions. The winner–control comparison therefore establishes that feature-engineering volume does not separate winners from **documented near-winners**, and the guild finding establishes that the **documented** top is small and recurring. Neither result speaks directly to the typical competitor who places mid-field and never publishes; a competitor of that kind is invisible to a writeup-based corpus by construction. The findings are best read as a characterization of how the documented top of tabular leaderboards is composed and behaves, not as a population-level account of all competitors.

### 5.5 Implications

**For practitioners**, the corpus suggests that returns to expanding feature-engineering *breadth* are limited: mastering the small canonized core (within-fold target encoding, validation discipline, sound ensembling) and matching the solution paradigm to the dataset's constraints (Section 4.2) appear to matter more than accumulating bespoke features, and the remaining feature-level edge lies in learned representations rather than additional hand-crafted ones. **For competition-as-method research** (Section 2.2), the results argue that the value extracted from competition writeups should be read with attention to community structure and technique diffusion, not only to technique inventories — and that near-winner controls are a cheap, informative addition to any winners-only corpus. **Methodologically**, the 53-technique taxonomy, reliability-validated at the family level (Section 3.6), is offered as a reusable instrument for coding tabular feature engineering, and the documentation-self-selection effect surfaced here is offered as a caution for any study that mines public competition writeups: such corpora describe the documented elite, and that filter must be stated rather than assumed away.
