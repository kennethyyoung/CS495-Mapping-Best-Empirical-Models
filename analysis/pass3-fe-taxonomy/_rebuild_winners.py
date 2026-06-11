"""Rebuild stage1_data.csv (winners) v1 from best-authoritative signal per row.
- 12 hard rows: source/STAGE-doc verified TRUE-sets (hardcoded below).
- s5e4, s6e1: FE source not local -> best-effort from booleans, FLAGGED for blind re-code.
- all other rows: derive TRUE-set from the (position-intact) first-53 booleans in the .bak.
n_fe recomputed under the confirmed convention: EXCLUDE c51 and c53.
Writes a clean, quoted, width-valid CSV; prints per-column totals vs STAGE1_FULL reference.
"""
import csv, re

SRC = 'analysis/pass3-fe-taxonomy/stage1_data.csv.bak'
OUT = 'analysis/pass3-fe-taxonomy/stage1_data.csv'
META = {51, 53}

# Source/doc-verified TRUE column NUMBERS (incl. meta flags c51/c53 where applicable).
VERIFIED = {
 'playground-series-s3e1':  {31, 39, 53},                       # dmitryuarov nb: latlon sin/cos, PCA, fork
 'playground-series-s3e3':  {26, 27, 28, 53},                   # Bill Cruise: rowwise, domain flags, ratios, fork
 'playground-series-s3e8':  {13, 28, 29},                       # Craig: interaction, ratio, gemstone ordinal
 'playground-series-s4e3':  {13, 28, 53},                       # Moonlit nb: X_Range*Pixels, Length/Thick ratio, fork
 'playground-series-s4e5':  {1, 15, 26, 48, 49},                # adaubas STAGE1_RESULTS table
 'playground-series-s4e7':  {53},                               # Cross Sellers: feature store fork only
 'playground-series-s5e6':  {1, 4, 17, 32, 45, 46},             # cdeotte: TE, 7 binary targets, combos, orig-TE, pseudo, residual
 'playground-series-s5e10': {38, 41, 44, 46},                   # Tilii: AE latents, gplearn, Lasso recovery, residual
 'playground-series-s5e11': {1, 2, 5, 10, 11, 12, 17, 18, 26},  # mahog nb (source-verified, 9)
 'playground-series-s5e12': {1, 9, 28},                         # wind1234it: TE, poly, domain ratio
 'playground-series-s6e4':  {1, 2, 6, 11, 12, 17, 18},          # kirill0212 nb (source-verified, 7)
 'playground-series-s3e13': {38, 51},                           # Umar: frozen-AE latents + explicit no-FE
 # --- batch 2: reconstructed from notes / STAGE2_LOG / source 2026-06-02 ---
 'playground-series-s3e4':  {26},                               # Ollie Kemp: 8 rowwise stats
 'playground-series-s3e5':  {51},                               # Heitor: explicit no-FE
 'playground-series-s3e7':  {51, 52},                           # Hardy Xu: minimal-FE + adversarial-validation FE
 'playground-series-s3e10': {51},                               # seascape: FE-impossible stance
 'playground-series-s4e11': {51},                               # Mahdi: explicit no FE
 'playground-series-s5e3':  {51},                               # cdeotte: minimal (2nd-place SVC no-FE)
 'icr-identify-age-related-conditions': {51},                   # room722: explicit no-FE (617-row overfit risk)
 'playground-series-s3e16': {8, 28, 48},                        # Ravi: log, anatomical ratios, perm-imp
 'playground-series-s3e17': {51},                               # ISoft: pure AutoML, no hand-crafted FE
 'playground-series-s3e23': {8},                                # oscarm524: log1p all features
 'playground-series-s3e24': {16, 48},                           # Ravi: brute-force combos + perm-imp
 'playground-series-s3e26': {10},                               # Hardy Xu: PLE binning
 'playground-series-s4e1':  {1, 2, 10, 13, 17, 27, 28, 39, 42},  # Iqbal: TE, casting, mult, combos, flags, ratio, SVD, TFIDF
 'playground-series-s4e9':  {1, 2, 10, 43, 47},                 # Mart Preusse: TE, binning, regex, outlier-aux
 'playground-series-s4e10': {1, 2, 10, 18},                     # omid: TE per-fold + all-cat + numerics-as-cats
 'playground-series-s5e8':  {1, 2, 8, 13, 17, 18, 31, 41},      # mahog nb: TE, log, mult, combos, cyclical, GP
 'tabular-playground-series-may-2022': {14, 15, 43},            # ambrosm: additive+threshold ternary, char extracts
}
# FE source NOT local -> explicit best-effort vector + flag for blind re-code / source-verify.
FLAG_VEC = {
 'playground-series-s5e4':  ({1},    'greysky 1552-feature pipeline in external generator notebook NOT local; only TE confirmable (writeup title); doc n_fe was 6'),
 'playground-series-s6e1':  ({1, 2}, 'mahog base FE references cdeotte/discussion notebooks NOT local; only TE confirmable; doc n_fe was 7'),
}

lines = [l for l in open(SRC, encoding='utf-8').read().split('\n') if l.strip()]
header = lines[0].split(',')
cols = [c for c in header if c.startswith('c') and len(c) > 2 and c[1:3].isdigit()]
LEAD = header.index('c01_te_basic')
N = len(header)

out_rows = [header]
recon = []
for line in lines[1:]:
    f = line.split(',')
    comp, rank, conf = f[0], f[1], f[2]
    ni = next(i for i in range(LEAD, len(f)) if re.search('[A-Za-z]', f[i]))
    date = f[-1]
    notes = ','.join(f[ni:-1])
    first53 = f[LEAD:LEAD + 53]
    if comp in VERIFIED:
        trues = VERIFIED[comp]
        notes += ' [REBUILD 2026-06-02: TRUE-set source/doc-verified; n_fe excludes c51/c53.]'
        src = 'verified'
    elif comp in FLAG_VEC:
        trues, reason = FLAG_VEC[comp]
        notes += f' [REBUILD 2026-06-02: {reason}; VERIFY via blind re-code.]'
        src = 'flagged'
    else:
        trues = {j + 1 for j, x in enumerate(first53) if x == '1'}  # nb=53 intact rows only
        src = 'booleans'
    vec = ['1' if (j + 1) in trues else '0' for j in range(53)]
    nfe = sum(1 for n in trues if n not in META)
    out_rows.append([comp, rank, conf] + vec + [str(nfe), notes, date])
    recon.append((comp, src, sum(int(x) for x in vec), nfe))

# write
with open(OUT, 'w', encoding='utf-8', newline='') as fh:
    csv.writer(fh, quoting=csv.QUOTE_MINIMAL).writerows(out_rows)

# per-column totals vs STAGE1_FULL reference (Stage-1 snapshot; final >= these after Stage-2 flips)
ref = {1: 19, 51: 8, 13: 7, 11: 7, 18: 7, 2: 6, 28: 6}
tot = {}
for r in out_rows[1:]:
    for j in range(53):
        if r[LEAD + j] == '1':
            tot[j + 1] = tot.get(j + 1, 0) + 1
print('Per-column totals (rebuilt) vs STAGE1_FULL ref:')
for c in sorted(ref):
    print(f'  col{c:<2d}: rebuilt={tot.get(c,0):2d}  S1ref={ref[c]:2d}')
print('\nSrc breakdown:', {s: sum(1 for _, ss, *_ in recon if ss == s) for s in ('verified', 'flagged', 'booleans')})
print('Flagged rows:', [c for c, s, *_ in recon if s == 'flagged'])
chk = list(csv.reader(open(OUT, encoding='utf-8')))
print('Strict re-parse:', len(chk) - 1, 'rows; widths=', set(len(r) for r in chk))
