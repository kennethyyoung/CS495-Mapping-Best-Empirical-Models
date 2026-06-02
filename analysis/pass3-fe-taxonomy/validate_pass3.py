"""Pass 3 CSV integrity validator. Run after ANY edit to a Pass 3 sheet.

Checks, per row:
  - field count matches the header exactly
  - the 53 boolean columns are all '0'/'1'
  - n_fe_techniques_used == count of TRUE boolean cols EXCLUDING meta cols (c51, c53)

Usage:  python validate_pass3.py [file1.csv file2.csv ...]
        (defaults to stage1_data.csv and controls_data.csv)
Exit code 1 if any problem is found, so it can gate a commit hook.
"""
import csv, sys, os

META = {'c51', 'c53'}            # flagged in notes, excluded from the n_fe count
HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULTS = ['stage1_data.csv', 'controls_data.csv']


def validate(path):
    rows = list(csv.reader(open(path, encoding='utf-8')))
    header, n = rows[0], len(rows[0])
    cidx = [i for i, c in enumerate(header) if c.startswith('c') and len(c) > 2 and c[1:3].isdigit()]
    if len(cidx) != 53:
        return [f'{os.path.basename(path)}: header has {len(cidx)} boolean cols, expected 53']
    nfe_i = header.index('n_fe_techniques_used')
    probs = []
    for ln, r in enumerate(rows[1:], 2):
        if not r:
            continue
        rid = f'{r[1] if len(r) > 1 else "?"}'
        if len(r) != n:
            probs.append(f'  L{ln} {rid}: {len(r)} fields, expected {n}')
            continue
        bvec = [r[i] for i in cidx]
        if any(x not in ('0', '1') for x in bvec):
            probs.append(f'  L{ln} {rid}: non-0/1 in boolean block')
            continue
        fe = sum(1 for i, j in zip(cidx, range(53))
                 if r[i] == '1' and header[i][:3] not in META)
        if not r[nfe_i].isdigit() or int(r[nfe_i]) != fe:
            probs.append(f'  L{ln} {rid}: n_fe={r[nfe_i]} but FE-count={fe}')
    return probs


def main(argv):
    files = argv[1:] or [os.path.join(HERE, f) for f in DEFAULTS]
    all_ok = True
    for path in files:
        probs = validate(path)
        if probs:
            all_ok = False
            print(f'FAIL {os.path.basename(path)} ({len(probs)} issue(s)):')
            print('\n'.join(probs))
        else:
            rows = sum(1 for _ in csv.reader(open(path, encoding='utf-8'))) - 1
            print(f'PASS {os.path.basename(path)}: {rows} rows valid')
    return 0 if all_ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
