from kaggle import KaggleApi
from pathlib import Path
import zipfile, os

api = KaggleApi()
api.authenticate()

SLUG = "playground-series-s4e10"
OUT = Path(r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models\data\tmp")
OUT.mkdir(exist_ok=True)

print(f"Downloading train.csv for {SLUG}...")
api.competition_download_file(SLUG, "train.csv", path=str(OUT))

# May come back as a zip
downloaded = list(OUT.iterdir())
print("Downloaded:", [f.name for f in downloaded])

# Unzip if needed
for f in downloaded:
    if f.suffix == ".zip":
        with zipfile.ZipFile(f) as z:
            z.extractall(OUT)
        f.unlink()

csv_file = OUT / "train.csv"
if csv_file.exists():
    import pandas as pd
    df = pd.read_csv(csv_file)
    n_features = len(df.columns) - 2  # subtract id and target
    pct_missing = round(df.isnull().sum().sum() / df.size * 100, 2)
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {len(df.columns)}  =>  n_features: {n_features}")
    print(f"  pct_missing: {pct_missing}%")
    csv_file.unlink()
    print("  CSV deleted.")
else:
    print("train.csv not found after extraction.")
