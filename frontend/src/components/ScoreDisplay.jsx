import { motion } from 'framer-motion'
import { Gauge } from 'lucide-react'

function ScoreDisplay({ score }) {
  const displayScore = score !== null ? score.toFixed(1) : '--'
  const percentage = score !== null ? (score / 10) * 100 : 0
  
  // Determine color based on score
  const getScoreColor = (score) => {
    if (score === null) return 'text-gray-400'
    if (score >= 8) return 'text-green-500'
    if (score >= 6) return 'text-yellow-500'
    if (score >= 4) return 'text-orange-500'
    return 'text-red-500'
  }
  
  const getScoreLabel = (score) => {
    if (score === null) return 'No Data'
    if (score >= 8) return 'Excellent'
    if (score >= 6) return 'Good'
    if (score >= 4) return 'Fair'
    return 'Poor'
  }
  
  return (
    <div className="card h-full flex flex-col">
      <div className="flex items-center space-x-2 mb-4">
        <Gauge className="text-primary-600 dark:text-primary-400" size={24} />
        <h2 className="text-xl font-semibold">Driving Score</h2>
      </div>
      
      <div className="flex-1 flex flex-col items-center justify-center">
        {/* Circular Score Display */}
        <div className="relative w-48 h-48 mb-4">
          <svg className="w-full h-full transform -rotate-90">
            {/* Background Circle */}
            <circle
              cx="96"
              cy="96"
              r="88"
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              className="text-gray-200 dark:text-gray-700"
            />
            {/* Progress Circle */}
            <motion.circle
              cx="96"
              cy="96"
              r="88"
              stroke="currentColor"
              strokeWidth="12"
              fill="none"
              strokeLinecap="round"
              className={getScoreColor(score)}
              initial={{ strokeDasharray: '0 552.92' }}
              animate={{ 
                strokeDasharray: `${(percentage / 100) * 552.92} 552.92` 
              }}
              transition={{ duration: 1, ease: 'easeOut' }}
            />
          </svg>
          
          {/* Score Text */}
          <div className="absolute inset-0 flex flex-col items-center justify-center">
            <motion.span
              className={`text-5xl font-bold ${getScoreColor(score)}`}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
            >
              {displayScore}
            </motion.span>
            <span className="text-sm text-gray-600 dark:text-gray-400 mt-1">
              out of 10
            </span>
          </div>
        </div>
        
        {/* Score Label */}
        <div className={`text-xl font-semibold ${getScoreColor(score)}`}>
          {getScoreLabel(score)}
        </div>
        
        {/* Additional Info */}
        <p className="text-sm text-gray-600 dark:text-gray-400 text-center mt-4">
          Your driving safety score is calculated in real-time based on speed, acceleration, braking, and steering patterns.
        </p>
      </div>
    </div>
  )
}

export default ScoreDisplay
