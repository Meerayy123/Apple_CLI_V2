import { useAuth } from "react-oidc-context";
import { Navigate } from "react-router-dom";

export default function LoginPage() {
  const auth = useAuth();
  if (auth.isAuthenticated) return <Navigate to="/portfolios" replace />;
  return (
    <div className="container" style={{ textAlign: "center", paddingTop: "4rem" }}>
      <h1>Portfolio Manager</h1>
      <p style={{ color: "#888", marginBottom: "2rem" }}>Sign in to access your portfolios.</p>
      <button
        onClick={() => auth.signinRedirect()}
        style={{
          background: "linear-gradient(135deg, #6e8efb, #a777e3)",
          color: "white",
          border: "none",
          padding: "0.8rem 2rem",
          borderRadius: "8px",
          fontWeight: 600,
          fontSize: "1rem",
          cursor: "pointer",
        }}
      >
        Sign in with Cognito
      </button>
    </div>
  );
}
