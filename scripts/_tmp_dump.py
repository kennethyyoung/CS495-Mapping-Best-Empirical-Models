import os
os.chdir(r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models")
import openpyxl
import pandas as pd

df = pd.read_excel("data/kaggle_meta_analysis.xlsx", sheet_name="Competition Data")
print(f"Shape: {df.shape}")
print("\n--- dtypes ---")
print(df.dtypes.to_string())
print("\n--- value counts for coded fields ---")
coded = [
    "target_type", "feature_type_dominant", "has_categorical", "distribution_shift",
    "missing_data_strategy", "encoding_strategy", "outlier_treatment", "scaling",
    "primary_model", "cv_strategy", "rare_class_handling", "ensemble_method",
    "fe_techniques", "hyperparameter_tuning", "original_data_usage",
    "finish_rank", "writeup_detail",
]
for col in coded:
    if col in df.columns:
        print(f"\n{col}:")
        print(df[col].value_counts(dropna=False).to_string())
