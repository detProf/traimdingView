
import logging
import time
import requests
import hmac
import hashlib
import json
from urllib.parse import urlencode
from config import load_config

# Configure logging
logging.basicConfig(
    filename="traimding_view.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class RealBroker:
    BASE_URL = "https://api.binance.com"

    def __init__(self):
        self.config = load_config()
        self.api_key = self.config["binance_api_key"]
        self.api_secret = self.config["binance_api_secret"]

    def log(self, message):
        """Log messages for debugging and tracking."""
        logging.info(message)
        print(message)

    def _sign_request(self, params):
        """Signs the API request using HMAC-SHA256."""
        query_string = urlencode(params)
        signature = hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()
        params["signature"] = signature
        return params

    def _send_request(self, method, endpoint, params=None):
        """Sends a signed request to Binance API."""
        headers = {"X-MBX-APIKEY": self.api_key}
        url = f"{self.BASE_URL}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=params)
            elif method == "POST":
                response = requests.post(url, headers=headers, params=params)

            data = response.json()
            if "code" in data and data["code"] < 0:
                self.log(f"Binance API Error: {data['msg']}")
                return None
            return data

        except requests.RequestException as e:
            logging.error(f"Request error: {e}", exc_info=True)
            return None

    def get_account_balance(self):
        """Fetches account balance from Binance."""
        params = {"timestamp": int(time.time() * 1000)}
        params = self._sign_request(params)
        data = self._send_request("GET", "/api/v3/account", params)

        if data:
            balances = {item["asset"]: float(item["free"]) for item in data["balances"]}
            self.log(f"Account Balance: {balances}")
            return balances
        return None

    def place_order(self, side, quantity, symbol="BTCUSDT", order_type="MARKET"):
        """Places a live trade order on Binance."""
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": order_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }
        params = self._sign_request(params)
        order = self._send_request("POST", "/api/v3/order", params)

        if order:
            self.log(f"Trade Executed: {side} {quantity} {symbol} at {order.get('fills', [{}])[0].get('price', 'Market Price')}")
        return order
