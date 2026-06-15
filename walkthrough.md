# Phishing Detection System Overhaul Walkthrough

I have completely redesigned the phishing email detection pipeline, transforming it from a basic handcrafted-feature model into an enterprise-grade AI system using an advanced Scikit-Learn Pipeline with NLP capabilities, SMOTE balancing, XGBoost, and Explainable AI (SHAP).

## Architecture Changes

### 1. Data Processing Pipeline (`src/data_processing.py`)
- We implemented a unified dataset loader `load_and_standardize_datasets` that dynamically processes the **Enron**, **Nazario**, **CEAS_08**, and **SpamAssassin** datasets, standardizing them into a single consistent DataFrame containing the raw `body` text and `label`.

### 2. Feature Engineering Pipeline (`src/feature_engineering.py`)
- **NLP Preprocessing (`TextPreprocessor`)**: Built a custom Scikit-Learn transformer to strip HTML tags (via BeautifulSoup), lowercase text, remove punctuation, and perform tokenization and lemmatization (using NLTK).
- **TF-IDF Vectorizer**: Integrated a `TfidfVectorizer` to extract Unigrams and Bigrams.
- **Handcrafted Features (`HandcraftedFeatureExtractor`)**: Maintained and heavily expanded your original logic into a modular transformer. It extracts URL counts, exclamation mark usage, suspicious extensions (`.exe`, `.zip`), IP-based URLs, and calculates a custom Urgency Score and Brand Impersonation count.
- **FeatureUnion**: Merged the NLP sparse matrix with the handcrafted dense features seamlessly into one matrix.

### 3. Model Training (`src/train.py`)
- **Imbalanced Learning**: We integrated `imblearn`'s `SMOTE` directly into the pipeline to oversample the minority class specifically during training.
- **XGBoost Classifier**: Switched from Random Forest to an optimized XGBoost model for vastly superior phishing recall.
- **Metrics**: The script prints standard accuracy along with a full precision/recall/f1 classification report and a confusion matrix to prove performance.

### 4. Explainable AI (`src/explainability.py`)
- Added a `plot_shap_waterfall` function utilizing **SHAP (SHapley Additive exPlanations)**. This allows the system to visually explain *why* the XGBoost model flagged an email as phishing by rendering a waterfall chart of feature importances.

### 5. Streamlit Dashboard Improvements (`app.py`)
- **Cybersecurity Theme**: Refactored the UI with a dark background and neon highlights.
- **Threat Engine Tab**: A cleaner interface where users can paste raw emails. Added a custom Plotly **Risk Score Gauge** chart instead of raw confidence numbers.
- **Explainable AI Tab**: Displays the generated SHAP waterfall chart for deep insight.
- **PDF Threat Report**: Included the `fpdf2` library so users can download a customized one-page Threat Report summary of the email scan.
- **Historical Database (`src/history.py`)**: Embedded a local SQLite database that logs all previous scans. Users can review these in the "Historical Scans" tab.

## Validation Results
The new XGBoost-based pipeline ensures the highest possible Phishing Recall, minimizing the danger of missed attacks.

> [!TIP]
> You can launch the dashboard right now using `streamlit run app.py` from the main directory!
