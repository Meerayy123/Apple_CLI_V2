import { useState, useEffect } from "react";
import { useAuth } from "react-oidc-context";
import { listMyPortfolios, deletePortfolio } from "../api/portfolios.js";
import PortfolioCard from "../components/PortfolioCard.jsx";
import CreatePortfolioForm from "../components/CreatePortfolioForm.jsx";
import ErrorBanner from "../components/ErrorBanner.jsx";
import LoadingSpinner from "../components/LoadingSpinner.jsx";

export default function PortfoliosListPage() {
  const auth = useAuth();
  const [portfolios, setPortfolios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchPortfolios = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await listMyPortfolios(auth.user?.id_token);
      setPortfolios(data);
    } catch (err) {
      setError(err.message);
      if (err.status === 401) auth.signinRedirect();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPortfolios();
  }, []);

  const handleDelete = async (portfolioId) => {
    try {
      await deletePortfolio(auth.user?.id_token, portfolioId);
      fetchPortfolios();
    } catch (err) {
      setError(err.message);
      if (err.status === 401) auth.signinRedirect();
    }
  };

  return (
    <div className="container">
      <h1>My Portfolios</h1>
      <CreatePortfolioForm onCreated={fetchPortfolios} />
      <ErrorBanner message={error} />
      {loading ? (
        <LoadingSpinner />
      ) : portfolios.length === 0 ? (
        <p>You have no portfolios yet. Create one above.</p>
      ) : (
        portfolios.map((p) => (
          <PortfolioCard key={p.id || p.portfolio_id} portfolio={p} onDelete={handleDelete} />
        ))
      )}
    </div>
  );
}
