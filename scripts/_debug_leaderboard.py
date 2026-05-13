from kaggle import KaggleApi

api = KaggleApi()
api.authenticate()

slug = "playground-series-s3e1"

# Get top 3 leaderboard with correct signature
result = api.competition_leaderboard_view(slug, page_size=3)
print("top 3 winners:")
for e in result:
    print(f"  rank team_name='{e.team_name}' score={e.score}")

# Test kernels_list with exact casing from leaderboard
for e in result:
    username = e.team_name
    kernels = api.kernels_list(competition=slug, user=username, sort_by="voteCount", page_size=5)
    count = len(kernels) if kernels else 0
    # also try lowercase
    kernels_lower = api.kernels_list(competition=slug, user=username.lower(), sort_by="voteCount", page_size=5)
    count_lower = len(kernels_lower) if kernels_lower else 0
    print(f"  {username}: {count} kernels (exact), {count_lower} kernels (lower)")
