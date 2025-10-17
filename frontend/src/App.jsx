import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import Dashboard from './components/Dashboard'
import FleetDashboard from './components/FleetDashboard'
import Header from './components/Header'
import Welcome from './components/Welcome'
import Login from './components/Login'
import { useDarkMode } from './hooks/useDarkMode'
import { useWebSocket } from './hooks/useWebSocket'

function DashboardPage() {
  const [darkMode, setDarkMode] = useDarkMode()
  const [drivingData, setDrivingData] = useState(null)
  const [score, setScore] = useState(null)
  const [feedback, setFeedback] = useState('')
  const [isConnected, setIsConnected] = useState(false)
  
  // WebSocket connection for real-time data
  const { lastMessage, connectionStatus } = useWebSocket('ws://localhost:8000/ws')
  
  useEffect(() => {
    setIsConnected(connectionStatus === 'connected')
  }, [connectionStatus])
  
  useEffect(() => {
    if (lastMessage) {
      try {
        const data = JSON.parse(lastMessage)
        if (data.type === 'driving_data') {
          setDrivingData(data.payload)
        } else if (data.type === 'score_update') {
          setScore(data.payload.score)
        } else if (data.type === 'feedback') {
          setFeedback(data.payload.feedback)
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }
  }, [lastMessage])
  
  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <Header 
          darkMode={darkMode} 
          setDarkMode={setDarkMode}
          isConnected={isConnected}
          showFleetLink={true}
        />
        
        <motion.main
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="container mx-auto px-4 py-8"
        >
          <Dashboard 
            drivingData={drivingData}
            score={score}
            feedback={feedback}
          />
        </motion.main>
      </div>
    </div>
  )
}

function FleetDashboardPage() {
  const [darkMode, setDarkMode] = useDarkMode()
  
  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
        <Header 
          darkMode={darkMode} 
          setDarkMode={setDarkMode}
          isConnected={false}
          showFleetLink={true}
        />
        
        <motion.main
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="container mx-auto px-4 py-8"
        >
          <FleetDashboard />
        </motion.main>
      </div>
    </div>
  )
}

function App() {
  const [darkMode] = useDarkMode()
  
  return (
    <div className={darkMode ? 'dark' : ''}>
      <Router>
        <Routes>
          <Route path="/" element={<Welcome />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/dashboard/fleet" element={<FleetDashboardPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
