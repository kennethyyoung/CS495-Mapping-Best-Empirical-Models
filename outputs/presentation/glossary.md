# Glossary of terms

Reference for the presentation. Terms that may not be immediately obvious to a Kaggle-naive or less technically inclined audience.

---

**Adversarial validation** — A technique to detect distribution shift between training and test data. Train a classifier to distinguish train rows from test rows; if it scores well, the two distributions differ meaningfully.

**AUC / ROC AUC** — Area Under the Receiver Operating Characteristic Curve. A scoring metric for binary classification that ranges from 0.5 (random guessing) to 1.0 (perfect ranking). Used in many Kaggle competitions because it doesn't require choosing a probability threshold.

**AutoGluon** — An open-source AutoML framework from Amazon that automatically builds and ensembles a stack of tabular models (gradient-boosted trees, neural networks, etc.) with minimal user configuration. Sometimes used as a base model, sometimes as an ensemble meta-learner.

**AutoML** — Automated Machine Learning. A family of frameworks (AutoGluon, H2O AutoML, FLAML, Light AutoML) that automate model selection, hyperparameter tuning, and ensembling — removing much of the manual work in building a tabular model.

**Base model** — One of several models whose predictions feed into a *stacker* or *ensemble* layer. Typically gradient-boosted trees, neural networks, or other classical models.

**Brute-force feature engineering** — Computationally enumerating many possible feature combinations (e.g., all pairs, triples, quadruples of categorical columns), training a small model on each, and keeping the combinations that improve cross-validation score.

**CatBoost** — A gradient-boosted decision tree library from Yandex, known for native handling of categorical features and built-in target encoding.

**Community-template-tweak** — A winning paradigm (7% of corpus) where the solution is built primarily on a forked public notebook from another community member, with one meaningful addition by the winner (a domain-specific feature, a meta-architecture change, or a post-processing step).

**Constraint-to-strategy coupling** — A pattern observed in this study where a measurable property of the competition (the *constraint* — e.g., dataset size, availability of an external original) is associated with a particular winning strategy. Six such couplings were tested quantitatively; two survived the strong-evidence threshold.

**Cross-validation (CV)** — A technique for estimating how well a model will perform on unseen data. The training set is split into multiple "folds"; the model is trained on all-but-one fold and validated on the held-out fold, repeated for each fold.

**cuDF / cuML / RAPIDS** — A set of NVIDIA libraries (RAPIDS umbrella) that provide GPU-accelerated equivalents of pandas (cuDF) and scikit-learn (cuML). Enable processing large tabular datasets and training many models in parallel on a GPU.

**DAE / Denoising Autoencoder** — A neural network that learns to reconstruct its input from a corrupted version of itself. Used in tabular competitions for missing-value imputation (where the task itself is reconstruction) and as a feature-extraction step where the trained encoder produces latent representations.

**DeepTables / TabM / RealMLP / TabNet / FT-Transformer / SAINT** — Various neural network architectures designed specifically for tabular data. Used as base models in ensemble-stacking wins.

**Distribution shift** — A situation where the statistical distribution of the test data differs from the training data. Can be *temporal* (test is from a later time period), *covariate* (different feature distributions), or *label-related* (different target distributions). Affects how cross-validation should be set up.

**Ensemble** — A predictive model formed by combining the predictions of multiple base models. The most common combination methods are stacking, hill climbing, mean blending, and weighted blending.

**Ensemble-stacking** — The dominant winning paradigm in 62% of this study's corpus. Many base models (5 to 100+) are trained, and their out-of-fold predictions are combined by a *stacker* — typically a simple linear model like Ridge regression or a hill-climbed weighted average.

**External original dataset** — When a Kaggle competition uses synthetic data generated from a publicly available real-world dataset, that real dataset is the "external original." Winners may use it by row concatenation, column merging, feature derivation, or direct lookup — or choose not to use it if it hurts cross-validation.

**Featured competition** — A monetized Kaggle competition with sponsor-funded prizes (typically tens of thousands of US dollars). Usually involves proprietary or sensitive datasets. Contrast with non-monetized Playground Series competitions.

**Feature engineering (FE)** — The process of creating new input features from existing ones to improve model performance. Examples: extracting digits from a numeric column, combining two categorical columns, computing aggregates within groups, encoding categorical variables as target means.

**GBM / Gradient-boosted machine** — A family of tabular models (most commonly XGBoost, LightGBM, CatBoost) that train an ensemble of decision trees sequentially, each correcting the errors of the previous one. The dominant model family in winning tabular Kaggle solutions (78% of this corpus).

**Hill climbing (HC)** — An ensembling method where many base models' predictions are combined using greedy weighted averaging. At each step, the model that most improves the current ensemble's cross-validation score is added with a tuned weight. Linear and simple.

**Hyperparameter tuning** — The process of finding the best configuration for a model's adjustable parameters (e.g., XGBoost's `max_depth`, `learning_rate`). Commonly done with Optuna, GridSearchCV, or random search.

**Identity lookup** — A *lookup-exploit* sub-type where the winner matches each test row to an exact row in the public original dataset by a key, then assigns the original's target value directly. Example: s3e14 (Sergey) matched test rows by `(fruitset, fruitmass)` keys.

**Inversion lookup** — A *lookup-exploit* sub-type where training rows with identical features happen to have *opposite* labels; the winner assigns the opposite label to any test row whose features match a training row. Example: s3e7 (Hardy Xu).

**k-fold (cross-validation)** — A specific form of cross-validation where the data is split into k equal parts (typically 5 or 10). The model is trained on k-1 parts and validated on the remaining one, repeated k times. The average score is the cross-validated estimate.

**KDTree lookup** — Using a k-dimensional-tree data structure to quickly find the nearest neighbor of each test point in a reference dataset. In our corpus, used as a *lookup-exploit* technique to attach the target of the nearest original-dataset row as a feature.

**Knowledge distillation** — Training a "student" model to match the soft (probability) predictions of a "teacher" model, in addition to the hard labels. Originally a technique for compressing large models into smaller ones; in this corpus, used by one winner for ensemble diversity.

**LAD regression** — Least Absolute Deviation regression. A linear regression variant that minimizes the sum of absolute errors instead of squared errors; well-suited as a stacker when the competition metric is MAE.

**LightGBM** — A gradient-boosted decision tree library from Microsoft. Known for being fast on large datasets and using leaf-wise tree growth instead of level-wise.

**Linear stacker** — A stacker that combines base-model predictions using a linear formula (Ridge regression, mean blend, weighted blend, hill-climbed weighted average, LAD regression). Contrasted with *nonlinear stackers* (CatBoost-as-stacker, NN-as-stacker, AutoGluon-as-stacker). Dominant in 80% of stacker-using wins.

**Lookup-exploit** — A winning paradigm (9% of corpus) where the solution exploits a property of the synthetic-data generator — typically that it preserves identifiable (feature, target) pairs from a public original dataset — to predict by direct key matching rather than by a learned model. Three sub-types: identity, inversion, distance-via-generator-flaw.

**MAP@K** — Mean Average Precision at K. A ranking metric used for top-K recommendation problems; measures how well the top-K predicted classes include the correct class.

**Matthews Correlation Coefficient (MCC)** — A binary classification metric that accounts for true positives, true negatives, false positives, and false negatives. Robust to class imbalance.

**Mean blend** — The simplest ensembling method: average the predictions of multiple base models with equal weight. A type of linear stacker.

**Notebook** — A Jupyter (`.ipynb`) document combining code, text, and output, hosted publicly on Kaggle. Winning notebooks are typically published after the competition closes.

**OOF / Out-of-fold predictions** — The validation predictions produced during cross-validation for each row in the training set. Used as input features for *stacking* ensembles.

**OpenFE** — An academic automated feature-engineering library (Zhang et al. 2022) that generates many candidate engineered features and selects useful ones. Used by one winner in this corpus (s4e4).

**Optuna** — An open-source hyperparameter optimization library. Uses Bayesian optimization to efficiently search large hyperparameter spaces.

**Origination score** — A 0–3 ordinal coded in Pass 2 of this study: 0 = pure fork from a public notebook; 1 = fork with a small tweak; 2 = significant original work built on a community foundation; 3 = mostly original. Zero entries in the 45-entry corpus were coded as score 0.

**Paradigm** — In this study, a classification of the overall winning strategy of a solution into one of six categories: ensemble-stacking, single-model-FE, lookup-exploit, problem-fit-NN, community-template-tweak, or mixed.

**Pass 1 / Pass 2** — The two-pass coding methodology used in this study. Pass 1 is the structured 38-column spreadsheet (capturing *what was used*). Pass 2 is the per-writeup qualitative re-evaluation (capturing *what was originated*, paradigm, citations, and per-winner unique edge).

**Photo-finish margin** — In this study, a tight gap (less than 0.0005 absolute or 0.1% relative) between the rank-1 and rank-3 private leaderboard scores. Indicates a competition where many competitors converged at the same score.

**PLE / Piecewise Linear Encoding** — A neural-network preprocessing technique for numerical features (Gorishniy et al. 2022, arXiv 2203.05556) that learns piecewise-linear embeddings instead of using raw values. Used by one winner (s3e26).

**Playground Series (PS)** — A series of monthly non-monetized Kaggle competitions, started in 2023, using synthetic datasets generated from publicly available real-world datasets. Successor to the Tabular Playground Series. Numbered by season (S3, S4, S5, S6) and episode (E1–E12).

**Private leaderboard (private LB)** — The Kaggle leaderboard computed on a hidden test split, revealed at the end of the competition. The "true" ranking. Contrasts with the *public leaderboard*, computed on a smaller visible split during the competition.

**Problem-fit neural network** — A winning paradigm (7% of corpus) where a custom neural network architecture is matched to a specific structural property of the data — for example, a two-branch network mirroring an interaction graph (s4 May 2022), a denoising autoencoder for an imputation task (s4 Jun 2022), or a Variable Selection Network at extreme small-data scale (ICR).

**Pseudo-labeling** — Training a model on the labeled training data, using it to predict labels for the test data, then retraining on the combined dataset with those predicted labels as ground truth for the test rows.

**Random Forest** — A tabular model that trains many decision trees on random subsets of features and rows, then averages their predictions. Predates gradient-boosted machines and is occasionally used as an ensemble component.

**Ridge regression as stacker** — A specific linear stacker: Ridge regression (L2-regularized linear regression) fit on the out-of-fold predictions of base models to produce the final prediction. The most common stacker in the corpus.

**RMSE / RMSLE** — Root Mean Squared Error / Root Mean Squared Logarithmic Error. Two regression evaluation metrics. RMSE penalizes large errors heavily; RMSLE applies a log transform first, which softens the penalty for over-predictions.

**Single-model heavy-FE** — A winning paradigm (13% of corpus) where one model class (often XGBoost) is trained on a large number of hand-engineered features, without ensembling. Most viable when training data is large enough to support many features without overfitting.

**Snap features** — Features generated by "snapping" each row to its nearest match in a reference dataset (often via KDTree lookup) and attaching properties of that match. Used as a lookup-exploit technique, especially in cdeotte's KGMON Playbook.

**Stacking** — An ensembling method where the out-of-fold predictions of multiple base models are used as input features to a second-level *stacker* model. The stacker learns to weight the base models optimally.

**Stratified k-fold** — A variant of k-fold cross-validation where the proportion of each class in each fold matches the proportion in the full dataset. Standard for classification tasks; preserves class balance across folds.

**Synthetic data / Synthetic generator** — Data produced by a programmatic process (rather than collected from real-world observations). Kaggle Playground Series competitions use synthetic data generated from public real-world datasets; the generator's properties (whether it preserves keys, introduces noise, etc.) determine which exploits are viable.

**Tabular Playground Series (TPS)** — The 2021–2022 predecessor to the Playground Series. Monthly non-monetized Kaggle competitions on synthetic tabular data.

**Target encoding** — A categorical-feature encoding technique that replaces each category with the mean of the target variable for rows in that category. Often computed within cross-validation folds to avoid leakage. The most common encoding technique in the corpus.

**Validation discipline** — The practice of deliberately choosing a submission with a lower public-leaderboard score because its cross-validation score is higher and more trustworthy. Anti-greedy: refuses to chase public-LB position when CV suggests overfitting.

**VSN / Variable Selection Network** — A neural network architecture from the Temporal Fusion Transformer paper (Lim et al. 2019, arXiv 1912.09363) that learns per-feature attention weights to select informative features. Used by the ICR winner at extreme small-data scale.

**Weighted blend** — An ensembling method where base-model predictions are combined using hand-tuned or optimized weights (as opposed to equal weights in a mean blend). A type of linear stacker.

**Winner unique edge** — A 200-character free-text field captured in Pass 2 for each entry, describing the single distinguishing element of that winner's solution. Used both for qualitative texture in the typology and as the strategy filter in the coupling-evidence framework.

**Writeup** — A public post on Kaggle's discussion forum where a competition winner (or top finisher) describes the methods, models, and tricks used in their solution. The primary source material for this study.

**XGBoost** — Extreme Gradient Boosting. A widely used gradient-boosted decision tree library; the original "modern" GBM (released 2014) and still a frequent winner in tabular Kaggle competitions.
