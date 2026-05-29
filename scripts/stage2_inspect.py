"""Inspect notebook cells for Stage 2 FE validation. Reads inline (no path bug)."""
import json
import sys
from pathlib import Path

def _safe(s):
    # Strip characters Windows cp932 codec can't encode; keep ASCII + common.
    return s.encode('ascii', errors='replace').decode('ascii')

def inspect(nb_path, code_only=True, max_chars=2000, start=0, end=None):
    with open(nb_path, encoding='utf-8') as f:
        nb = json.load(f)
    print(f"=== {Path(nb_path).name} ===")
    print(f"Total cells: {len(nb['cells'])}")
    if start or end is not None:
        print(f"Showing cells {start} to {end if end is not None else len(nb['cells'])-1}")
    print()
    for i, c in enumerate(nb['cells']):
        if i < start:
            continue
        if end is not None and i > end:
            break
        if code_only and c['cell_type'] != 'code':
            continue
        src = ''.join(c['source']) if c['source'] else '(empty)'
        if not src.strip():
            continue
        print(f"--- Cell {i} ({c['cell_type']}) ---")
        print(_safe(src[:max_chars]))
        if len(src) > max_chars:
            print(f"... [truncated {len(src)-max_chars} chars]")
        print()

if __name__ == '__main__':
    args = sys.argv[1:]
    code_only = '--all' not in args
    start = 0
    end = None
    for a in args:
        if a.startswith('--start='):
            start = int(a.split('=')[1])
        elif a.startswith('--end='):
            end = int(a.split('=')[1])
    path = [a for a in args if not a.startswith('--')][0]
    inspect(path, code_only=code_only, start=start, end=end)
