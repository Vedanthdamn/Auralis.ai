import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import FleetStats from './FleetStats'
import DriverRankings from './DriverRankings'
import FleetInsights from './FleetInsights'

function FleetDashboard({ fleetData }) {
  const [fleetSummary, setFleetSummary] = useState(null)
  const [drivers, setDrivers] = useState([])
  const [insights, setInsights] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [realtimeData, setRealtimeData] = useState(null)
  
  useEffect(() => {
    // Fetch fleet data on component mount
    fetchFleetData()
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchFleetData, 30000)
    
    return () => clearInterval(interval)
  }, [])
  
  useEffect(() => {
    // Update real-time data when fleetData changes
    if (fleetData) {
      setRealtimeData(fleetData)
    }
  }, [fleetData])
  
  const fetchFleetData = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Fetch fleet summary
      const summaryResponse = await fetch('http://localhost:8000/api/fleet/summary')
      if (!summaryResponse.ok) {
        throw new Error('Failed to fetch fleet summary')
      }
      const summaryData = await summaryResponse.json()
      setFleetSummary(summaryData)
      
      // Fetch drivers list
      const driversResponse = await fetch('http://localhost:8000/api/fleet/drivers')
      if (!driversResponse.ok) {
        throw new Error('Failed to fetch drivers')
      }
      const driversData = await driversResponse.json()
      setDrivers(driversData.drivers || [])
      
      // Fetch fleet insights
      const insightsResponse = await fetch('http://localhost:8000/api/fleet/insights')
      if (!insightsResponse.ok) {
        throw new Error('Failed to fetch insights')
      }
      const insightsData = await insightsResponse.json()
      setInsights(insightsData.insights || '')
      
      setLoading(false)
    } catch (err) {
      console.error('Error fetching fleet data:', err)
      setError(err.message)
      setLoading(false)
    }
  }
  
  if (loading && !fleetSummary) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-600 mx-auto mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Loading fleet data...</p>
        </div>
      </div>
    )
  }
  
  if (error) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <p className="text-red-600 dark:text-red-400 mb-4">Error: {error}</p>
          <button 
            onClick={fetchFleetData}
            className="btn btn-primary"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }
  
  return (
    <div className="space-y-6">
      {/* Real-time Fleet Simulation Data */}
      {realtimeData && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="card bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center">
              <span className="mr-2">🚕</span>
              Live Fleet Simulation Data
            </h3>
            <span className="px-3 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 text-sm rounded-full flex items-center">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
              Live
            </span>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
              <div className="text-sm text-gray-500 dark:text-gray-400">Speed</div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {realtimeData.speed?.toFixed(1) || '0.0'} <span className="text-sm text-gray-500">km/h</span>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
              <div className="text-sm text-gray-500 dark:text-gray-400">Acceleration</div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {realtimeData.acceleration?.toFixed(2) || '0.00'} <span className="text-sm text-gray-500">m/s²</span>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
              <div className="text-sm text-gray-500 dark:text-gray-400">Braking</div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {((realtimeData.braking_intensity || 0) * 100).toFixed(0)}%
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 p-3 rounded-lg">
              <div className="text-sm text-gray-500 dark:text-gray-400">Safety Score</div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {realtimeData.score?.toFixed(1) || 'N/A'} <span className="text-sm text-gray-500">/10</span>
              </div>
            </div>
          </div>
          {realtimeData.scenario && (
            <div className="mt-3 text-sm text-gray-600 dark:text-gray-300">
              <span className="font-medium">Scenario:</span> {realtimeData.scenario}
            </div>
          )}
        </motion.div>
      )}
      
      {/* Fleet Statistics Cards */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <FleetStats summary={fleetSummary} />
      </motion.div>
      
      {/* Fleet Insights */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
      >
        <FleetInsights insights={insights} summary={fleetSummary} />
      </motion.div>
      
      {/* Driver Rankings */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <DriverRankings drivers={drivers} onRefresh={fetchFleetData} />
      </motion.div>
    </div>
  )
}

export default FleetDashboard
