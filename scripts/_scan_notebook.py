import json

with open(r'C:\Users\Nebi\Documents\capstone\CS495-Mapping-Best-Empirical-Models\data\writeups\playground-series-s3e1\ps-s3e1-coordinates-key-to-victory.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

terms = ['original', 'concat', 'california', 'sklearn.datasets', 'fetch_california',
         'merge', 'additional', 'external', 'augment']

for i, cell in enumerate(nb['cells']):
    src = ''.join(cell['source'])
    hits = [t for t in terms if t.lower() in src.lower()]
    if hits:
        print(f'--- Cell {i} ({cell["cell_type"]}) hits: {hits} ---')
        print(src[:600])
        print()
