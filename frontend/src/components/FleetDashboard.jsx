import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import FleetStats from './FleetStats'
import DriverRankings from './DriverRankings'
import FleetInsights from './FleetInsights'

function FleetDashboard() {
  const [fleetSummary, setFleetSummary] = useState(null)
  const [drivers, setDrivers] = useState([])
  const [insights, setInsights] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  
  useEffect(() => {
    // Fetch fleet data on component mount
    fetchFleetData()
    
    // Refresh data every 30 seconds
    const interval = setInterval(fetchFleetData, 30000)
    
    return () => clearInterval(interval)
  }, [])
  
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
