
import logging
import torch
import numpy as np
from ai.methods import DQN, DoubleDQN, TDQN

# Configure logging
logging.basicConfig(
    filename="ai_decision_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class TradingAgent:
    def __init__(self, model_type="DQN", model_path=None):
        """Initialize AI trading agent with a selected model type."""
        self.model_type = model_type
        self.model = self._load_model(model_type, model_path)

    def _load_model(self, model_type, model_path):
        """Loads the appropriate AI model."""
        if model_type == "DQN":
            model = DQN()
        elif model_type == "DoubleDQN":
            model = DoubleDQN()
        elif model_type == "TDQN":
            model = TDQN()
        else:
            raise ValueError("Invalid model type. Choose from DQN, DoubleDQN, TDQN.")

        if model_path:
            model.load_state_dict(torch.load(model_path))
        return model

    def predict_action(self, state):
        """Predicts trade action using the trained AI model."""
        state_tensor = torch.tensor(state, dtype=torch.float32)
        action_probabilities = self.model(state_tensor)

        # Select action with highest probability
        action = torch.argmax(action_probabilities).item()
        confidence = torch.max(action_probabilities).item()

        self._log_decision(action, confidence)
        return action

    def _log_decision(self, action, confidence):
        """Logs AI trade decisions for debugging."""
        decision_map = {0: "SELL", 1: "BUY", 2: "HOLD"}
        logging.info(f"AI Decision: {decision_map[action]} | Confidence: {confidence:.2f}")

    def save_model(self, path):
        """Saves the trained AI model."""
        torch.save(self.model.state_dict(), path)
