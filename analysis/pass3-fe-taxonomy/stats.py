"""Reproduce the Pass-3 reliability and the paired winner-control significance
statistics reported in the research report (Sections 3.6, 4.5).

Standard library only -- no third-party dependency. Run from the repo root:

    python analysis/pass3-fe-taxonomy/stats.py

RELIABILITY is computed against the *pre-adjudication* primary coding
(`stage1_data_preadjudication.csv`, the clean validated snapshot from commit
6bd2092, before the four source-verified adjudication corrections were applied).
This is deliberate: the live `stage1_data.csv` is post-adjudication, and
adjudication moved the primary coding toward the blind re-code by construction,
so agreement against it would be circular and inflated. Reliability must measure
how independently the two codings agreed *before* reconciliation.

The PAIRED winner-vs-control comparison uses the live (post-adjudication)
`stage1_data.csv` -- the analyzed dataset -- and is computed on n_fe, matching
Section 4.5. (None of the four adjudicated winners fall in the 11 paired
competitions, so this choice does not affect the paired result.)

Expected output (matches the report): 53-col kappa 0.60 / 11-group 0.65;
AC1 0.94 / 0.78; positive agreement 46% / 58%; paired 7-3-1, sign-test p 0.34.
"""
import csv
import math
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
PREADJ = os.path.join(HERE, 'stage1_data_preadjudication.csv')  # reliability: pre-adjudication
CURRENT = os.path.join(HERE, 'stage1_data.csv')                  # paired: live analyzed data
CONTROLS = os.path.join(HERE, 'controls_data.csv')              # not touched by adjudication
BLIND = os.path.join(HERE, 'blind_v2.csv')
SAMPLE = os.path.join(HERE, 'blind_recode_sheet.csv')

# c01..c53 -> technique family (Groups A-K). Boundaries per SCHEMA.md / Section 3.4.
FAMILIES = {
    'A': range(1, 8), 'B': range(8, 13), 'C': range(13, 19), 'D': range(19, 27),
    'E': range(27, 32), 'F': range(32, 38), 'G': range(38, 42), 'H': range(42, 45),
    'I': range(45, 48), 'J': range(48, 51), 'K': range(51, 54),
}
FE_FAMILIES = [g for g in FAMILIES if g != 'K']  # A-J: FE families (K = meta flags)
CODES = ['c%02d' % i for i in range(1, 54)]


def _truthy(v):
    return str(v).strip().upper() in ('1', 'TRUE')


def load_codings(path, keycol):
    """competition_ref -> {c01..c53: bool} from a primary-data CSV."""
    rows = list(csv.reader(open(path, encoding='utf-8')))
    h = rows[0]
    code_idx = {n[:3]: i for i, n in enumerate(h) if n[:1] == 'c' and n[1:3].isdigit()}
    key_i = h.index(keycol)
    return {row[key_i]: {c: _truthy(row[code_idx[c]]) for c in CODES}
            for row in rows[1:] if row}


def load_nfe(path, keycol):
    """competition_ref -> n_fe_techniques_used (already excludes meta flags c51/c53)."""
    rows = list(csv.reader(open(path, encoding='utf-8')))
    h = rows[0]
    key_i, nfe_i = h.index(keycol), h.index('n_fe_techniques_used')
    return {row[key_i]: int(row[nfe_i]) for row in rows[1:] if row}


def load_blind():
    rows = list(csv.reader(open(BLIND, encoding='utf-8')))
    h = rows[0]
    idx = {c: h.index(c) for c in CODES}
    return {row[0]: {c: _truthy(row[idx[c]]) for c in CODES} for row in rows[1:] if row}


def load_sample_map():
    rows = list(csv.reader(open(SAMPLE, encoding='utf-8')))
    h = rows[0]
    ki, ci = h.index('kind'), h.index('competition')
    return {row[0]: (row[ki], row[ci]) for row in rows[1:] if row}


def agreement(pairs):
    """pairs: list of (primary, blind) booleans. Returns kappa, AC1, positive agreement.

    Positive agreement is the Jaccard form a/(a+b+c) -- the share of 'present'
    calls the two codings agree on, out of all cells either called present.
    """
    a = b = c = d = 0  # a=both yes, b=primary yes/blind no, c=primary no/blind yes, d=both no
    for x, y in pairs:
        if x and y:       a += 1
        elif x and not y: b += 1
        elif y and not x: c += 1
        else:             d += 1
    n = a + b + c + d
    po = (a + d) / n
    pe_cohen = ((a + b) / n) * ((a + c) / n) + ((c + d) / n) * ((b + d) / n)
    kappa = (po - pe_cohen) / (1 - pe_cohen)
    pi = (2 * a + b + c) / (2 * n)        # mean positive prevalence across both coders
    pe_gwet = 2 * pi * (1 - pi)
    ac1 = (po - pe_gwet) / (1 - pe_gwet)
    pos_jaccard = a / (a + b + c) if (a + b + c) else float('nan')
    return kappa, ac1, pos_jaccard, n


def sign_test_two_sided(n_pos, n_neg):
    """Two-sided sign test ignoring ties."""
    n = n_pos + n_neg
    k = max(n_pos, n_neg)
    tail = sum(math.comb(n, i) for i in range(k, n + 1)) / (2 ** n)
    return min(1.0, 2 * tail)


def main():
    # ---- Reliability: pre-adjudication winners + controls vs blind re-code ----
    primary = {'winner': load_codings(PREADJ, 'competition_ref'),
               'control': load_codings(CONTROLS, 'competition_ref')}
    kind = {'winner': 'winner', 'control': 'control'}
    blind = load_blind()
    smap = load_sample_map()

    col_pairs, grp_pairs, used = [], [], []
    for bid, (k, comp) in sorted(smap.items()):
        pc, bc = primary[kind[k]].get(comp), blind.get(bid)
        if pc is None or bc is None:
            raise SystemExit(f'No primary/blind match for {bid} ({k} {comp})')
        used.append((bid, k))
        for c in CODES:
            col_pairs.append((pc[c], bc[c]))
        for g, rng in FAMILIES.items():
            grp_pairs.append((any(pc['c%02d' % i] for i in rng),
                              any(bc['c%02d' % i] for i in rng)))

    nw = sum(1 for _, k in used if k == 'winner')
    print(f'Reliability (pre-adjudication coding vs blind intra-rater re-code; Section 3.6)')
    print(f'  sample: {len(used)} entries ({nw} winners, {len(used) - nw} controls)\n')
    print(f'  {"Resolution":<11}{"Cohen kappa":>13}{"Gwet AC1":>11}{"Pos. agree":>12}{"cells":>8}')
    for label, pairs in [('53-column', col_pairs), ('11-group', grp_pairs)]:
        kp, ac1, pos, n = agreement(pairs)
        print(f'  {label:<11}{kp:>13.2f}{ac1:>11.2f}{pos:>11.0%}{n:>8}')

    # ---- Paired winner-vs-control comparison (post-adjudication data; Section 4.5) ----
    w_codes = load_codings(CURRENT, 'competition_ref')
    c_codes = load_codings(CONTROLS, 'competition_ref')
    w_nfe = load_nfe(CURRENT, 'competition_ref')
    c_nfe = load_nfe(CONTROLS, 'competition_ref')
    comps = sorted(set(w_nfe) & set(c_nfe))

    def fam_count(cc):
        return sum(1 for g in FE_FAMILIES if any(cc['c%02d' % i] for i in FAMILIES[g]))

    win_hi = ctl_hi = tie = 0
    fam_w = fam_c = fam_t = 0
    for comp in comps:
        if w_nfe[comp] > c_nfe[comp]:   win_hi += 1
        elif c_nfe[comp] > w_nfe[comp]: ctl_hi += 1
        else:                           tie += 1
        wf, cf = fam_count(w_codes[comp]), fam_count(c_codes[comp])
        if wf > cf:   fam_w += 1
        elif cf > wf: fam_c += 1
        else:         fam_t += 1

    print(f'\nPaired winner-vs-control (n = {len(comps)} competitions; Section 4.5)')
    print(f'  by n_fe (technique count): winner higher {win_hi}, control higher {ctl_hi}, tie {tie}')
    print(f'    sign test on {win_hi}-vs-{ctl_hi} (ties dropped): p = {sign_test_two_sided(win_hi, ctl_hi):.2f}')
    print(f'    paired n_fe medians: winners {st.median([w_nfe[c] for c in comps]):.0f} '
          f'vs controls {st.median([c_nfe[c] for c in comps]):.0f}')
    print(f'  by FE-family count (secondary): winner higher {fam_w}, control higher {fam_c}, tie {fam_t}')


if __name__ == '__main__':
    main()
