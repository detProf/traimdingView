
from strategies.base_strategy import BaseStrategy
from data_feed import DataFeed

class MultiIndicatorStrategy(BaseStrategy):
    def __init__(self, rsi_period=14, overbought=70, oversold=30):
        self.rsi_period = rsi_period
        self.overbought = overbought
        self.oversold = oversold
        self.data_feed = DataFeed()

    def generate_signal(self, symbol, market_data):
        """
        Combines RSI and MACD to generate a trading signal.
        """
        rsi = self.data_feed.get_rsi(symbol, period=self.rsi_period, interval="1min")
        macd, signal, hist = self.data_feed.get_macd(symbol, interval="1min")

        if rsi is None or macd is None:
            return {"action": "HOLD", "symbol": symbol}

        if rsi > self.overbought and macd < signal:
            return {"action": "SELL", "symbol": symbol}
        elif rsi < self.oversold and macd > signal:
            return {"action": "BUY", "symbol": symbol}
        else:
            return {"action": "HOLD", "symbol": symbol}
