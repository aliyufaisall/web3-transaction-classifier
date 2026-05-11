import os
import pandas as pd

# Paths
FETCHED_PATH = os.path.join("data", "raw", "raw_transactions.csv")
KAGGLE_PATH = os.path.join("data", "raw", "kaggle_fraud_data.csv")
OUTPUT_PATH = os.path.join("data", "processed", "hybrid_training_data.csv")

def merge_data():
    print(" Loading Kaggle dataset...")
    kaggle_df = pd.read_csv(KAGGLE_PATH)
    
    # MLOPS BEST PRACTICE: Clean column names immediately
    # This removes hidden spaces or tabs that cause KeyErrors
    kaggle_df.columns = kaggle_df.columns.str.strip()
    
    print(" Summarizing fetched transactions...")
    fetched_df = pd.read_csv(FETCHED_PATH)
    
    # Calculate stats for the Vitalik row
    fetched_df['timeStamp'] = pd.to_datetime(fetched_df['timeStamp'], unit='s')
    avg_min_sent = fetched_df['timeStamp'].sort_values().diff().dt.total_seconds().mean() / 60
    
    # Mapping our summary to the cleaned Kaggle names
    vitalik_summary = {
        'Avg min between sent tnx': avg_min_sent,
        'Sent tnx': len(fetched_df),
        'Received Tnx': 0, 
        'total Ether sent': fetched_df['value'].astype(float).sum() / 10**18,
        'FLAG': 0 
    }
    
    important_cols = ['Avg min between sent tnx', 'Sent tnx', 'Received Tnx', 'total Ether sent', 'FLAG']
    
    # Double Check: If the column STILL isn't found, let's see what's actually there
    missing = [c for c in important_cols if c not in kaggle_df.columns]
    if missing:
        print(f" Still missing: {missing}")
        print(" Actual columns available in your file are:")
        print(kaggle_df.columns.tolist())
        return

    vitalik_row = pd.DataFrame([vitalik_summary])
    kaggle_subset = kaggle_df[important_cols]
    
    hybrid_df = pd.concat([kaggle_subset, vitalik_row], ignore_index=True)
    
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    hybrid_df.to_csv(OUTPUT_PATH, index=False)
    print(f" Success! Hybrid dataset created with {len(hybrid_df)} accounts.")

if __name__ == "__main__":
    merge_data()
