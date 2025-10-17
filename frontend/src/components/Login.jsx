import { useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { Activity, User, Mail, Car, Fuel, ArrowRight } from 'lucide-react'

function Login() {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    name: '',
    car: '',
    model: '',
    fuelType: ''
  })

  const [errors, setErrors] = useState({})

  const fuelTypes = ['Petrol', 'Diesel', 'Electric', 'Hybrid', 'CNG', 'LPG']

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required'
    }
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email'
    }
    
    if (!formData.name.trim()) {
      newErrors.name = 'Name is required'
    }
    
    if (!formData.car.trim()) {
      newErrors.car = 'Car brand is required'
    }
    
    if (!formData.model.trim()) {
      newErrors.model = 'Car model is required'
    }
    
    if (!formData.fuelType) {
      newErrors.fuelType = 'Fuel type is required'
    }
    
    return newErrors
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const newErrors = validateForm()
    
    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors)
      return
    }
    
    // Store user data in localStorage
    localStorage.setItem('userData', JSON.stringify(formData))
    
    // Navigate to dashboard
    navigate('/dashboard')
  }

  const containerVariants = {
    hidden: { opacity: 0, y: 50 },
    visible: {
      opacity: 1,
      y: 0,
      transition: {
        duration: 0.6,
        staggerChildren: 0.1
      }
    }
  }

  const itemVariants = {
    hidden: { opacity: 0, x: -20 },
    visible: {
      opacity: 1,
      x: 0,
      transition: { duration: 0.4 }
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-blue-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center px-4 py-8">
      <motion.div
        className="max-w-2xl w-full"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div
            className="flex justify-center mb-4"
            initial={{ scale: 0, rotate: -180 }}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ type: 'spring', stiffness: 260, damping: 20 }}
          >
            <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-blue-700 rounded-xl flex items-center justify-center shadow-lg">
              <Activity className="text-white" size={32} />
            </div>
          </motion.div>
          
          <motion.h1
            className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-blue-900 bg-clip-text text-transparent mb-2"
            variants={itemVariants}
          >
            Welcome to Auralis.ai
          </motion.h1>
          
          <motion.p
            className="text-gray-600 dark:text-gray-300"
            variants={itemVariants}
          >
            Please enter your details to get started
          </motion.p>
        </div>

        {/* Form */}
        <motion.form
          onSubmit={handleSubmit}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8 space-y-6"
          variants={itemVariants}
        >
          {/* Username */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              <User className="inline mr-2" size={16} />
              Username
            </label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleChange}
              className={`w-full px-4 py-3 rounded-lg border ${
                errors.username 
                  ? 'border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'
              } focus:ring-2 focus:border-transparent dark:bg-gray-700 dark:text-white transition-colors`}
              placeholder="Enter your username"
            />
            {errors.username && (
              <p className="text-red-500 text-sm mt-1">{errors.username}</p>
            )}
          </div>

          {/* Email */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              <Mail className="inline mr-2" size={16} />
              Email
            </label>
            <input
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              className={`w-full px-4 py-3 rounded-lg border ${
                errors.email 
                  ? 'border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'
              } focus:ring-2 focus:border-transparent dark:bg-gray-700 dark:text-white transition-colors`}
              placeholder="your.email@example.com"
            />
            {errors.email && (
              <p className="text-red-500 text-sm mt-1">{errors.email}</p>
            )}
          </div>

          {/* Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              <User className="inline mr-2" size={16} />
              Full Name
            </label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className={`w-full px-4 py-3 rounded-lg border ${
                errors.name 
                  ? 'border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'
              } focus:ring-2 focus:border-transparent dark:bg-gray-700 dark:text-white transition-colors`}
              placeholder="Enter your full name"
            />
            {errors.name && (
              <p className="text-red-500 text-sm mt-1">{errors.name}</p>
            )}
          </div>

          {/* Car Brand */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              <Car className="inline mr-2" size={16} />
              Car Brand
            </label>
            <input
              type="text"
              name="car"
              value={formData.car}
              onChange={handleChange}
              className={`w-full px-4 py-3 rounded-lg border ${
                errors.car 
                  ? 'border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'
              } focus:ring-2 focus:border-transparent dark:bg-gray-700 dark:text-white transition-colors`}
              placeholder="e.g., Toyota, Honda, Tesla"
            />
            {errors.car && (
              <p className="text-red-500 text-sm mt-1">{errors.car}</p>
            )}
          </div>

          {/* Car Model */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              <Car className="inline mr-2" size={16} />
              Car Model
            </label>
            <input
              type="text"
              name="model"
              value={formData.model}
              onChange={handleChange}
              className={`w-full px-4 py-3 rounded-lg border ${
                errors.model 
                  ? 'border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'
              } focus:ring-2 focus:border-transparent dark:bg-gray-700 dark:text-white transition-colors`}
              placeholder="e.g., Camry, Civic, Model 3"
            />
            {errors.model && (
              <p className="text-red-500 text-sm mt-1">{errors.model}</p>
            )}
          </div>

          {/* Fuel Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-2">
              <Fuel className="inline mr-2" size={16} />
              Fuel Type
            </label>
            <select
              name="fuelType"
              value={formData.fuelType}
              onChange={handleChange}
              className={`w-full px-4 py-3 rounded-lg border ${
                errors.fuelType 
                  ? 'border-red-500 focus:ring-red-500' 
                  : 'border-gray-300 dark:border-gray-600 focus:ring-blue-500'
              } focus:ring-2 focus:border-transparent dark:bg-gray-700 dark:text-white transition-colors`}
            >
              <option value="">Select fuel type</option>
              {fuelTypes.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
            {errors.fuelType && (
              <p className="text-red-500 text-sm mt-1">{errors.fuelType}</p>
            )}
          </div>

          {/* Submit Button */}
          <motion.button
            type="submit"
            className="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white py-4 rounded-lg font-semibold shadow-lg flex items-center justify-center gap-2"
            whileHover={{ scale: 1.02, boxShadow: '0 10px 30px rgba(59, 130, 246, 0.3)' }}
            whileTap={{ scale: 0.98 }}
          >
            Start Your Journey
            <ArrowRight size={20} />
          </motion.button>
        </motion.form>

        {/* Back to Welcome */}
        <motion.div
          className="text-center mt-6"
          variants={itemVariants}
        >
          <button
            onClick={() => navigate('/')}
            className="text-blue-600 dark:text-blue-400 hover:underline"
          >
            ← Back to Welcome
          </button>
        </motion.div>
      </motion.div>
    </div>
  )
}

export default Login
