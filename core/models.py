from enum import Enum
from dataclasses import dataclass
from datetime import datetime

class OrderType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    BUY_CALL = "BUY_CALL"
    BUY_PUT = "BUY_PUT"
    SELL_CALL = "SELL_CALL"
    SELL_PUT = "SELL_PUT"
    HOLD = "HOLD"

@dataclass
class Trade:
    symbol: str
    order_type: OrderType
    quantity: float
    price: float
    timestamp: datetime

@dataclass
class Position:
    symbol: str
    quantity: float
    avg_price: float

@dataclass
class MarketData:
    symbol: str
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: float
    timestamp: datetime
