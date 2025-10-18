import { motion } from 'framer-motion'
import ScoreDisplay from './ScoreDisplay'
import TelemetryCharts from './TelemetryCharts'
import FeedbackPanel from './FeedbackPanel'
import RealTimeMetrics from './RealTimeMetrics'

function Dashboard({ drivingData, score, feedback }) {
  return (
    <div className="space-y-6">
      {/* Real-time Metrics Cards - NEW */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <RealTimeMetrics drivingData={drivingData} />
      </motion.div>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Score Display - Takes 1 column */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <ScoreDisplay score={score} />
        </motion.div>
        
        {/* Telemetry Charts - Takes 2 columns */}
        <motion.div
          className="lg:col-span-2"
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <TelemetryCharts drivingData={drivingData} />
        </motion.div>
      </div>
      
      {/* Feedback Panel */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
      >
        <FeedbackPanel feedback={feedback} />
      </motion.div>
    </div>
  )
}

export default Dashboard
