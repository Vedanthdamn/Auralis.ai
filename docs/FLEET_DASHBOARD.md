# Fleet Dashboard - Setup Guide

The Fleet Dashboard extends Auralis.ai to support fleet operators like Uber and Ola, providing multi-driver/car tracking with AI-powered insights.

## Features

- **Real-time Fleet Monitoring**: Track multiple drivers and vehicles simultaneously
- **Driver Rankings**: Leaderboard showing driver performance and safety scores
- **AI-Powered Feedback**: Individual driver feedback using Mistral 7B via Ollama
- **Fleet Insights**: AI-generated fleet-level analytics and recommendations
- **Dark Mode Support**: Consistent with personal dashboard styling
- **Scalable Design**: Easy to add more drivers and vehicles

## Quick Start

### 1. Database Setup

The fleet dashboard requires additional database tables. If you're using Supabase:

1. Log in to your Supabase project
2. Go to SQL Editor
3. Run the SQL commands from `docs/fleet_database_schema.md`

Key tables to create:
- `drivers` - Driver profile information
- `vehicles` - Vehicle information
- `driver_stats` - Materialized view for performance (optional but recommended)

### 2. Generate Sample Data

To test the fleet dashboard with sample data:

```bash
# Make sure the backend is running first
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn main:app --reload

# In another terminal, generate sample data
cd scripts
python generate_fleet_data.py --drivers 5 --sessions 10
```

Options:
- `--drivers N`: Number of drivers to create (default: 5, max: 10)
- `--sessions M`: Number of sessions per driver (default: 10)

The script will:
- Create 5 drivers with different driving behaviors (excellent, good, average, poor)
- Generate 10 trips per driver with realistic telemetry data
- Send data to the backend API to populate the database

### 3. Configure Ollama (Optional but Recommended)

For AI-powered feedback using Mistral 7B:

```bash
# Install Ollama (if not already installed)
# Visit https://ollama.ai for installation instructions

# Pull the Mistral model
ollama pull mistral

# Start Ollama service
ollama serve
```

The system will automatically use Mistral for:
- Per-driver performance feedback
- Fleet-level insights and recommendations

If Ollama is not available, the system falls back to rule-based feedback.

### 4. Access the Fleet Dashboard

Start the frontend (if not already running):

```bash
cd frontend
npm run dev
```

Navigate to:
```
http://localhost:3000/dashboard/fleet
```

## Dashboard Components

### Fleet Statistics
Top-level overview showing:
- Total number of drivers
- Total trips completed
- Average fleet score
- Safest driver

### Fleet Insights
AI-generated insights about:
- Overall fleet performance
- Trends and patterns
- Drivers needing attention
- Recommendations for improvement

### Driver Rankings
Sortable list of all drivers showing:
- Ranking position (with medals for top 3)
- Driver name and ID
- Average safety score
- Total trip count
- Expandable cards with detailed stats

### Driver Details (Expanded View)
When you click on a driver card, you'll see:
- Best and worst scores
- Last trip date
- AI-powered personalized feedback
- Performance trends

## Navigation

The header includes navigation buttons to switch between:
- **Personal Dashboard** (`/dashboard`) - Single driver view with real-time telemetry
- **Fleet Dashboard** (`/dashboard/fleet`) - Multi-driver overview

Both dashboards:
- Share the same dark mode setting
- Use the same backend API
- Have consistent styling and animations

## API Endpoints

The fleet dashboard uses the following endpoints:

### Fleet Summary
```
GET /api/fleet/summary
```
Returns fleet-level statistics (total drivers, trips, average score, etc.)

### List Drivers
```
GET /api/fleet/drivers
```
Returns all drivers with their stats and rankings

### Driver Details
```
GET /api/fleet/drivers/{driver_id}
```
Returns detailed information for a specific driver

### Driver Feedback
```
POST /api/fleet/drivers/{driver_id}/feedback
```
Generates AI feedback for a specific driver

### Fleet Insights
```
GET /api/fleet/insights
```
Returns AI-generated fleet-level insights

## Customization

### Adding More Drivers

To add a new driver to the fleet:

1. **Via SQL** (if using Supabase):
```sql
INSERT INTO drivers (driver_id, name, email, phone, license_number)
VALUES ('DRV011', 'New Driver', 'email@example.com', '+1-555-0111', 'DL11111111');
```

2. **Via Script**: Edit `scripts/generate_fleet_data.py` and add to `DRIVER_PROFILES`

3. **Via API**: Create a session with a new `driver_id`:
```python
import requests

response = requests.post('http://localhost:8000/api/session', json={
    'driver_id': 'DRV011',
    'vehicle_id': 'VEH001'
})
```

### Configuring AI Model

To use a different Ollama model:

1. Edit `backend/services/ml_service.py`
2. Change the model name in the Ollama API calls:
```python
"model": "mistral",  # Change to "llama2" or other model
```

3. Make sure to pull the model first:
```bash
ollama pull your-model-name
```

## Troubleshooting

### Database Not Configured Error
**Symptom**: API returns "Database not configured"

**Solution**: 
1. Check `.env` file has valid Supabase credentials
2. Ensure database tables are created (run SQL from `docs/fleet_database_schema.md`)

### No Driver Data Available
**Symptom**: Fleet dashboard shows "No driver data available"

**Solution**:
1. Run the sample data generator: `python scripts/generate_fleet_data.py`
2. Or manually create driving sessions with `driver_id` set

### AI Feedback Not Working
**Symptom**: Feedback shows "Unable to generate feedback"

**Solution**:
1. Check if Ollama is running: `curl http://localhost:11434/api/tags`
2. Verify Mistral model is installed: `ollama list`
3. Check backend logs for Ollama connection errors

### Personal Dashboard Not Working
**Important**: The personal dashboard should remain completely unchanged. If you experience issues:
1. The personal dashboard is at `/dashboard` (without `/fleet`)
2. It uses the same backend but doesn't require fleet data
3. Check WebSocket connection for real-time updates

## Performance Considerations

The fleet dashboard is designed to scale, but keep these in mind:

- **Database Queries**: Use materialized views for fleets with >50 drivers
- **Refresh Rate**: Data auto-refreshes every 30 seconds
- **AI Feedback**: Generated on-demand to avoid overwhelming Ollama
- **Memory**: Each driver card with feedback uses ~100KB, plan accordingly

## Development

To extend the fleet dashboard:

1. **Backend**: Add new endpoints in `backend/app/routes.py`
2. **Frontend**: Create new components in `frontend/src/components/`
3. **Database**: Extend schema in `docs/fleet_database_schema.md`
4. **AI**: Modify prompts in `backend/services/ml_service.py`

## Support

For issues or questions:
- Check the main README.md for general setup
- Review API documentation at http://localhost:8000/docs (when backend is running)
- See backend logs for detailed error messages

## Future Enhancements

Planned features:
- [ ] Historical performance trends
- [ ] Driver-to-driver comparisons
- [ ] Automated alerts for safety issues
- [ ] Export reports (PDF/CSV)
- [ ] Real-time driver location tracking
- [ ] Integration with telematics devices
