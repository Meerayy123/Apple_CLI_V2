import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import { getPortfolio } from "../api/portfolios.js";
import HoldingsTable from "../components/HoldingsTable.jsx";
import TransactionsTable from "../components/TransactionsTable.jsx";
import BuyForm from "../components/BuyForm.jsx";
import SellForm from "../components/SellForm.jsx";
import ErrorBanner from "../components/ErrorBanner.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";

export default function PortfolioDetailPage() {
  const { id } = useParams();
  const auth = useAuth();
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    (async () => {
      try {
        setLoading(true);
        setError(null);
        const data = await getPortfolio(auth.user?.id_token, id);
        setPortfolio(data);
      } catch (err) {
        setError(err.message);
        if (err.status === 401) auth.signinRedirect();
      } finally {
        setLoading(false);
      }
    })();
  }, [id]);

  const handleTradeComplete = () => {
    setRefreshKey((k) => k + 1);
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="container">
      <Link to="/portfolios">← Back to portfolios</Link>
      <ErrorBanner message={error} />
      {portfolio && (
        <>
          <h1>{portfolio.name}</h1>
          <p style={{ color: "#666" }}>{portfolio.description}</p>

          <HoldingsTable portfolioId={id} refreshKey={refreshKey} />

          <h2>Place a trade</h2>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem", marginBottom: "2rem" }}>
            <BuyForm portfolioId={parseInt(id, 10)} onTradeComplete={handleTradeComplete} />
            <SellForm portfolioId={parseInt(id, 10)} onTradeComplete={handleTradeComplete} />
          </div>

          <TransactionsTable portfolioId={id} refreshKey={refreshKey} />
        </>
      )}
    </div>
  );
}
