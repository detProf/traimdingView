
import logging
import torch
import numpy as np
from ai.agent import TradingAgent
from ai.methods import DQN
from ai.ops import process_data
from data_feed import DataFeed
from config import load_config

# Configure logging
logging.basicConfig(
    filename="live_training.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class LiveTrainer:
    def __init__(self):
        self.config = load_config()
        self.data_feed = DataFeed(mode="live")
        self.agent = TradingAgent(DQN())
        self.memory = []

    def log(self, message):
        logging.info(message)
        print(message)

    def update_model(self, market_data, action):
        """Retrain AI model in real-time with new market data."""
        state = process_data(market_data)
        reward = self._calculate_profit_reward(action, market_data)

        # Store experience and retrain
        self.memory.append((state, action, reward))
        self.agent.train_step(self.memory)

        # Save model after every 100 updates
        if len(self.memory) % 100 == 0:
            self.agent.save_model("ai/models/model_dqn_live.pth")
            self.log("Live model updated & saved.")

    def _calculate_profit_reward(self, action, market_data):
        """Real-time reward function for maximizing P&L."""
        entry_price = market_data["close"].iloc[-2]
        exit_price = market_data["close"].iloc[-1]
        position_size = 1

        profit_loss = (exit_price - entry_price) * position_size

        if action == 1:  # Buy
            reward = profit_loss if profit_loss > 0 else profit_loss * 0.5
        elif action == 0:  # Sell
            reward = -profit_loss if profit_loss < 0 else -profit_loss * 0.5
        else:  # Hold
            reward = profit_loss * 0.1

        return reward
