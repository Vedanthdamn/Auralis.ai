# Fleet Management Database Schema Extension

This document extends the base schema to support fleet management features with multiple drivers and vehicles.

## Extended Tables

### 1. drivers
Stores driver profile information for fleet management.

```sql
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    driver_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    license_number VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster lookups
CREATE INDEX idx_drivers_driver_id ON drivers(driver_id);
CREATE INDEX idx_drivers_name ON drivers(name);
```

### 2. vehicles
Stores vehicle information for fleet management.

```sql
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    vehicle_id VARCHAR(255) UNIQUE NOT NULL,
    make VARCHAR(100),
    model VARCHAR(100),
    year INTEGER,
    license_plate VARCHAR(50),
    vin VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for faster lookups
CREATE INDEX idx_vehicles_vehicle_id ON vehicles(vehicle_id);
CREATE INDEX idx_vehicles_license_plate ON vehicles(license_plate);
```

### 3. driver_stats (Materialized View)
Pre-computed statistics for faster fleet dashboard loading.

```sql
CREATE MATERIALIZED VIEW driver_stats AS
SELECT 
    s.driver_id,
    d.name as driver_name,
    COUNT(DISTINCT s.session_id) as trip_count,
    AVG(e.score) as avg_score,
    MAX(e.score) as best_score,
    MIN(e.score) as worst_score,
    MAX(s.start_time) as last_trip_date,
    AVG(e.speed) as avg_speed,
    AVG(e.acceleration) as avg_acceleration,
    AVG(e.braking_intensity) as avg_braking
FROM sessions s
JOIN drivers d ON s.driver_id = d.driver_id
LEFT JOIN events e ON s.session_id = e.session_id
WHERE s.driver_id IS NOT NULL
GROUP BY s.driver_id, d.name;

-- Index for materialized view
CREATE UNIQUE INDEX idx_driver_stats_driver_id ON driver_stats(driver_id);

-- Refresh function
CREATE OR REPLACE FUNCTION refresh_driver_stats()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY driver_stats;
END;
$$ LANGUAGE plpgsql;
```

## Fleet Analytics Functions

### Get Fleet Summary
```sql
CREATE OR REPLACE FUNCTION get_fleet_summary()
RETURNS TABLE(
    total_drivers BIGINT,
    total_trips BIGINT,
    fleet_avg_score NUMERIC,
    safest_driver VARCHAR,
    safest_driver_score NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COUNT(DISTINCT driver_id)::BIGINT as total_drivers,
        SUM(trip_count)::BIGINT as total_trips,
        AVG(avg_score) as fleet_avg_score,
        (SELECT driver_name FROM driver_stats ORDER BY avg_score DESC LIMIT 1) as safest_driver,
        (SELECT avg_score FROM driver_stats ORDER BY avg_score DESC LIMIT 1) as safest_driver_score
    FROM driver_stats;
END;
$$ LANGUAGE plpgsql;
```

### Get Driver Rankings
```sql
CREATE OR REPLACE FUNCTION get_driver_rankings()
RETURNS TABLE(
    rank INTEGER,
    driver_id VARCHAR,
    driver_name VARCHAR,
    avg_score NUMERIC,
    trip_count BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ROW_NUMBER() OVER (ORDER BY ds.avg_score DESC)::INTEGER as rank,
        ds.driver_id,
        ds.driver_name,
        ds.avg_score,
        ds.trip_count
    FROM driver_stats ds
    ORDER BY ds.avg_score DESC;
END;
$$ LANGUAGE plpgsql;
```

## Sample Data for Testing

```sql
-- Insert sample drivers
INSERT INTO drivers (driver_id, name, email, phone, license_number) VALUES
('DRV001', 'John Smith', 'john.smith@fleet.com', '+1-555-0101', 'DL12345678'),
('DRV002', 'Sarah Johnson', 'sarah.johnson@fleet.com', '+1-555-0102', 'DL23456789'),
('DRV003', 'Michael Chen', 'michael.chen@fleet.com', '+1-555-0103', 'DL34567890'),
('DRV004', 'Emily Davis', 'emily.davis@fleet.com', '+1-555-0104', 'DL45678901'),
('DRV005', 'Robert Wilson', 'robert.wilson@fleet.com', '+1-555-0105', 'DL56789012');

-- Insert sample vehicles
INSERT INTO vehicles (vehicle_id, make, model, year, license_plate, vin) VALUES
('VEH001', 'Toyota', 'Camry', 2022, 'ABC123', '1HGBH41JXMN109186'),
('VEH002', 'Honda', 'Accord', 2023, 'XYZ789', '2HGBH41JXMN109187'),
('VEH003', 'Tesla', 'Model 3', 2023, 'ELC456', '3HGBH41JXMN109188'),
('VEH004', 'Ford', 'Fusion', 2021, 'DEF234', '4HGBH41JXMN109189'),
('VEH005', 'Chevrolet', 'Malibu', 2022, 'GHI567', '5HGBH41JXMN109190');
```

## Setup Instructions

1. Run the SQL commands above in your Supabase SQL editor
2. The materialized view will be automatically populated
3. Refresh the materialized view periodically (e.g., every hour) using:
   ```sql
   SELECT refresh_driver_stats();
   ```
4. For real-time updates, you can set up a trigger to refresh on data changes:
   ```sql
   CREATE OR REPLACE FUNCTION auto_refresh_driver_stats()
   RETURNS TRIGGER AS $$
   BEGIN
       PERFORM refresh_driver_stats();
       RETURN NULL;
   END;
   $$ LANGUAGE plpgsql;

   CREATE TRIGGER trigger_refresh_driver_stats
   AFTER INSERT OR UPDATE OR DELETE ON events
   FOR EACH STATEMENT
   EXECUTE FUNCTION auto_refresh_driver_stats();
   ```
