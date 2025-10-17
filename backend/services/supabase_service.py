import os
from typing import Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Note: Supabase integration is optional
# If credentials are not provided, the service will gracefully degrade
try:
    from supabase import create_client, Client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    print("⚠️ Supabase client not installed. Database features will be disabled.")

class SupabaseService:
    """
    Service for interacting with Supabase database
    Stores driving sessions, events, scores, and feedback
    """
    
    def __init__(self):
        self.client: Optional[Client] = None
        self.configured = False
        
        if SUPABASE_AVAILABLE:
            self._initialize()
    
    def _initialize(self):
        """Initialize Supabase client"""
        url = os.getenv('SUPABASE_URL')
        key = os.getenv('SUPABASE_KEY')
        
        if url and key and url != 'your_supabase_url_here':
            try:
                self.client = create_client(url, key)
                self.configured = True
                print("✅ Supabase client initialized")
            except Exception as e:
                print(f"❌ Failed to initialize Supabase: {e}")
        else:
            print("⚠️ Supabase credentials not configured. Database features disabled.")
    
    def is_configured(self) -> bool:
        """Check if Supabase is properly configured"""
        return self.configured
    
    async def create_session(self, session_id: str, driver_id: Optional[str] = None, 
                            vehicle_id: Optional[str] = None):
        """Create a new driving session"""
        if not self.configured:
            return None
        
        try:
            data = {
                'session_id': session_id,
                'driver_id': driver_id,
                'vehicle_id': vehicle_id,
                'start_time': datetime.utcnow().isoformat(),
            }
            
            result = self.client.table('sessions').insert(data).execute()
            return result.data
        except Exception as e:
            print(f"Error creating session: {e}")
            raise
    
    async def store_event(self, driving_data, score: float, session_id: Optional[str] = None):
        """Store a driving event with score"""
        if not self.configured:
            return None
        
        try:
            event_data = {
                'session_id': session_id,
                'timestamp': driving_data.timestamp.isoformat(),
                'speed': driving_data.speed,
                'acceleration': driving_data.acceleration,
                'braking_intensity': driving_data.braking_intensity,
                'steering_angle': driving_data.steering_angle,
                'jerk': driving_data.jerk,
                'score': score,
            }
            
            result = self.client.table('events').insert(event_data).execute()
            return result.data
        except Exception as e:
            print(f"Error storing event: {e}")
            raise
    
    async def store_feedback(self, session_id: str, feedback: str, score: float):
        """Store AI-generated feedback"""
        if not self.configured:
            return None
        
        try:
            data = {
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat(),
                'feedback': feedback,
                'score': score,
            }
            
            result = self.client.table('feedback').insert(data).execute()
            return result.data
        except Exception as e:
            print(f"Error storing feedback: {e}")
            raise
    
    async def get_session(self, session_id: str):
        """Get session details and events"""
        if not self.configured:
            raise Exception("Supabase not configured")
        
        try:
            # Get session info
            session = self.client.table('sessions').select('*').eq('session_id', session_id).execute()
            
            # Get events for this session
            events = self.client.table('events').select('*').eq('session_id', session_id).order('timestamp').execute()
            
            # Get feedback for this session
            feedback = self.client.table('feedback').select('*').eq('session_id', session_id).order('timestamp').execute()
            
            return {
                'session': session.data[0] if session.data else None,
                'events': events.data,
                'feedback': feedback.data,
            }
        except Exception as e:
            print(f"Error getting session: {e}")
            raise
    
    # Fleet Management Methods
    
    async def create_driver(self, driver_id: str, name: str, email: Optional[str] = None,
                           phone: Optional[str] = None, license_number: Optional[str] = None):
        """Create a new driver profile"""
        if not self.configured:
            return None
        
        try:
            data = {
                'driver_id': driver_id,
                'name': name,
                'email': email,
                'phone': phone,
                'license_number': license_number,
            }
            
            result = self.client.table('drivers').insert(data).execute()
            return result.data
        except Exception as e:
            print(f"Error creating driver: {e}")
            raise
    
    async def get_driver(self, driver_id: str):
        """Get driver profile"""
        if not self.configured:
            raise Exception("Supabase not configured")
        
        try:
            result = self.client.table('drivers').select('*').eq('driver_id', driver_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error getting driver: {e}")
            raise
    
    async def get_all_drivers(self):
        """Get all driver profiles"""
        if not self.configured:
            raise Exception("Supabase not configured")
        
        try:
            result = self.client.table('drivers').select('*').order('name').execute()
            return result.data
        except Exception as e:
            print(f"Error getting drivers: {e}")
            raise
    
    async def get_driver_stats(self, driver_id: Optional[str] = None):
        """Get driver statistics (from materialized view or computed)"""
        if not self.configured:
            raise Exception("Supabase not configured")
        
        try:
            # Try to query materialized view first (if it exists)
            try:
                query = self.client.table('driver_stats').select('*')
                if driver_id:
                    query = query.eq('driver_id', driver_id)
                result = query.execute()
                return result.data
            except:
                # Fall back to computing stats from raw data
                return await self._compute_driver_stats(driver_id)
        except Exception as e:
            print(f"Error getting driver stats: {e}")
            raise
    
    async def _compute_driver_stats(self, driver_id: Optional[str] = None):
        """Compute driver statistics from raw data"""
        if not self.configured:
            return []
        
        try:
            # Get all sessions with events
            query = self.client.table('sessions').select('*, events(score, speed, acceleration, braking_intensity)')
            if driver_id:
                query = query.eq('driver_id', driver_id)
            
            sessions = query.execute()
            
            # Aggregate stats per driver
            driver_stats = {}
            for session in sessions.data:
                did = session.get('driver_id')
                if not did:
                    continue
                
                if did not in driver_stats:
                    driver_stats[did] = {
                        'driver_id': did,
                        'trip_count': 0,
                        'scores': [],
                        'speeds': [],
                        'accelerations': [],
                        'braking_intensities': [],
                        'last_trip': session.get('start_time')
                    }
                
                driver_stats[did]['trip_count'] += 1
                
                # Aggregate event data
                events = session.get('events', [])
                for event in events:
                    if event.get('score') is not None:
                        driver_stats[did]['scores'].append(event['score'])
                    if event.get('speed') is not None:
                        driver_stats[did]['speeds'].append(event['speed'])
                    if event.get('acceleration') is not None:
                        driver_stats[did]['accelerations'].append(event['acceleration'])
                    if event.get('braking_intensity') is not None:
                        driver_stats[did]['braking_intensities'].append(event['braking_intensity'])
            
            # Compute averages
            result = []
            for did, stats in driver_stats.items():
                avg_score = sum(stats['scores']) / len(stats['scores']) if stats['scores'] else 0
                result.append({
                    'driver_id': did,
                    'driver_name': did,  # Would need to join with drivers table for actual name
                    'trip_count': stats['trip_count'],
                    'avg_score': round(avg_score, 2),
                    'best_score': max(stats['scores']) if stats['scores'] else None,
                    'worst_score': min(stats['scores']) if stats['scores'] else None,
                    'last_trip_date': stats['last_trip'],
                    'avg_speed': round(sum(stats['speeds']) / len(stats['speeds']), 2) if stats['speeds'] else 0,
                    'avg_acceleration': round(sum(stats['accelerations']) / len(stats['accelerations']), 2) if stats['accelerations'] else 0,
                    'avg_braking': round(sum(stats['braking_intensities']) / len(stats['braking_intensities']), 2) if stats['braking_intensities'] else 0
                })
            
            return result
        except Exception as e:
            print(f"Error computing driver stats: {e}")
            return []
    
    async def get_fleet_summary(self):
        """Get fleet-level summary statistics"""
        if not self.configured:
            raise Exception("Supabase not configured")
        
        try:
            # Try to use SQL function if it exists
            try:
                result = self.client.rpc('get_fleet_summary').execute()
                if result.data:
                    return result.data[0]
            except:
                pass
            
            # Fall back to computing from driver stats
            driver_stats = await self.get_driver_stats()
            
            if not driver_stats:
                return {
                    'total_drivers': 0,
                    'total_trips': 0,
                    'fleet_avg_score': 0,
                    'safest_driver': None,
                    'safest_driver_score': None,
                    'most_improved_driver': None,
                    'most_improved_score': None,
                    'high_performers': 0,
                    'average_performers': 0,
                    'low_performers': 0
                }
            
            total_drivers = len(driver_stats)
            total_trips = sum(stat.get('trip_count', 0) for stat in driver_stats)
            fleet_avg_score = sum(stat.get('avg_score', 0) for stat in driver_stats) / total_drivers
            
            # Categorize drivers by performance
            high_performers = len([d for d in driver_stats if d.get('avg_score', 0) >= 8])
            average_performers = len([d for d in driver_stats if 5 <= d.get('avg_score', 0) < 8])
            low_performers = len([d for d in driver_stats if d.get('avg_score', 0) < 5])
            
            # Find safest driver
            safest = max(driver_stats, key=lambda x: x.get('avg_score', 0))
            
            # Find most improved driver (simplified - uses best_score - avg_score as improvement indicator)
            # In a real scenario, this would compare historical data over time
            most_improved = None
            max_improvement = 0
            
            for driver in driver_stats:
                best = driver.get('best_score', 0)
                worst = driver.get('worst_score', 0)
                if best and worst:
                    improvement = best - worst
                    if improvement > max_improvement:
                        max_improvement = improvement
                        most_improved = driver
            
            return {
                'total_drivers': total_drivers,
                'total_trips': total_trips,
                'fleet_avg_score': round(fleet_avg_score, 2),
                'safest_driver': safest.get('driver_name') or safest.get('driver_id'),
                'safest_driver_score': safest.get('avg_score'),
                'most_improved_driver': most_improved.get('driver_name') or most_improved.get('driver_id') if most_improved else None,
                'most_improved_score': most_improved.get('avg_score') if most_improved else None,
                'high_performers': high_performers,
                'average_performers': average_performers,
                'low_performers': low_performers
            }
        except Exception as e:
            print(f"Error getting fleet summary: {e}")
            raise
