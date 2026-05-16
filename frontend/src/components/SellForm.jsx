import { useState } from "react";
import { useAuth } from "react-oidc-context";
import { sell } from "../api/trades.js";
import ErrorBanner from "./ErrorBanner.jsx";

export default function SellForm({ portfolioId, onTradeComplete }) {
  const auth = useAuth();
  const [ticker, setTicker] = useState("");
  const [quantity, setQuantity] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!ticker.trim()) { setError("Ticker is required"); return; }
    const qty = parseFloat(quantity);
    if (!qty || qty <= 0) { setError("Quantity must be a positive number"); return; }
    try {
      setLoading(true);
      setError(null);
      setSuccess(null);
      await sell(auth.user?.id_token, { portfolio_id: portfolioId, ticker: ticker.toUpperCase(), quantity: qty });
      setSuccess(`Sold ${qty} shares of ${ticker.toUpperCase()}`);
      setTicker("");
      setQuantity("");
      setTimeout(() => setSuccess(null), 3000);
      if (onTradeComplete) onTradeComplete();
    } catch (err) {
      setError(err.message);
      if (err.status === 401) auth.signinRedirect();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: "1px solid #eee", borderRadius: "8px", padding: "1rem" }}>
      <h3 style={{ marginTop: 0 }}>Sell</h3>
      <ErrorBanner message={error} />
      {success && <div className="success">{success}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "0.5rem" }}>
          <label htmlFor="sell-ticker" style={{ display: "block", marginBottom: "0.25rem" }}>Ticker</label>
          <input id="sell-ticker" value={ticker} onChange={(e) => setTicker(e.target.value)} disabled={loading} />
        </div>
        <div style={{ marginBottom: "0.5rem" }}>
          <label htmlFor="sell-qty" style={{ display: "block", marginBottom: "0.25rem" }}>Quantity</label>
          <input id="sell-qty" type="number" min="1" value={quantity} onChange={(e) => setQuantity(e.target.value)} disabled={loading} />
        </div>
        <button type="submit" disabled={loading}>{loading ? "Selling…" : "Sell"}</button>
      </form>
    </div>
  );
}
