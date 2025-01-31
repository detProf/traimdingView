# brokers/paper_broker.py

from datetime import datetime
from typing import List, Dict

from core.interfaces import IBroker
from core.models import Trade, OrderType, Position

class PaperBroker(IBroker):
    """
    A paper trading broker that simulates trades in memory.
    """

    def __init__(self, starting_balance: float = 100000.0):
        self.balance = starting_balance
        self.trades: List[Trade] = []
        # positions dict keyed by symbol, value is a Position object
        self.positions: Dict[str, Position] = {}

    def place_order(self, symbol: str, order_type: OrderType, quantity: float) -> None:
        """
        Simulates placing an order by recording a Trade and updating positions.
        For simplicity, assumes price is a mock or not tracked dynamically.
        """
        # For a paper broker, we might simulate a fill price or assume a certain price.
        # Here, we'll just mock the price as 100.0 for illustration.
        mock_price = 100.0
        
        trade = Trade(
            symbol=symbol,
            order_type=order_type,
            quantity=quantity,
            price=mock_price,
            timestamp=datetime.now()
        )
        self.trades.append(trade)

        # Update the position
        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol=symbol, quantity=0.0, avg_price=0.0)

        position = self.positions[symbol]

        if order_type in (OrderType.BUY, OrderType.BUY_CALL, OrderType.BUY_PUT):
            # Increase position
            new_quantity = position.quantity + quantity
            # Recalculate avg price (weighted)
            if position.quantity == 0:
                new_avg_price = mock_price
            else:
                new_avg_price = (
                    (position.quantity * position.avg_price) + (quantity * mock_price)
                ) / new_quantity

            position.quantity = new_quantity
            position.avg_price = new_avg_price

        elif order_type in (OrderType.SELL, OrderType.SELL_CALL, OrderType.SELL_PUT):
            # Decrease position
            new_quantity = position.quantity - quantity
            if new_quantity < 0:
                raise ValueError("Cannot sell more than current position quantity.")
            position.quantity = new_quantity
            # If we close out the position, reset avg_price
            if position.quantity == 0:
                position.avg_price = 0.0

        # Note: For a more complete paper trading simulation, we would
        # also update self.balance based on the cost or proceeds of the trade.

    def get_positions(self) -> List[Position]:
        """
        Returns the current open positions.
        """
        return list(self.positions.values())

    def get_balance(self) -> float:
        """
        Returns the current cash balance (mock).
        In a more advanced simulation, this might include
        unrealized PnL, or we could calculate it directly.
        """
        return self.balance
