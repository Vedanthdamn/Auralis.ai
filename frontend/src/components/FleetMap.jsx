import { useEffect, useRef, useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet'
import { motion } from 'framer-motion'
import { Map as MapIcon, Navigation } from 'lucide-react'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

// Fix for default marker icons in React-Leaflet
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
})

// Mock fleet data generator
const generateMockFleetData = () => {
  const baseLocation = { lat: 37.7749, lng: -122.4194 } // San Francisco
  
  return Array.from({ length: 12 }, (_, i) => ({
    id: `vehicle-${i + 1}`,
    driverId: `driver-${i + 1}`,
    driverName: `Driver ${i + 1}`,
    position: {
      lat: baseLocation.lat + (Math.random() - 0.5) * 0.1,
      lng: baseLocation.lng + (Math.random() - 0.5) * 0.1,
    },
    speed: Math.random() * 100,
    score: 5 + Math.random() * 5,
    status: ['active', 'idle', 'warning'][Math.floor(Math.random() * 3)],
    heading: Math.random() * 360,
  }))
}

function FleetMap({ fleetData }) {
  const [vehicles, setVehicles] = useState([])
  const [center] = useState({ lat: 37.7749, lng: -122.4194 })
  const mapRef = useRef(null)
  
  useEffect(() => {
    // Use real fleet data if available, otherwise use mock data
    if (fleetData && fleetData.vehicles) {
      setVehicles(fleetData.vehicles)
    } else {
      // Generate mock data and update periodically
      setVehicles(generateMockFleetData())
      
      const interval = setInterval(() => {
        setVehicles(prevVehicles => 
          prevVehicles.map(v => ({
            ...v,
            position: {
              lat: v.position.lat + (Math.random() - 0.5) * 0.001,
              lng: v.position.lng + (Math.random() - 0.5) * 0.001,
            },
            speed: Math.max(0, v.speed + (Math.random() - 0.5) * 5),
            score: Math.max(0, Math.min(10, v.score + (Math.random() - 0.5) * 0.5)),
          }))
        )
      }, 3000)
      
      return () => clearInterval(interval)
    }
  }, [fleetData])
  
  const getMarkerColor = (status, score) => {
    if (status === 'warning' || score < 5) return '#ef4444' // red
    if (status === 'idle') return '#f59e0b' // orange
    return '#10b981' // green
  }
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card-glass h-full"
    >
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-2 rounded-lg bg-gradient-to-br from-tesla-accent/20 to-tesla-cyan/20">
            <MapIcon className="text-tesla-accent" size={24} />
          </div>
          <div>
            <h2 className="text-xl font-semibold">Live Fleet Map</h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {vehicles.length} vehicles tracked
            </p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-tesla-success rounded-full animate-pulse" />
          <span className="text-sm text-gray-600 dark:text-gray-400">Live</span>
        </div>
      </div>
      
      <div className="relative h-[500px] rounded-xl overflow-hidden border border-gray-200 dark:border-tesla-border/50">
        <MapContainer
          center={[center.lat, center.lng]}
          zoom={12}
          className="h-full w-full"
          ref={mapRef}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          
          {vehicles.map((vehicle) => (
            <CircleMarker
              key={vehicle.id}
              center={[vehicle.position.lat, vehicle.position.lng]}
              radius={8}
              fillColor={getMarkerColor(vehicle.status, vehicle.score)}
              color="white"
              weight={2}
              opacity={1}
              fillOpacity={0.8}
            >
              <Popup>
                <div className="p-2 min-w-[200px]">
                  <div className="font-bold text-lg mb-2">{vehicle.driverName}</div>
                  <div className="space-y-1 text-sm">
                    <div className="flex justify-between">
                      <span className="text-gray-600">Vehicle:</span>
                      <span className="font-medium">{vehicle.id}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Speed:</span>
                      <span className="font-medium">{vehicle.speed.toFixed(1)} km/h</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Score:</span>
                      <span className={`font-medium ${
                        vehicle.score >= 7 ? 'text-green-600' : 
                        vehicle.score >= 5 ? 'text-yellow-600' : 
                        'text-red-600'
                      }`}>
                        {vehicle.score.toFixed(1)}/10
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-gray-600">Status:</span>
                      <span className={`font-medium capitalize ${
                        vehicle.status === 'active' ? 'text-green-600' : 
                        vehicle.status === 'idle' ? 'text-yellow-600' : 
                        'text-red-600'
                      }`}>
                        {vehicle.status}
                      </span>
                    </div>
                  </div>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
        
        {/* Legend */}
        <div className="absolute bottom-4 right-4 bg-white dark:bg-tesla-gray/95 backdrop-blur-md 
                      rounded-lg p-3 shadow-lg border border-gray-200 dark:border-tesla-border/50">
          <div className="text-xs font-semibold mb-2 text-gray-700 dark:text-gray-300">Status</div>
          <div className="space-y-1">
            <div className="flex items-center space-x-2 text-xs">
              <div className="w-3 h-3 bg-tesla-success rounded-full" />
              <span className="text-gray-600 dark:text-gray-400">Active</span>
            </div>
            <div className="flex items-center space-x-2 text-xs">
              <div className="w-3 h-3 bg-tesla-warning rounded-full" />
              <span className="text-gray-600 dark:text-gray-400">Idle</span>
            </div>
            <div className="flex items-center space-x-2 text-xs">
              <div className="w-3 h-3 bg-tesla-danger rounded-full" />
              <span className="text-gray-600 dark:text-gray-400">Warning</span>
            </div>
          </div>
        </div>
      </div>
      
      {/* Fleet summary */}
      <div className="grid grid-cols-3 gap-4 mt-4">
        <div className="text-center p-3 rounded-lg bg-gradient-to-br from-tesla-success/10 to-tesla-success/5 
                      border border-tesla-success/20">
          <div className="text-2xl font-bold text-tesla-success">
            {vehicles.filter(v => v.status === 'active').length}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Active</div>
        </div>
        <div className="text-center p-3 rounded-lg bg-gradient-to-br from-tesla-warning/10 to-tesla-warning/5 
                      border border-tesla-warning/20">
          <div className="text-2xl font-bold text-tesla-warning">
            {vehicles.filter(v => v.status === 'idle').length}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Idle</div>
        </div>
        <div className="text-center p-3 rounded-lg bg-gradient-to-br from-tesla-danger/10 to-tesla-danger/5 
                      border border-tesla-danger/20">
          <div className="text-2xl font-bold text-tesla-danger">
            {vehicles.filter(v => v.status === 'warning').length}
          </div>
          <div className="text-xs text-gray-600 dark:text-gray-400 mt-1">Warning</div>
        </div>
      </div>
    </motion.div>
  )
}

export default FleetMap
