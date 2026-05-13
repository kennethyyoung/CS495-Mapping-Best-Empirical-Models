"""
Phase A field extractor.

For each competition in data/raw/, reads:
  - topics.json  (solution writeup titles + vote counts)
  - leaderboard.json  (top-3 finisher usernames, if populated)
  - notebooks/  (directory names encode username + kernel slug)

Sends a structured prompt to Claude and extracts:
  primary_model, uses_ensemble, ensemble_type, uses_nn,
  uses_original_data, key_techniques, confidence, notes

Output: data/extracted_fields.csv
"""

import json
import time
from pathlib import Path

import anthropic
import pandas as pd

ROOT = Path(__file__).parent.parent
RAW_DIR = ROOT / "data" / "raw"
OUT_PATH = ROOT / "data" / "extracted_fields.csv"

SOLUTION_KEYWORDS_RE = __import__("re").compile(
    r"\b(1st|2nd|3rd|4th|5th|gold|silver|bronze|winner|winning|solution|writeup|"
    r"place solution|my approach|what worked)\b",
    __import__("re").IGNORECASE,
)

MODEL = "claude-haiku-4-5-20251001"

SYSTEM_PROMPT = """\
You are a research assistant helping with a meta-analysis of winning solutions \
in Kaggle tabular machine learning competitions. For each competition you will \
receive a list of solution writeup titles posted in the discussion forum, along \
with any available leaderboard and notebook metadata.

Your task: extract structured information about what the TOP FINISHERS \
(1st, 2nd, 3rd place) did. Focus on titles that indicate a top placement. \
If a title doesn't mention placement, use vote count as a rough signal of \
relevance.

Respond with a single JSON object — no markdown, no explanation, just the JSON.\
"""

EXTRACTION_SCHEMA = {
    "primary_model": "string — dominant model used by the winner: "
        "'xgboost' | 'lightgbm' | 'catboost' | 'neural_network' | 'linear' | "
        "'ensemble_mixed' | 'automl' | 'unknown'",
    "uses_ensemble": "boolean — did the winner combine multiple models?",
    "ensemble_type": "string or null — 'stacking' | 'blending' | 'averaging' | null",
    "stacking_levels": "integer or null — number of stacking levels if mentioned",
    "uses_nn": "boolean — did the winner use a neural network (even as part of ensemble)?",
    "uses_original_data": "boolean or null — did they use the original (non-synthetic) dataset? "
        "null if not mentioned or not applicable",
    "key_techniques": "list of short strings — notable techniques mentioned "
        "(e.g. 'pseudo labeling', 'hill climbing', 'target encoding', 'feature engineering'). "
        "Max 5 items.",
    "top_place_mentioned": "integer or null — highest placement explicitly mentioned "
        "(e.g. 1 for '1st place', 2 for '2nd place', null if none)",
    "confidence": "string — 'high' (clear explicit statements) | "
        "'medium' (implied or partial) | 'low' (sparse titles, mostly unknown)",
    "notes": "string — one sentence explaining what you inferred and from which titles",
}


def _build_prompt(slug: str, sol_topics: list[dict], leaderboard: list[dict], nb_names: list[str]) -> str:
    lines = [f"Competition: {slug}\n"]

    if leaderboard:
        lines.append("Leaderboard top 3:")
        for e in leaderboard:
            lines.append(f"  #{e['rank']} {e['teamName']} (score: {e['score']})")
        lines.append("")

    if sol_topics:
        lines.append("Solution writeup titles (sorted by votes):")
        for t in sol_topics:
            lines.append(f"  [{t['votes']} votes] {t['title']}")
        lines.append("")

    if nb_names:
        lines.append("Available notebooks (username__kernel-slug):")
        for n in nb_names[:5]:
            lines.append(f"  {n}")
        lines.append("")

    lines.append("Extract fields per this schema:")
    lines.append(json.dumps(EXTRACTION_SCHEMA, indent=2))

    return "\n".join(lines)


def extract_competition(client: anthropic.Anthropic, slug: str, comp_dir: Path) -> dict:
    # Load topics
    topics_path = comp_dir / "topics.json"
    topics = json.loads(topics_path.read_text()) if topics_path.exists() else []
    sol_topics = sorted(
        [t for t in topics if SOLUTION_KEYWORDS_RE.search(t.get("title", ""))],
        key=lambda t: t.get("votes", 0),
        reverse=True,
    )[:8]  # top 8 by votes

    # Load leaderboard
    lb_path = comp_dir / "leaderboard.json"
    leaderboard = json.loads(lb_path.read_text()) if lb_path.exists() else []

    # Get notebook directory names
    nb_dir = comp_dir / "notebooks"
    nb_names = [d.name for d in nb_dir.iterdir() if d.is_dir()] if nb_dir.exists() else []

    if not sol_topics and not leaderboard and not nb_names:
        return _empty_result(slug, "no data available")

    prompt = _build_prompt(slug, sol_topics, leaderboard, nb_names)

    try:
        resp = client.messages.create(
            model=MODEL,
            max_tokens=512,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text.strip()
        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        fields = json.loads(raw)
    except Exception as e:
        return _empty_result(slug, f"extraction error: {e}")

    fields["competition_ref"] = slug
    fields["n_sol_topics"] = len(sol_topics)
    return fields


def _empty_result(slug: str, reason: str) -> dict:
    return {
        "competition_ref": slug,
        "primary_model": "unknown",
        "uses_ensemble": None,
        "ensemble_type": None,
        "stacking_levels": None,
        "uses_nn": None,
        "uses_original_data": None,
        "key_techniques": [],
        "top_place_mentioned": None,
        "confidence": "low",
        "notes": reason,
        "n_sol_topics": 0,
    }


def main() -> None:
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

    comp_dirs = sorted(RAW_DIR.iterdir())
    results = []
    total = len(comp_dirs)

    for i, comp_dir in enumerate(comp_dirs):
        if not comp_dir.is_dir():
            continue
        slug = comp_dir.name
        print(f"[{i+1}/{total}] {slug}", end=" ... ", flush=True)
        result = extract_competition(client, slug, comp_dir)
        print(result.get("confidence", "?"), f"| {result.get('primary_model', '?')}")
        results.append(result)
        time.sleep(0.3)  # light rate limiting

    df = pd.DataFrame(results)
    # Normalize key_techniques list → semicolon string for CSV
    df["key_techniques"] = df["key_techniques"].apply(
        lambda x: "; ".join(x) if isinstance(x, list) else (x or "")
    )
    df.to_csv(OUT_PATH, index=False)
    print(f"\nSaved → {OUT_PATH}")
    print(f"  high confidence:   {(df['confidence'] == 'high').sum()}/{len(df)}")
    print(f"  medium confidence: {(df['confidence'] == 'medium').sum()}/{len(df)}")
    print(f"  low confidence:    {(df['confidence'] == 'low').sum()}/{len(df)}")
    print(f"\nPrimary model breakdown:")
    print(df["primary_model"].value_counts().to_string())


if __name__ == "__main__":
    main()
