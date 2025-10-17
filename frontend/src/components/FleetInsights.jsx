import { Lightbulb, TrendingUp, AlertCircle } from 'lucide-react'

function FleetInsights({ insights, summary }) {
  if (!insights && !summary) {
    return null
  }
  
  // Determine insight type based on fleet average score
  const fleetAvg = summary?.fleet_avg_score || 0
  
  const getInsightStyle = () => {
    if (fleetAvg >= 7) {
      return {
        icon: TrendingUp,
        color: 'text-green-600 dark:text-green-400',
        bgColor: 'bg-green-50 dark:bg-green-900/20',
        borderColor: 'border-green-200 dark:border-green-800',
        title: 'Fleet Performance: Excellent'
      }
    } else if (fleetAvg >= 5) {
      return {
        icon: Lightbulb,
        color: 'text-yellow-600 dark:text-yellow-400',
        bgColor: 'bg-yellow-50 dark:bg-yellow-900/20',
        borderColor: 'border-yellow-200 dark:border-yellow-800',
        title: 'Fleet Performance: Good'
      }
    } else {
      return {
        icon: AlertCircle,
        color: 'text-red-600 dark:text-red-400',
        bgColor: 'bg-red-50 dark:bg-red-900/20',
        borderColor: 'border-red-200 dark:border-red-800',
        title: 'Fleet Performance: Needs Attention'
      }
    }
  }
  
  const style = getInsightStyle()
  const IconComponent = style.icon
  
  return (
    <div className={`card ${style.bgColor} border-2 ${style.borderColor}`}>
      <div className="flex items-start space-x-4">
        <div className={`p-3 rounded-lg ${style.bgColor}`}>
          <IconComponent className={style.color} size={28} />
        </div>
        
        <div className="flex-1">
          <h2 className="text-xl font-semibold mb-2 text-gray-900 dark:text-gray-100">
            {style.title}
          </h2>
          
          <div className={`text-gray-700 dark:text-gray-300 leading-relaxed`}>
            {insights ? (
              <p>{insights}</p>
            ) : (
              <p>Loading fleet insights...</p>
            )}
          </div>
          
          {summary && (
            <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <p className="text-xs text-gray-600 dark:text-gray-400">High Performers</p>
                  <p className="text-lg font-semibold text-green-600 dark:text-green-400">
                    {summary.high_performers || 0}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-600 dark:text-gray-400">Average</p>
                  <p className="text-lg font-semibold text-yellow-600 dark:text-yellow-400">
                    {summary.average_performers || 0}
                  </p>
                </div>
                <div>
                  <p className="text-xs text-gray-600 dark:text-gray-400">Needs Training</p>
                  <p className="text-lg font-semibold text-red-600 dark:text-red-400">
                    {summary.low_performers || 0}
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default FleetInsights
