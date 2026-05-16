import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from 'react-oidc-context'
import { getMyPortfolios } from '../api/portfolios'
import './Home.css'

const Home = () => {
  const auth = useAuth()
  const [portfolios, setPortfolios] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (auth.isAuthenticated) {
      loadPortfolios()
    } else {
      setLoading(false)
    }
  }, [auth.isAuthenticated])

  const loadPortfolios = async () => {
    try {
      setLoading(true)
      const data = await getMyPortfolios(auth)
      setPortfolios(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (!auth.isAuthenticated) {
    return (
      <div className="home-container auth-prompt">
        <div className="hero-content">
          <h1>Apple CLI Portfolio Manager</h1>
          <p>Manage your investments, track holdings, and execute trades with ease.</p>
          <button className="btn-primary" onClick={() => auth.signinRedirect()}>
            Get Started
          </button>
        </div>
      </div>
    )
  }

  if (loading) {
    return <div className="home-container"><div className="loader">Loading portfolios...</div></div>
  }

  return (
    <div className="home-container">
      <div className="home-header">
        <h1>My Portfolios</h1>
        <Link to="/portfolios/new" className="btn-primary">
          + Create Portfolio
        </Link>
      </div>

      {error && <div className="error-alert">{error}</div>}

      {portfolios.length === 0 && !error ? (
        <div className="empty-state">
          <h2>No Portfolios Yet</h2>
          <p>Create your first portfolio to start tracking your investments.</p>
          <Link to="/portfolios/new" className="btn-secondary">
            Create Portfolio
          </Link>
        </div>
      ) : (
        <div className="portfolio-grid">
          {portfolios.map(p => (
            <Link to={`/portfolios/${p.id || p.portfolio_id}`} key={p.id || p.portfolio_id} className="portfolio-card">
              <div className="card-content">
                <h3>{p.name}</h3>
                <p className="description">{p.description}</p>
              </div>
              <div className="card-footer">
                <span className="view-details">View Details &rarr;</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

export default Home
