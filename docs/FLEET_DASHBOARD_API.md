# Fleet Dashboard API Documentation

## Overview
This document describes the enhanced Fleet Dashboard API endpoints that provide aggregated fleet data, driver statistics, rankings, and AI-powered feedback.

## API Endpoints

### 1. GET /api/fleet/summary
Returns aggregated fleet-level statistics.

**Response:**
```json
{
  "total_drivers": 5,
  "total_trips": 120,
  "fleet_avg_score": 7.5,
  "safest_driver": "John Doe",
  "safest_driver_score": 9.2,
  "most_improved_driver": "Jane Smith",
  "most_improved_score": 8.1,
  "high_performers": 2,
  "average_performers": 2,
  "low_performers": 1
}
```

**Fields:**
- `total_drivers`: Total number of drivers in fleet
- `total_trips`: Combined trip count across all drivers
- `fleet_avg_score`: Average safety score across entire fleet (0-10)
- `safest_driver`: Name of driver with highest average score
- `safest_driver_score`: Highest average score in fleet
- `most_improved_driver`: Driver showing greatest improvement
- `most_improved_score`: Score of most improved driver
- `high_performers`: Count of drivers with score >= 8.0
- `average_performers`: Count of drivers with score 5.0-7.9
- `low_performers`: Count of drivers with score < 5.0

### 2. GET /api/fleet/drivers
Returns list of all drivers with statistics and rankings.

**Query Parameters:**
- `include_feedback` (optional, boolean): Include AI-generated feedback for each driver

**Response:**
```json
{
  "drivers": [
    {
      "driver_id": "DRV001",
      "driver_name": "John Doe",
      "avg_score": 9.2,
      "trip_count": 45,
      "best_score": 9.8,
      "worst_score": 8.5,
      "last_trip_date": "2024-01-15T10:30:00",
      "avg_speed": 62.5,
      "avg_acceleration": 1.2,
      "avg_braking": 0.3,
      "rank": 1
    }
  ],
  "total_count": 5
}
```

**Driver Fields:**
- `driver_id`: Unique driver identifier
- `driver_name`: Driver's full name
- `avg_score`: Average driving safety score (0-10)
- `trip_count`: Total number of trips
- `best_score`: Highest score achieved
- `worst_score`: Lowest score achieved
- `last_trip_date`: ISO timestamp of most recent trip
- `avg_speed`: Average speed in km/h
- `avg_acceleration`: Average acceleration in m/s²
- `avg_braking`: Average braking intensity (0-1)
- `rank`: Driver ranking by avg_score (1 = best)

### 3. GET /api/fleet/insights
Returns AI-generated insights for the entire fleet.

**Response:**
```json
{
  "insights": "Fleet Overview: 5 drivers with 7.5/10 average score...",
  "timestamp": "2025-10-17T20:00:00.000000",
  "fleet_summary": {
    "total_drivers": 5,
    "total_trips": 120,
    "fleet_avg_score": 7.5,
    "safest_driver": "John Doe",
    "safest_driver_score": 9.2
  }
}
```

**Fields:**
- `insights`: Natural language insights about fleet performance
- `timestamp`: ISO timestamp when insights were generated
- `fleet_summary`: Basic fleet statistics

### 4. POST /api/fleet/drivers/{driver_id}/feedback
Generates AI-powered feedback for a specific driver.

**Path Parameters:**
- `driver_id`: Unique driver identifier

**Response:**
```json
{
  "driver_id": "DRV001",
  "driver_name": "John Doe",
  "feedback": "Outstanding performance! Maintaining an average score of 9.2/10...",
  "score": 9.2,
  "timestamp": "2025-10-17T20:00:00.000000"
}
```

**Fields:**
- `driver_id`: Driver identifier
- `driver_name`: Driver's full name
- `feedback`: AI-generated natural language feedback
- `score`: Current average safety score
- `timestamp`: ISO timestamp when feedback was generated

## AI Model Configuration

### Mistral Model Selection
The API uses Ollama with the following model priority:

1. **Primary Model**: `mistral:7b-instruct-q4_0`
   - Quantized 4-bit version (~4.1 GB)
   - Optimized for instruction following
   - Best balance of quality and performance

2. **Fallback Model**: `mistral:latest`
   - Latest stable Mistral release
   - Falls back if q4_0 variant not available

3. **Final Fallback**: `mistral`
   - Generic Mistral model tag
   - Catches any available Mistral variant

If all Ollama models fail, the system falls back to rule-based feedback generation.

**Note**: Model digests (e.g., b17615239298) may vary based on your Ollama installation. The system automatically uses whichever variant is available from the priority list above.

### Rule-Based Fallback
When AI models are unavailable, the system generates feedback using:
- Score thresholds (Excellent: >=8, Good: 6-7.9, Fair: 4-5.9, Poor: <4)
- Specific metrics analysis (speed, braking, acceleration)
- Performance trends (improvement, consistency)

## Data Aggregation

### Driver Statistics
Driver statistics are computed from raw driving events:
- **Average Score**: Mean of all event scores
- **Trip Count**: Number of distinct driving sessions
- **Best/Worst Score**: Maximum and minimum scores achieved
- **Average Metrics**: Mean speed, acceleration, and braking intensity
- **Last Trip**: Most recent session timestamp

### Fleet Summary
Fleet-level metrics aggregate across all drivers:
- **Fleet Average**: Mean of all driver averages
- **Performance Categories**: Drivers grouped by score ranges
- **Top Performers**: Safest driver and most improved driver

## Database Support

### Supabase Integration
When configured, the API queries:
- `drivers` table: Driver profiles
- `sessions` table: Driving sessions
- `events` table: Real-time driving events
- `driver_stats` view: Pre-computed statistics (if available)

### Mock Data Fallback
When Supabase is not configured, the API returns sample data for:
- 5 sample drivers with varied performance levels
- Realistic metrics and scores
- Proper data structure for frontend compatibility

This allows frontend development and testing without database setup.

## Frontend Integration

### React Component Usage
The API is designed for seamless integration with React components:

```javascript
// Fleet Summary
const summaryResponse = await fetch('http://localhost:8000/api/fleet/summary')
const summary = await summaryResponse.json()
// Use with FleetStats component

// Driver List
const driversResponse = await fetch('http://localhost:8000/api/fleet/drivers')
const { drivers } = await driversResponse.json()
// Use with DriverRankings and DriverCard components

// Fleet Insights
const insightsResponse = await fetch('http://localhost:8000/api/fleet/insights')
const { insights } = await insightsResponse.json()
// Use with FleetInsights component

// Individual Driver Feedback
const feedbackResponse = await fetch(
  `http://localhost:8000/api/fleet/drivers/${driverId}/feedback`,
  { method: 'POST' }
)
const feedback = await feedbackResponse.json()
// Display in DriverCard expanded view
```

## Error Handling

### HTTP Status Codes
- `200 OK`: Successful response
- `404 Not Found`: Driver not found
- `500 Internal Server Error`: Server error
- `503 Service Unavailable`: Database not configured (when mock data is disabled)

### Error Response Format
```json
{
  "detail": "Error message description"
}
```

## Testing

### Manual Testing
Use the provided test script:
```bash
cd /tmp
./test_fleet_api.sh
```

### Automated Validation
Run the Python validation script:
```bash
python /tmp/validate_fleet_api.py
```

### Expected Test Results
All endpoints should return:
- Status code 200
- Valid JSON response
- All expected fields present
- Reasonable data values

## Performance Considerations

### Response Times
- `/fleet/summary`: ~10-50ms
- `/fleet/drivers`: ~20-100ms (depends on driver count)
- `/fleet/insights`: ~100-500ms (includes AI generation)
- `/fleet/drivers/{id}/feedback`: ~100-500ms (includes AI generation)

### Optimization Tips
1. Use `include_feedback=false` for faster driver list responses
2. Cache fleet summary on frontend (refresh every 30-60 seconds)
3. Generate driver feedback on-demand (when card is expanded)
4. Use WebSocket for real-time score updates

## Changelog

### Version 1.1 (Current)
- Added Mistral 7B instruct q4_0 model support
- Enhanced fleet summary with performance categorization
- Added most improved driver tracking
- Improved AI feedback quality and consistency
- Added mock data support for development
- Enhanced error handling and fallbacks

### Version 1.0
- Initial fleet dashboard API
- Basic driver statistics and rankings
- Simple rule-based feedback
