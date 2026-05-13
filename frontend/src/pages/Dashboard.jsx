import React from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/Dashboard.css'

function Dashboard() {
  const navigate = useNavigate()
  const user = JSON.parse(localStorage.getItem('user') || '{}')

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    navigate('/login')
  }

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>Calculator App</h1>
        <div className="header-actions">
          <button onClick={() => navigate('/profile')} className="btn-secondary">
            Profile
          </button>
          <button onClick={handleLogout} className="btn-danger">
            Logout
          </button>
        </div>
      </header>

      <main className="dashboard-content">
        <div className="welcome-card">
          <h2>Welcome, {user.username}!</h2>
          <p>Email: {user.email}</p>
          <p>This is your dashboard. Use the menu above to manage your profile or change your password.</p>
        </div>
      </main>
    </div>
  )
}

export default Dashboard
