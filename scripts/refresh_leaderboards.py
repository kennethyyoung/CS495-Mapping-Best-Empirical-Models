"""
Re-fetches leaderboard top-3 for each competition in data/raw/ and writes
leaderboard.json. Run this once after fixing the page=1 API bug.
"""

import json
import time
from pathlib import Path

from kaggle import KaggleApi

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "data" / "raw"


def get_leaderboard_top(api: KaggleApi, slug: str, top_n: int = 3) -> list[dict]:
    entries = []
    try:
        board = api.competition_leaderboard_view(slug, page_size=top_n)
        for rank, entry in enumerate(board[:top_n], start=1):
            name = getattr(entry, "team_name", None) or getattr(entry, "teamName", None) or ""
            score = getattr(entry, "score", None)
            entries.append({"rank": rank, "teamName": name, "score": str(score)})
    except Exception as e:
        print(f"  ERROR: {e}")
    return entries


def main() -> None:
    api = KaggleApi()
    api.authenticate()

    comp_dirs = sorted(d for d in RAW_DIR.iterdir() if d.is_dir())
    total = len(comp_dirs)

    for i, comp_dir in enumerate(comp_dirs):
        slug = comp_dir.name
        lb_path = comp_dir / "leaderboard.json"
        if lb_path.exists():
            existing = json.loads(lb_path.read_text())
            if existing:  # already populated, skip
                names = [e["teamName"] for e in existing]
                display = ", ".join(names).encode("ascii", errors="replace").decode("ascii")
                print(f"[{i+1}/{total}] {slug} ... skip ({display})")
                continue

        print(f"[{i+1}/{total}] {slug}", end=" ... ", flush=True)
        entries = get_leaderboard_top(api, slug)
        (comp_dir / "leaderboard.json").write_text(json.dumps(entries, indent=2))
        names = [e["teamName"] for e in entries]
        display = ", ".join(names) if names else "empty"
        print(display.encode("ascii", errors="replace").decode("ascii"))
        time.sleep(0.4)

    print("\nDone.")


if __name__ == "__main__":
    main()
