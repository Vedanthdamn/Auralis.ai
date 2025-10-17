import { useState } from 'react'
import { motion } from 'framer-motion'
import { Trophy, TrendingUp, Calendar, RefreshCw } from 'lucide-react'
import DriverCard from './DriverCard'

function DriverRankings({ drivers, onRefresh }) {
  const [expandedDriver, setExpandedDriver] = useState(null)
  const [sortBy, setSortBy] = useState('rank')
  
  if (!drivers || drivers.length === 0) {
    return (
      <div className="card">
        <div className="text-center py-8">
          <p className="text-gray-600 dark:text-gray-400">No driver data available</p>
          <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
            Start recording trips to see driver rankings
          </p>
        </div>
      </div>
    )
  }
  
  // Sort drivers based on selected criteria
  const sortedDrivers = [...drivers].sort((a, b) => {
    switch (sortBy) {
      case 'rank':
        return (a.rank || 999) - (b.rank || 999)
      case 'trips':
        return (b.trip_count || 0) - (a.trip_count || 0)
      case 'name':
        return (a.driver_name || '').localeCompare(b.driver_name || '')
      default:
        return 0
    }
  })
  
  const getRankBadge = (rank) => {
    if (rank === 1) {
      return '🥇'
    } else if (rank === 2) {
      return '🥈'
    } else if (rank === 3) {
      return '🥉'
    }
    return rank
  }
  
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center space-x-3">
          <Trophy className="text-primary-600 dark:text-primary-400" size={28} />
          <div>
            <h2 className="text-2xl font-semibold text-gray-900 dark:text-gray-100">
              Driver Rankings
            </h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {drivers.length} driver{drivers.length !== 1 ? 's' : ''} in fleet
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          {/* Sort Options */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:ring-2 focus:ring-primary-500"
          >
            <option value="rank">By Rank</option>
            <option value="trips">By Trips</option>
            <option value="name">By Name</option>
          </select>
          
          {/* Refresh Button */}
          <button
            onClick={onRefresh}
            className="btn btn-secondary flex items-center space-x-2"
            title="Refresh data"
          >
            <RefreshCw size={16} />
            <span className="hidden sm:inline">Refresh</span>
          </button>
        </div>
      </div>
      
      {/* Driver Cards Grid */}
      <div className="space-y-4">
        {sortedDrivers.map((driver, index) => (
          <motion.div
            key={driver.driver_id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: index * 0.05 }}
          >
            <DriverCard
              driver={driver}
              rankBadge={getRankBadge(driver.rank)}
              isExpanded={expandedDriver === driver.driver_id}
              onToggle={() => setExpandedDriver(
                expandedDriver === driver.driver_id ? null : driver.driver_id
              )}
            />
          </motion.div>
        ))}
      </div>
    </div>
  )
}

export default DriverRankings
