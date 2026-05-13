from kaggle import KaggleApi
api = KaggleApi(); api.authenticate()
resp = api.competitions_list(search="playground-series-s6e4")
comps = resp.competitions
print(f"Results: {len(comps)}")
if comps:
    c = comps[0]
    print(f"ref={c.ref!r}")
    print(f"title={c.title!r}")
    print(f"evaluationMetric={c.evaluationMetric!r}")
    print(f"url={c.url!r}")
    # dump all non-private attrs
    for attr in [a for a in dir(c) if not a.startswith('_')]:
        try:
            val = getattr(c, attr)
            if not callable(val):
                print(f"  {attr} = {val!r}")
        except: pass
