"""Apply adjudicated corrections to stage1_data.csv (winners), found via the blind re-code.
n_fe recomputed excluding c51/c53. 2026-06-02."""
import csv

SRC = 'analysis/pass3-fe-taxonomy/stage1_data.csv'
META = {51, 53}
# competition -> (corrected TRUE column numbers, adjudication note)
FIX = {
 'tabular-playground-series-feb-2022': ({11},
   'ADJUDICATED 2026-06-02: +c11 (SCHEMA cites this entry as the c11 digit-features example); -c35 (no NN-as-feature in source).'),
 'playground-series-s3e8': ({9, 13, 26, 28, 29},
   'ADJUDICATED 2026-06-02: +c09 (carat**3) +c26 (per-row max/min of x,y) confirmed in notebook cells 58/73.'),
 'playground-series-s5e3': ({32, 51},
   'ADJUDICATED 2026-06-02: +c32 (writeup maps orig.groupby(c).target.mean()) despite author "no FE" (c51 stands).'),
 'playground-series-s4e4': ({6, 8, 13, 14, 16, 26, 46, 49, 50, 52},
   'ADJUDICATED 2026-06-02: OpenFE pipeline per writeup -> +c13/c14/c16/c26/c46/c49/c50; -c09 (writeup: polynomials did not work); -c28 (ratios automated not domain -> c13); -c48 (it is SFS=c49 not permutation).'),
}

r = list(csv.reader(open(SRC, encoding='utf-8')))
h = r[0]
cidx = [i for i, c in enumerate(h) if c.startswith('c') and c[1:3].isdigit()]
nfe_i = h.index('n_fe_techniques_used')
notes_i = h.index('pass3_notes')

changed = []
for row in r[1:]:
    if not row or row[0] not in FIX:
        continue
    trues, note = FIX[row[0]]
    for k, i in enumerate(cidx):
        row[i] = '1' if (k + 1) in trues else '0'
    row[nfe_i] = str(sum(1 for n in trues if n not in META))
    row[notes_i] = row[notes_i] + ' [' + note + ']'
    changed.append((row[0], sorted(trues), row[nfe_i]))

with open(SRC, 'w', encoding='utf-8', newline='') as f:
    csv.writer(f, quoting=csv.QUOTE_MINIMAL).writerows(r)

print('Applied corrections:')
for comp, t, nfe in changed:
    print(f'  {comp:36s} -> {["c%02d"%x for x in t]}  n_fe={nfe}')
