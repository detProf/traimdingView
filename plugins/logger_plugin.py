# plugins/logger_plugin.py

import logging
from core.models import Trade
from core.interfaces import IPlugin

class LoggerPlugin(IPlugin):
    """
    A plugin that implements IPlugin to log trade execution events.
    """

    def on_trade_executed(self, trade: Trade) -> None:
        """
        Called whenever a trade is executed. Logs trade details.
        """
        logging.info(f"Trade executed: {trade}")
