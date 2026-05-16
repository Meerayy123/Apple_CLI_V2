import { useState, useEffect } from "react";
import { useAuth } from "react-oidc-context";
import { getHoldings } from "../api/portfolios.js";
import ErrorBanner from "./ErrorBanner.jsx";

export default function HoldingsTable({ portfolioId, refreshKey }) {
  const auth = useAuth();
  const [holdings, setHoldings] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getHoldings(auth.user?.id_token, portfolioId);
        if (!cancelled) setHoldings(data);
      } catch (err) {
        if (!cancelled) setError(err.message);
        if (err.status === 401) auth.signinRedirect();
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => { cancelled = true; };
  }, [portfolioId, refreshKey]);

  if (loading) return <div>Loading holdings…</div>;

  return (
    <div>
      <h2>Holdings</h2>
      <ErrorBanner message={error} />
      {holdings.length === 0 ? (
        <p>This portfolio has no holdings yet.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Quantity</th>
            </tr>
          </thead>
          <tbody>
            {holdings.map((h) => (
              <tr key={h.ticker}>
                <td>{h.ticker}</td>
                <td>{h.quantity}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
