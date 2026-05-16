import sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('data/kaggle_meta_analysis.xlsx')
ws = wb['Competition Data']
headers = [cell.value for cell in ws[1]]

ref_idx = headers.index('competition_ref')

FIXES = {
    'icr-identify-age-related-conditions': {
        'feature_type_dominant': 'mixed',
    },
    'playground-series-s5e5': {
        'has_categorical': False,
    },
    'playground-series-s3e6': {
        'has_categorical': True,
    },
    'playground-series-s4e5': {
        'encoding_strategy': 'not_described',
    },
    'playground-series-s3e9': {
        'encoding_strategy': 'not_described',
    },
    # Round 2 fixes (session 11 writeup audit)
    'playground-series-s3e11': {
        # store_sqft has 20 unique values (writeup); 0 was a coding gap, not true cardinality
        'max_cardinality': 20,
    },
}

for row in ws.iter_rows(min_row=2):
    ref = row[ref_idx].value
    if ref not in FIXES:
        continue
    for field, new_val in FIXES[ref].items():
        idx = headers.index(field)
        old_val = row[idx].value
        row[idx].value = new_val
        print(f'[{ref}] {field}: {old_val!r} → {new_val!r}')

wb.save('data/kaggle_meta_analysis.xlsx')
print('\nSaved.')
