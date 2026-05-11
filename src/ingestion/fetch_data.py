import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ETHERSCAN_API_KEY")

# DEBUG: Check if the key is loaded correctly
if not API_KEY:
    print(" ERROR: .env file not found or ETHERSCAN_API_KEY is missing!")
else:
    # Prints just the first 5 chars to be safe
    print(f" API Key loaded: {API_KEY[:5]}...") 

RAW_DATA_DIR = os.path.join("data", "raw")

def fetch_and_save_txs(address, filename="raw_transactions.csv"):
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    
    url = "https://api.etherscan.io/v2/api"
    
    # 1. THE HEADERS (This makes you look like a human, not a bot)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    params = {
        'chainid': '1',
        'module': 'account',
        'action': 'txlist',
        'address': address,
        'startblock': 0,
        'endblock': 99999999,
        'sort': 'desc',
        'apikey': API_KEY
    }
    
    print(f"📡 Fetching transactions for {address}...")
    
    try:
        # 2. THE REQUEST (Now including the headers parameter)
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code != 200:
            print(f" Server Error: {response.status_code}")
            print(f"Raw Response: {response.text[:200]}") 
            return None

        data = response.json()
        
        if data['status'] == '1' and 'result' in data:
            df = pd.DataFrame(data['result'])
            save_path = os.path.join(RAW_DATA_DIR, filename)
            df.to_csv(save_path, index=False)
            print(f" Success! {len(df)} transactions saved to {save_path}")
            return save_path
        else:
            # This handles cases where API key is wrong or address has no txs
            print(f" API Error: {data.get('message', 'No message')}")
            print(f"Details: {data.get('result', 'None')}")
            return None
            
    
    except Exception as e:
        import traceback
        print(" A Python error occurred!")
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        # This shows you the exact line number where it crashed
        traceback.print_exc() 
        return None


if __name__ == "__main__":
    # Using Vitalik's address for testing
    VITALIK_ETH_ADDR = "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
    fetch_and_save_txs(VITALIK_ETH_ADDR)


