import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, ChevronUp, User, Activity, Calendar, MessageSquare } from 'lucide-react'

function DriverCard({ driver, rankBadge, isExpanded, onToggle }) {
  const [feedback, setFeedback] = useState('')
  const [loadingFeedback, setLoadingFeedback] = useState(false)
  
  const avgScore = driver.avg_score || 0
  
  // Determine score color
  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-500'
    if (score >= 6) return 'text-yellow-500'
    if (score >= 4) return 'text-orange-500'
    return 'text-red-500'
  }
  
  const getScoreBgColor = (score) => {
    if (score >= 8) return 'bg-green-100 dark:bg-green-900/30'
    if (score >= 6) return 'bg-yellow-100 dark:bg-yellow-900/30'
    if (score >= 4) return 'bg-orange-100 dark:bg-orange-900/30'
    return 'bg-red-100 dark:bg-red-900/30'
  }
  
  const getScoreLabel = (score) => {
    if (score >= 8) return 'Excellent'
    if (score >= 6) return 'Good'
    if (score >= 4) return 'Fair'
    return 'Poor'
  }
  
  // Fetch AI feedback when card is expanded
  useEffect(() => {
    if (isExpanded && !feedback && !loadingFeedback) {
      fetchDriverFeedback()
    }
  }, [isExpanded])
  
  const fetchDriverFeedback = async () => {
    setLoadingFeedback(true)
    try {
      const response = await fetch(`http://localhost:8000/api/fleet/drivers/${driver.driver_id}/feedback`, {
        method: 'POST'
      })
      
      if (response.ok) {
        const data = await response.json()
        setFeedback(data.feedback || 'No feedback available')
      } else {
        setFeedback('Unable to generate feedback at this time')
      }
    } catch (error) {
      console.error('Error fetching feedback:', error)
      setFeedback('Error loading feedback')
    } finally {
      setLoadingFeedback(false)
    }
  }
  
  const formatDate = (dateString) => {
    if (!dateString) return 'N/A'
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
  }
  
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden hover:shadow-lg transition-shadow duration-200">
      <div
        className="p-4 cursor-pointer"
        onClick={onToggle}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4 flex-1">
            {/* Rank Badge */}
            <div className="text-3xl font-bold text-gray-400 dark:text-gray-600 w-12 text-center">
              {rankBadge}
            </div>
            
            {/* Driver Info */}
            <div className="flex-1">
              <div className="flex items-center space-x-2 mb-1">
                <User size={18} className="text-gray-500 dark:text-gray-400" />
                <h3 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                  {driver.driver_name || driver.driver_id}
                </h3>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {driver.driver_id}
              </p>
            </div>
            
            {/* Score Display */}
            <div className={`px-6 py-3 rounded-lg ${getScoreBgColor(avgScore)}`}>
              <div className="text-center">
                <div className={`text-3xl font-bold ${getScoreColor(avgScore)}`}>
                  {avgScore.toFixed(1)}
                </div>
                <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">
                  {getScoreLabel(avgScore)}
                </div>
              </div>
            </div>
            
            {/* Trip Count */}
            <div className="text-center px-4">
              <div className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {driver.trip_count || 0}
              </div>
              <div className="text-xs text-gray-600 dark:text-gray-400">
                Trips
              </div>
            </div>
            
            {/* Expand/Collapse Icon */}
            <div className="text-gray-400 dark:text-gray-600">
              {isExpanded ? <ChevronUp size={24} /> : <ChevronDown size={24} />}
            </div>
          </div>
        </div>
      </div>
      
      {/* Expanded Details */}
      <AnimatePresence>
        {isExpanded && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: 'auto', opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.3 }}
            className="border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-900/50"
          >
            <div className="p-4 space-y-4">
              {/* Additional Stats */}
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <Activity size={16} className="text-gray-500 dark:text-gray-400" />
                    <p className="text-xs text-gray-600 dark:text-gray-400">Best Score</p>
                  </div>
                  <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    {driver.best_score ? driver.best_score.toFixed(1) : 'N/A'}
                  </p>
                </div>
                
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <Activity size={16} className="text-gray-500 dark:text-gray-400" />
                    <p className="text-xs text-gray-600 dark:text-gray-400">Worst Score</p>
                  </div>
                  <p className="text-lg font-semibold text-gray-900 dark:text-gray-100">
                    {driver.worst_score ? driver.worst_score.toFixed(1) : 'N/A'}
                  </p>
                </div>
                
                <div>
                  <div className="flex items-center space-x-2 mb-1">
                    <Calendar size={16} className="text-gray-500 dark:text-gray-400" />
                    <p className="text-xs text-gray-600 dark:text-gray-400">Last Trip</p>
                  </div>
                  <p className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                    {formatDate(driver.last_trip_date)}
                  </p>
                </div>
              </div>
              
              {/* AI Feedback Section */}
              <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-start space-x-2 mb-2">
                  <MessageSquare size={18} className="text-primary-600 dark:text-primary-400 mt-1" />
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                    AI-Powered Feedback
                  </h4>
                </div>
                
                <div className="bg-white dark:bg-gray-800 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
                  {loadingFeedback ? (
                    <div className="flex items-center space-x-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                      <span className="text-sm text-gray-600 dark:text-gray-400">
                        Generating feedback...
                      </span>
                    </div>
                  ) : (
                    <p className="text-sm text-gray-700 dark:text-gray-300 leading-relaxed">
                      {feedback || 'Click to load feedback'}
                    </p>
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

export default DriverCard
