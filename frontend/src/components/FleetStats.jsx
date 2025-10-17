import { motion } from 'framer-motion'
import { Users, Car, TrendingUp, Award } from 'lucide-react'

function FleetStats({ summary }) {
  if (!summary) {
    return null
  }
  
  const stats = [
    {
      icon: Users,
      label: 'Total Drivers',
      value: summary.total_drivers || 0,
      color: 'text-blue-600 dark:text-blue-400',
      bgColor: 'bg-blue-100 dark:bg-blue-900'
    },
    {
      icon: Car,
      label: 'Total Trips',
      value: summary.total_trips || 0,
      color: 'text-green-600 dark:text-green-400',
      bgColor: 'bg-green-100 dark:bg-green-900'
    },
    {
      icon: TrendingUp,
      label: 'Fleet Avg Score',
      value: summary.fleet_avg_score ? summary.fleet_avg_score.toFixed(1) : '0.0',
      suffix: '/10',
      color: 'text-purple-600 dark:text-purple-400',
      bgColor: 'bg-purple-100 dark:bg-purple-900'
    },
    {
      icon: Award,
      label: 'Safest Driver',
      value: summary.safest_driver || 'N/A',
      subtitle: summary.safest_driver_score ? `${summary.safest_driver_score.toFixed(1)}/10` : '',
      color: 'text-yellow-600 dark:text-yellow-400',
      bgColor: 'bg-yellow-100 dark:bg-yellow-900'
    }
  ]
  
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.label}
          className="card"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
        >
          <div className="flex items-start space-x-4">
            <div className={`p-3 rounded-lg ${stat.bgColor}`}>
              <stat.icon className={stat.color} size={24} />
            </div>
            
            <div className="flex-1">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                {stat.label}
              </p>
              <div className="flex items-baseline space-x-1">
                <span className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                  {stat.value}
                </span>
                {stat.suffix && (
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {stat.suffix}
                  </span>
                )}
              </div>
              {stat.subtitle && (
                <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                  {stat.subtitle}
                </p>
              )}
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  )
}

export default FleetStats
