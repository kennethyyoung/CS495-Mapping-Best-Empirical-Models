"""Build a seeded, stratified 12-entry BLIND re-coding sheet for intra-rater reliability.
Stratifies across era (s3/s4/s5/s6/other) and source-confidence, mixing winners + controls.
Identity fields are read from columns BEFORE the corrupted boolean block, so corruption is irrelevant here.
Output: blind_recode_sheet.csv (blank 53 cols for the user to fill from SOURCE ONLY).
"""
import csv, random, re

random.seed(495)  # reproducible
DIR = 'analysis/pass3-fe-taxonomy/'

def era(comp):
    m = re.search(r's(\d)e\d', comp)
    if m: return 's' + m.group(1)
    return 'other'

entries = []
# winners
for r in list(csv.reader(open(DIR + 'stage1_data.csv.bak', encoding='utf-8')))[1:]:
    if not r: continue
    entries.append({'kind': 'winner', 'comp': r[0], 'rank': r[1], 'author': '', 'conf': r[2],
                    'era': era(r[0]), 'folder': 'data/writeups/' + r[0]})
# controls
for r in list(csv.reader(open(DIR + 'controls_data.csv', encoding='utf-8')))[1:]:
    if not r: continue
    entries.append({'kind': 'control', 'comp': r[1], 'rank': r[2], 'author': r[3], 'conf': r[4],
                    'era': era(r[1]), 'folder': 'data/writeups/' + r[1]})

# stratified pick: 1 guaranteed per era bucket, then fill to 12 weighted toward codeable
# (notebook+writeup) sources but keeping 2-3 harder writeup-only/notes-only for honesty.
by_era = {}
for e in entries:
    by_era.setdefault(e['era'], []).append(e)

picked, seen = [], set()
def add(e):
    key = (e['comp'], e['rank'], e['kind'])
    if key not in seen:
        seen.add(key); picked.append(e)

# 1 per era to guarantee spread
for k in sorted(by_era):
    add(random.choice(by_era[k]))
# ensure >=3 controls in the sample
ctrls = [e for e in entries if e['kind'] == 'control']
random.shuffle(ctrls)
for e in ctrls[:3]: add(e)
# fill remainder toward notebook+writeup (most codeable) for a fair reliability test
pool = [e for e in entries if 'notebook' in e['conf']]
random.shuffle(pool)
for e in pool:
    if len(picked) >= 12: break
    add(e)
# top up if still short
random.shuffle(entries)
for e in entries:
    if len(picked) >= 12: break
    add(e)

picked = picked[:12]
picked.sort(key=lambda e: (e['era'], e['comp'], e['rank']))

cols = [c for c in csv.reader(open(DIR + 'controls_data.csv', encoding='utf-8')).__next__()
        if c.startswith('c') and len(c) > 2 and c[1:3].isdigit()]
out = DIR + 'blind_recode_sheet.csv'
with open(out, 'w', encoding='utf-8', newline='') as fh:
    w = csv.writer(fh)
    w.writerow(['entry_id', 'kind', 'competition', 'rank', 'author', 'source_confidence', 'source_folder'] + cols + ['n_fe_techniques_used', 'recoder_notes'])
    for i, e in enumerate(picked, 1):
        w.writerow([f'B{i:02d}', e['kind'], e['comp'], e['rank'], e['author'], e['conf'], e['folder']] + [''] * 53 + ['', ''])

print(f'Wrote {out} with {len(picked)} entries:')
for i, e in enumerate(picked, 1):
    print(f'  B{i:02d} [{e["era"]}] {e["kind"]:7s} {e["comp"]:34s} r{e["rank"]:<3s} {e["conf"]}')
from collections import Counter
print('  era spread :', dict(Counter(e['era'] for e in picked)))
print('  kind spread:', dict(Counter(e['kind'] for e in picked)))
print('  conf spread:', dict(Counter(e['conf'] for e in picked)))
