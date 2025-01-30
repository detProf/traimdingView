
import json
import os
import logging
import asyncio
import threading
import websockets
from flask import Flask, request, jsonify
from config import load_config, save_config
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

app = Flask(__name__)
config = load_config()
data_feed = DataFeed()
broker = RealBroker() if config["use_live_trading"] else PaperBroker()
risk_manager = RiskManager()
rule_strategy = RSIStrategy()
ai_strategy = AIStrategy()
logger = LoggingPlugin()
clients = set()

@app.route("/update-config", methods=["POST"])
def update_config():
    """Endpoint to update config settings dynamically."""
    global config
    data = request.json
    if "use_live_trading" in data:
        config["use_live_trading"] = data["use_live_trading"]
        save_config(config)
        return jsonify({"success": True, "message": "Config updated successfully"}), 200
    return jsonify({"error": "Invalid request"}), 400

async def send_updates():
    """Sends real-time updates to WebSocket clients."""
    while True:
        account_info = broker.get_account_info()
        message = json.dumps({"type": "update", "data": account_info})
        
        if clients:
            await asyncio.wait([client.send(message) for client in clients])
        
        await asyncio.sleep(2)

async def handle_client(websocket, path):
    """Handles WebSocket connections."""
    clients.add(websocket)
    try:
        async for _ in websocket:
            pass
    finally:
        clients.remove(websocket)

def run_websocket():
    """Run WebSocket server."""
    asyncio.set_event_loop(asyncio.new_event_loop())
    server = websockets.serve(handle_client, "0.0.0.0", 6789)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

threading.Thread(target=run_websocket, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
