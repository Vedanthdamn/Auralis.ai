import { Moon, Sun, Activity, Users, Menu } from 'lucide-react'
import { motion } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'

function Header({ darkMode, setDarkMode, isConnected, showFleetLink = false, onMenuClick }) {
  const location = useLocation()
  
  return (
    <header className="bg-white/80 dark:bg-tesla-gray/80 backdrop-blur-xl shadow-lg border-b border-gray-200 dark:border-tesla-border/50 sticky top-0 z-30">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            {/* Menu Button */}
            {onMenuClick && (
              <button
                onClick={onMenuClick}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-tesla-border/30 transition-colors"
                aria-label="Toggle menu"
              >
                <Menu size={24} />
              </button>
            )}
            
            <motion.div 
              className="flex items-center space-x-3"
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.5 }}
            >
              <div className="w-10 h-10 bg-gradient-to-br from-tesla-accent to-tesla-cyan rounded-xl flex items-center justify-center shadow-lg">
                <Activity className="text-white" size={24} />
              </div>
              <div>
                <h1 className="text-2xl font-bold bg-gradient-to-r from-tesla-accent to-tesla-cyan bg-clip-text text-transparent">
                  Auralis.ai
                </h1>
                <p className="text-xs text-gray-600 dark:text-gray-400">
                  AI-Powered Driver Safety Scoring
                </p>
              </div>
            </motion.div>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* Navigation Links */}
            {showFleetLink && (
              <div className="hidden md:flex items-center space-x-2">
                <Link
                  to="/dashboard"
                  className={`px-4 py-2 rounded-xl font-medium transition-all duration-200 ${
                    location.pathname === '/dashboard'
                      ? 'bg-gradient-to-r from-tesla-accent to-tesla-cyan text-white shadow-lg'
                      : 'bg-gray-200 dark:bg-tesla-gray/60 hover:bg-gray-300 dark:hover:bg-tesla-gray/80 text-gray-900 dark:text-gray-100 border border-gray-300 dark:border-tesla-border/50'
                  }`}
                >
                  <span className="flex items-center space-x-2">
                    <Activity size={18} />
                    <span>Personal</span>
                  </span>
                </Link>
                
                <Link
                  to="/dashboard/fleet"
                  className={`px-4 py-2 rounded-xl font-medium transition-all duration-200 ${
                    location.pathname === '/dashboard/fleet'
                      ? 'bg-gradient-to-r from-tesla-accent to-tesla-cyan text-white shadow-lg'
                      : 'bg-gray-200 dark:bg-tesla-gray/60 hover:bg-gray-300 dark:hover:bg-tesla-gray/80 text-gray-900 dark:text-gray-100 border border-gray-300 dark:border-tesla-border/50'
                  }`}
                >
                  <span className="flex items-center space-x-2">
                    <Users size={18} />
                    <span>Fleet</span>
                  </span>
                </Link>
              </div>
            )}
            
            {/* Connection Status */}
            {isConnected !== undefined && (
              <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-gray-100 dark:bg-tesla-gray/40 border border-gray-200 dark:border-tesla-border/30">
                <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-tesla-success animate-pulse shadow-lg shadow-tesla-success/50' : 'bg-tesla-danger'}`} />
                <span className="text-sm text-gray-600 dark:text-gray-400">
                  {isConnected ? 'Live' : 'Offline'}
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
