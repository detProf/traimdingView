
import React, { useState, useEffect } from "react";

function App() {
  const [accountInfo, setAccountInfo] = useState(null);
  const [useLiveTrading, setUseLiveTrading] = useState(false);

  useEffect(() => {
    const ws = new WebSocket("ws://localhost:6789");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === "update") {
        setAccountInfo(data.data);
      }
    };

    return () => ws.close();
  }, []);

  // Update config.json to reflect live trading selection
  const toggleLiveTrading = async () => {
    const newMode = !useLiveTrading;
    setUseLiveTrading(newMode);

    const response = await fetch("/update-config", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ use_live_trading: newMode }),
    });

    if (response.ok) {
      alert(`Trading mode updated to: ${newMode ? "Live" : "Paper"}`);
    } else {
      alert("Failed to update trading mode.");
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1>Traimding View - AI Trading Dashboard</h1>
      <button onClick={toggleLiveTrading}>
        Switch to {useLiveTrading ? "Paper Trading" : "Live Trading"}
      </button>
      {accountInfo ? (
        <div>
          <h2>Account Balance: ${accountInfo.balance.toFixed(2)}</h2>
          <h3>Trade History:</h3>
          <ul>
            {accountInfo.trades.map((trade, index) => (
              <li key={index}>
                {trade.date}: {trade.action.toUpperCase()} at ${trade.price}
              </li>
            ))}
          </ul>
        </div>
      ) : (
        <p>Loading account info...</p>
      )}
    </div>
  );
}

export default App;
