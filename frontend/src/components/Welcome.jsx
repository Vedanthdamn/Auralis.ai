import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { Activity, ArrowRight } from 'lucide-react'

function Welcome() {
  const navigate = useNavigate()

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.3,
        delayChildren: 0.2
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        ease: 'easeOut'
      }
    }
  }

  const logoVariants = {
    hidden: { scale: 0, rotate: -180 },
    visible: {
      scale: 1,
      rotate: 0,
      transition: {
        type: 'spring',
        stiffness: 260,
        damping: 20,
        duration: 1
      }
    }
  }

  const buttonVariants = {
    hover: {
      scale: 1.05,
      boxShadow: '0 10px 30px rgba(59, 130, 246, 0.3)',
      transition: {
        duration: 0.2
      }
    },
    tap: {
      scale: 0.95
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center px-4">
      <motion.div
        className="max-w-4xl w-full text-center"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Logo */}
        <motion.div
          className="flex justify-center mb-8"
          variants={logoVariants}
        >
          <div className="w-24 h-24 bg-gradient-to-br from-blue-500 to-blue-700 rounded-2xl flex items-center justify-center shadow-2xl">
            <Activity className="text-white" size={48} strokeWidth={2.5} />
          </div>
        </motion.div>

        {/* Title */}
        <motion.h1
          className="text-6xl md:text-7xl lg:text-8xl font-bold mb-6"
          variants={itemVariants}
        >
          <span className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-900 bg-clip-text text-transparent">
            Auralis.ai
          </span>
        </motion.h1>

        {/* Description */}
        <motion.p
          className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-4 leading-relaxed"
          variants={itemVariants}
        >
          AI-Powered Driver Safety Scoring System
        </motion.p>

        <motion.p
          className="text-lg md:text-xl text-gray-500 dark:text-gray-400 mb-12 max-w-2xl mx-auto"
          variants={itemVariants}
        >
          Experience real-time driving behavior analysis and safety feedback powered by advanced machine learning. 
          Make every journey safer with intelligent insights.
        </motion.p>

        {/* Features */}
        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12"
          variants={itemVariants}
        >
          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
            <div className="text-3xl mb-3">📊</div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-2">Real-time Analysis</h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              Live telemetry tracking and instant safety scoring
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
            <div className="text-3xl mb-3">🤖</div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-2">AI Feedback</h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              Intelligent suggestions to improve your driving
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg">
            <div className="text-3xl mb-3">🚗</div>
            <h3 className="font-semibold text-gray-800 dark:text-white mb-2">Personalized</h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm">
              Customized insights based on your vehicle and driving style
            </p>
          </div>
        </motion.div>

        {/* CTA Button */}
        <motion.button
          onClick={() => navigate('/login')}
          className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-10 py-4 rounded-full text-lg font-semibold shadow-xl flex items-center gap-3 mx-auto"
          variants={buttonVariants}
          whileHover="hover"
          whileTap="tap"
        >
          Get Started
          <ArrowRight size={20} />
        </motion.button>

        {/* Floating particles effect */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
          {[...Array(5)].map((_, i) => (
            <motion.div
              key={i}
              className="absolute w-2 h-2 bg-blue-400 rounded-full opacity-20"
              style={{
                left: `${20 + i * 15}%`,
                top: `${30 + i * 10}%`
              }}
              animate={{
                y: [0, -30, 0],
                opacity: [0.2, 0.5, 0.2]
              }}
              transition={{
                duration: 3 + i,
                repeat: Infinity,
                ease: 'easeInOut'
              }}
            />
          ))}
        </div>
      </motion.div>
    </div>
  )
}

export default Welcome
