import { Moon, Sun, Activity, Users } from 'lucide-react'
import { motion } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'

function Header({ darkMode, setDarkMode, isConnected, showFleetLink = false }) {
  const location = useLocation()
  
  return (
    <header className="bg-white dark:bg-gray-800 shadow-md border-b border-gray-200 dark:border-gray-700">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <motion.div 
            className="flex items-center space-x-3"
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-700 rounded-lg flex items-center justify-center">
              <Activity className="text-white" size={24} />
            </div>
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 bg-clip-text text-transparent">
                Auralis.ai
              </h1>
              <p className="text-xs text-gray-600 dark:text-gray-400">
                AI-Powered Driver Safety Scoring
              </p>
            </div>
          </motion.div>
          
          <div className="flex items-center space-x-4">
            {/* Navigation Links */}
            {showFleetLink && (
              <div className="flex items-center space-x-2">
                <Link
                  to="/dashboard"
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    location.pathname === '/dashboard'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100'
                  }`}
                >
                  <span className="flex items-center space-x-2">
                    <Activity size={18} />
                    <span className="hidden sm:inline">Personal</span>
                  </span>
                </Link>
                
                <Link
                  to="/dashboard/fleet"
                  className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                    location.pathname === '/dashboard/fleet'
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100'
                  }`}
                >
                  <span className="flex items-center space-x-2">
                    <Users size={18} />
                    <span className="hidden sm:inline">Fleet</span>
                  </span>
                </Link>
              </div>
            )}
            
            {/* Connection Status */}
            {isConnected !== undefined && (
              <div className="flex items-center space-x-2">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`} />
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {isConnected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
            )}
            
            {/* Dark Mode Toggle */}
            <button
              onClick={() => setDarkMode(!darkMode)}
              className="btn btn-secondary flex items-center space-x-2"
              aria-label="Toggle dark mode"
            >
              {darkMode ? <Sun size={18} /> : <Moon size={18} />}
              <span className="hidden sm:inline">
                {darkMode ? 'Light' : 'Dark'}
              </span>
            </button>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
