# main.py

import logging
from datetime import datetime

from config.config_loader import load_config
from brokers.paper_broker import PaperBroker
from brokers.real_broker import RealBroker
from strategies.classical_strategy import ClassicalStrategy
from strategies.ml_strategy import MLStrategy
from strategies.multi_action_strategy import MultiActionStrategy
from risk_management.basic_risk_manager import BasicRiskManager
from data.ingestion import fetch_data
from core.models import Trade

def main():
    # 1. Load config
    config = load_config()
    
    # 2. Pick broker based on config
    broker_type = config.get("broker", "paper")
    if broker_type == "paper":
        broker = PaperBroker()
    else:
        broker = RealBroker()

    # 3. Pick strategy based on config
    strategy_type = config.get("strategy", "classical_strategy")
    if strategy_type == "classical_strategy":
        strategy = ClassicalStrategy()
    elif strategy_type == "ml_strategy":
        strategy = MLStrategy(config)
    elif strategy_type == "multi_action_strategy":
        strategy = MultiActionStrategy(config)
    else:
        raise ValueError(f"Unknown strategy: {strategy_type}")

    # 4. Create instance of BasicRiskManager
    risk_manager = BasicRiskManager(config)

    # 5. Simple trading logic:
    #    - Fetch data
    #    - Generate signal
    #    - Create Trade object
    #    - Risk check
    #    - Place order if valid
    
    # Example: pick the first symbol from config
    symbols = config.get("symbols", ["AAPL"])
    if not symbols:
        raise ValueError("No symbols configured.")
    symbol = symbols[0]

    # Fetch some historical data (mock or real)
    df = fetch_data(symbol, "2023-01-01", "2023-01-10")

    # Generate a trading signal
    order_type = strategy.generate_signal(df)

    # Use the last close as the price for demonstration
    last_close = df.iloc[-1]["Close"]

    # Create a trade object (mock quantity)
    trade = Trade(
        symbol=symbol,
        order_type=order_type,
        quantity=10,
        price=float(last_close),
        timestamp=datetime.now()
    )

    # Validate the trade
    if risk_manager.validate_order(trade):
        # If valid, place the order
        broker.place_order(symbol, order_type, trade.quantity)
        logging.info(f"Order placed: {trade}")
    else:
        logging.warning("Trade not placed due to risk constraints.")

if __name__ == "__main__":
    main()
