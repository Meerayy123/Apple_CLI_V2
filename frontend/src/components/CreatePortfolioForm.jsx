import { useState } from "react";
import { useAuth } from "react-oidc-context";
import { createPortfolio } from "../api/portfolios.js";
import { useUsername } from "../auth/useUsername.js";
import ErrorBanner from "./ErrorBanner.jsx";

export default function CreatePortfolioForm({ onCreated }) {
  const auth = useAuth();
  const username = useUsername();
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      setError("Name is required");
      return;
    }
    try {
      setLoading(true);
      setError(null);
      setSuccess(null);
      await createPortfolio(auth.user?.id_token, { username, name, description });
      setName("");
      setDescription("");
      setSuccess("Portfolio created successfully!");
      setTimeout(() => setSuccess(null), 3000);
      if (onCreated) onCreated();
    } catch (err) {
      setError(err.message);
      if (err.status === 401) auth.signinRedirect();
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ border: "1px solid #eee", borderRadius: "8px", padding: "1rem", marginBottom: "2rem" }}>
      <h2 style={{ marginTop: 0 }}>Create Portfolio</h2>
      <ErrorBanner message={error} />
      {success && <div className="success">{success}</div>}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: "0.75rem" }}>
          <label htmlFor="pf-name" style={{ display: "block", marginBottom: "0.25rem", fontWeight: 500 }}>Name</label>
          <input id="pf-name" value={name} onChange={(e) => setName(e.target.value)} disabled={loading} style={{ width: "100%" }} />
        </div>
        <div style={{ marginBottom: "0.75rem" }}>
          <label htmlFor="pf-desc" style={{ display: "block", marginBottom: "0.25rem", fontWeight: 500 }}>Description</label>
          <textarea id="pf-desc" value={description} onChange={(e) => setDescription(e.target.value)} disabled={loading} rows={3} style={{ width: "100%" }} />
        </div>
        <button type="submit" disabled={loading}>{loading ? "Creating…" : "Create"}</button>
      </form>
    </div>
  );
}
