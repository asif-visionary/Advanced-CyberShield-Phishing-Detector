import joblib

email_model = joblib.load("email_model.pkl")
url_model = joblib.load("url_model.pkl")

print("✓ Email model loaded")
print("✓ URL model loaded")