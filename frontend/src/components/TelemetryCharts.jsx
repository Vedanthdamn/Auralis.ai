import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts'
import { TrendingUp, Activity } from 'lucide-react'

function TelemetryCharts({ drivingData }) {
  const [chartData, setChartData] = useState([])
  const maxDataPoints = 30
  
  useEffect(() => {
    if (drivingData) {
      setChartData(prev => {
        const newData = [...prev, {
          timestamp: new Date(drivingData.timestamp).toLocaleTimeString(),
          speed: drivingData.speed,
          acceleration: drivingData.acceleration,
          braking: drivingData.braking_intensity,
        }]
        
        // Keep only last N data points
        if (newData.length > maxDataPoints) {
          return newData.slice(newData.length - maxDataPoints)
        }
        return newData
      })
    }
  }, [drivingData])
  
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-tesla-gray/95 backdrop-blur-md border border-tesla-border/50 rounded-lg p-3 shadow-xl">
          <p className="text-xs text-gray-400 mb-1">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm font-medium" style={{ color: entry.color }}>
              {entry.name}: {entry.value?.toFixed(2)}
            </p>
          ))}
        </div>
      )
    }
    return null
  }
  
  return (
    <div className="card-glass h-full relative overflow-hidden">
      {/* Animated background */}
      <motion.div
        className="absolute inset-0 opacity-5"
        animate={{
          background: [
            'radial-gradient(circle at 0% 0%, rgba(59, 130, 246, 0.3) 0%, transparent 50%)',
            'radial-gradient(circle at 100% 100%, rgba(6, 182, 212, 0.3) 0%, transparent 50%)',
            'radial-gradient(circle at 0% 0%, rgba(59, 130, 246, 0.3) 0%, transparent 50%)',
          ],
        }}
        transition={{
          duration: 10,
          repeat: Infinity,
          ease: 'linear',
        }}
      />
      
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-2">
            <div className="p-2 rounded-lg bg-gradient-to-br from-tesla-accent/20 to-tesla-cyan/20">
              <Activity className="text-tesla-accent" size={24} />
            </div>
            <div>
              <h2 className="text-xl font-semibold">Real-Time Telemetry</h2>
              <p className="text-xs text-gray-600 dark:text-gray-400">Live sensor data</p>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-tesla-accent rounded-full animate-pulse" />
            <span className="text-xs text-gray-600 dark:text-gray-400">Streaming</span>
          </div>
        </div>
        
        <div className="space-y-6">
          {/* Speed Chart - with gradient area */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Speed (km/h)
              </h3>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-tesla-accent" />
                <span className="text-xs text-gray-600 dark:text-gray-400">
                  {drivingData?.speed?.toFixed(1) || '--'}
                </span>
              </div>
            </div>
            <div className="bg-tesla-dark/20 rounded-lg p-2 border border-tesla-border/30">
              <ResponsiveContainer width="100%" height={120}>
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="speedGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" opacity={0.3} />
                  <XAxis 
                    dataKey="timestamp" 
                    className="text-xs"
                    tick={{ fill: '#6b7280', fontSize: 10 }}
                    tickFormatter={(value) => value.split(':').slice(1).join(':')}
                    stroke="#2a2a2a"
                  />
                  <YAxis 
                    className="text-xs"
                    tick={{ fill: '#6b7280', fontSize: 10 }}
                    domain={[0, 120]}
                    stroke="#2a2a2a"
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey="speed"
                    stroke="#3b82f6"
                    strokeWidth={2}
                    fill="url(#speedGradient)"
                    isAnimationActive={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          {/* Acceleration Chart */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Acceleration (m/s²)
              </h3>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-tesla-success" />
                <span className="text-xs text-gray-600 dark:text-gray-400">
                  {drivingData?.acceleration?.toFixed(2) || '--'}
                </span>
              </div>
            </div>
            <div className="bg-tesla-dark/20 rounded-lg p-2 border border-tesla-border/30">
              <ResponsiveContainer width="100%" height={120}>
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="accelGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10b981" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#10b981" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" opacity={0.3} />
                  <XAxis 
                    dataKey="timestamp" 
                    className="text-xs"
                    tick={{ fill: '#6b7280', fontSize: 10 }}
                    tickFormatter={(value) => value.split(':').slice(1).join(':')}
                    stroke="#2a2a2a"
                  />
                  <YAxis 
                    className="text-xs"
                    tick={{ fill: '#6b7280', fontSize: 10 }}
                    domain={[-5, 5]}
                    stroke="#2a2a2a"
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey="acceleration"
                    stroke="#10b981"
                    strokeWidth={2}
                    fill="url(#accelGradient)"
                    isAnimationActive={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
          
          {/* Braking Chart */}
          <div>
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300">
                Braking Intensity
              </h3>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 rounded-full bg-tesla-danger" />
                <span className="text-xs text-gray-600 dark:text-gray-400">
                  {drivingData?.braking_intensity?.toFixed(2) || '--'}
                </span>
              </div>
            </div>
            <div className="bg-tesla-dark/20 rounded-lg p-2 border border-tesla-border/30">
              <ResponsiveContainer width="100%" height={120}>
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="brakeGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ef4444" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#ef4444" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#2a2a2a" opacity={0.3} />
                  <XAxis 
                    dataKey="timestamp" 
                    className="text-xs"
                    tick={{ fill: '#6b7280', fontSize: 10 }}
                    tickFormatter={(value) => value.split(':').slice(1).join(':')}
                    stroke="#2a2a2a"
                  />
                  <YAxis 
                    className="text-xs"
                    tick={{ fill: '#6b7280', fontSize: 10 }}
                    domain={[0, 1]}
                    stroke="#2a2a2a"
                  />
                  <Tooltip content={<CustomTooltip />} />
                  <Area
                    type="monotone"
                    dataKey="braking"
                    stroke="#ef4444"
                    strokeWidth={2}
                    fill="url(#brakeGradient)"
                    isAnimationActive={false}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default TelemetryCharts
