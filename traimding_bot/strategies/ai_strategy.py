
import logging
import numpy as np
import torch
from ai.agent import TradingAgent
from ai.live_train import LiveTrainer
from risk_manager.risk_manager import RiskManager

# Configure logging
logging.basicConfig(
    filename="traimding_view.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class AIStrategy:
    def __init__(self, model_path="ai/models/model_dqn_live.pth"):
        self.agent = TradingAgent(model_path=model_path)
        self.live_trainer = LiveTrainer()
        self.risk_manager = RiskManager()

    def log(self, message):
        """Log AI trading decisions."""
        logging.info(message)
        print(message)

    def generate_signal(self, market_data):
        """
        Uses the AI agent to generate a buy/sell/hold signal.
        Filters out low-confidence decisions.
        """
        try:
            state = np.array(market_data["close"].values).reshape(1, -1)
            action = self.agent.predict_action(torch.tensor(state, dtype=torch.float32))

            # Get risk-controlled position size
            trade_price = market_data["close"].iloc[-1]
            position_size = self.risk_manager.calculate_position_size(trade_price)

            if action == 1:  # Buy
                self.log(f"AI Decision: BUY at {trade_price} | Position Size: {position_size}")
                self.live_trainer.update_model(market_data, 1)
                return {"action": "buy", "price": trade_price, "position_size": position_size}

            elif action == 0:  # Sell
                self.log(f"AI Decision: SELL at {trade_price} | Position Size: {position_size}")
                self.live_trainer.update_model(market_data, 0)
                return {"action": "sell", "price": trade_price, "position_size": position_size}

            else:  # Hold
                self.log("AI Decision: HOLD")
                return None

        except Exception as e:
            logging.error(f"AI strategy error: {e}", exc_info=True)
            return None
