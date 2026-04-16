import { useEffect, useMemo, useState } from 'react'

const WEATHER_BASE = '/api/weather'
const USERS_BASE = '/api/users'

function App() {
  const [cities, setCities] = useState([])
  const [selectedCity, setSelectedCity] = useState('Bogota')
  const [weather, setWeather] = useState(null)
  const [users, setUsers] = useState([])
  const [admin, setAdmin] = useState(null)
  const [loadingWeather, setLoadingWeather] = useState(false)
  const [loadingUsers, setLoadingUsers] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    loadCities()
    loadUsers()
    loadAdmin()
  }, [])

  useEffect(() => {
    if (selectedCity) {
      loadWeather(selectedCity)
    }
  }, [selectedCity])

  async function loadCities() {
    try {
      const response = await fetch(`${WEATHER_BASE}/cities`)
      const data = await response.json()
      setCities(data.cities || [])
    } catch (err) {
      setError('Could not load supported cities.')
    }
  }

  async function loadWeather(city) {
    setLoadingWeather(true)
    setError('')
    try {
      const response = await fetch(`${WEATHER_BASE}/weather/${encodeURIComponent(city)}`)
      if (!response.ok) {
        const details = await response.json()
        throw new Error(details.detail || 'Failed to fetch weather.')
      }
      const data = await response.json()
      setWeather(data)
    } catch (err) {
      setError(err.message)
      setWeather(null)
    } finally {
      setLoadingWeather(false)
    }
  }

  async function loadUsers() {
    setLoadingUsers(true)
    try {
      const response = await fetch(`${USERS_BASE}/users`)
      const data = await response.json()
      setUsers(data.users || [])
    } catch (err) {
      setError('Could not load local users.')
    } finally {
      setLoadingUsers(false)
    }
  }

  async function loadAdmin() {
    try {
      const response = await fetch(`${USERS_BASE}/users/admin`)
      const data = await response.json()
      setAdmin(data)
    } catch (err) {
      setError('Could not load admin profile.')
    }
  }

  const weatherSummary = useMemo(() => {
    if (!weather) return 'Select a city to inspect current weather conditions.'
    return `${weather.city} is currently ${weather.temperature_celsius} °C with ${weather.weather_label.toLowerCase()}.`
  }, [weather])

  return (
    <div className="page-shell">
      <header className="hero-card">
        <div>
          <p className="eyebrow">Containerized Demo Platform</p>
          <h1>SkyRoute Weather Dashboard</h1>
          <p className="hero-copy">
            A React frontend consuming two FastAPI backend services: one internal user service and one weather integration service.
          </p>
        </div>
        <div className="hero-badge">
          <span>Frontend</span>
          <strong>React + Nginx</strong>
        </div>
      </header>

      <main className="grid-layout">
        <section className="panel weather-panel">
          <div className="panel-header">
            <div>
              <p className="section-label">Weather</p>
              <h2>Current Weather by City</h2>
            </div>
            <span className="pill">External API via FastAPI</span>
          </div>

          <label className="field-label" htmlFor="city">Supported cities</label>
          <select
            id="city"
            className="city-select"
            value={selectedCity}
            onChange={(event) => setSelectedCity(event.target.value)}
          >
            {cities.map((city) => (
              <option key={city} value={city}>{city}</option>
            ))}
          </select>

          <button className="primary-button" onClick={() => loadWeather(selectedCity)}>
            Refresh weather
          </button>

          <div className="summary-card">
            {loadingWeather ? <p>Loading weather data...</p> : <p>{weatherSummary}</p>}
          </div>

          {weather && (
            <div className="metrics-grid">
              <div className="metric-card">
                <span>Temperature</span>
                <strong>{weather.temperature_celsius} °C</strong>
              </div>
              <div className="metric-card">
                <span>Wind Speed</span>
                <strong>{weather.wind_speed_kmh} km/h</strong>
              </div>
              <div className="metric-card">
                <span>Daylight</span>
                <strong>{weather.is_day ? 'Day' : 'Night'}</strong>
              </div>
              <div className="metric-card">
                <span>Weather Code</span>
                <strong>{weather.weather_code}</strong>
              </div>
            </div>
          )}
        </section>

        <section className="panel users-panel">
          <div className="panel-header">
            <div>
              <p className="section-label">Users</p>
              <h2>Local Admin Service</h2>
            </div>
            <span className="pill alt">Internal FastAPI service</span>
          </div>

          {admin && (
            <div className="admin-card">
              <p className="card-title">Admin Account</p>
              <h3>{admin.full_name}</h3>
              <p>{admin.email}</p>
              <div className="tags">
                <span>{admin.role}</span>
                <span>{admin.status}</span>
              </div>
            </div>
          )}

          <div className="users-list">
            <div className="users-list-header">
              <p className="card-title">Available Local Users</p>
              {loadingUsers && <span>Loading...</span>}
            </div>
            {users.map((user) => (
              <div className="user-row" key={user.username}>
                <div>
                  <strong>{user.full_name}</strong>
                  <p>{user.email}</p>
                </div>
                <div className="tags">
                  <span>{user.role}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      </main>

      {error && <footer className="error-banner">{error}</footer>}
    </div>
  )
}

export default App
