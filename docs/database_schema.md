# Supabase Database Schema for DriveMind.ai

This document describes the database schema for storing driving sessions, events, scores, and AI feedback.

## Tables

### 1. sessions
Stores information about each driving session.

```sql
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    driver_id VARCHAR(255),
    vehicle_id VARCHAR(255),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster lookups
CREATE INDEX idx_sessions_session_id ON sessions(session_id);
CREATE INDEX idx_sessions_driver_id ON sessions(driver_id);
CREATE INDEX idx_sessions_start_time ON sessions(start_time DESC);
```

### 2. events
Stores individual driving events (telemetry data points).

```sql
CREATE TABLE events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) REFERENCES sessions(session_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    speed DECIMAL(6,2),
    acceleration DECIMAL(6,2),
    braking_intensity DECIMAL(4,2),
    steering_angle DECIMAL(6,2),
    jerk DECIMAL(6,2),
    score DECIMAL(4,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster queries
CREATE INDEX idx_events_session_id ON events(session_id);
CREATE INDEX idx_events_timestamp ON events(timestamp DESC);
```

### 3. scores
Stores aggregated scores for sessions or time periods.

```sql
CREATE TABLE scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) REFERENCES sessions(session_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    score DECIMAL(4,2) NOT NULL,
    confidence DECIMAL(4,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_scores_session_id ON scores(session_id);
CREATE INDEX idx_scores_timestamp ON scores(timestamp DESC);
```

### 4. feedback
Stores AI-generated feedback.

```sql
CREATE TABLE feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id VARCHAR(255) REFERENCES sessions(session_id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    score DECIMAL(4,2),
    feedback TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_feedback_session_id ON feedback(session_id);
CREATE INDEX idx_feedback_timestamp ON feedback(timestamp DESC);
```

## Setup Instructions

1. Create a Supabase account at https://supabase.com
2. Create a new project
3. Go to the SQL editor
4. Run the SQL commands above to create tables
5. Copy your project URL and anon/public key
6. Update the `.env` file in the backend directory with your credentials:
   ```
   SUPABASE_URL=your_project_url
   SUPABASE_KEY=your_anon_key
   ```

## Row Level Security (RLS)

For production, you should enable RLS on these tables:

```sql
-- Enable RLS
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE events ENABLE ROW LEVEL SECURITY;
ALTER TABLE scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE feedback ENABLE ROW LEVEL SECURITY;

-- Example policy: Allow all operations for authenticated users
CREATE POLICY "Allow all for authenticated users" ON sessions
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON events
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON scores
    FOR ALL USING (auth.role() = 'authenticated');

CREATE POLICY "Allow all for authenticated users" ON feedback
    FOR ALL USING (auth.role() = 'authenticated');
```

## Sample Queries

### Get all events for a session
```sql
SELECT * FROM events 
WHERE session_id = 'your-session-id' 
ORDER BY timestamp;
```

### Get average score for a session
```sql
SELECT AVG(score) as avg_score 
FROM events 
WHERE session_id = 'your-session-id';
```

### Get feedback for a session
```sql
SELECT * FROM feedback 
WHERE session_id = 'your-session-id' 
ORDER BY timestamp DESC;
```
