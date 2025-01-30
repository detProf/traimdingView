
from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def run(self, *args, **kwargs):
        pass
