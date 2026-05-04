"""
Competition discovery and pre-filtering.

Fetches playground (PS3–PS5) and featured (2022+) competitions from the
Kaggle API, applies keyword exclusion, and scores each candidate by whether
a solution-writeup discussion exists. Outputs a ranked shortlist to:
    data/kaggle_candidates_v2.xlsx
"""

import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from kaggle import KaggleApi

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

# --- Exclusion / inclusion patterns ---

EXCLUDE_KEYWORDS = [
    # Time series / forecasting
    "forecast", "time series", "timeseries", "sales forecast", "mini-course sales",
    # Computer vision / imaging
    "image", "vision", "satellite", "aerial", "radiology", "rsna",
    "lumbar", "fracture", "aneurysm", "trauma", "mammograph", "cryo-et",
    "object detection", "segmentation", "point cloud", "3d",
    # NLP / text
    "nlp", "text classification", "sentiment", "language model",
    "essay", "writing quality", "writing process",
    "patent", "jigsaw", "toxic", "chatbot", "multilingual", "translation",
    "curriculum recommendation", "misconception",
    # LLM / generative AI
    "llm", "gemma", "gemini", "gpt", "chatgpt", "red teaming",
    "prompt recovery", "ai-generated text", "ai generated",
    # Speech / audio
    "speech", "audio", "sound",
    # Bio / molecular
    "protein", "molecule", "drug", "genomic", "enzyme", "polymer",
    "vesuvius", "ink detection",
    # Game AI / RL / puzzles
    "lux ai", "kore", "chess", "santa 20", "capture the flag",
    "arc-agi", "arc prize", "arc agi", "llm-20-questions", "20 questions",
    "drawing with", "orbit-wars",
    # Math olympiad
    "olympiad", "mathematical olympiad",
    # Sports analytics
    "nfl", "fifa", "bundesliga", "march mania", "march machine learning mania",
    # Geospatial / location
    "foursquare", "location matching",
    # Hackathons / non-standard
    "hackathon", "konwinski",
    # Video
    "video", "dfl-bundesliga",
]

PS_SLUG = re.compile(r"playground-series-s([3-5])e\d+$")

SOLUTION_KEYWORDS = re.compile(
    r"\b(1st|2nd|3rd|gold|silver|bronze|winner|winning|solution|writeup|"
    r"place solution|my approach|what worked)\b",
    re.IGNORECASE,
)


def _slug(ref: str) -> str:
    """Extract competition slug from full URL or return as-is."""
    return ref.rstrip("/").split("/")[-1]


def _is_excluded(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in EXCLUDE_KEYWORDS)


def _is_ps3_to_s5(ref: str) -> bool:
    return bool(PS_SLUG.search(_slug(ref)))


def _is_monetized(reward: str | None, category: str) -> bool:
    if category != "featured":
        return False
    if not reward:
        return False
    non_cash = {"knowledge", "kudos", "swag", ""}
    return reward.strip().lower() not in non_cash


def _fetch_topics(competition_slug: str, auth: tuple, page_size: int = 20) -> list[dict]:
    """Return top discussion topics (by vote) for a competition."""
    url = f"https://www.kaggle.com/api/v1/competitions/{competition_slug}/topics"
    try:
        resp = requests.get(
            url,
            params={"sortBy": "voteCount", "pageSize": page_size},
            auth=auth,
            timeout=15,
        )
        if resp.ok:
            return resp.json().get("topics", [])
    except requests.RequestException:
        pass
    return []


def _score_topics(topics: list[dict]) -> tuple[bool, int]:
    """Return (has_solution_topic, n_solution_topics)."""
    solution_topics = [
        t for t in topics if SOLUTION_KEYWORDS.search(t.get("title", ""))
    ]
    return bool(solution_topics), len(solution_topics)


def _list_competitions(api: KaggleApi, category: str, max_pages: int = 10) -> list:
    comps = []
    for page in range(1, max_pages + 1):
        result = api.competitions_list(category=category, sort_by="latestDeadline", page=page)
        batch = list(result.competitions) if hasattr(result, "competitions") else []
        if not batch:
            break
        comps.extend(batch)
        time.sleep(0.3)
    return comps


def scrape_candidates(auth: tuple) -> pd.DataFrame:
    api = KaggleApi()
    api.authenticate()

    candidates: list[dict] = []

    # --- Playground Series S3–S5 (filter by ref slug, title is episode-specific) ---
    for comp in _list_competitions(api, "playground"):
        if not _is_ps3_to_s5(comp.ref):
            continue
        if _is_excluded(comp.title):
            continue
        candidates.append(("playground", comp))

    # --- Featured 2022+ ---
    cutoff = datetime(2022, 1, 1, tzinfo=timezone.utc)
    for comp in _list_competitions(api, "featured"):
        deadline = comp.deadline
        if deadline is None:
            continue
        if deadline.tzinfo is None:
            deadline = deadline.replace(tzinfo=timezone.utc)
        if deadline < cutoff:
            continue
        if _is_excluded(comp.title):
            continue
        candidates.append(("featured", comp))

    # --- Build rows with solution topic detection ---
    records = []
    for category, comp in candidates:
        slug = _slug(comp.ref)
        topics = _fetch_topics(slug, auth)
        has_solution, n_solutions = _score_topics(topics)
        time.sleep(0.3)

        records.append({
            "competition_ref": slug,
            "title": comp.title,
            "category": category,
            "eval_metric": comp.evaluation_metric,
            "n_teams": comp.team_count,
            "end_date": comp.deadline.date() if comp.deadline else None,
            "is_monetized": _is_monetized(comp.reward, category),
            "has_solution_topic": has_solution,
            "n_solution_topics": n_solutions,
            "url": f"https://www.kaggle.com/competitions/{slug}",
        })

    df = pd.DataFrame(records)
    df = df.sort_values(
        ["has_solution_topic", "n_solution_topics", "n_teams"],
        ascending=[False, False, False],
    ).reset_index(drop=True)
    return df


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    creds = json.loads((Path.home() / ".kaggle" / "kaggle.json").read_text())
    auth = (creds["username"], creds["key"])

    print("Fetching competition list...")
    df = scrape_candidates(auth)

    out = DATA_DIR / "kaggle_candidates_v2.xlsx"
    df.to_excel(out, index=False)

    print(f"\nSaved {len(df)} candidates → {out}")
    print(f"  with solution topic:    {df['has_solution_topic'].sum()}")
    print(f"  without solution topic: {(~df['has_solution_topic']).sum()}")
    print()
    print(df[["competition_ref", "category", "n_teams", "has_solution_topic", "n_solution_topics"]].to_string())


if __name__ == "__main__":
    main()
