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
