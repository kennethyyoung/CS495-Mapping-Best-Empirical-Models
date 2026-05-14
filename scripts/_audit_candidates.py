import pandas as pd

candidates = pd.read_excel(
    r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models\data\kaggle_candidates_v2.xlsx"
)
coded = pd.read_excel(
    r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models\data\kaggle_meta_analysis.xlsx",
    sheet_name="Competition Data"
)

print("Candidates columns:", list(candidates.columns))
print("Total candidates:", len(candidates))
print()

if "recommended_action" in candidates.columns:
    print("recommended_action breakdown:")
    print(candidates["recommended_action"].value_counts().to_string())
    print()

coded_slugs = set(coded["competition_ref"].astype(str).str.strip())
if "competition_ref" in candidates.columns:
    cand_slugs = set(candidates["competition_ref"].astype(str).str.strip())
    not_coded = cand_slugs - coded_slugs
    print(f"Candidates not in coded dataset ({len(not_coded)}):")
    sub = candidates[candidates["competition_ref"].isin(not_coded)][
        [c for c in ["competition_ref", "recommended_action", "has_solution_topic", "title"] if c in candidates.columns]
    ]
    print(sub.to_string(index=False))
