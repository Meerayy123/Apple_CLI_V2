import { Link } from "react-router-dom";

export default function PortfolioCard({ portfolio, onDelete }) {
  const handleDelete = () => {
    if (window.confirm("Delete this portfolio? This cannot be undone.")) {
      onDelete(portfolio.id || portfolio.portfolio_id);
    }
  };
  return (
    <div style={{ border: "1px solid #eee", borderRadius: "8px", padding: "1rem", marginBottom: "1rem" }}>
      <h3 style={{ margin: "0 0 0.5rem 0" }}>{portfolio.name}</h3>
      <p style={{ color: "#666", margin: "0 0 1rem 0" }}>{portfolio.description}</p>
      <div style={{ display: "flex", gap: "0.5rem" }}>
        <Link to={`/portfolios/${portfolio.id || portfolio.portfolio_id}`}>
          <button>View</button>
        </Link>
        <button onClick={handleDelete} style={{ color: "#b00020", borderColor: "#b00020" }}>Delete</button>
      </div>
    </div>
  );
}
