
from plugins.base_plugin import BasePlugin

class SamplePlugin(BasePlugin):
    def run(self, trade_info):
        print(f"Logged trade: {trade_info}")
