"""
Fetches leaderboard + solution topics for new candidate competitions
(TPS 2022 and PS S6) and reports coding availability before committing
to full data collection.
"""
import json
import re
import time
from pathlib import Path

import requests
from kaggle import KaggleApi

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "data" / "raw"

SOLUTION_KEYWORDS = re.compile(
    r"\b(1st|2nd|3rd|gold|silver|bronze|winner|winning|solution|writeup|"
    r"place solution|my approach|what worked)\b",
    re.IGNORECASE,
)

# Screened candidates: TPS 2022 (tabular only) + PS S6
NEW_SLUGS = [
    # TPS 2022 — excluded: jan (SMAPE/time-series), jul (clustering), sep (SMAPE/time-series)
    "tabular-playground-series-feb-2022",
    "tabular-playground-series-mar-2022",
    "tabular-playground-series-apr-2022",
    "tabular-playground-series-may-2022",
    "tabular-playground-series-jun-2022",
    "tabular-playground-series-aug-2022",
    "tabular-playground-series-oct-2022",
    "tabular-playground-series-nov-2022",
    # PS S6
    "playground-series-s6e1",
    "playground-series-s6e2",
    "playground-series-s6e3",
    "playground-series-s6e4",
]

def fetch_topics(slug, auth):
    url = f"https://www.kaggle.com/api/v1/competitions/{slug}/topics"
    try:
        r = requests.get(url, params={"sortBy": "voteCount", "pageSize": 30},
                         auth=auth, timeout=15)
        if r.ok:
            return r.json().get("topics", [])
    except Exception:
        pass
    return []

def get_leaderboard(api, slug):
    try:
        board = api.competition_leaderboard_view(slug, page_size=3)
        return [
            {
                "rank": i + 1,
                "teamName": getattr(e, "teamName", None) or getattr(e, "team_name", "") or "",
                "score": str(getattr(e, "score", "")),
            }
            for i, e in enumerate(board[:3])
        ]
    except Exception:
        return []

def check_notebooks(api, slug, leaderboard):
    """Check if any top-3 finisher has a public notebook for this competition."""
    for entry in leaderboard:
        username = entry["teamName"]
        if not username:
            continue
        try:
            kernels = api.kernels_list(competition=slug, user=username,
                                       sort_by="voteCount", page_size=5)
            if kernels:
                return username, getattr(kernels[0], "ref", "unknown")
        except Exception:
            pass
        time.sleep(0.3)
    return None, None

creds = json.loads((Path.home() / ".kaggle" / "kaggle.json").read_text())
auth = (creds["username"], creds["key"])

api = KaggleApi()
api.authenticate()

print(f"{'Slug':<48} {'Teams':>5}  {'Sol.Topics':>10}  {'Notebook?':>10}  {'Top3'}")
print("-" * 105)

results = []
for slug in NEW_SLUGS:
    comp_dir = RAW_DIR / slug
    comp_dir.mkdir(parents=True, exist_ok=True)

    topics = fetch_topics(slug, auth)
    (comp_dir / "topics.json").write_text(json.dumps(topics, indent=2))
    sol_topics = [t for t in topics if SOLUTION_KEYWORDS.search(t.get("title", ""))]

    leaderboard = get_leaderboard(api, slug)
    (comp_dir / "leaderboard.json").write_text(json.dumps(leaderboard, indent=2))

    nb_user, nb_ref = check_notebooks(api, slug, leaderboard)
    top3 = ", ".join(e["teamName"] for e in leaderboard if e["teamName"])

    # Pull n_teams from leaderboard length as proxy (API doesn't expose it here)
    # Use competition_list to get team count
    n_sol = len(sol_topics)
    nb_str = nb_ref if nb_ref else "none"

    results.append({
        "slug": slug,
        "n_solution_topics": n_sol,
        "has_notebook": nb_ref is not None,
        "notebook_ref": nb_ref or "",
        "top3": top3,
        "sol_topic_titles": [t.get("title", "") for t in sol_topics[:3]],
    })

    print(f"  {slug:<46} {n_sol:>10} sol  {nb_str[:28]:>30}  {top3[:30]}")
    time.sleep(1.0)

print("\n--- SUMMARY ---")
has_source = [r for r in results if r["n_solution_topics"] > 0 or r["has_notebook"]]
no_source  = [r for r in results if r["n_solution_topics"] == 0 and not r["has_notebook"]]
print(f"Codeable (solution topic or notebook): {len(has_source)}/{len(results)}")
print(f"No source available:                   {len(no_source)}/{len(results)}")

if no_source:
    print("\nSkip these:")
    for r in no_source:
        print(f"  {r['slug']}")

print("\nSolution topic titles found:")
for r in results:
    if r["sol_topic_titles"]:
        print(f"\n  {r['slug']}:")
        for t in r["sol_topic_titles"]:
            print(f"    - {t}")
