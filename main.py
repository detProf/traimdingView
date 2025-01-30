
import time
import json
import logging
import asyncio
import threading
import websockets
import redis
import pymongo
import pika
from config import load_config
from data_feed import DataFeed
from broker.paper_broker import PaperBroker
from broker.real_broker import RealBroker
from risk_manager.risk_manager import RiskManager
from strategies.rsi_strategy import RSIStrategy
from strategies.ai_strategy import AIStrategy
from plugins.logging_plugin import LoggingPlugin

# Configure logging
logging.basicConfig(
    filename="traimding_view.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class TraimdingViewBot:
    def __init__(self):
        self.config = load_config()
        self.data_feed = DataFeed()
        self.broker = RealBroker() if self.config["use_live_trading"] else PaperBroker()
        self.risk_manager = RiskManager()
        self.rule_strategy = RSIStrategy()
        self.ai_strategy = AIStrategy()
        self.logger = LoggingPlugin()
        self.running = False
        self.clients = set()

        # MongoDB Connection
        self.mongo_client = pymongo.MongoClient("mongodb://mongodb:27017/")
        self.db = self.mongo_client["trading_data"]
        self.trade_collection = self.db["trade_history"]

        # Redis Connection
        self.redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

        # RabbitMQ Connection with Retry Logic
        self.rabbit_connection = self.connect_to_rabbitmq()
        self.channel = self.rabbit_connection.channel()
        self.channel.queue_declare(queue="trade_orders")

    def connect_to_rabbitmq(self, max_retries=5, delay=5):
        """Attempts to establish a connection to RabbitMQ with retries."""
        for attempt in range(max_retries):
            try:
                return pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
            except Exception as e:
                self.log(f"RabbitMQ connection failed (attempt {attempt+1}/{max_retries}): {e}")
                time.sleep(delay)
        raise Exception("Failed to connect to RabbitMQ after multiple attempts.")

    def log(self, message):
        """Log messages for debugging and tracking."""
        logging.info(message)
        print(message)

    async def broadcast_update(self):
        """Send real-time trade updates to WebSocket clients."""
        account_info = self.broker.get_account_info()
        message = json.dumps({"type": "update", "data": account_info})

        if self.clients:
            await asyncio.wait([client.send(message) for client in self.clients])

    async def handle_client(self, websocket, path):
        """Manage WebSocket clients."""
        self.clients.add(websocket)
        try:
            async for _ in websocket:
                pass
        finally:
            self.clients.remove(websocket)

    def run_websocket(self):
        """Run WebSocket server in a separate thread."""
        asyncio.set_event_loop(asyncio.new_event_loop())
        server = websockets.serve(self.handle_client, "0.0.0.0", 6789)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()

    def execute_trade(self, trade_order):
        """Verify liquidity before sending trade order to RabbitMQ and confirm execution."""
        symbol = trade_order["symbol"]
        position_size = trade_order["position_size"]

        # Verify if there's enough liquidity before executing the trade
        if not self.risk_manager.verify_liquidity(symbol, position_size):
            self.log(f"Trade aborted: Not enough liquidity for {symbol} ({position_size} units).")
            return False

        try:
            self.channel.basic_publish(
                exchange="", routing_key="trade_orders", body=json.dumps(trade_order)
            )
            self.log(f"Trade order sent to RabbitMQ: {trade_order}")
            return True
        except Exception as e:
            self.log(f"Trade execution failed: {e}")
            return False

    def run(self):
        """Main loop to fetch data, compute signals, and execute trades."""
        self.running = True
        threading.Thread(target=self.run_websocket, daemon=True).start()
        self.log("Traimding View trading bot started.")

        try:
            while self.running:
                market_data = self.data_feed.get_latest_data()
                if market_data is None:
                    self.log("No market data received, skipping iteration.")
                    time.sleep(self.config["interval"])
                    continue

                rule_signal = self.rule_strategy.generate_signal(market_data)
                ai_signal = self.ai_strategy.generate_signal(market_data)

                # Execute based on selected strategy
                final_signal = ai_signal if self.config["use_ai"] else rule_signal

                if final_signal:
                    position_size = self.risk_manager.calculate_position_size()
                    trade_order = {
                        "action": final_signal["action"],
                        "position_size": position_size,
                        "price": final_signal.get("price", 0)
                    }
                    if self.execute_trade(trade_order):
                        # Log to MongoDB
                        self.trade_collection.insert_one(trade_order)

                    asyncio.run(self.broadcast_update())  # Send WebSocket update

                time.sleep(self.config["interval"])

        except KeyboardInterrupt:
            self.log("Trading bot stopped manually.")
        except Exception as e:
            logging.error(f"Unexpected error: {e}", exc_info=True)
        finally:
            self.stop()

    def stop(self):
        """Stop the bot safely."""
        self.running = False
        self.log("Traimding View trading bot stopped.")

if __name__ == "__main__":
    bot = TraimdingViewBot()
    bot.run()
