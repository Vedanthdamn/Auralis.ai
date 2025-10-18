import { motion, AnimatePresence } from 'framer-motion'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  FileText, 
  Settings, 
  X,
  Activity,
  Map
} from 'lucide-react'

function Sidebar({ isOpen, onClose }) {
  const location = useLocation()
  
  const menuItems = [
    { 
      path: '/dashboard', 
      icon: LayoutDashboard, 
      label: 'Personal Dashboard',
      description: 'Individual driver monitoring'
    },
    { 
      path: '/dashboard/fleet', 
      icon: Users, 
      label: 'Fleet Dashboard',
      description: 'Multi-vehicle tracking'
    },
    { 
      path: '/dashboard/map', 
      icon: Map, 
      label: 'Live Map',
      description: 'Real-time fleet locations'
    },
    { 
      path: '/logs', 
      icon: FileText, 
      label: 'Activity Logs',
      description: 'View system logs'
    },
    { 
      path: '/analytics', 
      icon: Activity, 
      label: 'Analytics',
      description: 'Performance insights'
    },
    { 
      path: '/settings', 
      icon: Settings, 
      label: 'Settings',
      description: 'Configure preferences'
    },
  ]
  
  const isActive = (path) => location.pathname === path
  
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40 lg:hidden"
          />
          
          {/* Sidebar */}
          <motion.aside
            initial={{ x: -300 }}
            animate={{ x: 0 }}
            exit={{ x: -300 }}
            transition={{ type: 'spring', damping: 25, stiffness: 200 }}
            className="sidebar"
          >
            {/* Header */}
            <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-tesla-border/50">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-tesla-accent to-tesla-cyan 
                              flex items-center justify-center">
                  <Activity className="text-white" size={24} />
                </div>
                <div>
                  <h2 className="text-xl font-bold bg-gradient-to-r from-tesla-accent to-tesla-cyan 
                               bg-clip-text text-transparent">
                    Auralis.ai
                  </h2>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    Driver Safety System
                  </p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-tesla-border/30
                         transition-colors"
              >
                <X size={20} />
              </button>
            </div>
            
            {/* Menu Items */}
            <nav className="flex-1 overflow-y-auto py-6">
              {menuItems.map((item) => {
                const Icon = item.icon
                const active = isActive(item.path)
                
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={onClose}
                    className={`sidebar-item ${active ? 'active' : ''}`}
                  >
                    <Icon size={20} />
                    <div className="flex-1">
                      <div className="font-medium">{item.label}</div>
                      <div className="text-xs opacity-70">{item.description}</div>
                    </div>
                    {active && (
                      <motion.div
                        layoutId="activeIndicator"
                        className="w-1 h-8 bg-tesla-accent rounded-full absolute right-0"
                      />
                    )}
                  </Link>
                )
              })}
            </nav>
            
            {/* Footer */}
            <div className="p-6 border-t border-gray-200 dark:border-tesla-border/50">
              <div className="card-glass p-4 text-center">
                <div className="text-sm font-medium text-gray-700 dark:text-gray-300">
                  System Status
                </div>
                <div className="flex items-center justify-center space-x-2 mt-2">
                  <div className="w-2 h-2 bg-tesla-success rounded-full animate-pulse" />
                  <span className="text-xs text-tesla-success">All Systems Operational</span>
                </div>
              </div>
            </div>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  )
}

export default Sidebar
