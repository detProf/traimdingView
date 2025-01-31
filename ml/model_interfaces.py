# ml/model_interfaces.py

from abc import ABC, abstractmethod
from typing import Any

class IMLModel(ABC):
    @abstractmethod
    def predict_action(self, features: Any) -> str:
        """
        Predicts and returns an action based on the provided features.
        """
        pass

class IMLTrainer(ABC):
    @abstractmethod
    def train(self, data: Any) -> None:
        """
        Trains the model on the given data.
        """
        pass

    @abstractmethod
    def evaluate(self, data: Any) -> float:
        """
        Evaluates the model on the given data and returns a performance metric.
        """
        pass
