
import logging
from config import load_config

# Configure logging
logging.basicConfig(
    filename="trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class RiskManager:
    def __init__(self):
        self.config = load_config()
        self.max_risk_per_trade = self.config.get("max_risk_per_trade", 0.02)  # 2% risk per trade
        self.stop_loss_percentage = self.config.get("stop_loss_percentage", 0.01)  # 1% stop loss
        self.take_profit_percentage = self.config.get("take_profit_percentage", 0.03)  # 3% take profit

    def log(self, message):
        """
        Log messages for debugging and tracking.
        """
        logging.info(message)
        print(message)

    def calculate_position_size(self, account_balance, trade_price):
        """
        Determines the number of shares to trade based on account balance and risk percentage.
        """
        risk_amount = account_balance * self.max_risk_per_trade
        position_size = risk_amount / trade_price
        position_size = max(1, int(position_size))  # Ensure at least 1 unit is traded
        self.log(f"Calculated position size: {position_size} units")
        return position_size

    def apply_risk_controls(self, entry_price):
        """
        Returns stop-loss and take-profit prices based on predefined risk percentages.
        """
        stop_loss = entry_price * (1 - self.stop_loss_percentage)
        take_profit = entry_price * (1 + self.take_profit_percentage)
        self.log(f"Stop-loss set at {stop_loss:.2f}, Take-profit at {take_profit:.2f}")
        return stop_loss, take_profit
    
    def verify_liquidity(self, symbol, order_size):
        """Check if there is enough market liquidity for the trade."""
        order_book = self.broker.get_order_book(symbol)  # Fetch real-time order book
        best_bid = order_book["bids"][0]  # Best available buy price
        best_ask = order_book["asks"][0]  # Best available sell price

        if order_size > best_ask["size"]:
            return False  # Not enough liquidity for a market buy
        if order_size > best_bid["size"]:
            return False  # Not enough liquidity for a market sell

        return True
