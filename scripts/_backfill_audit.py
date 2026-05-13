import pandas as pd

df = pd.read_excel(
    r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models\data\kaggle_meta_analysis.xlsx",
    sheet_name="Competition Data",
)

NOT_DESCRIBED = {"not described", "not_described", "nan", "none", ""}

target_cols = ["cv_strategy", "encoding_strategy", "missing_data_strategy", "scaling", "hyperparameter_tuning", "best_single_model"]

def is_nd(val):
    return str(val).strip().lower() in NOT_DESCRIBED

df["n_missing"] = df[target_cols].apply(lambda row: sum(is_nd(v) for v in row), axis=1)

print(f"{'competition_ref':<40} {'wd':>3} {'missing':>8}  empty fields")
print("-" * 90)
for _, row in df.sort_values(["writeup_detail", "n_missing"], ascending=[False, True]).iterrows():
    empty = [c for c in target_cols if is_nd(row[c])]
    url = str(row.get("writeup_url", "")).strip()
    url_short = url[:60] if url and url != "nan" else "(no url)"
    print(f"  {row['competition_ref']:<38} {int(row['writeup_detail'] or 0):>3} {row['n_missing']:>8}  {', '.join(empty)}")

print()
print("writeup_detail breakdown:")
print(df["writeup_detail"].value_counts().sort_index().to_string())
print()
print("writeup_url present:", (df["writeup_url"].astype(str).str.strip().str.lower().isin(NOT_DESCRIBED) == False).sum(), "/", len(df))
