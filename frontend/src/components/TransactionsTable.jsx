import { useState, useEffect } from "react";
import { useAuth } from "react-oidc-context";
import { getTransactions } from "../api/portfolios.js";
import ErrorBanner from "./ErrorBanner.jsx";

export default function TransactionsTable({ portfolioId, refreshKey }) {
  const auth = useAuth();
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getTransactions(auth.user?.id_token, portfolioId);
        if (!cancelled) setTransactions(data);
      } catch (err) {
        if (!cancelled) setError(err.message);
        if (err.status === 401) auth.signinRedirect();
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [portfolioId, refreshKey]);

  if (loading) return <div>Loading transactions…</div>;

  return (
    <div>
      <h2>Transaction History</h2>
      <ErrorBanner message={error} />
      {transactions.length === 0 ? (
        <p>No transactions yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Type</th>
              <th>Ticker</th>
              <th>Quantity</th>
              <th>Price</th>
            </tr>
          </thead>
          <tbody>
            {transactions.map((t) => (
              <tr key={t.transaction_id || `${t.ticker}-${t.timestamp}`}>
                <td>{new Date(t.timestamp || t.date_time).toLocaleString()}</td>
                <td>{t.type || t.transaction_type}</td>
                <td>{t.ticker}</td>
                <td>{t.quantity}</td>
                <td>${parseFloat(t.price).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
