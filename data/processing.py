# data/processing.py

import pandas as pd

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Prepares features for machine learning or other analytics by
    calculating moving averages or performing normalization, etc.
    """
    df = df.copy()
    df['MA_5'] = df['Close'].rolling(window=5).mean()
    df['MA_10'] = df['Close'].rolling(window=10).mean()
    # Example of normalization (commented out):
    # df['Close_norm'] = (df['Close'] - df['Close'].min()) / (df['Close'].max() - df['Close'].min())
    return df

def split_train_test(df: pd.DataFrame, test_size: float = 0.2):
    """
    Splits the DataFrame into train and test sets for ML training.
    """
    split_idx = int(len(df) * (1 - test_size))
    train_df = df.iloc[:split_idx].copy()
    test_df = df.iloc[split_idx:].copy()
    return train_df, test_df
