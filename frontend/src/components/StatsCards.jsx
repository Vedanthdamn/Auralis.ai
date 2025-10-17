import { Gauge, Zap, AlertTriangle, Wind } from 'lucide-react'
import { motion } from 'framer-motion'

function StatsCards({ drivingData }) {
  const stats = [
    {
      label: 'Current Speed',
      value: drivingData ? `${drivingData.speed.toFixed(1)} km/h` : '--',
      icon: Gauge,
      color: 'text-blue-600 dark:text-blue-400',
      bgColor: 'bg-blue-100 dark:bg-blue-900/30',
    },
    {
      label: 'Acceleration',
      value: drivingData ? `${drivingData.acceleration.toFixed(2)} m/s²` : '--',
      icon: Zap,
      color: 'text-green-600 dark:text-green-400',
      bgColor: 'bg-green-100 dark:bg-green-900/30',
    },
    {
      label: 'Braking Intensity',
      value: drivingData ? `${(drivingData.braking_intensity * 100).toFixed(0)}%` : '--',
      icon: AlertTriangle,
      color: 'text-red-600 dark:text-red-400',
      bgColor: 'bg-red-100 dark:bg-red-900/30',
    },
    {
      label: 'Steering Angle',
      value: drivingData ? `${drivingData.steering_angle.toFixed(1)}°` : '--',
      icon: Wind,
      color: 'text-purple-600 dark:text-purple-400',
      bgColor: 'bg-purple-100 dark:bg-purple-900/30',
    },
  ]
  
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat, index) => (
        <motion.div
          key={stat.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: index * 0.1 }}
          className="card"
        >
          <div className="flex items-center justify-between">
            <div className="flex-1">
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                {stat.label}
              </p>
              <p className="text-2xl font-bold text-gray-900 dark:text-gray-100">
                {stat.value}
              </p>
            </div>
            <div className={`${stat.bgColor} ${stat.color} p-3 rounded-lg`}>
              <stat.icon size={24} />
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  )
}

export default StatsCards
