
from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signal(self, symbol, market_data):
        pass
