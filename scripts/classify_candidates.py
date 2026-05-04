"""
Adds recommended_action and reason columns to kaggle_candidates_v2.xlsx
based on competition type. Run once; review the output.
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

# action: "keep" | "exclude" | "verify"
CLASSIFICATIONS = {
    # --- Clearly out of scope: NOT tabular cross-sectional ---

    # Sports tracking / computer vision
    "nfl-player-contact-detection":             ("exclude", "Player tracking video/sensor data, not tabular rows"),
    # Accessibility / chart-to-text (NLP + vision)
    "benetech-making-graphs-accessible":        ("exclude", "Convert chart images to text — vision + NLP, not tabular"),
    # Time series sensor data (sleep staging from wrist sensor)
    "child-mind-institute-detect-sleep-states": ("exclude", "Time series sensor data, not cross-sectional rows"),
    # NLP: scoring free-text clinical notes
    "nbme-score-clinical-patient-notes":        ("exclude", "Raw text input (clinical notes) — NLP, not tabular"),
    # Astrophysics spectroscopy (signal processing)
    "ariel-data-challenge-2025":                ("exclude", "Spectroscopy signal data, not standard tabular"),
    "ariel-data-challenge-2024":                ("exclude", "Spectroscopy signal data, not standard tabular"),
    # NLP: student math misconceptions from text
    "map-charting-student-math-misunderstandings": ("exclude", "Text classification of student responses — NLP"),
    # Time series: sensor behavior detection
    "cmi-detect-behavior-with-sensor-data":     ("exclude", "Time series sensor data, not cross-sectional"),
    # Recommender system (sequence/interaction data)
    "otto-recommender-system":                  ("exclude", "Session-based recommender — interaction sequences, not tabular rows"),
    # NLP: essay scoring
    "commonlit-evaluate-student-summaries":     ("exclude", "Essay text scoring — NLP, not tabular"),
    # Cryo-electron tomography (3D imaging)
    "czii-cryo-et-object-identification":       ("exclude", "3D cryo-EM imaging data, not tabular"),
    # Time series: high-frequency trading
    "optiver-trading-at-the-close":             ("exclude", "High-frequency time series financial data"),
    "optiver-realized-volatility-prediction":   ("exclude", "High-frequency time series financial data"),
    # NLP: essay/writing quality
    "feedback-prize-english-language-learning": ("exclude", "Essay text scoring — NLP"),
    "feedback-prize-2021":                      ("exclude", "Essay text scoring — NLP"),
    "feedback-prize-effectiveness":             ("exclude", "Essay text scoring — NLP"),
    # NLP: code understanding
    "AI4Code":                                  ("exclude", "Code ordering task — NLP/sequence, not tabular"),
    # Time series: energy forecasting
    "predict-energy-behavior-of-prosumers":     ("exclude", "Time series energy prediction, not cross-sectional"),
    # NLP: machine translation
    "deep-past-initiative-machine-translation": ("exclude", "Machine translation — NLP sequence-to-sequence"),
    # Single-cell biology (multimodal omics)
    "open-problems-multimodal":                 ("exclude", "Single-cell gene expression — biology omics, not standard tabular"),
    "open-problems-single-cell-perturbations":  ("exclude", "Single-cell gene expression — biology omics, not standard tabular"),
    # Recommender: fashion
    "h-and-m-personalized-fashion-recommendations": ("exclude", "Recommender system — user-item interaction sequences"),
    # NLP: PII detection in text
    "pii-detection-removal-from-educational-data": ("exclude", "Named entity recognition in text — NLP"),
    # Time series: stock exchange
    "jpx-tokyo-stock-exchange-prediction":      ("exclude", "Time series stock price prediction"),
    # Molecular: drug binding prediction
    "leash-BELKA":                              ("exclude", "Molecular drug binding — chemistry/biology, not tabular"),
    # Time series: commodity
    "mitsui-commodity-prediction-challenge":    ("exclude", "Time series commodity price prediction"),
    # Biology: Parkinson's progression (longitudinal/time series)
    "amp-parkinsons-disease-progression-prediction": ("exclude", "Longitudinal disease progression — time series, not cross-sectional"),
    # Time series: quantitative finance
    "hull-tactical-market-prediction":          ("exclude", "Time series financial market prediction"),
    "ubiquant-market-prediction":               ("exclude", "Time series financial market prediction"),
    # Game AI / RL
    "orbit-wars":                               ("exclude", "Game AI / reinforcement learning, not tabular"),
    # LLM / AGI benchmarks
    "nvidia-nemotron-model-reasoning-challenge": ("exclude", "LLM reasoning challenge, not tabular ML"),
    "kaggle-measuring-agi":                     ("exclude", "AGI benchmark, not tabular ML"),
    # Hackathons
    "google-tunix-hackathon":                   ("exclude", "Hackathon format, not a standard prediction competition"),
    "bigquery-ai-hackathon":                    ("exclude", "Hackathon format, not a standard prediction competition"),
    "openai-to-z-challenge":                    ("exclude", "Hackathon format, not a standard prediction competition"),
    # Data-centric (no standard prediction target)
    "playground-series-s3e21":                  ("exclude", "Data-centric challenge — no standard prediction task"),

    # --- Verify: tabular but need to confirm winning model is tree-based ---

    # Game log data → tabular but complex; tree-based plausible
    "predict-student-performance-from-game-play": ("verify", "Tabular game-log data; confirm winning model is tree-based"),
    # CO2 emissions by district/month — could be time series or tabular regression
    "playground-series-s3e20":                  ("verify", "CO2 emissions regression; check if cross-sectional or time series"),
    # Imputation challenge — unusual task structure
    "playground-series-s3e15":                  ("verify", "Feature imputation challenge — unusual task; confirm standard supervised setup"),
    # Enzyme substrate (multi-label bio) — tabular but niche domain
    "playground-series-s3e18":                  ("verify", "Multi-label enzyme substrate — tabular but unusual domain; confirm tree-based"),

    # --- Keep: clearly in scope ---

    "amex-default-prediction":                  ("keep", "Tabular credit default prediction — tree-based dominant"),
    "child-mind-institute-problematic-internet-use": ("keep", "Tabular survey/actigraphy features — tree-based dominant"),
    "icr-identify-age-related-conditions":      ("keep", "Tabular binary classification — tree-based dominant"),
    "home-credit-credit-risk-model-stability":  ("keep", "Tabular credit risk — tree-based dominant"),
}

PS_KEEP_DEFAULT = "keep"
PS_KEEP_REASON  = "Playground Series tabular classification/regression — in scope by default"


def classify(ref: str) -> tuple[str, str]:
    if ref in CLASSIFICATIONS:
        return CLASSIFICATIONS[ref]
    if ref.startswith("playground-series-s"):
        return PS_KEEP_DEFAULT, PS_KEEP_REASON
    return "verify", "Featured competition not yet classified — review manually"


def main() -> None:
    path = DATA_DIR / "kaggle_candidates_v2.xlsx"
    df = pd.read_excel(path)

    df[["recommended_action", "reason"]] = df["competition_ref"].apply(
        lambda ref: pd.Series(classify(ref))
    )

    # Sort: keep first, verify second, exclude last; within each group by n_teams desc
    order = {"keep": 0, "verify": 1, "exclude": 2}
    df["_sort"] = df["recommended_action"].map(order)
    df = df.sort_values(["_sort", "n_teams"], ascending=[True, False]).drop(columns="_sort")
    df = df.reset_index(drop=True)

    df.to_excel(path, index=False)

    print("Updated", path)
    print()
    print(df["recommended_action"].value_counts().to_string())
    print()
    print("--- KEEP ---")
    keep = df[df["recommended_action"] == "keep"]
    print(keep[["competition_ref", "category", "n_teams"]].to_string(index=False))
    print()
    print("--- VERIFY (needs your review) ---")
    verify = df[df["recommended_action"] == "verify"]
    for _, row in verify.iterrows():
        print(f"  {row['competition_ref']} ({row['category']}, {row['n_teams']} teams)")
        print(f"    -> {row['reason']}")


if __name__ == "__main__":
    main()
