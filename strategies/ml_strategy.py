# strategies/ml_strategy.py

import pandas as pd

from core.interfaces import IStrategy
from core.models import OrderType
from ml.model_selector import get_ml_model

class MLStrategy(IStrategy):
    def __init__(self, config: dict):
        """
        Initializes the ML-based strategy by loading an ML model
        according to the given config (e.g., 'ml_model': 'random_forest').
        """
        self.model = get_ml_model(config)

    def generate_signal(self, data: pd.DataFrame) -> OrderType:
        """
        Generates a trading signal using an ML model. Extracts features from 'data'
        (e.g., the last row) and calls the model's 'predict_action' method.
        The model returns a string like "BUY", "SELL", etc., which we map to OrderType.
        """
        # Example of taking the last row as features
        features = data.iloc[[-1]]  # Keep as DataFrame for the model

        # Model predicts an action string ("BUY", "SELL", "HOLD", etc.)
        prediction_str = self.model.predict_action(features)

        # Map the string to our OrderType enum
        # We assume the prediction_str matches the enum member names exactly:
        try:
            return OrderType(prediction_str)
        except ValueError:
            # If not recognized, default to HOLD
            return OrderType.HOLD
