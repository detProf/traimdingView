
import logging
import numpy as np
import torch
from trading_bot.agent import TradingAgent  # AI Agent from the existing bot

# Configure logging
logging.basicConfig(
    filename="traimding_view.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class AIPlugin:
    def __init__(self, model_path="models/model_dqn.pth"):
        self.agent = TradingAgent()
        self.agent.load_model(model_path)

    def log(self, message):
        """Log AI trading decisions."""
        logging.info(message)
        print(message)

    def generate_signal(self, market_data):
        """
        Uses the AI agent to generate a buy/sell/hold signal.
        """
        try:
            state = np.array(market_data["close"].values).reshape(1, -1)
            action = self.agent.predict_action(torch.tensor(state, dtype=torch.float32))
            
            signal = "hold"
            if action == 0:
                signal = "sell"
            elif action == 1:
                signal = "buy"

            self.log(f"AI Decision: {signal} at price {market_data['close'].iloc[-1]}")
            return {"action": signal, "price": market_data["close"].iloc[-1]}

        except Exception as e:
            logging.error(f"AI strategy error: {e}", exc_info=True)
            return None
