import { useAuth } from 'react-oidc-context'
import { Link, useNavigate } from 'react-router-dom'
import { useUsername } from '../hooks/useUsername'
import './NavBar.css'

const NavBar = () => {
  const auth = useAuth()
  const username = useUsername()
  const navigate = useNavigate()

  const handleLogout = () => {
    // Clear session storage just in case
    sessionStorage.clear()
    
    // Perform OIDC logout. Adjust based on your Cognito setup
    auth.signoutRedirect()
  }

  return (
    <nav className="navbar">
      <div className="nav-brand">
        <Link to="/" className="nav-logo">
          <span className="logo-icon">🍏</span> Apple CLI
        </Link>
      </div>
      
      <div className="nav-links">
        {auth.isAuthenticated && (
          <>
            <Link to="/" className="nav-link">Portfolios</Link>
            <Link to="/securities" className="nav-link">Market</Link>
          </>
        )}
      </div>

      <div className="nav-auth">
        {auth.isLoading ? (
          <span className="nav-text">Loading...</span>
        ) : auth.isAuthenticated ? (
          <div className="user-menu">
            <span className="nav-username">Hi, {username}</span>
            <button className="btn-logout" onClick={handleLogout}>
              Logout
            </button>
          </div>
        ) : (
          <button className="btn-login" onClick={() => auth.signinRedirect()}>
            Login
          </button>
        )}
      </div>
    </nav>
  )
}

export default NavBar
