from abc import ABC, abstractmethod
from typing import List, Union, Optional

from core.models import OrderType, Trade, Position

class IBroker(ABC):
    @abstractmethod
    def place_order(self, symbol: str, order_type: OrderType, quantity: float) -> None:
        pass

    @abstractmethod
    def get_positions(self) -> List[Position]:
        pass

    @abstractmethod
    def get_balance(self) -> float:
        pass


class IStrategy(ABC):
    @abstractmethod
    def generate_signal(self, data) -> OrderType:
        pass


class IIndicator(ABC):
    @abstractmethod
    def calculate(self, data) -> Union[float, dict]:
        pass


class IRiskManager(ABC):
    @abstractmethod
    def validate_order(self, trade: Trade) -> bool:
        pass


class IPlugin(ABC):
    """
    A generic plugin interface that allows new plugins to hook into
    different parts of the application lifecycle or event flow.
    Subclasses can override only the methods they need.
    """

    def on_app_start(self) -> None:
        """
        Called when the application is starting up.
        """
        pass

    def on_app_stop(self) -> None:
        """
        Called when the application is stopping.
        """
        pass

    def on_data_fetched(self, data) -> None:
        """
        Called immediately after data is fetched (historical or real-time),
        before the strategy logic is applied.
        """
        pass

    def on_signal_generated(self, order_type: OrderType, data=None) -> None:
        """
        Called after a strategy generates a trading signal.
        """
        pass

    def on_order_validated(self, trade: Trade, is_valid: bool) -> None:
        """
        Called after the risk manager validates (or invalidates) an order.
        """
        pass

    def on_trade_executed(self, trade: Trade) -> None:
        """
        Called whenever a trade is executed.
        """
        pass
