import os
os.chdir(r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models")
import pandas as pd
import numpy as np

df = pd.read_excel("data/kaggle_meta_analysis.xlsx", sheet_name="Competition Data")
N = len(df)

# Truly missing = we don't know what the winner did
UNKNOWN = {"not_described", "not described", "nan", ""}

def is_unknown(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return True
    if isinstance(v, bool):
        return False  # True/False are valid answers
    return str(v).strip().lower() in UNKNOWN

def fill_rate(col):
    vals = df[col].tolist()
    filled = sum(1 for v in vals if not is_unknown(v))
    return filled, N, round(filled / N * 100, 1)

FLOWCHART_FIELDS = [
    "target_type", "n_features", "pct_missing", "feature_type_dominant",
    "has_categorical", "missing_data_strategy", "encoding_strategy",
    "scaling", "outlier_treatment", "rare_class_handling",
    "primary_model", "ensemble_method", "cv_strategy",
    "hyperparameter_tuning", "original_data_usage", "fe_techniques",
]

print(f"DATASET: {N} entries\n")
print(f"{'Field':<30s}  {'Filled':>6}  {'Unknown':>7}  {'Fill%':>6}  Status")
print("-" * 65)
for col in FLOWCHART_FIELDS:
    if col not in df.columns:
        print(f"  {col:<30s}  MISSING COLUMN")
        continue
    filled, total, pct = fill_rate(col)
    unknown = total - filled
    status = "✓" if pct >= 80 else ("!" if pct >= 50 else "✗")
    print(f"  {col:<30s}  {filled:>4}/{total}  {unknown:>6}unk  {pct:>5.1f}%  {status}")

print("\n--- CONSISTENCY ISSUES (synonyms / type mismatches) ---")
checks = {
    "encoding_strategy":   ["target", "target_encoding", "OHE", "one_hot_encoding",
                             "one_hot", "ohe", "label", "label_encoding"],
    "scaling":             ["standard", "standard_scaler"],
    "outlier_treatment":   ["not described", "not_described"],
    "rare_class_handling": ["not described", "not_described"],
    "original_data_usage": ["True", "False", "not_used"],
    "ensemble_method":     ["weighted_blending", "weighted_blend", "blending"],
    "distribution_shift":  ["TRUE", "FALSE", "low", "not described", "not_described"],
}
for col, variants in checks.items():
    counts = df[col].value_counts(dropna=False)
    found = {v: int(counts.get(v, 0)) for v in variants if counts.get(v, 0) > 0}
    if found:
        print(f"  {col}: {found}")

print("\n--- FIELDS LIKELY TOO SPARSE FOR FLOWCHART NODES ---")
for col in FLOWCHART_FIELDS:
    if col not in df.columns: continue
    filled, total, pct = fill_rate(col)
    if pct < 50:
        counts = df[col].value_counts(dropna=False)
        nd = int(counts.get("not_described", 0)) + int(counts.get("not described", 0))
        print(f"  {col}: {filled}/{total} filled, {nd} genuinely unknown")
