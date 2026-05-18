import sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('data/kaggle_meta_analysis.xlsx')
ws = wb['Competition Data']
headers = [cell.value for cell in ws[1]]
rows = list(ws.iter_rows(min_row=2, values_only=True))

def col(name):
    idx = headers.index(name)
    return [r[idx] for r in rows]

def get(row_dict, name):
    return str(row_dict.get(name, '') or '').strip()

flags = []

for r in rows:
    d = dict(zip(headers, r))
    ref = get(d, 'competition_ref')

    pct     = float(d.get('pct_missing') or 0)
    card    = d.get('max_cardinality')
    has_cat = str(d.get('has_categorical') or '').upper()
    enc     = get(d, 'encoding_strategy')
    mds     = get(d, 'missing_data_strategy')
    scale   = get(d, 'scaling')
    model   = get(d, 'dominant_base_model')
    tt      = get(d, 'target_type')
    cv      = get(d, 'cv_strategy')
    ft      = get(d, 'feature_type_dominant')
    n_rows  = d.get('n_rows')

    SKIP = {'not_described', 'not_applicable', 'automated', 'none', ''}

    # 1. has_categorical=FALSE but encoding_strategy is a real technique
    enc_vals = [v.strip() for v in enc.split(';') if v.strip() not in SKIP]
    if has_cat == 'FALSE' and enc_vals:
        flags.append((ref, 'has_categorical=FALSE but encoding_strategy set',
                      f'encoding_strategy={enc}'))

    # 2. has_categorical=TRUE but max_cardinality=0
    try:
        card_i = int(float(card)) if card is not None else None
    except (ValueError, TypeError):
        card_i = None
    if has_cat == 'TRUE' and card_i == 0:
        flags.append((ref, 'has_categorical=TRUE but max_cardinality=0',
                      f'max_cardinality={card}'))

    # 3. has_categorical=FALSE but max_cardinality > 0
    if has_cat == 'FALSE' and card_i is not None and card_i > 0:
        flags.append((ref, 'has_categorical=FALSE but max_cardinality>0',
                      f'max_cardinality={card}'))

    # 4. target_type=regression but cv_strategy contains stratified
    cv_vals = [v.strip() for v in cv.split(';') if v.strip() not in SKIP]
    if tt == 'regression' and any('stratified' in v for v in cv_vals):
        flags.append((ref, 'regression target but stratified CV',
                      f'cv_strategy={cv}'))

    # 5. pct_missing > 1% but missing_data_strategy = none
    if pct > 1.0 and mds == 'none':
        flags.append((ref, f'pct_missing={pct:.1f}% but missing_data_strategy=none', ''))

    # 6. GBM + explicit scaling (unusual — worth checking)
    scale_vals = [v.strip() for v in scale.split(';') if v.strip() not in SKIP]
    if model == 'gbm' and scale_vals:
        flags.append((ref, f'GBM but scaling={scale}', ''))

    # 7. feature_type_dominant=numeric but has_categorical=TRUE
    if ft == 'numeric' and has_cat == 'TRUE':
        flags.append((ref, 'feature_type_dominant=numeric but has_categorical=TRUE', ''))

    # 8. pct_missing > 0 and missing_data_strategy = not_described
    if pct > 0 and mds == 'not_described':
        flags.append((ref, f'pct_missing={pct:.2f}% but missing_data_strategy=not_described',
                      '(genuine gap)'))

if flags:
    print(f'{len(flags)} flags found:\n')
    for ref, issue, detail in flags:
        print(f'  [{ref}]')
        print(f'    {issue}')
        if detail:
            print(f'    {detail}')
        print()
else:
    print('No contradictions found.')
