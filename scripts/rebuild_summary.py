"""
Rebuilds data/solution_summary.csv from data already on disk:
  - data/raw/{slug}/leaderboard.json  → winner names
  - data/raw/{slug}/topics.json       → solution topic count
  - data/raw/{slug}/solution_text.txt → github URLs, model keyword mentions
  - data/extracted_fields.csv         → primary_model from Phase A extraction
"""

import json
import re
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "data" / "raw"
EXTRACTED = ROOT / "data" / "extracted_fields.csv"
OUT = ROOT / "data" / "solution_summary.csv"

SOLUTION_KEYWORDS = re.compile(
    r"\b(1st|2nd|3rd|gold|silver|bronze|winner|winning|solution|writeup|"
    r"place solution|my approach|what worked)\b",
    re.IGNORECASE,
)
GITHUB_RE = re.compile(r"https?://github\.com/[\w\-]+/[\w\-.\w]+", re.IGNORECASE)
MODEL_PATTERNS = {
    "xgboost":  re.compile(r"\bxgb(oost)?\b", re.IGNORECASE),
    "lightgbm": re.compile(r"\blgb(m)?\b|\blightgbm\b", re.IGNORECASE),
    "catboost": re.compile(r"\bcatboost\b|\bcgb\b", re.IGNORECASE),
}


def process(slug: str, comp_dir: Path) -> dict:
    # Winner names from leaderboard
    lb_path = comp_dir / "leaderboard.json"
    leaderboard = json.loads(lb_path.read_text(encoding="utf-8")) if lb_path.exists() else []
    names = [e.get("teamName", "") for e in leaderboard]

    # Solution topic count from topics.json
    topics_path = comp_dir / "topics.json"
    topics = json.loads(topics_path.read_text(encoding="utf-8")) if topics_path.exists() else []
    n_sol = sum(1 for t in topics if SOLUTION_KEYWORDS.search(t.get("title", "")))

    # GitHub URLs and model mentions from solution_text.txt (may be empty)
    text_path = comp_dir / "solution_text.txt"
    text = text_path.read_text(encoding="utf-8", errors="ignore") if text_path.exists() else ""
    github_urls = sorted(set(GITHUB_RE.findall(text)))
    mentions = {m: bool(pat.search(text)) for m, pat in MODEL_PATTERNS.items()}

    return {
        "competition_ref": slug,
        "winner_1st": names[0] if len(names) > 0 else "",
        "winner_2nd": names[1] if len(names) > 1 else "",
        "winner_3rd": names[2] if len(names) > 2 else "",
        "n_solution_topics": n_sol,
        "github_urls": "; ".join(github_urls),
        "has_github_link": bool(github_urls),
        "mentions_xgboost": mentions["xgboost"],
        "mentions_lightgbm": mentions["lightgbm"],
        "mentions_catboost": mentions["catboost"],
    }


def main() -> None:
    comp_dirs = sorted(d for d in RAW_DIR.iterdir() if d.is_dir())

    rows = [process(d.name, d) for d in comp_dirs]
    summary = pd.DataFrame(rows)

    # Merge primary_model from Phase A extraction
    if EXTRACTED.exists():
        extracted = pd.read_csv(EXTRACTED, usecols=["competition_ref", "primary_model",
                                                     "confidence", "uses_ensemble",
                                                     "ensemble_type", "uses_nn"])
        summary = summary.merge(extracted, on="competition_ref", how="left")
    else:
        summary["primary_model"] = "not described"

    summary.to_csv(OUT, index=False)
    print(f"Saved → {OUT}")
    print(f"  competitions: {len(summary)}")
    print(f"  with winner names: {(summary['winner_1st'] != '').sum()}/{len(summary)}")
    print()
    print("primary_model breakdown:")
    print(summary["primary_model"].value_counts().to_string())
    print()
    print("confidence breakdown:")
    print(summary["confidence"].value_counts().to_string())


if __name__ == "__main__":
    main()
