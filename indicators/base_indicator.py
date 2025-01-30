
from abc import ABC, abstractmethod

class BaseIndicator(ABC):
    @abstractmethod
    def compute(self, prices):
        pass
