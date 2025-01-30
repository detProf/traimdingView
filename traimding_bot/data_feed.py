
import logging
import json
import time
import pandas as pd
import requests
import pymongo
import redis
from alpha_vantage.timeseries import TimeSeries
from config import load_config

# Configure logging
logging.basicConfig(
    filename="data_feed.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class DataFeed:
    def __init__(self, mode="live"):
        self.config = load_config()
        self.api_key = self.config["alpha_vantage_api_key"]
        self.symbol = self.config["symbol"]
        self.interval = self.config["interval"]
        self.mode = mode
        self.ts = TimeSeries(key=self.api_key, output_format="pandas")

        # MongoDB Connection
        self.mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.db = self.mongo_client["trading_data"]
        self.market_data_collection = self.db["market_data"]

        # Redis Connection
        self.redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

        self.last_data = None  # Cache previous data to prevent excessive API calls

        if self.mode == "backtest":
            self.historical_data = pd.read_csv(self.config["historical_data_path"], index_col="date", parse_dates=True)
            self.historical_index = 0

    def log(self, message):
        """Log messages for debugging and tracking."""
        logging.info(message)
        print(message)

    def fetch_historical_data_from_api(self, symbol, save_path):
        """Fetch historical data from an external API and save it to MongoDB and Redis."""
        self.log(f"Fetching historical data for {symbol}...")

        try:
            data, _ = self.ts.get_daily(symbol=symbol, outputsize="full")
            data.reset_index(inplace=True)

            # Save data locally
            data.to_csv(save_path)
            self.log(f"Historical data saved to {save_path}")

            # Store in MongoDB
            self.market_data_collection.insert_many(data.to_dict("records"))

            # Cache in Redis
            self.redis_client.set(f"market_data:{symbol}", json.dumps(data.to_dict("records")))

        except Exception as e:
            logging.error(f"Error fetching historical data for {symbol}: {e}")

    def get_latest_data(self):
        """Fetch latest market data based on mode (live or backtest)."""
        try:
            if self.mode == "backtest":
                if self.historical_index < len(self.historical_data):
                    row = self.historical_data.iloc[self.historical_index]
                    self.historical_index += 1
                    return pd.DataFrame([row])
                else:
                    self.log("End of historical data reached.")
                    return None

            # Check Redis cache
            cached_data = self.redis_client.get(f"market_data:{self.symbol}")
            if cached_data:
                return pd.DataFrame(json.loads(cached_data))

            # Check MongoDB
            latest_data = list(self.market_data_collection.find({"symbol": self.symbol}).sort("date", -1).limit(1))
            if latest_data:
                return pd.DataFrame(latest_data)

            # Fetch live data
            self.log(f"Fetching live market data for {self.symbol}...")
            data, _ = self.ts.get_intraday(symbol=self.symbol, interval=self.interval, outputsize="compact")
            self.last_data = data
            return data

        except Exception as e:
            logging.error(f"Error fetching market data: {e}", exc_info=True)
            return self.last_data  # Return cached data if API call fails
