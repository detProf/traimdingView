
import logging
import pandas as pd
from data_feed import DataFeed
from broker.paper_broker import PaperBroker
from strategies.rsi_strategy import RSIStrategy
from plugins.ai_plugin import AIPlugin
from risk_manager.risk_manager import RiskManager

# Configure logging
logging.basicConfig(
    filename="traimding_view.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class Backtester:
    def __init__(self, strategy_type="rule"):
        self.data_feed = DataFeed(mode="backtest")
        self.broker = PaperBroker()
        self.risk_manager = RiskManager()
        self.strategy = RSIStrategy() if strategy_type == "rule" else AIPlugin()
        self.trades = []

    def log(self, message):
        """Log messages for debugging and tracking."""
        logging.info(message)
        print(message)

    def run_backtest(self):
        """Runs the strategy on historical data and simulates trade execution."""
        self.log(f"Starting backtest using {'AI' if isinstance(self.strategy, AIPlugin) else 'Rule-based'} strategy...")

        while True:
            market_data = self.data_feed.get_latest_data()
            if market_data is None:
                break

            signal = self.strategy.generate_signal(market_data)
            if signal:
                position_size = self.risk_manager.calculate_position_size(self.broker.balance, signal["price"])
                self.broker.place_order(signal["action"], position_size)
                self.trades.append({
                    "date": market_data.index[-1],
                    "action": signal["action"],
                    "price": signal["price"]
                })

        self.log(f"Backtest complete. Final balance: {self.broker.get_account_info()['balance']}")

    def get_trade_log(self):
        """Returns the trade history from the backtest."""
        return pd.DataFrame(self.trades)

# Example Usage
if __name__ == "__main__":
    strategy_type = "ai"  # Change to "rule" for RSI-based backtesting
    backtester = Backtester(strategy_type=strategy_type)
    backtester.run_backtest()
    trade_log = backtester.get_trade_log()
    trade_log.to_csv(f"backtest_results_{strategy_type}.csv")
    print(f"Backtest complete. Results saved to 'backtest_results_{strategy_type}.csv'.")
