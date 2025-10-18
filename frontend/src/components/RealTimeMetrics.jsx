import { motion } from 'framer-motion'
import { Gauge, TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react'

function MetricCard({ label, value, unit, trend, icon: Icon, status = 'normal' }) {
  const getStatusColor = () => {
    switch (status) {
      case 'success':
        return 'border-glow-success'
      case 'warning':
        return 'border-glow-warning'
      case 'danger':
        return 'border-glow-danger'
      default:
        return 'border-glow'
    }
  }
  
  const getValueColor = () => {
    switch (status) {
      case 'success':
        return 'from-tesla-success to-green-400'
      case 'warning':
        return 'from-tesla-warning to-yellow-400'
      case 'danger':
        return 'from-tesla-danger to-red-400'
      default:
        return 'from-tesla-accent to-tesla-cyan'
    }
  }
  
  const TrendIcon = trend > 0 ? TrendingUp : trend < 0 ? TrendingDown : null
  
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      whileHover={{ scale: 1.05, y: -5 }}
      transition={{ duration: 0.3 }}
      className={`metric-card ${getStatusColor()}`}
    >
      {/* Icon */}
      <div className="flex items-center justify-between w-full mb-3">
        <div className="p-2 rounded-lg bg-gradient-to-br from-tesla-accent/20 to-tesla-cyan/20">
          {Icon && <Icon className="text-tesla-accent" size={24} />}
        </div>
        {TrendIcon && (
          <TrendIcon 
            size={16} 
            className={trend > 0 ? 'text-tesla-success' : 'text-tesla-danger'} 
          />
        )}
      </div>
      
      {/* Value */}
      <div className="w-full text-center">
        <div className={`text-4xl font-bold bg-gradient-to-r ${getValueColor()} bg-clip-text text-transparent`}>
          {value !== null && value !== undefined ? value : '--'}
          {unit && <span className="text-xl ml-1">{unit}</span>}
        </div>
        
        {/* Label */}
        <div className="metric-label mt-2">
          {label}
        </div>
        
        {/* Trend indicator */}
        {trend !== undefined && trend !== 0 && (
          <div className={`text-xs mt-1 ${trend > 0 ? 'text-tesla-success' : 'text-tesla-danger'}`}>
            {trend > 0 ? '+' : ''}{trend.toFixed(1)}%
          </div>
        )}
      </div>
      
      {/* Animated scan line effect */}
      <motion.div
        className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-tesla-accent to-transparent opacity-50"
        animate={{
          y: [0, 120, 0],
        }}
        transition={{
          duration: 3,
          repeat: Infinity,
          ease: "linear",
        }}
      />
    </motion.div>
  )
}

function RealTimeMetrics({ drivingData }) {
  const metrics = [
    {
      label: 'Speed',
      value: drivingData?.speed?.toFixed(1) || null,
      unit: 'km/h',
      icon: Gauge,
      status: drivingData?.speed > 100 ? 'danger' : drivingData?.speed > 80 ? 'warning' : 'success',
      trend: 0,
    },
    {
      label: 'Acceleration',
      value: drivingData?.acceleration?.toFixed(2) || null,
      unit: 'm/s²',
      icon: TrendingUp,
      status: Math.abs(drivingData?.acceleration || 0) > 3 ? 'danger' : 'normal',
      trend: drivingData?.acceleration || 0,
    },
    {
      label: 'Steering Angle',
      value: drivingData?.steering_angle?.toFixed(1) || null,
      unit: '°',
      icon: Gauge,
      status: Math.abs(drivingData?.steering_angle || 0) > 30 ? 'warning' : 'normal',
      trend: 0,
    },
    {
      label: 'Brake Force',
      value: drivingData?.brake?.toFixed(2) || null,
      unit: 'N',
      icon: AlertTriangle,
      status: (drivingData?.brake || 0) > 0.5 ? 'danger' : 'success',
      trend: 0,
    },
    {
      label: 'Risk Index',
      value: drivingData?.score ? (10 - drivingData.score).toFixed(1) : null,
      unit: '/10',
      icon: AlertTriangle,
      status: drivingData?.score < 5 ? 'danger' : drivingData?.score < 7 ? 'warning' : 'success',
      trend: 0,
    },
  ]
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
      {metrics.map((metric, index) => (
        <motion.div
          key={metric.label}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <MetricCard {...metric} />
        </motion.div>
      ))}
    </div>
  )
}

export default RealTimeMetrics
