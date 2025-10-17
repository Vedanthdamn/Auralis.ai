import { useState, useEffect } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { TrendingUp } from 'lucide-react'

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
  
  return (
    <div className="card h-full">
      <div className="flex items-center space-x-2 mb-4">
        <TrendingUp className="text-primary-600 dark:text-primary-400" size={24} />
        <h2 className="text-xl font-semibold">Real-Time Telemetry</h2>
      </div>
      
      <div className="space-y-6">
        {/* Speed Chart */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Speed (km/h)
          </h3>
          <ResponsiveContainer width="100%" height={150}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
              <XAxis 
                dataKey="timestamp" 
                className="text-xs"
                tick={{ fill: 'currentColor' }}
                tickFormatter={(value) => value.split(':').slice(1).join(':')}
              />
              <YAxis 
                className="text-xs"
                tick={{ fill: 'currentColor' }}
                domain={[0, 120]}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0, 0, 0, 0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="speed" 
                stroke="#3b82f6" 
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        {/* Acceleration Chart */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Acceleration (m/s²)
          </h3>
          <ResponsiveContainer width="100%" height={150}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
              <XAxis 
                dataKey="timestamp" 
                className="text-xs"
                tick={{ fill: 'currentColor' }}
                tickFormatter={(value) => value.split(':').slice(1).join(':')}
              />
              <YAxis 
                className="text-xs"
                tick={{ fill: 'currentColor' }}
                domain={[-5, 5]}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0, 0, 0, 0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="acceleration" 
                stroke="#10b981" 
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
        
        {/* Braking Chart */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Braking Intensity
          </h3>
          <ResponsiveContainer width="100%" height={150}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-gray-300 dark:stroke-gray-700" />
              <XAxis 
                dataKey="timestamp" 
                className="text-xs"
                tick={{ fill: 'currentColor' }}
                tickFormatter={(value) => value.split(':').slice(1).join(':')}
              />
              <YAxis 
                className="text-xs"
                tick={{ fill: 'currentColor' }}
                domain={[0, 1]}
              />
              <Tooltip 
                contentStyle={{ 
                  backgroundColor: 'rgba(0, 0, 0, 0.8)', 
                  border: 'none', 
                  borderRadius: '8px',
                  color: '#fff'
                }}
              />
              <Line 
                type="monotone" 
                dataKey="braking" 
                stroke="#ef4444" 
                strokeWidth={2}
                dot={false}
                isAnimationActive={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default TelemetryCharts
