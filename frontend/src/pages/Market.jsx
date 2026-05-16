import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from 'react-oidc-context'
import { getSecurities, buySecurity, sellSecurity } from '../api/trades'
import { getMyPortfolios } from '../api/portfolios'
import './Market.css'

const Market = () => {
  const auth = useAuth()
  const [securities, setSecurities] = useState([])
  const [portfolios, setPortfolios] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  const [tradeModal, setTradeModal] = useState({
    isOpen: false,
    type: 'buy', // 'buy' or 'sell'
    security: null,
    portfolioId: '',
    quantity: 1,
    isSubmitting: false,
    error: null
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      setLoading(true)
      const [secData, portData] = await Promise.all([
        getSecurities(auth),
        getMyPortfolios(auth)
      ])
      setSecurities(secData)
      setPortfolios(portData)
      
      if (portData.length > 0) {
        setTradeModal(prev => ({ ...prev, portfolioId: portData[0].id || portData[0].portfolio_id }))
      }
    } catch (err) {
      setError("Failed to load market data")
    } finally {
      setLoading(false)
    }
  }

  const openTradeModal = (type, security) => {
    setTradeModal(prev => ({
      ...prev,
      isOpen: true,
      type,
      security,
      quantity: 1,
      error: null
    }))
  }

  const closeTradeModal = () => {
    setTradeModal(prev => ({ ...prev, isOpen: false }))
  }

  const handleTradeSubmit = async (e) => {
    e.preventDefault()
    
    if (!tradeModal.portfolioId) {
      setTradeModal(prev => ({ ...prev, error: "Please select a portfolio" }))
      return
    }

    try {
      setTradeModal(prev => ({ ...prev, isSubmitting: true, error: null }))
      
      if (tradeModal.type === 'buy') {
        await buySecurity(
          tradeModal.portfolioId, 
          tradeModal.security.ticker, 
          parseInt(tradeModal.quantity, 10),
          auth
        )
      } else {
        await sellSecurity(
          tradeModal.portfolioId, 
          tradeModal.security.ticker, 
          parseInt(tradeModal.quantity, 10),
          tradeModal.security.price, // For sell, pass current price
          auth
        )
      }
      
      closeTradeModal()
      alert(`Successfully ${tradeModal.type === 'buy' ? 'bought' : 'sold'} ${tradeModal.quantity} shares of ${tradeModal.security.ticker}`)
    } catch (err) {
      setTradeModal(prev => ({ ...prev, error: err.message }))
    } finally {
      setTradeModal(prev => ({ ...prev, isSubmitting: false }))
    }
  }

  if (loading) {
    return <div className="market-container"><div className="loader">Loading market data...</div></div>
  }

  return (
    <div className="market-container">
      <div className="market-header">
        <h1>Market</h1>
        <p className="description">Explore and trade available securities.</p>
      </div>

      {error && <div className="error-alert">{error}</div>}

      <div className="securities-grid">
        {securities.map(sec => (
          <div key={sec.ticker} className="security-card">
            <div className="security-header">
              <span className="ticker">{sec.ticker}</span>
              <span className="price">${sec.price.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
            </div>
            <div className="security-body">
              <span className="issuer">{sec.issuer}</span>
            </div>
            <div className="security-actions">
              <button className="btn-buy" onClick={() => openTradeModal('buy', sec)}>Buy</button>
              <button className="btn-sell" onClick={() => openTradeModal('sell', sec)}>Sell</button>
            </div>
          </div>
        ))}
      </div>

      {tradeModal.isOpen && (
        <div className="modal-overlay">
          <div className="trade-modal">
            <h2>{tradeModal.type === 'buy' ? 'Buy' : 'Sell'} {tradeModal.security.ticker}</h2>
            <p className="current-price">Current Price: ${tradeModal.security.price.toFixed(2)}</p>
            
            {tradeModal.error && <div className="error-alert">{tradeModal.error}</div>}
            
            <form onSubmit={handleTradeSubmit} className="trade-form">
              <div className="form-group">
                <label>Portfolio</label>
                {portfolios.length > 0 ? (
                  <select 
                    value={tradeModal.portfolioId} 
                    onChange={e => setTradeModal(prev => ({ ...prev, portfolioId: e.target.value }))}
                  >
                    {portfolios.map(p => (
                      <option key={p.id || p.portfolio_id} value={p.id || p.portfolio_id}>
                        {p.name}
                      </option>
                    ))}
                  </select>
                ) : (
                  <div className="no-portfolios-warning">
                    You don't have any portfolios yet. <Link to="/portfolios/new">Create one first</Link>.
                  </div>
                )}
              </div>
              
              <div className="form-group">
                <label>Quantity</label>
                <input 
                  type="number" 
                  min="1" 
                  value={tradeModal.quantity} 
                  onChange={e => setTradeModal(prev => ({ ...prev, quantity: e.target.value }))}
                  required
                />
              </div>
              
              <div className="trade-summary">
                <span>Estimated Total:</span>
                <span>${(tradeModal.quantity * tradeModal.security.price).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}</span>
              </div>
              
              <div className="form-actions">
                <button type="button" className="btn-cancel" onClick={closeTradeModal}>Cancel</button>
                <button 
                  type="submit" 
                  className={`btn-submit ${tradeModal.type === 'buy' ? 'btn-buy' : 'btn-sell'}`} 
                  disabled={tradeModal.isSubmitting || portfolios.length === 0}
                >
                  {tradeModal.isSubmitting ? 'Processing...' : `Confirm ${tradeModal.type === 'buy' ? 'Buy' : 'Sell'}`}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Market
