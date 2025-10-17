import { MessageSquare, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'

function FeedbackPanel({ feedback }) {
  return (
    <div className="card">
      <div className="flex items-center space-x-2 mb-4">
        <Sparkles className="text-primary-600 dark:text-primary-400" size={24} />
        <h2 className="text-xl font-semibold">AI-Generated Feedback</h2>
      </div>
      
      <div className="bg-gradient-to-br from-primary-50 to-blue-50 dark:from-gray-700 dark:to-gray-800 rounded-lg p-6 border border-primary-200 dark:border-gray-600">
        {feedback ? (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="space-y-3"
          >
            <div className="flex items-start space-x-3">
              <MessageSquare className="text-primary-600 dark:text-primary-400 mt-1 flex-shrink-0" size={20} />
              <p className="text-gray-700 dark:text-gray-200 leading-relaxed">
                {feedback}
              </p>
            </div>
          </motion.div>
        ) : (
          <div className="text-center text-gray-500 dark:text-gray-400 py-8">
            <MessageSquare className="mx-auto mb-3 opacity-50" size={32} />
            <p>AI feedback will appear here once driving data is received.</p>
            <p className="text-sm mt-2">
              The system analyzes your driving patterns and provides personalized suggestions.
            </p>
          </div>
        )}
      </div>
      
      {feedback && (
        <div className="mt-4 text-xs text-gray-500 dark:text-gray-400 flex items-center space-x-2">
          <Sparkles size={14} />
          <span>Powered by AI Language Model</span>
        </div>
      )}
    </div>
  )
}

export default FeedbackPanel
