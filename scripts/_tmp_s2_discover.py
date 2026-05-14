import os
os.chdir(r"C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models")
from kaggle import KaggleApi

api = KaggleApi()
api.authenticate()

def list_comps(search, pages=3):
    results = []
    for p in range(1, pages+1):
        r = api.competitions_list(search=search, page=p, page_size=50)
        batch = r.competitions if hasattr(r, 'competitions') else []
        if not batch:
            break
        results.extend(batch)
    return results

def summarize(comps_raw, year_filter=None):
    out = []
    for c in comps_raw:
        ref = str(c.ref) if hasattr(c, 'ref') else ""
        if not ref:
            continue
        # strip base URL if present
        ref = ref.replace("https://www.kaggle.com/competitions/", "")
        deadline = str(c.deadline)[:10] if hasattr(c, 'deadline') else ""
        if year_filter and not any(y in deadline for y in year_filter):
            continue
        out.append({
            "ref": ref,
            "title": str(c.title) if hasattr(c, 'title') else "",
            "deadline": deadline,
            "n_teams": c.team_count if hasattr(c, 'team_count') else 0,
            "metric": str(c.evaluation_metric) if hasattr(c, 'evaluation_metric') else "",
        })
    return sorted(out, key=lambda x: x["ref"])

# TPS 2022
print("=== TPS 2022 (S2 equivalent) ===")
tps = list_comps("tabular-playground-series-2022")
rows = summarize(tps)
if not rows:
    # try month-based search
    for month in ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]:
        r = list_comps(f"tabular-playground-series-{month}-2022")
        rows += summarize(r, year_filter=["2022"])
    rows = sorted({r["ref"]: r for r in rows}.values(), key=lambda x: x["ref"])

for c in rows:
    print(f"  {c['ref']:55s}  {c['deadline']}  teams:{c['n_teams']:4}  {c['metric']}")

print(f"\nTotal TPS 2022: {len(rows)}\n")

# PS S6
print("=== PS S6 (2026, currently running) ===")
s6 = list_comps("playground-series-s6")
s6_rows = summarize(s6, year_filter=["2026"])
for c in s6_rows:
    print(f"  {c['ref']:55s}  {c['deadline']}  teams:{c['n_teams']:4}  {c['metric']}")
print(f"\nTotal PS S6: {len(s6_rows)}")
