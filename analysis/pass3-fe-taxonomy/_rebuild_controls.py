"""One-off: rebuild controls_data.csv from authoritative TRUE-sets (notes + source-verified).
Reads the .bak, writes a clean, properly-quoted, width-validated CSV. 2026-06-02."""
import csv, re

SRC = 'analysis/pass3-fe-taxonomy/controls_data.csv.bak'
OUT = 'analysis/pass3-fe-taxonomy/controls_data.csv'

# Authoritative TRUE column sets per control (FE + meta). meta = c51,c53 (excluded from n_fe).
TRUE = {
 'playground-series-s6e2':  ['c01','c02','c06','c13'],
 'playground-series-s5e10': ['c01','c46'],
 'playground-series-s6e3':  ['c06','c11','c14','c15','c17','c26','c28','c31','c32'],
 'playground-series-s5e8':  ['c01','c05','c41'],
 'playground-series-s6e4':  ['c01','c02','c06','c10','c11','c17','c32','c53'],
 'playground-series-s5e5':  ['c51','c53'],
 'playground-series-s5e6':  ['c10','c51'],
 'playground-series-s5e4':  ['c01','c09','c12','c16','c17','c18','c19','c26','c27','c28','c31','c32'],
 'playground-series-s4e11': ['c10','c51','c53'],
 'playground-series-s4e10': ['c48','c51'],
 'playground-series-s6e1':  ['c01','c02','c08','c09','c10','c13','c14','c17','c28','c29','c32','c45','c53'],
}
REPAIR_NOTE = {
 'playground-series-s5e4':  " [REPAIR 2026-06-02: n_fe corrected 13->12; only 12 techniques enumerated/coded. Source re-read found additional codeable techniques NOT in original coding (c07 NaN-indicator cols, c43 Episode_Title parsing, c29 Time/Sentiment ordinal) - candidates for re-code, NOT added here to preserve repair scope.]",
 'playground-series-s4e10': " [REPAIR 2026-06-02: n_fe field corrected 0->1 to match note's stated n_fe_tech=1 (c48); booleans c48+c51 intact.]",
 'playground-series-s5e6':  " [REPAIR 2026-06-02: original booleans had 1s at c10/c50/c53 conflicting with note's stated c10(FE)+c51(minimal,meta); reconstructed to note {c10,c51}. c50 is a likely off-by-one shift artifact of c51. Source-verify recommended.]",
 'playground-series-s4e11': " [REPAIR 2026-06-02: original booleans had 1s at c10/c50/c52/c53 conflicting with note's stated c10+c51+c53 (n_fe=1 meta=2); reconstructed to note {c10,c51,c53}. c50/c52 are likely shift artifacts. Source-verify recommended.]",
}
META = {'c51','c53'}

lines = [l for l in open(SRC, encoding='utf-8').read().split('\n') if l.strip()]
header = lines[0].split(',')
cols = [c for c in header if c.startswith('c') and len(c) > 2 and c[1:3].isdigit()]
assert len(cols) == 53, len(cols)
nfe_i = header.index('n_fe_techniques_used')

recon, out_rows = [], [header]
for line in lines[1:]:
    f = line.split(',')
    comp = f[1]
    lead = f[0:5]
    date = f[-1]
    ni = next(i for i in range(5, len(f)) if re.search('[A-Za-z]', f[i]))  # notes start
    notes = ','.join(f[ni:-1])
    if comp in REPAIR_NOTE:
        notes += REPAIR_NOTE[comp]
    trues = set(TRUE[comp])
    vec = ['1' if c[:3] in trues else '0' for c in cols]          # c[:3] = short code e.g. 'c01'
    nfe = sum(1 for c in cols if c[:3] in trues and c[:3] not in META)
    new_ones = sum(1 for x in vec if x == '1')
    assert new_ones == len(trues), f'{comp}: built {new_ones} ones but TRUE-set has {len(trues)} (bad code?)'
    old_ones = sum(1 for x in f[5:ni] if x == '1')
    out_rows.append(lead + vec + [str(nfe), notes, date])
    recon.append((comp, f[3], old_ones, new_ones, nfe))

errs = []
for r in out_rows[1:]:
    if len(r) != len(header): errs.append((r[1], 'len', len(r)))
    bvec = r[5:58]
    if len(bvec) != 53 or any(x not in ('0', '1') for x in bvec): errs.append((r[1], 'bool'))
    fe = sum(1 for j, c in enumerate(cols) if r[5 + j] == '1' and c[:3] not in META)
    if int(r[nfe_i]) != fe: errs.append((r[1], 'nfe', r[nfe_i], fe))

with open(OUT, 'w', encoding='utf-8', newline='') as fh:
    csv.writer(fh, quoting=csv.QUOTE_MINIMAL).writerows(out_rows)

print('RECONCILIATION (control | author | old_surviving_1s | new_total_1s | n_fe):')
for comp, auth, oo, nt, nfe in recon:
    flag = '' if oo == nt else '  <-- count changed (see repair note)'
    print(f'  {comp:26s} {auth:14s} old1s={oo:2d} new1s={nt:2d} n_fe={nfe}{flag}')
print('\nVALIDATION:', errs if errs else 'PASS - all rows correct width, 53 clean booleans, n_fe==FE-count')
chk = list(csv.reader(open(OUT, encoding='utf-8')))
print('Strict re-parse:', len(chk) - 1, 'data rows; widths=', set(len(r) for r in chk))
