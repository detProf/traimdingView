
from strategies.base_strategy import BaseStrategy
from data_feed import DataFeed

class SampleStrategy(BaseStrategy):
    def __init__(self, rsi_period=14, overbought=70, oversold=30):
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold
        self.data_feed = DataFeed()

    def generate_signal(self, symbol, market_data):
        """
        Generates a trading signal using RSI.
        """
        rsi = self.data_feed.get_rsi(symbol, period=self.rsi_period, interval="1min")

        if rsi is None:
            return {"action": "HOLD", "symbol": symbol}

        if rsi > self.overbought:
            return {"action": "SELL", "symbol": symbol}
        elif rsi < self.oversold:
            return {"action": "BUY", "symbol": symbol}
        else:
            return {"action": "HOLD", "symbol": symbol}
