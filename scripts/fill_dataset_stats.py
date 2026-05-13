"""
Downloads train.csv for each competition in kaggle_meta_analysis.xlsx,
extracts n_features and pct_missing, writes them back to the sheet.
Only fills rows where both fields are currently empty/null.
Skips competitions where download fails (not joined yet).
"""
from kaggle import KaggleApi
from pathlib import Path
import zipfile, pandas as pd, openpyxl

api = KaggleApi()
api.authenticate()

ROOT = Path(__file__).parent.parent
XL_PATH = ROOT / "data" / "kaggle_meta_analysis.xlsx"
TMP = ROOT / "data" / "tmp"
TMP.mkdir(exist_ok=True)

wb = openpyxl.load_workbook(XL_PATH)
ws = wb["Competition Data"]
headers = [c.value for c in ws[1]]

ref_col    = headers.index("competition_ref") + 1
nfeat_col  = headers.index("n_features") + 1
pmiss_col  = headers.index("pct_missing") + 1

updated, skipped, failed = [], [], []

for r in range(2, ws.max_row + 1):
    slug = str(ws.cell(r, ref_col).value or "").strip()
    if not slug:
        continue

    nfeat_val = ws.cell(r, nfeat_col).value
    pmiss_val = ws.cell(r, pmiss_col).value
    if nfeat_val not in (None, "", "not_described") and pmiss_val not in (None, "", "not_described"):
        skipped.append(slug)
        continue

    csv_path = TMP / "train.csv"
    try:
        api.competition_download_file(slug, "train.csv", path=str(TMP), quiet=True)

        # unzip if needed
        for f in TMP.iterdir():
            if f.suffix == ".zip":
                with zipfile.ZipFile(f) as z:
                    z.extractall(TMP)
                f.unlink()

        if not csv_path.exists():
            print(f"  {slug}: train.csv not found after download")
            failed.append(slug)
            continue

        df = pd.read_csv(csv_path)
        csv_path.unlink()

        # subtract id and target columns (assume first col is id, last is target)
        n_features = len(df.columns) - 2
        pct_missing = round(df.isnull().sum().sum() / df.size * 100, 2)

        ws.cell(r, nfeat_col).value = n_features
        ws.cell(r, pmiss_col).value = pct_missing
        updated.append(f"{slug}: n_features={n_features}, pct_missing={pct_missing}%")
        print(f"  {slug}: {n_features} features, {pct_missing}% missing")

    except Exception as e:
        print(f"  {slug}: FAILED — {e}")
        failed.append(slug)

wb.save(XL_PATH)
print(f"\nDone. Updated: {len(updated)}, Skipped (already filled): {len(skipped)}, Failed: {len(failed)}")
if failed:
    print("Failed (likely not joined):", failed)
