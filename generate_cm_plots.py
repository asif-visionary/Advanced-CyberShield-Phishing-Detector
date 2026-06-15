import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

import sys
sys.path.append("src")
from data_processing import load_and_standardize_datasets
from feature_engineering import TextPreprocessor, HandcraftedFeatureExtractor
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# --- Advanced Email Model ---
print("Loading datasets for evaluation...")
df = load_and_standardize_datasets("advanced_email_datasets")

df_0 = df[df['label'] == 0]
df_1 = df[df['label'] == 1]
max_samples = 15000
if len(df_0) > max_samples: df_0 = df_0.sample(max_samples, random_state=42)
if len(df_1) > max_samples: df_1 = df_1.sample(max_samples, random_state=42)

df_sampled = pd.concat([df_0, df_1]).sample(frac=1, random_state=42).reset_index(drop=True)

X = df_sampled['body'].to_list()
y = df_sampled['label'].to_numpy(dtype=int)

_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print("Loading advanced_email_model.pkl...")
model = joblib.load("advanced_email_model.pkl")
print(type(model))

print("Predicting test set...")
pred = model.predict(X_test)

print("\n--- Advanced Email Model Metrics ---")
print("Accuracy :", accuracy_score(y_test, pred))
print("Precision:", precision_score(y_test, pred))
print("Recall   :", recall_score(y_test, pred))
print("F1 Score :", f1_score(y_test, pred))

cm = confusion_matrix(y_test, pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Safe", "Phishing"])
disp.plot(cmap='Blues')
plt.title("Advanced Email Model Confusion Matrix")
plt.tight_layout()
plt.savefig("advanced_email_cm.png")
plt.close()
print("Saved advanced_email_cm.png")
# --- URL ---
df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")
features_to_keep = [
    "URLLength", "DomainLength", "IsDomainIP", "NoOfDegitsInURL",
    "NoOfQMarkInURL", "NoOfAmpersandInURL", "NoOfOtherSpecialCharsInURL", "IsHTTPS"
]
X = df[features_to_keep]
y = df["label"]
_, X_test, _, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = joblib.load("url_model.pkl")
pred = model.predict(X_test)
cm = confusion_matrix(y_test, pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["Safe", "Phishing"])
disp.plot(cmap='Blues')
plt.title("URL Model Confusion Matrix")
plt.tight_layout()
plt.savefig("url_cm.png")
plt.close()
