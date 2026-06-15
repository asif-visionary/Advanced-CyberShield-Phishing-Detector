import pandas as pd

df = pd.read_csv("PhiUSIIL_Phishing_URL_Dataset.csv")

print(df.columns.tolist())
print(df.head())