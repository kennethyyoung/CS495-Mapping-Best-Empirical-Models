"""Inspect notebook cells for Stage 2 FE validation. Reads inline (no path bug)."""
import json
import sys
from pathlib import Path

def inspect(nb_path, code_only=True, max_chars=2000):
    with open(nb_path, encoding='utf-8') as f:
        nb = json.load(f)
    print(f"=== {Path(nb_path).name} ===")
    print(f"Total cells: {len(nb['cells'])}\n")
    for i, c in enumerate(nb['cells']):
        if code_only and c['cell_type'] != 'code':
            continue
        src = ''.join(c['source']) if c['source'] else '(empty)'
        if not src.strip():
            continue
        print(f"--- Cell {i} ({c['cell_type']}) ---")
        print(src[:max_chars])
        if len(src) > max_chars:
            print(f"... [truncated {len(src)-max_chars} chars]")
        print()

if __name__ == '__main__':
    inspect(sys.argv[1], code_only='--all' not in sys.argv)
