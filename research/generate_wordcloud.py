import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re

# The text about feature engineering techniques
text = """Feature store (12 versions); component models on feature subsets (previously insured, vehicle damage); feature importance via CatBoost
single-fold none log1p transforms; product/division/sum/diff pairs; binned features (9 bins); groupby z-score features (26); residual modeling (NN on LR residuals, XGB on NN residuals); cuML TargetEncoder ratio features (medical
domain pairs); polynomial features (sq; cb); target encoding; original data concat Autoencoder latent features; genetic programming features (11 GP); XGBoost residual boosting; multiple feature type representations
(categorical/numerical/mixed) original data concat; dual numeric+categorical representation Digit extraction from numericals; pairwise/triple/quadruple digit interactions + TE/CE; base feature pairs + TE/CE; quantile binning;
categorical version of credit_score; TE with alternative targets tfidf_svd, feature_creation, interaction_features, numeric_type_casting Groupby aggregations (mean/std/count/min/max/nunique/skew); groupby histogram bins; groupby
quantiles; NaN base-2 encoding; numerical rounding/binning; digit extraction from floats; categorical column combinations (all pairs); division features (ratios of aggregated features) TE/CE on feature bigrams (competition +
original targets); products of numerical bigrams; cyclical features target_encoding_pairs (1-6 way), interaction_features, rounding_features, te_descriptive_stats text_feature_extraction (horsepower/displacement from engine),
mileage_binning, outlier_classification (IQR price_bin), target_encoding_median (leakfree per fold), catboost_oof_as_feature Row-wise statistics (sum/std/max); sorted features; count threshold features (nb_sup6/7/8); target
encoding on row sum; target transformation (subtract feature mean x0.1); permutation + backward feature selection not_applicable All pairs/triples/quadruples of 8 features (162 combos); TE of 162 combos x7 binary targets (2268
cols); TE using original dataset; residual boosting (XGB over LR base margin); pseudo labeling; repeated KFold seed averaging; retrain on 100% data Original dataset poisonous probability as engineered feature; confident
disagreement overwriting (predictions >0.99 threshold) Label encoding; TE (mean/median/min/max/nunique) + CE per column; column combinations (2-6 way); treating numerics as categorical + TE/CE; Policy Start Date decomposition;
GPU-accelerated search of 145K+ combinations -> 170 kept Ratio features (length/thickness); range x area interaction; min-max normalized thickness feature; feature dropping via CV + feature importance + correlation Brute-force
feature combinations (80-120 kept); permutation importance for feature pruning Log transformation of all features (core improvement); PCA/t-SNE/clustering tried but failed Post-processing: match test rows to original dataset by
fruitset+fruitmass key -> assign original yield values; automated matching script (2073 test samples x 776 unique yields) Piecewise linear encoding (PLE) for continuous features; embedding layers for categorical features (edema,
stage); value rounding for GBT features Domain features (meat yield/surface area/weight ratios/pseudo BMI/viscera ratio); log transform on weight; post-processing (round to nearest integer); feature subset selection (6-10
features per model) None described — AutoML handles internally Feature subset selection across models; duplicate grouping (360K->3000 groups); log1p target transformation; store_sqft treated as categorical None None — FE tried
but worsened CV; post-processing with OptimizedRounder for ordinal class cutoffs XGBoost predictions as GAM input features; Lasso predictions as GAM input features; interaction terms in GAM Nonlinear features for linear
regression (from partial dependence plots); feature selection by CV; target encoding of AgeInDays (treated as categorical) Ordinal encoding of gemstone quality categoricals; aspect ratio features; carat x aspect ratio
interaction; encoding methodology comparison via CV Permutation importance for feature selection (per model separately) Coordinate-based geographic features (from public notebook) Categorical feature identification; OHE vs native
 encoding comparison; duplicate/leakage exploitation (opposite label assignment; predict 0.5 for test duplicates); adversarial validation to filter original dataset; removal of train duplicates with test counterparts
Domain-driven risk flags (age<34; hourly rate<60; distance>=20; tenure<4 years; job hopper); composite AttritionRisk score; MonthlyIncome/Age ratio; AverageTenure (TotalWorkingYears/NumCompaniesWorked) original data merge as new
feature (match_p) automated_fe (OpenFE), feature_selection (sequential) aggregates Custom reverse-transformation of decamer counts to 100-dimensional random index space for Manhattan distance matching of train/test pairs sharing
generation seed Xgbfir interaction graph analysis identifying two disconnected feature components; two-branch NN architecture restricting interactions to graph components; unique_characters feature; pairwise interaction features
(i_02_21, i_05_22, i_00_01_26) Feature-wise linear embeddings of values and null mask with additive fusion; conditional ensemble by F4 null count (single-null rows predicted separately); mean imputation for F1 and F3 groups
Cyclical feature encoding; formula-based score feature from public discussion; categorical copy of each numeric feature for TE; digit features; TE (mean/std/skew) of feature and digit combinations; ordinal mapping of categorical
features (GBDT set); Isotonic Regression post-processing Quantile and equal-width binning; digit features; all features treated as categorical; within-fold target encoding (cuml TargetEncoder, 5-fold, smooth=10); genetic
programming (gplearn) nonlinear features; original dataset target statistics (mean, smoothed mean, WoE, entropy) as external TE; DVAE latent representations for diversity; knowledge distillation (soft labels = 0.5 * hard labels +
 0.5 * teacher RealMLP OOF) Snap features (nearest original IBM value mapping); decimal digit extraction; nested/leak-free target encoding on all 16 categorical columns; bigrams, trigrams, binned numerics; arithmetic interactions
 (TC_deviation, MC-to-TC ratio); multi-scale binning (up to 5000 quantile bins); categorical cross-features; frequency/count encoding; service count aggregations; original IBM cKDTree nearest-neighbor lookup; radix interaction
features; synthetic artifact detection (Benford's Law deviation, TF-IDF on numeric strings, fractional fingerprints); PCA/GRP projection on original IBM data; cyclical tenure features Digit features (individual digits at integer
and decimal positions for all numeric columns); magnitude-based rounding of numerics; frequency encoding of categoricals and digit columns (rare categories mapped to default bucket); pairwise interaction cross-features (string
concatenation of column pairs, filtered by key columns); target encoding (sklearn TargetEncoder)"""

stopwords = ['combinatiuns']

# Create the word cloud
wordcloud = WordCloud(width=1600, height=800,
                      background_color='white',
                      colormap='viridis',
                      max_words=200,
                      relative_scaling=0.5,
                      min_font_size=10).generate(text)

# Create figure and display
plt.figure(figsize=(20, 10))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Feature Engineering Techniques Word Cloud', fontsize=20, pad=20)
plt.tight_layout(pad=0)

# Save the word cloud
plt.savefig('research/feature_engineering_wordcloud.png', dpi=300, bbox_inches='tight')
print("Word cloud saved to research/feature_engineering_wordcloud.png")
plt.close()
