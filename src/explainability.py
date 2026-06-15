import shap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_feature_names(pipeline):
    """
    Extracts feature names from the combined FeatureUnion.
    """
    features_union = pipeline.named_steps['features']
    
    # 1. TF-IDF features
    tfidf_pipeline = dict(features_union.transformer_list).get('tfidf')
    tfidf_vectorizer = tfidf_pipeline.named_steps['vectorizer']
    tfidf_names = tfidf_vectorizer.get_feature_names_out()
    
    # 2. Handcrafted features
    handcrafted_names = [
        "Num URLs", "Num HTML Tags", "Num Exclamations", "Num Special Chars",
        "Uppercase Ratio", "Suspicious Attachment", "Urgency Score",
        "Brand Impersonation", "IP-based URL", "Shortened URL", "URL Entropy"
    ]
    
    return np.concatenate([tfidf_names, handcrafted_names])

def plot_shap_waterfall(pipeline, text):
    """
    Plots a SHAP waterfall plot for a single text instance.
    """
    classifier = pipeline.named_steps['classifier']
    feature_union = pipeline.named_steps['features']
    
    # Transform text to features
    X_transformed = feature_union.transform([text])
    
    # Density for SHAP (XGBoost expects dense or sparse, but SHAP prefers dense for waterfall sometimes)
    if hasattr(X_transformed, "toarray"):
        X_dense = X_transformed.toarray()
    else:
        X_dense = X_transformed
        
    feature_names = get_feature_names(pipeline)
    
    explainer = shap.TreeExplainer(classifier)
    shap_values = explainer(X_dense)
    
    # Configure SHAP
    shap_values.feature_names = feature_names
    
    plt.figure(figsize=(8, 5))
    shap.plots.waterfall(shap_values[0], max_display=10, show=False)
    plt.tight_layout()
    plt.savefig("shap_waterfall.png")
    plt.close()
