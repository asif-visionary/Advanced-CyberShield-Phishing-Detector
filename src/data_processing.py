import pandas as pd
import os
import glob

def load_and_standardize_datasets(dataset_dir="advanced_email_datasets"):
    """
    Loads Enron, Nazario, CEAS, and SpamAssassin datasets, extracts the 'body' 
    and 'label', and concatenates them into a single standardized DataFrame.
    """
    all_data = []
    
    # 1. Enron
    enron_path = os.path.join(dataset_dir, "Enron.csv")
    if os.path.exists(enron_path):
        df = pd.read_csv(enron_path, usecols=['body', 'label'])
        all_data.append(df)
        print(f"Loaded Enron: {len(df)} rows")
        
    # 2. Nazario
    nazario_path = os.path.join(dataset_dir, "Nazario.csv")
    if os.path.exists(nazario_path):
        df = pd.read_csv(nazario_path, usecols=['body', 'label'])
        all_data.append(df)
        print(f"Loaded Nazario: {len(df)} rows")
        
    # 3. CEAS_08
    ceas_path = os.path.join(dataset_dir, "CEAS_08.csv")
    if os.path.exists(ceas_path):
        df = pd.read_csv(ceas_path, usecols=['body', 'label'])
        all_data.append(df)
        print(f"Loaded CEAS_08: {len(df)} rows")
        
    # 4. SpamAssassin
    spam_path = os.path.join(dataset_dir, "SpamAssasin.csv")
    if os.path.exists(spam_path):
        df = pd.read_csv(spam_path, usecols=['body', 'label'])
        all_data.append(df)
        print(f"Loaded SpamAssassin: {len(df)} rows")
        
    if not all_data:
        raise FileNotFoundError(f"No datasets found in {dataset_dir}")
        
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Drop rows where body is NaN
    combined_df = combined_df.dropna(subset=['body'])
    
    # Ensure text is string
    combined_df['body'] = combined_df['body'].astype(str)
    
    print(f"\nTotal Standardized Data: {len(combined_df)} rows")
    print(f"Label Distribution:\n{combined_df['label'].value_counts()}")
    
    return combined_df
