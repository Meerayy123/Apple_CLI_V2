import { Routes, Route, Navigate } from "react-router-dom";
import { useAuth } from "react-oidc-context";
import LoginPage from "./pages/LoginPage.jsx";
import CallbackPage from "./pages/CallbackPage.jsx";
import PortfoliosListPage from "./pages/PortfoliosListPage.jsx";
import PortfolioDetailPage from "./pages/PortfolioDetailPage.jsx";
import ProtectedRoute from "./auth/ProtectedRoute.jsx";
import NavBar from "./components/NavBar.jsx";

export default function App() {
  const auth = useAuth();
  return (
    <>
      {auth.isAuthenticated && <NavBar />}
      <Routes>
        <Route path="/" element={<Navigate to="/portfolios" replace />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/callback" element={<CallbackPage />} />
        <Route
          path="/portfolios"
          element={
            <ProtectedRoute>
              <PortfoliosListPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/portfolios/:id"
          element={
            <ProtectedRoute>
              <PortfolioDetailPage />
            </ProtectedRoute>
          }
        />
        <Route path="*" element={<Navigate to="/portfolios" replace />} />
      </Routes>
    </>
  );
}
