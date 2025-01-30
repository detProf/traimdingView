
import pandas as pd
from indicators.base_indicator import BaseIndicator

class RSIIndicator(BaseIndicator):
    def __init__(self, period=14):
        self.period = period

    def compute(self, prices):
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi.iloc[-1]
