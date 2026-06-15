import pandas as pd
import numpy as np
import joblib
import warnings
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from sklearn.pipeline import FeatureUnion
from sklearn.feature_extraction.text import TfidfVectorizer
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTE
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from sklearn.ensemble import RandomForestClassifier

from data_processing import load_and_standardize_datasets
from feature_engineering import TextPreprocessor, HandcraftedFeatureExtractor

warnings.filterwarnings('ignore', category=UserWarning, module='bs4')

def main():
    print("Loading datasets...")
    df = load_and_standardize_datasets("../advanced_email_datasets")
    
    # Stratified Sampling to manage memory and time (max 15k per class)
    max_samples = 15000
    df_0 = df[df['label'] == 0]
    df_1 = df[df['label'] == 1]
    
    if len(df_0) > max_samples: df_0 = df_0.sample(max_samples, random_state=42)
    if len(df_1) > max_samples: df_1 = df_1.sample(max_samples, random_state=42)
    
    df_sampled = pd.concat([df_0, df_1]).sample(frac=1, random_state=42).reset_index(drop=True)
    print(f"Sampled Dataset Size: {len(df_sampled)}")
    
    X = df_sampled['body'].to_list()
    y = df_sampled['label'].to_numpy(dtype=int)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print("\nBuilding Pipeline...")
    features = FeatureUnion([
        ('tfidf', ImbPipeline([
            ('clean', TextPreprocessor()),
            ('vectorizer', TfidfVectorizer(max_features=3000, ngram_range=(1,2)))
        ])),
        ('handcrafted', HandcraftedFeatureExtractor())
    ])
    
    pipeline = ImbPipeline([
        ('features', features),
        ('smote', SMOTE(random_state=42)),
        # Using XGBoost as default for best performance
        ('classifier', XGBClassifier(n_estimators=150, max_depth=6, learning_rate=0.1, n_jobs=-1, random_state=42))
    ])
    
    print("Training Model (This may take a while)...")
    pipeline.fit(X_train, y_train)
    
    print("\nEvaluating Model...")
    y_pred = pipeline.predict(X_test)
    
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1-Score:  {f1_score(y_test, y_pred):.4f}")
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    print("Saving Model...")
    joblib.dump(pipeline, "../advanced_email_model.pkl")
    print("Model saved to ../advanced_email_model.pkl")

if __name__ == "__main__":
    main()
