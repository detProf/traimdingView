# strategies/multi_action_strategy.py

import pandas as pd

from core.interfaces import IStrategy
from core.models import OrderType
from indicators.rsi import RsiIndicator
from ml.model_selector import get_ml_model

class MultiActionStrategy(IStrategy):
    """
    Example of a multi-action strategy that combines an RSI indicator
    with an ML model prediction to yield multi-action outputs like
    BUY_CALL, BUY_PUT, SELL_CALL, SELL_PUT, etc.
    """

    def __init__(self, config: dict, rsi_period: int = 14):
        self.rsi_indicator = RsiIndicator(period=rsi_period)
        self.model = get_ml_model(config)  # The model might return "call", "put", etc.

    def generate_signal(self, data: pd.DataFrame) -> OrderType:
        # Calculate RSI
        rsi_value = self.rsi_indicator.calculate(data)
        
        # Basic RSI-based category
        if rsi_value < 30:
            rsi_bias = "bullish"
        elif rsi_value > 70:
            rsi_bias = "bearish"
        else:
            rsi_bias = "neutral"

        # Get an ML model suggestion (mocked to return a single string, e.g., "call", "put")
        # Here we take the last row as features:
        features = data.iloc[[-1]]
        ml_output = self.model.predict_action(features)

        # Combine RSI bias + ML output into final multi-action decision
        if rsi_bias == "bullish" and ml_output.lower() == "call":
            return OrderType.BUY_CALL
        elif rsi_bias == "bullish" and ml_output.lower() == "put":
            return OrderType.BUY_PUT
        elif rsi_bias == "bearish" and ml_output.lower() == "call":
            return OrderType.SELL_CALL
        elif rsi_bias == "bearish" and ml_output.lower() == "put":
            return OrderType.SELL_PUT
        else:
            # If we're neutral or don't match above conditions, just HOLD
            return OrderType.HOLD
