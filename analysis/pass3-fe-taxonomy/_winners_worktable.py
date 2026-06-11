"""Diagnostic worktable for the winners v1 rebuild. NON-DESTRUCTIVE (reads .bak, writes nothing to data).
For each winner row, reconcile three independent signals:
  1. n_fe  = integer immediately before the notes text (robust to boolean drift)
  2. BOOL  = 1-count (minus meta c51/c53) of the FIRST 53 boolean-position fields
  3. NOTE  = TRUE-set parsed from notes (cNN + 'col N' tokens, TRUE-portion only)
Rows where BOOL==n_fe AND NOTE==n_fe are high-confidence; the rest are flagged for manual reconstruction.
"""
import csv, re

SRC = 'analysis/pass3-fe-taxonomy/stage1_data.csv.bak'
META = {51, 53}
lines = [l for l in open(SRC, encoding='utf-8').read().split('\n') if l.strip()]
header = lines[0].split(',')
cols = [c for c in header if c.startswith('c') and len(c) > 2 and c[1:3].isdigit()]
LEAD = header.index('c01_te_basic')  # first boolean col index (=3 for winners)


def parse_note_cols(notes):
    """Return set of column numbers asserted TRUE in the notes."""
    # cut off the NOT-marked / NOT portion to avoid counting excluded cols
    cut = re.split(r'NOT\s*marked|NOT:|not marked|NOT MARKED', notes)[0]
    nums = set(int(m) for m in re.findall(r'\bc(\d\d)\b', cut))
    for grp in re.findall(r'col\s*([\d\s\+]+)', cut):
        for m in re.findall(r'\d+', grp):
            n = int(m)
            if 1 <= n <= 53:
                nums.add(n)
    return nums


rows_info = []
for line in lines[1:]:
    f = line.split(',')
    comp, rank, conf = f[0], f[1], f[2]
    ni = next(i for i in range(LEAD, len(f)) if re.search('[A-Za-z]', f[i]))  # notes start
    nfe = int(f[ni - 1]) if f[ni - 1].isdigit() else None
    notes = ','.join(f[ni:-1])
    first53 = f[LEAD:LEAD + 53]
    bool_ok = len(first53) == 53 and all(x in ('0', '1') for x in first53)
    bcount = sum(1 for j, x in enumerate(first53) if x == '1' and (j + 1) not in META) if bool_ok else None
    ncols = parse_note_cols(notes)
    ncount = len([n for n in ncols if n not in META])
    b_match = (bcount == nfe)
    n_match = (ncount == nfe) and len(ncols) > 0
    rows_info.append((comp, rank, conf, nfe, bcount if bool_ok else 'X', b_match, sorted(ncols), ncount, n_match))

print(f'{"comp":34s} {"rk":3s} {"nfe":3s} {"bool":4s} {"bOK":3s} {"noteCols":3s} {"nOK":3s}  verdict')
hi = note_only = bool_only = manual = 0
for comp, rank, conf, nfe, bc, bm, ncols, ncount, nm in rows_info:
    if bm and nm: v, t = 'AUTO (bool+note agree)', 'hi'
    elif nm and not bm: v, t = 'use NOTE (note reconciles)', 'note'
    elif bm and not nm: v, t = 'use BOOL (bool reconciles)', 'bool'
    else: v, t = '*** MANUAL / source re-read ***', 'man'
    if t == 'hi': hi += 1
    elif t == 'note': note_only += 1
    elif t == 'bool': bool_only += 1
    else: manual += 1
    print(f'{comp:34s} {rank:3s} {str(nfe):3s} {str(bc):4s} {str(bm)[0]:3s} {ncount:3d} {str(nm)[0]:3s}  {v}')
print(f'\nSUMMARY: AUTO(bool+note)={hi}  NOTE-only={note_only}  BOOL-only={bool_only}  MANUAL={manual}  (total {len(rows_info)})')
