# plugins/notification_plugin.py

import logging
from typing import Optional
from core.interfaces import IPlugin
from core.models import Trade, OrderType

class NotificationPlugin(IPlugin):
    """
    A plugin that sends notifications when certain events occur, such as trade executions.
    Here, we provide a simple skeleton that logs and simulates sending a notification.
    In a real scenario, you might integrate email, Slack, or another service.
    """

    def __init__(self, notification_method: Optional[str] = "email"):
        self.notification_method = notification_method

    def on_app_start(self) -> None:
        logging.info("NotificationPlugin: Application is starting up.")
        # Potentially send a "system online" notification.

    def on_app_stop(self) -> None:
        logging.info("NotificationPlugin: Application is stopping.")
        # Potentially send a "system offline" notification.

    def on_data_fetched(self, data) -> None:
        # You could send or log data-related notifications here.
        pass

    def on_signal_generated(self, order_type: OrderType, data=None) -> None:
        # Notify about the signal if desired.
        pass

    def on_order_validated(self, trade: Trade, is_valid: bool) -> None:
        # Notify about validation outcome if desired.
        pass

    def on_trade_executed(self, trade: Trade) -> None:
        """
        Called whenever a trade is executed. For now, just logs a notification.
        In a real implementation, this might send an email, text, or Slack message.
        """
        logging.info(f"NotificationPlugin: Trade executed ({self.notification_method} notification) -> {trade}")
