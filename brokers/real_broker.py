# brokers/real_broker.py

from typing import List

from core.interfaces import IBroker
from core.models import OrderType, Position

class RealBroker(IBroker):
    """
    A skeleton for a live broker implementation, e.g. Alpaca, Interactive Brokers, etc.
    Currently, methods are stubs or raise NotImplementedError.
    """

    def place_order(self, symbol: str, order_type: OrderType, quantity: float) -> None:
        # Here you'd integrate with a real brokerage API to place the order.
        raise NotImplementedError("Live order placement not implemented yet.")

    def get_positions(self) -> List[Position]:
        # Here you'd fetch positions from the brokerage API.
        raise NotImplementedError("Fetching live positions not implemented yet.")

    def get_balance(self) -> float:
        # Here you'd fetch the current account balance from the brokerage API.
        raise NotImplementedError("Fetching live balance not implemented yet.")
