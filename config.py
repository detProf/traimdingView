
import json
import os

CONFIG_FILE = "config.json"

def load_config():
    """Load configuration from a JSON file to allow frontend updates."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    else:
        default_config = {
            "stocks": [],
            "default_stocks": ["AAPL", "TSLA", "AMZN", "MSFT", "SPY"],
            "interval": "5min",
            "data_directory": "data/",
            "use_live_trading": False,
            "binance_api_key": "your_binance_api_key",
            "binance_api_secret": "your_binance_api_secret",
            "alpha_vantage_api_key": "your_alpha_vantage_api_key",
        }
        with open(CONFIG_FILE, "w") as file:
            json.dump(default_config, file, indent=4)
        return default_config

def save_config(config):
    """Save configuration changes to JSON file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)

config = load_config()
