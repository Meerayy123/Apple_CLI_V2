import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { useAuth } from 'react-oidc-context'
import { createPortfolio } from '../api/portfolios'
import './CreatePortfolio.css'

const CreatePortfolio = () => {
  const auth = useAuth()
  const navigate = useNavigate()
  const [formData, setFormData] = useState({ name: '', description: '' })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!formData.name.trim()) {
      setError("Name is required")
      return
    }

    try {
      setLoading(true)
      setError(null)
      const result = await createPortfolio(formData, auth)
      // Redirect to the new portfolio
      navigate(`/portfolios/${result.portfolio_id || result.id}`)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="create-portfolio-container">
      <div className="form-card">
        <h2>Create New Portfolio</h2>
        <p className="form-subtitle">Set up a new portfolio to start managing investments.</p>
        
        {error && <div className="error-alert">{error}</div>}
        
        <form onSubmit={handleSubmit} className="portfolio-form">
          <div className="form-group">
            <label htmlFor="name">Portfolio Name</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Tech Growth Fund"
              disabled={loading}
              autoComplete="off"
            />
          </div>
          
          <div className="form-group">
            <label htmlFor="description">Description</label>
            <textarea
              id="description"
              name="description"
              value={formData.description}
              onChange={handleChange}
              placeholder="Briefly describe the strategy or purpose of this portfolio."
              disabled={loading}
              rows={4}
            />
          </div>
          
          <div className="form-actions">
            <Link to="/" className="btn-cancel">Cancel</Link>
            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? 'Creating...' : 'Create Portfolio'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default CreatePortfolio
