
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from main import TradingBot
from config import BOT_CONFIG, config, save_config

class TradingBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Bot UI")

        self.bot = None
        self.running = False

        # UI Layout
        self.create_widgets()
        self.load_config()

    def create_widgets(self):
        # Bot Control Buttons
        self.start_button = ttk.Button(self.root, text="Start Bot", command=self.start_bot)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop Bot", command=self.stop_bot, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        # Settings Section
        self.symbols_label = ttk.Label(self.root, text="Stock Symbols (comma-separated):")
        self.symbols_label.grid(row=1, column=0, padx=10, pady=10)

        self.symbols_entry = ttk.Entry(self.root, width=50)
        self.symbols_entry.grid(row=1, column=1, padx=10, pady=10)

        self.interval_label = ttk.Label(self.root, text="Interval:")
        self.interval_label.grid(row=2, column=0, padx=10, pady=10)

        self.interval_entry = ttk.Entry(self.root)
        self.interval_entry.grid(row=2, column=1, padx=10, pady=10)

        self.position_size_label = ttk.Label(self.root, text="Position Size:")
        self.position_size_label.grid(row=3, column=0, padx=10, pady=10)

        self.position_size_entry = ttk.Entry(self.root)
        self.position_size_entry.grid(row=3, column=1, padx=10, pady=10)

        self.strategy_label = ttk.Label(self.root, text="Trading Strategy:")
        self.strategy_label.grid(row=4, column=0, padx=10, pady=10)

        self.strategy_var = tk.StringVar()
        self.strategy_menu = ttk.Combobox(self.root, textvariable=self.strategy_var, values=["SampleStrategy", "MultiIndicatorStrategy"])
        self.strategy_menu.grid(row=4, column=1, padx=10, pady=10)

        # Account Info Section
        self.account_label = ttk.Label(self.root, text="Account Balance:")
        self.account_label.grid(row=5, column=0, padx=10, pady=10)

        self.balance_var = tk.StringVar(value="Loading...")
        self.balance_label = ttk.Label(self.root, textvariable=self.balance_var)
        self.balance_label.grid(row=5, column=1, padx=10, pady=10)

        # Positions Section
        self.positions_label = ttk.Label(self.root, text="Open Positions:")
        self.positions_label.grid(row=6, column=0, padx=10, pady=10)

        self.positions_text = tk.Text(self.root, height=5, width=50)
        self.positions_text.grid(row=6, column=1, padx=10, pady=10)

        # Manual Trade Section
        self.trade_label = ttk.Label(self.root, text="Manual Trade:")
        self.trade_label.grid(row=7, column=0, padx=10, pady=10)

        self.symbol_entry = ttk.Entry(self.root)
        self.symbol_entry.grid(row=7, column=1, padx=10, pady=10)

        self.trade_type_var = tk.StringVar(value="BUY")
        self.trade_type_menu = ttk.Combobox(self.root, textvariable=self.trade_type_var, values=["BUY", "SELL"])
        self.trade_type_menu.grid(row=8, column=1, padx=10, pady=10)

        self.quantity_entry = ttk.Entry(self.root)
        self.quantity_entry.grid(row=9, column=1, padx=10, pady=10)

        self.trade_button = ttk.Button(self.root, text="Execute Trade", command=self.execute_trade)
        self.trade_button.grid(row=10, column=1, padx=10, pady=10)

        # Logs Section
        self.logs_label = ttk.Label(self.root, text="Logs:")
        self.logs_label.grid(row=11, column=0, padx=10, pady=10)

        self.logs_text = tk.Text(self.root, height=10, width=70)
        self.logs_text.grid(row=11, column=1, padx=10, pady=10)

    def load_config(self):
        """Load the config values into the UI fields."""
        self.symbols_entry.insert(0, ",".join(BOT_CONFIG["symbols"]))
        self.interval_entry.insert(0, BOT_CONFIG["interval"])
        self.position_size_entry.insert(0, str(BOT_CONFIG["position_size"]))
        self.strategy_var.set(BOT_CONFIG["strategy"])

    def update_config(self):
        """Update the config file and in-memory BOT_CONFIG."""
        config["settings"]["symbols"] = self.symbols_entry.get()
        config["settings"]["interval"] = self.interval_entry.get()
        config["settings"]["position_size"] = self.position_size_entry.get()
        config["settings"]["strategy"] = self.strategy_var.get()
        save_config(config)

    def start_bot(self):
        if not self.running:
            self.update_config()
            self.running = True
            self.bot = TradingBot(ui_mode=True, log_callback=self.update_logs)
            self.bot_thread = threading.Thread(target=self.bot.run, daemon=True)
            self.bot_thread.start()

            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)

    def stop_bot(self):
        if self.running:
            self.running = False
            self.bot.stop()
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

    def update_logs(self, message):
        self.logs_text.insert(tk.END, message + "\n")
        self.logs_text.yview(tk.END)

    def update_account_info(self):
        if self.bot:
            account_info = self.bot.broker.get_account_info()
            self.balance_var.set(f"${account_info['cash']:.2f}")
            self.positions_text.delete("1.0", tk.END)
            for symbol, quantity in account_info['positions'].items():
                self.positions_text.insert(tk.END, f"{symbol}: {quantity} shares\n")

    def execute_trade(self):
        symbol = self.symbol_entry.get().upper()
        trade_type = self.trade_type_var.get()
        try:
            quantity = int(self.quantity_entry.get())
            if self.bot:
                trade = self.bot.broker.place_order(symbol, quantity, trade_type)
                self.update_logs(f"Manual Trade: {trade}")
                self.update_account_info()
        except ValueError:
            messagebox.showerror("Input Error", "Invalid quantity entered")

if __name__ == "__main__":
    root = tk.Tk()
    app = TradingBotUI(root)
    root.mainloop()
