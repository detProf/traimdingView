# strategies/classical_strategy.py

from core.interfaces import IStrategy
from core.models import OrderType
from indicators.rsi import RsiIndicator

class ClassicalStrategy(IStrategy):
    def __init__(self, period=14):
        self.rsi_indicator = RsiIndicator(period=period)

    def generate_signal(self, data) -> OrderType:
        """
        Uses a classical RSI-based strategy:
          - If RSI < 30, return BUY
          - If RSI > 70, return SELL
          - Otherwise, HOLD
        """
        rsi_value = self.rsi_indicator.calculate(data)

        if rsi_value < 30:
            return OrderType.BUY
        elif rsi_value > 70:
            return OrderType.SELL
        else:
            return OrderType.HOLD
