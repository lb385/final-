import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import '../styles/Profile.css'

function Profile({ setIsAuthenticated }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [showPasswordForm, setShowPasswordForm] = useState(false)

  // Profile form state
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')

  // Password form state
  const [oldPassword, setOldPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')

  const navigate = useNavigate()

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.get(
        `${import.meta.env.VITE_API_URL}/api/profile`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      setUser(response.data)
      setUsername(response.data.username)
      setEmail(response.data.email)
    } catch (err) {
      if (err.response?.status === 401) {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        setIsAuthenticated(false)
        navigate('/login')
      } else {
        setError('Failed to load profile')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleProfileUpdate = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    try {
      const token = localStorage.getItem('access_token')
      const response = await axios.put(
        `${import.meta.env.VITE_API_URL}/api/profile`,
        {
          username: username !== user.username ? username : undefined,
          email: email !== user.email ? email : undefined
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      setUser(response.data)
      localStorage.setItem('user', JSON.stringify(response.data))
      setSuccess('Profile updated successfully')
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to update profile')
    }
  }

  const handlePasswordChange = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    if (newPassword !== confirmPassword) {
      setError('New passwords do not match')
      return
    }

    try {
      const token = localStorage.getItem('access_token')
      await axios.post(
        `${import.meta.env.VITE_API_URL}/api/profile/change-password`,
        {
          old_password: oldPassword,
          new_password: newPassword,
          confirm_password: confirmPassword
        },
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      setSuccess('Password changed successfully')
      setOldPassword('')
      setNewPassword('')
      setConfirmPassword('')
      setShowPasswordForm(false)
      setTimeout(() => setSuccess(''), 3000)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to change password')
    }
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    setIsAuthenticated(false)
    navigate('/login')
  }

  const handleDeleteAccount = async () => {
    if (!window.confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
      return
    }

    try {
      const token = localStorage.getItem('access_token')
      await axios.delete(
        `${import.meta.env.VITE_API_URL}/api/account`,
        {
          headers: {
            Authorization: `Bearer ${token}`
          }
        }
      )
      
      // Account deleted successfully, redirect to login
      localStorage.removeItem('access_token')
      localStorage.removeItem('user')
      setIsAuthenticated(false)
      navigate('/login')
    } catch (err) {
      setError('Failed to delete account. Please try again.')
    }
  }

  if (loading) {
    return <div className="profile-container"><p>Loading...</p></div>
  }

  return (
    <div className="profile-container">
      <header className="profile-header">
        <h1>My Profile</h1>
        <div className="header-actions">
          <button onClick={() => navigate('/dashboard')} className="btn-secondary">
            Dashboard
          </button>
          <button onClick={handleLogout} className="btn-secondary">
            Logout
          </button>
          <button onClick={handleDeleteAccount} className="btn-danger">
            Delete Account
          </button>
        </div>
      </header>

      <main className="profile-content">
        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <section className="profile-section">
          <h2>Update Profile</h2>
          <form onSubmit={handleProfileUpdate}>
            <div className="form-group">
              <label htmlFor="username">Username</label>
              <input
                id="username"
                name="username"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                minLength="3"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">Email</label>
              <input
                id="email"
                name="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />
            </div>

            <button type="submit" className="btn-primary">
              Save Profile
            </button>
          </form>
        </section>

        <section className="profile-section">
          <h2>Password Management</h2>
          <button 
            onClick={() => setShowPasswordForm(!showPasswordForm)}
            className="btn-secondary"
          >
            {showPasswordForm ? 'Cancel' : 'Change Password'}
          </button>

          {showPasswordForm && (
            <form onSubmit={handlePasswordChange} className="password-form">
              <div className="form-group">
                <label htmlFor="oldPassword">Current Password</label>
                <input
                  id="oldPassword"
                  name="oldPassword"
                  type="password"
                  value={oldPassword}
                  onChange={(e) => setOldPassword(e.target.value)}
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="newPassword">New Password</label>
                <input
                  id="newPassword"
                  name="newPassword"
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  minLength="8"
                  required
                />
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword">Confirm New Password</label>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  minLength="8"
                  required
                />
              </div>

              <button type="submit" className="btn-primary">
                Update Password
              </button>
            </form>
          )}
        </section>
      </main>
    </div>
  )
}

export default Profile
