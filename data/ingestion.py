# data/ingestion.py

import pandas as pd
from datetime import datetime

def fetch_data(symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """
    Fetches historical market data for a given symbol. This example fetches data from a CSV file.
    In a real scenario, this could be replaced with an API call.
    """
    # Placeholder: Replace with actual CSV or API logic
    # Example (CSV): df = pd.read_csv(f"{symbol}.csv", parse_dates=['Date'])
    # For now, we'll create a mock DataFrame:
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    df = pd.DataFrame({
        'Date': dates,
        'Open': [100 + i for i in range(len(dates))],
        'High': [105 + i for i in range(len(dates))],
        'Low': [95 + i for i in range(len(dates))],
        'Close': [102 + i for i in range(len(dates))],
        'Volume': [1000 + (i * 10) for i in range(len(dates))]
    })
    return df

def fetch_realtime_data(symbol: str) -> pd.DataFrame:
    """
    Fetches real-time market data for a given symbol. Currently returns mock data.
    Replace with actual real-time data API logic when available.
    """
    now = datetime.now()
    df = pd.DataFrame({
        'Date': [now],
        'Open': [100],
        'High': [105],
        'Low': [95],
        'Close': [102],
        'Volume': [1500]
    })
    return df
