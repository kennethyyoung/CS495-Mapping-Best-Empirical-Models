"""Inspect key cells of a notebook for data types, preprocessing, and FE."""
import json
import sys
from pathlib import Path

NB_PATH = Path(r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models\data\writeups\playground-series-s6e4\ps6e4-ensemble-cv-0-98155.ipynb")

nb = json.loads(NB_PATH.read_text(encoding="utf-8"))
cells = nb.get("cells", [])
print(f"Total cells: {len(cells)}\n")

# Keywords to flag as relevant
KEYWORDS = [
    "read_csv", "columns", "dtype", "nunique", "head(",
    "StandardScaler", "MinMaxScaler", "RobustScaler",
    "LabelEncoder", "OrdinalEncoder", "TargetEncoder", "OneHotEncoder", "get_dummies",
    "fillna", "dropna", "SimpleImputer", "isna", "isnull",
    "object", "category", "categorical",
    "StratifiedKFold", "KFold", "GroupKFold",
    "feature", "TARGET", "target", "FEATURES",
]

for i, c in enumerate(cells):
    src = "".join(c.get("source", []))
    if any(k in src for k in KEYWORDS):
        print(f"=== Cell {i} ({c['cell_type']}) ===")
        print(src[:800])
        print()
