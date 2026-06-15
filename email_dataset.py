import pandas as pd

df = pd.read_csv("email_phishing_data.csv")

print(df.columns.tolist())
print(df.head())