# analysis/data/data_fetch.py
import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env (if exists)
load_dotenv()

# Get URL from .env or default
url = os.getenv("DATA_URL", "https://cryptodatadownload.com/cdd/Binance_BTCUSDT_1h.csv")
local_path = Path("analysis/data/Binance_BTCUSDT_1h.csv")

try:
    print(f"Trying online URL: {url}")
    df = pd.read_csv(url, skiprows=1)
except Exception as e:
    print(f"Failed to fetch from URL ({e}), falling back to local file: {local_path}")
    df = pd.read_csv(local_path, skiprows=1)

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])
print("Loaded rows:", len(df))