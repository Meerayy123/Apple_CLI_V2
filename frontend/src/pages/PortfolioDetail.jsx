import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useAuth } from 'react-oidc-context'
import { getPortfolioDetails, deletePortfolio } from '../api/portfolios'
import './PortfolioDetail.css'

const PortfolioDetail = () => {
  const { id } = useParams()
  const auth = useAuth()
  const navigate = useNavigate()
  
  const [portfolio, setPortfolio] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('holdings') // 'holdings' or 'transactions'
  const [isDeleting, setIsDeleting] = useState(false)

  const [holdings, setHoldings] = useState([])
  const [transactions, setTransactions] = useState([])
  const [loadingTabs, setLoadingTabs] = useState({ holdings: false, transactions: false })

  useEffect(() => {
    loadPortfolio()
  }, [id])

  useEffect(() => {
    if (activeTab === 'holdings') {
      loadHoldings()
    } else if (activeTab === 'transactions') {
      loadTransactions()
    }
  }, [activeTab, id])

  const loadHoldings = async () => {
    try {
      setLoadingTabs(prev => ({ ...prev, holdings: true }))
      const data = await getPortfolioHoldings(id, auth)
      setHoldings(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoadingTabs(prev => ({ ...prev, holdings: false }))
    }
  }

  const loadTransactions = async () => {
    try {
      setLoadingTabs(prev => ({ ...prev, transactions: true }))
      const { getPortfolioTransactions } = await import('../api/portfolios')
      const data = await getPortfolioTransactions(id, auth)
      setTransactions(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoadingTabs(prev => ({ ...prev, transactions: false }))
    }
  }

  const loadPortfolio = async () => {
    try {
      setLoading(true)
      const data = await getPortfolioDetails(id, auth)
      setPortfolio(data)
      setError(null)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this portfolio? This action cannot be undone.')) {
      return
    }
    
    try {
      setIsDeleting(true)
      await deletePortfolio(id, auth)
      navigate('/')
    } catch (err) {
      alert(`Failed to delete portfolio: ${err.message}`)
      setIsDeleting(false)
    }
  }

  if (loading) {
    return <div className="portfolio-detail-container"><div className="loader">Loading details...</div></div>
  }

  if (error || !portfolio) {
    return (
      <div className="portfolio-detail-container">
        <div className="error-alert">
          {error || "Portfolio not found"}
        </div>
        <Link to="/" className="btn-secondary">Back to Portfolios</Link>
      </div>
    )
  }

  return (
    <div className="portfolio-detail-container">
      <div className="portfolio-header">
        <div>
          <div className="breadcrumbs">
            <Link to="/">Portfolios</Link> &gt; <span>{portfolio.name}</span>
          </div>
          <h1>{portfolio.name}</h1>
          <p className="description">{portfolio.description}</p>
        </div>
        <div className="header-actions">
          <div className="portfolio-balance">
            <span className="balance-label">Total Balance (Est.)</span>
            <span className="balance-value">${(portfolio.balance || 0).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
          </div>
          <button className="btn-danger" onClick={handleDelete} disabled={isDeleting}>
            {isDeleting ? 'Deleting...' : 'Delete Portfolio'}
          </button>
        </div>
      </div>

      <div className="portfolio-tabs">
        <button 
          className={`tab-btn ${activeTab === 'holdings' ? 'active' : ''}`}
          onClick={() => setActiveTab('holdings')}
        >
          Holdings
        </button>
        <button 
          className={`tab-btn ${activeTab === 'transactions' ? 'active' : ''}`}
          onClick={() => setActiveTab('transactions')}
        >
          Transactions
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'holdings' ? (
          <div className="holdings-view">
            <div className="section-header">
              <h2>Holdings</h2>
              <Link to="/securities" className="btn-secondary">Trade Securities</Link>
            </div>
            
            {loadingTabs.holdings ? (
              <p>Loading holdings...</p>
            ) : holdings.length === 0 ? (
              <div className="empty-state">
                <p>No holdings found. Go to the Market to make a trade!</p>
              </div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Ticker</th>
                    <th>Quantity</th>
                  </tr>
                </thead>
                <tbody>
                  {holdings.map(h => (
                    <tr key={h.id || h.ticker}>
                      <td className="ticker-cell">{h.ticker}</td>
                      <td>{h.quantity}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        ) : (
          <div className="transactions-view">
            <h2>Transactions</h2>
            {loadingTabs.transactions ? (
              <p>Loading transactions...</p>
            ) : transactions.length === 0 ? (
              <div className="empty-state">
                <p>No transactions found.</p>
              </div>
            ) : (
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Type</th>
                    <th>Ticker</th>
                    <th>Quantity</th>
                    <th>Price</th>
                  </tr>
                </thead>
                <tbody>
                  {transactions.map(t => (
                    <tr key={t.transaction_id}>
                      <td>{new Date(t.timestamp || t.date_time).toLocaleString()}</td>
                      <td>
                        <span className={`badge ${t.type || t.transaction_type}`}>
                          {t.type || t.transaction_type}
                        </span>
                      </td>
                      <td className="ticker-cell">{t.ticker}</td>
                      <td>{t.quantity}</td>
                      <td>${parseFloat(t.price).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default PortfolioDetail
