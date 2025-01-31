# risk_management/basic_risk_manager.py

from core.interfaces import IRiskManager
from core.models import Trade

class BasicRiskManager(IRiskManager):
    """
    A simple risk manager that checks if an order exceeds
    configured position size limits or other basic constraints.
    """

    def __init__(self, config: dict):
        risk_config = config.get("risk", {})
        self.max_position_size = risk_config.get("max_position_size", 100)
        self.stop_loss_percent = risk_config.get("stop_loss_percent", 0.02)

    def validate_order(self, trade: Trade) -> bool:
        """
        Validates the trade against basic risk constraints such as
        maximum position size. Additional checks can be added as needed.
        """
        if trade.quantity > self.max_position_size:
            print(f"RiskManager: Trade quantity {trade.quantity} exceeds max position size {self.max_position_size}.")
            return False

        # Other checks (e.g., price constraints, stop-loss triggers, etc.) can go here.

        return True
