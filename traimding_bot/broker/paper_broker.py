
import logging
from broker.base_broker import BaseBroker
from config import load_config

# Configure logging
logging.basicConfig(
    filename="trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class PaperBroker(BaseBroker):
    def __init__(self):
        self.config = load_config()
        self.balance = self.config.get("initial_balance", 10000)
        self.positions = {}  # Store open positions
        self.trade_history = []  # Log executed trades

    def log(self, message):
        """Log messages for debugging and tracking."""
        logging.info(message)
        print(message)

    def place_order(self, signal, quantity):
        """Simulate order execution in a paper trading environment."""
        if quantity <= 0:
            self.log("Invalid trade size, order rejected.")
            return

        order_type = "BUY" if signal == "buy" else "SELL"
        self.log(f"Placing {order_type} order for {quantity} units.")

        if order_type == "BUY":
            if self.balance < quantity * self.config["trade_price"]:
                self.log("Insufficient balance, order rejected.")
                return
            self.balance -= quantity * self.config["trade_price"]
            self.positions[self.config["symbol"]] = self.positions.get(self.config["symbol"], 0) + quantity
        else:
            if self.positions.get(self.config["symbol"], 0) < quantity:
                self.log("Insufficient holdings, order rejected.")
                return
            self.balance += quantity * self.config["trade_price"]
            self.positions[self.config["symbol"]] -= quantity

        self.trade_history.append({
            "type": order_type,
            "quantity": quantity,
            "price": self.config["trade_price"]
        })
        self.log(f"Order executed: {order_type} {quantity} units at {self.config['trade_price']}")

    def get_account_info(self):
        """Retrieve simulated account information."""
        return {
            "balance": self.balance,
            "positions": self.positions,
            "trade_history": self.trade_history
        }
