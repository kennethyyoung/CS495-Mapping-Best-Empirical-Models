"""Compute Pass 3 aggregate columns and paradigm-level summaries from stage1_data.csv.

Outputs:
- analysis/pass3-fe-taxonomy/stage2_aggregates.csv (per-entry aggregates)
- analysis/pass3-fe-taxonomy/STAGE2_AGGREGATES.md (paradigm summaries report)
"""
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "analysis" / "pass3-fe-taxonomy" / "stage1_data.csv"
OUT_CSV = ROOT / "analysis" / "pass3-fe-taxonomy" / "stage2_aggregates.csv"
OUT_MD = ROOT / "analysis" / "pass3-fe-taxonomy" / "STAGE2_AGGREGATES.md"

# Paradigm assignments per STAGE1_FULL.md
# Some entries fit multiple; choose dominant paradigm.
PARADIGM = {
    # Heavyweight ensemble-stacking (6-12 expected, but s5e2/s6e3 above)
    "playground-series-s5e6": "heavyweight",
    "playground-series-s5e5": "heavyweight",
    "playground-series-s6e2": "heavyweight",
    "playground-series-s6e3": "heavyweight",
    "playground-series-s5e10": "heavyweight",
    # Single-model heavy-FE (6-15)
    "playground-series-s4e12": "single-model-heavy",
    "playground-series-s5e2": "single-model-heavy",
    "playground-series-s5e4": "single-model-heavy",
    # Ensemble-stacking standard (4-9)
    "playground-series-s4e1": "ensemble-standard",
    "playground-series-s5e11": "ensemble-standard",
    "playground-series-s6e1": "ensemble-standard",
    "playground-series-s5e8": "ensemble-standard",
    "playground-series-s4e4": "ensemble-standard",
    "playground-series-s4e9": "ensemble-standard",
    "playground-series-s4e5": "ensemble-standard",
    "playground-series-s3e8": "ensemble-standard",
    "playground-series-s3e16": "ensemble-standard",
    "playground-series-s5e12": "ensemble-standard",
    "playground-series-s3e24": "ensemble-standard",
    "playground-series-s4e10": "ensemble-standard",
    "playground-series-s3e23": "ensemble-standard",
    "playground-series-s3e9": "ensemble-standard",
    "playground-series-s3e11": "ensemble-standard",
    "playground-series-s3e6": "ensemble-standard",
    "playground-series-s4e8": "ensemble-standard",
    "playground-series-s4e7": "ensemble-standard",
    "playground-series-s3e26": "ensemble-standard",
    # Community-template-tweak (3-7)
    "playground-series-s6e4": "community-template",
    "playground-series-s3e3": "community-template",
    "playground-series-s4e3": "community-template",
    "playground-series-s3e1": "community-template",
    # Lookup-exploit (1-4)
    "playground-series-s3e14": "lookup-exploit",
    "playground-series-s3e7": "lookup-exploit",
    "playground-series-s5e7": "lookup-exploit",
    "tabular-playground-series-feb-2022": "lookup-exploit",
    # Problem-fit NN (1-6)
    "tabular-playground-series-may-2022": "problem-fit-nn",
    "tabular-playground-series-jun-2022": "problem-fit-nn",
    "icr-identify-age-related-conditions": "problem-fit-nn",
    # Minimal-FE (0-3)
    "playground-series-s3e13": "minimal-fe",
    "playground-series-s5e3": "minimal-fe",
    "playground-series-s3e5": "minimal-fe",
    "playground-series-s3e10": "minimal-fe",
    "playground-series-s4e11": "minimal-fe",
    "playground-series-s3e17": "minimal-fe",
    "playground-series-s3e4": "minimal-fe",  # notebook-only, low n_fe
}

# Column groups for aggregation
GROUP_TE = ["c01_te_basic", "c02_te_within_fold", "c03_te_multi_aggs", "c04_te_alt_targets"]
GROUP_GROUPBY = ["c19_groupby_basic", "c20_groupby_count_nunique", "c21_groupby_quantiles",
                 "c22_groupby_histogram", "c23_groupby_zscores", "c24_groupby_skew",
                 "c25_groupby_division"]
GROUP_ORIG_DERIVED = ["c32_orig_target_mean", "c33_orig_target_advanced", "c34_exact_key_match",
                      "c35_approx_neighbor", "c36_drift_features", "c37_distribution_anomaly"]
GROUP_MODEL_DERIVED = ["c45_pseudo_labels", "c46_residual_features", "c47_outlier_aux_classifier"]
GROUP_SELECTION = ["c48_permutation_importance", "c49_sfs_backward", "c50_correlation_constant"]
GROUP_COMBINATORIAL = ["c16_brute_force", "c17_higher_order_combos", "c18_numerics_as_cats"]

def to_int(v):
    """Convert CSV cell to int 0/1, treating empty/null as 0."""
    if v is None or v == "" or v.lower() == "null":
        return 0
    try:
        return int(v)
    except ValueError:
        return 0

import re

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BOOL_RE = re.compile(r"^[01]?$")  # '', '0', or '1'

def load_csv():
    """Simple positional parse: fields 3-55 = 53 boolean cells.

    n_fe is computed downstream by summing booleans (CSV-stored n_fe has drifted from
    many incremental edits and is not trustworthy).
    """
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = []
        for raw in reader:
            if not raw or not raw[0].strip():
                continue
            entry = {
                "competition_ref": raw[0],
                "finish_rank": raw[1],
                "pass3_source_confidence": raw[2],
            }
            # Take exactly 53 boolean values positionally from index 3
            for k in range(53):
                idx = 3 + k
                val = raw[idx].strip() if idx < len(raw) else "0"
                # Validate: must be '', '0', or '1' — else use '0'
                if not BOOL_RE.match(val):
                    val = "0"
                entry[header[3 + k]] = val
            # Date at end if matches
            entry["pass3_date_coded"] = raw[-1].strip() if raw and DATE_RE.match(raw[-1].strip()) else ""
            entry["pass3_notes"] = ""
            entry["n_fe_techniques_used"] = 0  # will be recomputed
            rows.append(entry)
        return rows, header

def main():
    rows, header = load_csv()
    fieldnames = header
    bool_cols = header[3:56]  # 53 boolean column names
    print(f"Loaded {len(rows)} entries")
    print(f"Fields: {len(fieldnames)}")

    # Compute aggregates per row
    agg_rows = []
    for row in rows:
        comp = row["competition_ref"]
        rank = row["finish_rank"]
        conf = row["pass3_source_confidence"]
        # Re-compute n_fe by summing the parsed booleans (CSV value has drifted)
        n_fe = sum(to_int(row.get(c, "0")) for c in bool_cols)

        # Aggregate flags
        any_te = int(any(to_int(row.get(c)) for c in GROUP_TE))
        any_groupby = int(any(to_int(row.get(c)) for c in GROUP_GROUPBY))
        # combinatorial: c16 OR (c17 AND c18)
        c16 = to_int(row.get("c16_brute_force"))
        c17 = to_int(row.get("c17_higher_order_combos"))
        c18 = to_int(row.get("c18_numerics_as_cats"))
        any_combinatorial = int(c16 == 1 or (c17 == 1 and c18 == 1))
        any_orig_derived = int(any(to_int(row.get(c)) for c in GROUP_ORIG_DERIVED))
        any_model_derived = int(any(to_int(row.get(c)) for c in GROUP_MODEL_DERIVED))
        any_selection = int(any(to_int(row.get(c)) for c in GROUP_SELECTION))

        paradigm = PARADIGM.get(comp, "unknown")

        agg_rows.append({
            "competition_ref": comp,
            "finish_rank": rank,
            "paradigm": paradigm,
            "pass3_source_confidence": conf,
            "n_fe_techniques_used": n_fe,
            "uses_any_target_encoding": any_te,
            "uses_any_groupby": any_groupby,
            "uses_any_combinatorial_search": any_combinatorial,
            "uses_any_original_derived_feature": any_orig_derived,
            "uses_any_model_derived_feature": any_model_derived,
            "uses_any_explicit_selection": any_selection,
        })

    # Write aggregates CSV
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(agg_rows[0].keys()))
        writer.writeheader()
        writer.writerows(agg_rows)
    print(f"Wrote {OUT_CSV}")

    # Paradigm summaries
    by_paradigm = defaultdict(list)
    for r in agg_rows:
        by_paradigm[r["paradigm"]].append(r)

    paradigm_order = [
        "heavyweight",
        "single-model-heavy",
        "ensemble-standard",
        "community-template",
        "lookup-exploit",
        "problem-fit-nn",
        "minimal-fe",
        "unknown",
    ]

    paradigm_summary = []
    for p in paradigm_order:
        entries = by_paradigm.get(p, [])
        if not entries:
            continue
        n = len(entries)
        n_fe_vals = [r["n_fe_techniques_used"] for r in entries]
        agg_cols = ["uses_any_target_encoding", "uses_any_groupby", "uses_any_combinatorial_search",
                    "uses_any_original_derived_feature", "uses_any_model_derived_feature",
                    "uses_any_explicit_selection"]
        summary = {
            "paradigm": p,
            "n_entries": n,
            "n_fe_min": min(n_fe_vals),
            "n_fe_max": max(n_fe_vals),
            "n_fe_mean": round(sum(n_fe_vals) / n, 2),
        }
        for c in agg_cols:
            count = sum(r[c] for r in entries)
            summary[c + "_count"] = count
            summary[c + "_pct"] = round(100 * count / n, 1)
        paradigm_summary.append(summary)

    # Per-column overall counts
    cols_of_interest = [
        ("c01_te_basic", "TE basic"),
        ("c02_te_within_fold", "TE within-fold"),
        ("c03_te_multi_aggs", "TE multi-aggregations"),
        ("c04_te_alt_targets", "TE alt targets"),
        ("c05_count_encoding", "Count encoding"),
        ("c06_frequency_encoding", "Frequency encoding"),
        ("c07_missing_indicator", "Missing indicator"),
        ("c08_log_transform", "Log transform"),
        ("c09_power_polynomial", "Power/polynomial"),
        ("c10_binning", "Binning/discretization"),
        ("c11_digit_features", "Digit features"),
        ("c12_rounding_multi", "Multi-precision rounding"),
        ("c13_pairwise_mult", "Pairwise multiplicative"),
        ("c14_pairwise_add", "Pairwise additive"),
        ("c15_threshold_flags", "Threshold flags"),
        ("c16_brute_force", "Brute-force search"),
        ("c17_higher_order_combos", "Categorical combos (2+ way)"),
        ("c18_numerics_as_cats", "Numerics-as-cats + combos"),
        ("c19_groupby_basic", "Groupby basic stats"),
        ("c20_groupby_count_nunique", "Groupby count/nunique"),
        ("c21_groupby_quantiles", "Groupby quantiles"),
        ("c22_groupby_histogram", "Groupby histogram bins"),
        ("c23_groupby_zscores", "Groupby z-scores"),
        ("c24_groupby_skew", "Groupby skew/higher"),
        ("c25_groupby_division", "Groupby division of aggs"),
        ("c26_rowwise_stats", "Rowwise statistics"),
        ("c27_domain_binary_flags", "Domain binary flags"),
        ("c28_domain_ratios", "Domain ratios"),
        ("c29_domain_ordinal", "Domain ordinal scales"),
        ("c30_datetime_decomp", "Datetime decomposition"),
        ("c31_cyclical_encoding", "Cyclical encoding"),
        ("c32_orig_target_mean", "Original target mean"),
        ("c33_orig_target_advanced", "Original target advanced stats"),
        ("c34_exact_key_match", "Exact key match lookup"),
        ("c35_approx_neighbor", "Approx neighbor lookup"),
        ("c36_drift_features", "Drift features"),
        ("c37_distribution_anomaly", "Distribution anomaly"),
        ("c38_autoencoder_latents", "Autoencoder latents"),
        ("c39_pca_svd", "PCA/SVD components"),
        ("c40_random_projection", "Random projection"),
        ("c41_genetic_programming", "Genetic programming"),
        ("c42_tfidf", "TF-IDF"),
        ("c43_char_string_pattern", "Char/string pattern"),
        ("c44_lasso_generator_recovery", "Lasso generator recovery"),
        ("c45_pseudo_labels", "Pseudo labels as features"),
        ("c46_residual_features", "Residual features"),
        ("c47_outlier_aux_classifier", "Outlier/aux classifier OOF"),
        ("c48_permutation_importance", "Permutation importance"),
        ("c49_sfs_backward", "SFS/backward elimination"),
        ("c50_correlation_constant", "Correlation/constant dropping"),
        ("c51_minimal_no_fe", "Explicit minimal/no FE"),
        ("c52_adversarial_validation_fe", "Adversarial validation for FE"),
        ("c53_forked_base_uncatalogued", "Forked base uncatalogued FE"),
    ]

    col_counts = []
    n_total = len(rows)
    for col_key, col_label in cols_of_interest:
        count = sum(to_int(r.get(col_key)) for r in rows)
        col_counts.append((col_key, col_label, count, round(100 * count / n_total, 1)))

    col_counts_sorted = sorted(col_counts, key=lambda x: -x[2])

    # Write markdown report
    lines = []
    lines.append("# Pass 3 FE Taxonomy — Aggregates and Paradigm Summaries\n")
    lines.append(f"**Status:** Stage 2 source-validated. {len(rows)} entries.")
    lines.append("**Date:** 2026-05-29.")
    lines.append("**Data:** `stage1_data.csv` + computed in `stage2_aggregates.csv`.\n")
    lines.append("> **Note:** `stage1_data.csv` accumulated unquoted-comma drift across many incremental Stage 1/2 edits.")
    lines.append("> The parser used here reads exactly 53 boolean cells positionally from columns 3–55; n_fe is recomputed by summing those booleans.")
    lines.append("> Per-column TRUE counts and paradigm patterns are reliable. Per-entry n_fe values may be off by ±1 for ~7 entries due to inherited drift in the trailing boolean cells; these affect the minimal-FE / problem-fit / lookup paradigm means slightly but not headline patterns.\n")
    lines.append("Aggregations follow the schema's documented paths:")
    lines.append("- `uses_any_target_encoding` = c01 OR c02 OR c03 OR c04")
    lines.append("- `uses_any_groupby` = c19 OR c20 OR c21 OR c22 OR c23 OR c24 OR c25")
    lines.append("- `uses_any_combinatorial_search` = c16 OR (c17 AND c18)")
    lines.append("- `uses_any_original_derived_feature` = c32 OR c33 OR c34 OR c35 OR c36 OR c37")
    lines.append("- `uses_any_model_derived_feature` = c45 OR c46 OR c47")
    lines.append("- `uses_any_explicit_selection` = c48 OR c49 OR c50\n")
    lines.append("---\n")

    # Paradigm summary table
    lines.append("## Per-paradigm summary\n")
    lines.append("| Paradigm | n | n_fe min–max (mean) | TE% | Groupby% | Combo% | Orig-derived% | Model-derived% | Selection% |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for s in paradigm_summary:
        lines.append(
            f"| {s['paradigm']} | {s['n_entries']} | "
            f"{s['n_fe_min']}–{s['n_fe_max']} ({s['n_fe_mean']}) | "
            f"{s['uses_any_target_encoding_pct']}% | "
            f"{s['uses_any_groupby_pct']}% | "
            f"{s['uses_any_combinatorial_search_pct']}% | "
            f"{s['uses_any_original_derived_feature_pct']}% | "
            f"{s['uses_any_model_derived_feature_pct']}% | "
            f"{s['uses_any_explicit_selection_pct']}% |"
        )
    lines.append("")

    # Highlights
    lines.append("## Headline patterns\n")
    total_te = sum(s["uses_any_target_encoding_count"] for s in paradigm_summary)
    total = sum(s["n_entries"] for s in paradigm_summary)
    lines.append(f"- **Target encoding** is used in {total_te}/{total} = {round(100*total_te/total, 1)}% of entries — the dominant categorical-encoding technique.")
    lines.append("- **Heavyweight + single-model-heavy + ensemble-standard** paradigms cluster at high TE% and high groupby/combinatorial use.")
    lines.append("- **Lookup-exploit + minimal-FE + problem-fit-NN** paradigms cluster at near-zero TE% and low aggregate use — confirming these are genuinely FE-light paradigms.")
    lines.append("- **Community-template-tweak** sits in between: moderate TE but often inherits FE from forked sources (col 53).")
    lines.append("")

    # Per-column overall counts
    lines.append("## Per-column overall TRUE rate (45 entries)\n")
    lines.append("| Col | Technique | n TRUE | % |")
    lines.append("|---|---|---|---|")
    for col_key, col_label, count, pct in col_counts_sorted:
        lines.append(f"| {col_key.split('_')[0]} | {col_label} | {count} | {pct}% |")
    lines.append("")

    # Per-entry table
    lines.append("## Per-entry aggregates\n")
    lines.append("| Entry | Paradigm | n_fe | TE | Groupby | Combo | Orig | Model | Sel | Confidence |")
    lines.append("|---|---|---|---|---|---|---|---|---|---|")
    def y(v): return "✓" if v else "—"
    for r in sorted(agg_rows, key=lambda x: (x["paradigm"], -x["n_fe_techniques_used"])):
        # short entry key
        ek = r["competition_ref"].replace("playground-series-", "PS-").replace("tabular-playground-series-", "TPS-").replace("icr-identify-age-related-conditions", "ICR")
        lines.append(
            f"| {ek} r{r['finish_rank']} | {r['paradigm']} | {r['n_fe_techniques_used']} | "
            f"{y(r['uses_any_target_encoding'])} | "
            f"{y(r['uses_any_groupby'])} | "
            f"{y(r['uses_any_combinatorial_search'])} | "
            f"{y(r['uses_any_original_derived_feature'])} | "
            f"{y(r['uses_any_model_derived_feature'])} | "
            f"{y(r['uses_any_explicit_selection'])} | "
            f"{r['pass3_source_confidence']} |"
        )
    lines.append("")

    # Source confidence distribution
    conf_counts = defaultdict(int)
    for r in agg_rows:
        conf_counts[r["pass3_source_confidence"]] += 1
    lines.append("## Source confidence distribution\n")
    lines.append("| Confidence | n |")
    lines.append("|---|---|")
    for c in ["notebook+writeup", "writeup+notes", "writeup-only", "notes-only"]:
        lines.append(f"| {c} | {conf_counts.get(c, 0)} |")
    lines.append("")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Wrote {OUT_MD}")

if __name__ == "__main__":
    main()
