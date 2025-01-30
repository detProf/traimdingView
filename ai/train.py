
import os
import logging
import torch
import numpy as np
import pandas as pd
from ai.agent import TradingAgent
from ai.methods import DQN, PPO, SAC
from ai.ops import process_data
from data_feed import DataFeed
from config import load_config

# Configure logging
logging.basicConfig(
    filename="ai_training.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class AITrainer:
    def __init__(self, model_type="DQN"):
        self.config = load_config()
        self.data_feed = DataFeed(mode="backtest")
        self.model_type = model_type
        self.model = self._initialize_model(model_type)
        self.agent = TradingAgent(self.model)
        self.memory = []

        # Ensure historical data is available
        if not os.path.exists(self.config["historical_data_path"]):
            raise FileNotFoundError(f"Historical data file not found: {self.config['historical_data_path']}")

    def _initialize_model(self, model_type):
        """Initialize AI model based on selected training type."""
        if model_type == "DQN":
            return DQN()
        elif model_type == "PPO":
            return PPO()
        elif model_type == "SAC":
            return SAC()
        else:
            raise ValueError("Invalid model type. Choose from DQN, PPO, SAC.")

    def fetch_missing_data(self):
        """Automatically fetch missing historical data from an API."""
        from data_feed import fetch_historical_data_from_api  # Ensure this function exists

        logging.info("Fetching missing historical data...")
        fetch_historical_data_from_api(self.config["symbol"], self.config["historical_data_path"])
        logging.info(f"Data saved to {self.config['historical_data_path']}")

    def train(self, epochs=1000):
        """Train AI trading agent using historical market data."""
        logging.info(f"Starting {self.model_type} training for {epochs} epochs...")

        for epoch in range(epochs):
            market_data = self.data_feed.get_latest_data()
            if market_data is None:
                logging.warning("No historical data available! Attempting to fetch data...")
                self.fetch_missing_data()
                continue  # Retry after fetching data

            state = process_data(market_data)
            action = self.agent.predict_action(torch.tensor(state, dtype=torch.float32))
            reward = self._calculate_profit_reward(action, market_data)

            self.memory.append((state, action, reward))
            self.agent.train_step(self.memory)

            if epoch % 100 == 0:
                logging.info(f"Epoch {epoch}/{epochs} - Last Trade Reward: {reward}")

        self.agent.save_model(f"ai/models/model_{self.model_type}.pth")
        logging.info(f"{self.model_type} training complete. Model saved.")

if __name__ == "__main__":
    trainer = AITrainer(model_type="DQN")
    trainer.train(epochs=2000)
