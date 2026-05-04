"""
Raw solution data collector.

For each competition in data/kaggle_candidates_v2.xlsx:
  1. Fetches discussion topic list and identifies solution writeups by title
  2. Scrapes the HTML body of each solution topic (GitHub links, model mentions)
  3. Downloads the top-voted notebooks via the Kaggle kernels API
  4. Saves everything to data/raw/{competition_ref}/
  5. Writes data/solution_summary.csv with model mention flags per competition

Run after kaggle_scraper_v2.py.
"""

import json
import re
import time
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from kaggle import KaggleApi

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

SOLUTION_KEYWORDS = re.compile(
    r"\b(1st|2nd|3rd|gold|silver|bronze|winner|winning|solution|writeup|"
    r"place solution|my approach|what worked)\b",
    re.IGNORECASE,
)

GITHUB_RE = re.compile(r"https?://github\.com/[\w\-]+/[\w\-.\w]+", re.IGNORECASE)

MODEL_PATTERNS = {
    "xgboost": re.compile(r"\bxgb(oost)?\b", re.IGNORECASE),
    "lightgbm": re.compile(r"\blgb(m)?\b|\blightgbm\b", re.IGNORECASE),
    "catboost": re.compile(r"\bcatboost\b|\bcgb\b", re.IGNORECASE),
}


# ---------------------------------------------------------------------------
# Kaggle API helpers
# ---------------------------------------------------------------------------

def _fetch_topics(slug: str, auth: tuple, page_size: int = 30) -> list[dict]:
    url = f"https://www.kaggle.com/api/v1/competitions/{slug}/topics"
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


def _solution_topics(topics: list[dict]) -> list[dict]:
    return [t for t in topics if SOLUTION_KEYWORDS.search(t.get("title", ""))]


def _scrape_topic_body(topic_url: str, session: requests.Session) -> str:
    """Scrape body text from a Kaggle discussion page."""
    try:
        resp = session.get(topic_url, timeout=20)
        if not resp.ok:
            return ""
        soup = BeautifulSoup(resp.text, "html.parser")
        # Discussion bodies live in <div class="markdown-converter__text--rendered">
        bodies = soup.find_all("div", class_=re.compile(r"markdown"))
        return "\n\n".join(b.get_text(separator="\n") for b in bodies)
    except Exception:
        return ""


def _download_kernels(api: KaggleApi, slug: str, out_dir: Path, top_n: int = 5) -> list[str]:
    """Download top-voted competition kernels. Returns list of saved paths."""
    saved = []
    try:
        kernels = api.kernels_list(
            competition=slug,
            sort_by="voteCount",
            page_size=top_n,
        )
        for k in kernels:
            kernel_ref = k.ref  # e.g. "username/kernel-slug"
            kernel_dir = out_dir / "notebooks" / kernel_ref.replace("/", "__")
            kernel_dir.mkdir(parents=True, exist_ok=True)
            try:
                api.kernels_pull(kernel_ref, path=str(kernel_dir), metadata=False)
                saved.append(str(kernel_dir))
                time.sleep(0.5)
            except Exception:
                pass
    except Exception:
        pass
    return saved


def _extract_model_mentions(text: str) -> dict[str, bool]:
    return {model: bool(pat.search(text)) for model, pat in MODEL_PATTERNS.items()}


def _primary_model(mentions: dict[str, bool], text: str) -> str:
    """Pick the most-mentioned model; fall back to first detected."""
    counts = {
        model: len(pat.findall(text))
        for model, pat in MODEL_PATTERNS.items()
    }
    detected = {m: c for m, c in counts.items() if c > 0}
    if not detected:
        return "not described"
    return max(detected, key=lambda m: detected[m])


# ---------------------------------------------------------------------------
# Per-competition processing
# ---------------------------------------------------------------------------

def process_competition(
    slug: str,
    auth: tuple,
    session: requests.Session,
    api: KaggleApi,
) -> dict:
    comp_dir = RAW_DIR / slug
    comp_dir.mkdir(parents=True, exist_ok=True)

    # 1. Fetch topic list
    topics = _fetch_topics(slug, auth)
    (comp_dir / "topics.json").write_text(json.dumps(topics, indent=2))

    # 2. Identify solution topics
    sol_topics = _solution_topics(topics)

    # 3. Scrape body text for each solution topic
    all_text = ""
    github_urls: list[str] = []

    for topic in sol_topics[:5]:  # cap at 5 to respect rate limits
        url = topic.get("topicUrl", "")
        if not url:
            continue
        full_url = f"https://www.kaggle.com{url}" if url.startswith("/") else url
        body = _scrape_topic_body(full_url, session)
        if body:
            all_text += f"\n\n--- {topic['title']} ---\n{body}"
            github_urls.extend(GITHUB_RE.findall(body))
        time.sleep(1.0)  # be polite

    (comp_dir / "solution_text.txt").write_text(all_text, encoding="utf-8")

    # 4. Download top notebooks
    notebook_paths = _download_kernels(api, slug, comp_dir)

    # Also scan notebook files for model mentions
    for nb_path in notebook_paths:
        for f in Path(nb_path).rglob("*.ipynb"):
            try:
                all_text += f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                pass

    # 5. Extract model signals
    mentions = _extract_model_mentions(all_text)
    primary = _primary_model(mentions, all_text)
    unique_github = sorted(set(github_urls))

    return {
        "competition_ref": slug,
        "n_solution_topics": len(sol_topics),
        "github_urls": "; ".join(unique_github),
        "has_github_link": bool(unique_github),
        "primary_model": primary,
        "mentions_xgboost": mentions["xgboost"],
        "mentions_lightgbm": mentions["lightgbm"],
        "mentions_catboost": mentions["catboost"],
        "n_notebooks_downloaded": len(notebook_paths),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(only_with_solution_topic: bool = True) -> None:
    candidates_path = DATA_DIR / "kaggle_candidates_v2.xlsx"
    if not candidates_path.exists():
        raise FileNotFoundError(
            f"{candidates_path} not found — run kaggle_scraper_v2.py first"
        )

    df = pd.read_excel(candidates_path)
    if only_with_solution_topic and "has_solution_topic" in df.columns:
        df = df[df["has_solution_topic"] == True].reset_index(drop=True)

    creds = json.loads((Path.home() / ".kaggle" / "kaggle.json").read_text())
    auth = (creds["username"], creds["key"])

    # Authenticated session for HTML scraping
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (research project; kaggle meta-analysis)"
    })
    session.auth = auth

    api = KaggleApi()
    api.authenticate()

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    results = []
    total = len(df)
    for i, row in df.iterrows():
        slug = row["competition_ref"]
        print(f"[{i+1}/{total}] {slug}")
        result = process_competition(slug, auth, session, api)
        results.append(result)
        time.sleep(1.0)

    summary = pd.DataFrame(results)
    out = DATA_DIR / "solution_summary.csv"
    summary.to_csv(out, index=False)
    print(f"\nSaved summary → {out}")
    print(f"  has github link:  {summary['has_github_link'].sum()}/{len(summary)}")
    print(f"  primary_model breakdown:")
    print(summary["primary_model"].value_counts().to_string())


if __name__ == "__main__":
    main()
