import { useState, useEffect, useRef, useCallback } from 'react'

export function useWebSocket(url) {
  const [lastMessage, setLastMessage] = useState(null)
  const [connectionStatus, setConnectionStatus] = useState('disconnected')
  const wsRef = useRef(null)
  const reconnectTimeoutRef = useRef(null)
  const reconnectAttemptsRef = useRef(0)
  const maxReconnectAttempts = 5
  const reconnectDelay = 3000
  
  const connect = useCallback(() => {
    try {
      const ws = new WebSocket(url)
      
      ws.onopen = () => {
        console.log('WebSocket connected')
        setConnectionStatus('connected')
        reconnectAttemptsRef.current = 0
      }
      
      ws.onmessage = (event) => {
        setLastMessage(event.data)
      }
      
      ws.onerror = (error) => {
        console.error('WebSocket error:', error)
        setConnectionStatus('error')
      }
      
      ws.onclose = () => {
        console.log('WebSocket disconnected')
        setConnectionStatus('disconnected')
        
        // Attempt to reconnect
        if (reconnectAttemptsRef.current < maxReconnectAttempts) {
          reconnectAttemptsRef.current += 1
          console.log(`Reconnecting... Attempt ${reconnectAttemptsRef.current}`)
          reconnectTimeoutRef.current = setTimeout(() => {
            connect()
          }, reconnectDelay)
        }
      }
      
      wsRef.current = ws
    } catch (error) {
      console.error('Failed to create WebSocket:', error)
      setConnectionStatus('error')
    }
  }, [url])
  
  useEffect(() => {
    connect()
    
    return () => {
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [connect])
  
  const sendMessage = useCallback((message) => {
    if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
      wsRef.current.send(typeof message === 'string' ? message : JSON.stringify(message))
    } else {
      console.warn('WebSocket is not connected')
    }
  }, [])
  
  return {
    sendMessage,
    lastMessage,
    connectionStatus,
  }
}
