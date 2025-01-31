# indicators/rsi.py

import pandas as pd
from core.interfaces import IIndicator

class RsiIndicator(IIndicator):
    def __init__(self, period: int = 14):
        self.period = period

    def calculate(self, data: pd.DataFrame) -> float:
        """
        Calculates the RSI (Relative Strength Index) for the provided data.
        Assumes 'data' is a DataFrame with a 'close' column.
        
        Returns the most recent RSI value as a float.
        """
        if 'close' not in data.columns:
            raise ValueError("DataFrame must contain a 'close' column.")

        # Calculate price changes
        delta = data['close'].diff()

        # Separate gains and losses
        gains = delta.clip(lower=0)
        losses = -1 * delta.clip(upper=0)

        # Calculate rolling mean gains and losses
        avg_gain = gains.rolling(window=self.period, min_periods=self.period).mean()
        avg_loss = losses.rolling(window=self.period, min_periods=self.period).mean()

        # Avoid division by zero
        avg_loss = avg_loss.replace(to_replace=0, value=1e-10)

        # Calculate RS (Relative Strength)
        rs = avg_gain / avg_loss

        # Calculate RSI
        rsi = 100.0 - (100.0 / (1.0 + rs))

        # Return the latest RSI value
        return rsi.iloc[-1]
