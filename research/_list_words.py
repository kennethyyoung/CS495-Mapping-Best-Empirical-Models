from wordcloud import WordCloud
import re

with open('research/generate_wordcloud.py', encoding='utf-8') as f:
    text = f.read()

marker = 'text = """'
start = text.index(marker) + len(marker)
end = text.index('"""', start)
body = text[start:end]

abbrev_map = {
    r'\bXGB\b': 'XGBoost',
    r'\bTE\b': 'target encoding',
    r'\bCE\b': 'count encoding',
    r'\bLR\b': 'linear regression',
    r'\bNN\b': 'neural network',
    r'\bGP\b': 'genetic programming',
    r'\bNaN\b': 'missing',
    r'\bbinned\b': 'binning',
    r'\bbins\b': 'binning',
    r'\bcombos\b': 'combinations',
    r'\btransform\b': 'transformation',
    r'\bnumerical\b': 'numeric',
}
for pattern, replacement in abbrev_map.items():
    body = re.sub(pattern, replacement, body, flags=re.IGNORECASE)

stopwords = [
    'combinatiuns', 'not_applicable', 'tfidf_svd', 'feature_creation',
    'numeric_type_casting', 'interaction_features', 'target_encoding_pairs',
    'rounding_features', 'te_descriptive_stats', 'text_feature_extraction',
    'outlier_classification', 'target_encoding_median', 'catboost_oof_as_feature',
    'leakfree',
    'IBM', 'yield', 'horsepower', 'displacement', 'engine', 'mileage_binning',
    'price_bin', 'credit_score', 'insured', 'vehicle', 'damage',
    'age', 'distance', 'tenure', 'store', 'IQR',
    # generic English
    'of', 'for', 'on', 'as', 'to', 'from', 'all', 'and', 'with', 'per',
    'by', 'but', 'via', 'way', 'over', 'using', 'kept', 'tried', 'data',
    'based', 'treated', 'single', 'two', 'multiple', 'None', 'previously',
    'test', 'train', 'cols', 'vs',
    # noise abbreviations and artifacts
    'x', 'x0', 'x7', 'z', 'sq', 'cb', 'nb_sup6', 't',
    # too generic given the topic
    'feature', 'features', 'encoding', 'count', 'column', 'columns', 'original', 'pairs',
    # remaining competition-specific noise
    'fruitset', 'fruitmass', 'edema', 'meat', 'BMI', 'viscera', 'gemstone',
    'AgeInDays', 'store_sqft', '360K', '145K', 'carat', 'stage',
    # remaining generic noise
    'poisonous', 'confident', 'disagreement', 'overwriting', 'assign',
    'handles', 'internally', 'failed', 'SNE', 'Brute', 'force', 'script',
    'samples', 'yields', 'FE', 'worsened', 'in',
    # CV/training concepts, not FE
    'fold', 'CV', 'KFold', 'seed', 'retrain', 'averaging', 'repeated',
    # too generic standalone
    'value', 'model', 'score', 'base', 'version', 'wise', 'key', 'integer',
    'groups', 'input', 'comparison', 'separately', 'public', 'diff', 'type',
    'dual', 'alternative', 'sorted', 'subtract', 'backward', 'margin',
    'probability', 'engineered', 'treating', 'range', 'core', 'improvement',
    'match', 'automated', 'unique', 'continuous', 'round', 'described',
    'across', 'class', 'terms', 'plots', 'quality', 'methodology', 'notebook',
    'identification', 'native', 'opposite', 'assignment', 'predict', 'filter',
    'removal', 'counterparts', 'driven', 'flags', 'rate', 'years', 'new',
    'merge', 'composite', 'post processing',
    # competition-specific leftovers
    'medical', 'thickness', 'area', 'aspect', 'length', 'surface', 'risk',
    'hourly', 'job', 'hopper', 'Policy', 'Start', 'Date', 'GPU', 'accelerated',
    # code variables
    'AttritionRisk', 'MonthlyIncome', 'AverageTenure', 'TotalWorkingYears',
    'NumCompaniesWorked', 'match_p', 'automated_fe', 'OptimizedRounder', 'PLE',
]
wc = WordCloud(max_words=200, stopwords=stopwords).generate(body)
freqs = sorted(wc.words_.items(), key=lambda x: -x[1])
for word, freq in freqs:
    print(f'{freq:.3f}  {word}')
