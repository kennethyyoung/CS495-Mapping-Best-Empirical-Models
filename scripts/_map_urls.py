"""
Maps out what URL resources exist for each coded entry:
  - writeup_url from Excel (if any)
  - top solution topic URLs reconstructed from topics.json
  - whether a GitHub link appears in the topic title
"""
import json
import re
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "data" / "raw"

df = pd.read_excel(ROOT / "data" / "kaggle_meta_analysis.xlsx", sheet_name="Competition Data")

NOT_DESCRIBED = {"not described", "not_described", "nan", "none", ""}
target_cols = ["cv_strategy", "encoding_strategy", "missing_data_strategy",
               "scaling", "hyperparameter_tuning", "best_single_model"]

SOLUTION_RE = re.compile(
    r"\b(1st|2nd|3rd|gold|silver|bronze|winner|winning|solution|writeup|"
    r"place solution|my approach|what worked)\b", re.IGNORECASE
)
GITHUB_RE = re.compile(r"github\.com", re.IGNORECASE)

def is_nd(val):
    return str(val).strip().lower() in NOT_DESCRIBED

rows = []
for _, row in df.sort_values(["writeup_detail", "competition_ref"], ascending=[False, True]).iterrows():
    slug = row["competition_ref"]
    wd = int(row.get("writeup_detail") or 0)
    n_missing = sum(is_nd(row[c]) for c in target_cols)
    empty_fields = [c for c in target_cols if is_nd(row[c])]

    # Check topics.json for solution topics
    topics_path = RAW_DIR / slug / "topics.json"
    top_topics = []
    has_github_in_title = False
    if topics_path.exists():
        topics = json.loads(topics_path.read_text(encoding="utf-8"))
        sol = sorted(
            [t for t in topics if SOLUTION_RE.search(t.get("title", ""))],
            key=lambda t: t.get("votes", 0), reverse=True
        )[:3]
        for t in sol:
            tid = t.get("id") or t.get("topicId", "")
            title = t.get("title", "")
            votes = t.get("votes", 0)
            url = f"https://www.kaggle.com/competitions/{slug}/discussion/{tid}"
            if GITHUB_RE.search(title):
                has_github_in_title = True
            top_topics.append((votes, title[:60], url))

    rows.append({
        "slug": slug,
        "wd": wd,
        "n_missing": n_missing,
        "empty_fields": ", ".join(empty_fields),
        "top_topics": top_topics,
        "has_github_title": has_github_in_title,
    })

print(f"{'#':<3} {'competition':<38} {'wd':>3} {'miss':>5}  top solution topic (votes) + url")
print("=" * 110)
for i, r in enumerate(rows, 1):
    slug_short = r["slug"].replace("playground-series-", "ps-")
    print(f"\n{i:<3} {slug_short:<38} {r['wd']:>3} {r['n_missing']:>5}  missing: {r['empty_fields']}")
    for votes, title, url in r["top_topics"]:
        gh = " [GH]" if GITHUB_RE.search(title) else ""
        print(f"     [{votes:>4}v] {title}{gh}")
        print(f"            {url}")
