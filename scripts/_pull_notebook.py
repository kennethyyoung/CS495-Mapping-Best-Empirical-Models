from kaggle import KaggleApi
from pathlib import Path

api = KaggleApi()
api.authenticate()

BASE = Path(r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models\data\writeups")

notebooks = [
    ("kirill0212/ps6e4-ensemble-cv-0-98155", BASE / "playground-series-s6e4"),
]

for ref, out in notebooks:
    out.mkdir(parents=True, exist_ok=True)
    api.kernels_pull(ref, path=str(out), metadata=False)
    pulled = [f.name for f in out.iterdir() if f.suffix == ".ipynb"]
    print(f"{ref} -> {pulled}")
