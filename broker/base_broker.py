
from abc import ABC, abstractmethod

class BaseBroker(ABC):
    @abstractmethod
    def place_order(self, symbol, quantity, order_type):
        pass

    @abstractmethod
    def get_account_info(self):
        pass
