import { motion } from 'framer-motion'
import { Gauge, TrendingUp } from 'lucide-react'

function ScoreDisplay({ score }) {
  const displayScore = score !== null ? score.toFixed(1) : '--'
  const percentage = score !== null ? (score / 10) * 100 : 0
  
  // Determine color based on score
  const getScoreColor = (score) => {
    if (score === null) return 'text-gray-400'
    if (score >= 8) return 'text-tesla-success'
    if (score >= 6) return 'text-tesla-warning'
    if (score >= 4) return 'text-orange-500'
    return 'text-tesla-danger'
  }
  
  const getScoreGradient = (score) => {
    if (score === null) return 'from-gray-400 to-gray-500'
    if (score >= 8) return 'from-tesla-success to-green-400'
    if (score >= 6) return 'from-tesla-warning to-yellow-400'
    if (score >= 4) return 'from-orange-500 to-orange-600'
    return 'from-tesla-danger to-red-600'
  }
  
  const getScoreLabel = (score) => {
    if (score === null) return 'No Data'
    if (score >= 8) return 'Excellent'
    if (score >= 6) return 'Good'
    if (score >= 4) return 'Fair'
    return 'Poor'
  }
  
  return (
    <div className="card-glass h-full flex flex-col relative overflow-hidden">
      {/* Animated background gradient */}
      <motion.div
        className="absolute inset-0 opacity-10"
        animate={{
          background: [
            'radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.3) 0%, transparent 50%)',
            'radial-gradient(circle at 80% 50%, rgba(6, 182, 212, 0.3) 0%, transparent 50%)',
            'radial-gradient(circle at 20% 50%, rgba(59, 130, 246, 0.3) 0%, transparent 50%)',
          ],
        }}
        transition={{
          duration: 8,
          repeat: Infinity,
          ease: 'linear',
        }}
      />
      
      <div className="relative z-10">
        <div className="flex items-center space-x-2 mb-4">
          <div className="p-2 rounded-lg bg-gradient-to-br from-tesla-accent/20 to-tesla-cyan/20">
            <Gauge className="text-tesla-accent" size={24} />
          </div>
          <div>
            <h2 className="text-xl font-semibold">Driving Score</h2>
            <p className="text-xs text-gray-600 dark:text-gray-400">Real-time safety rating</p>
          </div>
        </div>
        
        <div className="flex-1 flex flex-col items-center justify-center py-6">
          {/* Circular Score Display with glow effect */}
          <div className="relative w-48 h-48 mb-4">
            {/* Glow effect */}
            <motion.div
              className="absolute inset-0 rounded-full blur-xl opacity-30"
              animate={{
                boxShadow: [
                  `0 0 40px ${score >= 8 ? '#10b981' : score >= 6 ? '#f59e0b' : '#ef4444'}`,
                  `0 0 80px ${score >= 8 ? '#10b981' : score >= 6 ? '#f59e0b' : '#ef4444'}`,
                  `0 0 40px ${score >= 8 ? '#10b981' : score >= 6 ? '#f59e0b' : '#ef4444'}`,
                ],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                ease: 'easeInOut',
              }}
            />
            
            <svg className="w-full h-full transform -rotate-90 relative z-10">
              {/* Background Circle */}
              <circle
                cx="96"
                cy="96"
                r="88"
                stroke="currentColor"
                strokeWidth="12"
                fill="none"
                className="text-gray-200 dark:text-tesla-border"
              />
              {/* Progress Circle */}
              <motion.circle
                cx="96"
                cy="96"
                r="88"
                stroke="url(#scoreGradient)"
                strokeWidth="12"
                fill="none"
                strokeLinecap="round"
                initial={{ strokeDasharray: '0 552.92' }}
                animate={{ 
                  strokeDasharray: `${(percentage / 100) * 552.92} 552.92` 
                }}
                transition={{ duration: 1, ease: 'easeOut' }}
              />
              {/* Gradient definition */}
              <defs>
                <linearGradient id="scoreGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor={score >= 8 ? '#10b981' : score >= 6 ? '#f59e0b' : '#ef4444'} />
                  <stop offset="100%" stopColor={score >= 8 ? '#34d399' : score >= 6 ? '#fbbf24' : '#f87171'} />
                </linearGradient>
              </defs>
            </svg>
            
            {/* Score Text */}
            <div className="absolute inset-0 flex flex-col items-center justify-center">
              <motion.span
                className={`text-6xl font-bold bg-gradient-to-r ${getScoreGradient(score)} bg-clip-text text-transparent`}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ duration: 0.5, delay: 0.2, type: 'spring' }}
              >
                {displayScore}
              </motion.span>
              <span className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                out of 10
              </span>
            </div>
          </div>
          
          {/* Score Label with badge */}
          <motion.div 
            className={`px-6 py-2 rounded-full bg-gradient-to-r ${getScoreGradient(score)} text-white font-semibold text-lg shadow-lg`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            {getScoreLabel(score)}
          </motion.div>
          
          {/* Additional Info */}
          <p className="text-sm text-gray-600 dark:text-gray-400 text-center mt-6 px-4">
            Your driving safety score is calculated in real-time based on speed, acceleration, braking, and steering patterns.
          </p>
          
          {/* Performance indicator */}
          {score !== null && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.7 }}
              className="mt-4 flex items-center space-x-2 text-sm"
            >
              <TrendingUp size={16} className="text-tesla-accent" />
              <span className="text-gray-600 dark:text-gray-400">
                {score >= 8 ? 'Outstanding performance!' : score >= 6 ? 'Good driving habits' : 'Room for improvement'}
              </span>
            </motion.div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ScoreDisplay
