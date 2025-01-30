
import pandas as pd
from indicators.base_indicator import BaseIndicator

class MACDIndicator(BaseIndicator):
    def __init__(self, fast_period=12, slow_period=26, signal_period=9):
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period

    def compute(self, prices):
        ema_fast = prices.ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = prices.ewm(span=self.slow_period, adjust=False).mean()
        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()
        macd_histogram = macd_line - signal_line

        return macd_line.iloc[-1], signal_line.iloc[-1], macd_histogram.iloc[-1]
