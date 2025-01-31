# risk_management/advanced_risk_manager.py

from typing import List
from core.interfaces import IRiskManager
from core.models import Trade, Position, OrderType
from brokers.paper_broker import PaperBroker  # Assuming using PaperBroker for accessing positions
import logging

class AdvancedRiskManager(IRiskManager):
    """
    An advanced risk manager that enforces multiple risk constraints, such as:
    - Maximum position size per symbol
    - Maximum number of open positions
    - Maximum total exposure
    - Stop-loss based on price movements
    - Leverage limits
    """

    def __init__(self, config: dict, broker: PaperBroker):
        """
        Initializes the AdvancedRiskManager with detailed risk parameters.

        :param config: Configuration dictionary containing risk parameters.
        :param broker: An instance of IBroker to access current positions.
        """
        risk_config = config.get("risk", {})
        self.max_position_size = risk_config.get("max_position_size", 100)
        self.stop_loss_percent = risk_config.get("stop_loss_percent", 0.02)
        self.max_open_positions = risk_config.get("max_open_positions", 50)
        self.max_total_exposure = risk_config.get("max_total_exposure", 1000000.0)
        self.leverage = risk_config.get("leverage", 2.0)
        self.broker = broker

    def validate_order(self, trade: Trade) -> bool:
        """
        Validates the trade against multiple risk constraints.

        :param trade: The Trade object to validate.
        :return: True if the trade is valid, False otherwise.
        """
        logging.debug(f"Validating trade: {trade}")

        # 1. Check individual position size
        if trade.quantity > self.max_position_size:
            logging.warning(
                f"Trade quantity {trade.quantity} exceeds max position size {self.max_position_size}."
            )
            return False

        # 2. Check maximum number of open positions
        current_positions: List[Position] = self.broker.get_positions()
        if len(current_positions) >= self.max_open_positions and not self._position_exists(trade.symbol):
            logging.warning(
                f"Number of open positions {len(current_positions)} exceeds max allowed {self.max_open_positions}."
            )
            return False

        # 3. Check total exposure
        total_exposure = self._calculate_total_exposure(current_positions, trade)
        if total_exposure > self.max_total_exposure:
            logging.warning(
                f"Total exposure {total_exposure} exceeds max allowed {self.max_total_exposure}."
            )
            return False

        # 4. Check leverage
        current_balance = self.broker.get_balance()
        if total_exposure > current_balance * self.leverage:
            logging.warning(
                f"Total exposure {total_exposure} exceeds allowed leverage {self.leverage}x of balance {current_balance}."
            )
            return False

        # 5. Check stop-loss (simplified example)
        # Note: In a real scenario, you'd track the entry price and current price to determine stop-loss
        # Here, we'll assume if the trade price drops by stop_loss_percent, it's invalid
        if trade.order_type in {OrderType.BUY, OrderType.BUY_CALL, OrderType.BUY_PUT}:
            potential_price = trade.price * (1 - self.stop_loss_percent)
            if trade.price < potential_price:
                logging.warning(
                    f"Trade price {trade.price} triggers stop-loss at {potential_price}."
                )
                return False

        # Additional risk checks can be implemented here

        logging.info("Trade validated successfully.")
        return True

    def _calculate_total_exposure(self, current_positions: List[Position], trade: Trade) -> float:
        """
        Calculates the total market exposure including the new trade.

        :param current_positions: List of current open positions.
        :param trade: The new Trade to be considered.
        :return: Total exposure as a float.
        """
        exposure = 0.0
        for position in current_positions:
            exposure += position.quantity * position.avg_price

        # Include the new trade's exposure
        if trade.order_type in {OrderType.BUY, OrderType.BUY_CALL, OrderType.BUY_PUT}:
            exposure += trade.quantity * trade.price
        elif trade.order_type in {OrderType.SELL, OrderType.SELL_CALL, OrderType.SELL_PUT}:
            exposure -= trade.quantity * trade.price  # Assuming selling reduces exposure

        logging.debug(f"Calculated total exposure: {exposure}")
        return exposure

    def _position_exists(self, symbol: str) -> bool:
        """
        Checks if a position for the given symbol already exists.

        :param symbol: The trading symbol to check.
        :return: True if position exists, False otherwise.
        """
        current_positions: List[Position] = self.broker.get_positions()
        for position in current_positions:
            if position.symbol == symbol and position.quantity > 0:
                logging.debug(f"Position exists for symbol: {symbol}")
                return True
        logging.debug(f"No existing position for symbol: {symbol}")
        return False
