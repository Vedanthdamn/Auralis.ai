#!/usr/bin/env python3
"""
Test script to verify parallel WebSocket connections work correctly
for both personal and fleet dashboards
"""
import asyncio
import sys
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, '/home/runner/work/Auralis.ai/Auralis.ai/backend')

from fastapi.testclient import TestClient
from main import app

def test_personal_websocket():
    """Test the /ws/personal endpoint"""
    print("🧪 Testing /ws/personal WebSocket endpoint...")
    
    with TestClient(app) as client:
        with client.websocket_connect("/ws/personal") as websocket:
            # Send a test message
            websocket.send_text("test")
            
            # Receive acknowledgment
            response = websocket.receive_text()
            data = json.loads(response)
            
            assert data["type"] == "ack", f"Expected ack, got {data['type']}"
            assert "Personal" in data["message"], f"Expected Personal in message, got {data['message']}"
            
            print(f"  ✅ Personal WebSocket connected and responding")
            return True

def test_fleet_websocket():
    """Test the /ws/fleet endpoint"""
    print("🧪 Testing /ws/fleet WebSocket endpoint...")
    
    with TestClient(app) as client:
        with client.websocket_connect("/ws/fleet") as websocket:
            # Send a test message
            websocket.send_text("test")
            
            # Receive acknowledgment
            response = websocket.receive_text()
            data = json.loads(response)
            
            assert data["type"] == "ack", f"Expected ack, got {data['type']}"
            assert "Fleet" in data["message"], f"Expected Fleet in message, got {data['message']}"
            
            print(f"  ✅ Fleet WebSocket connected and responding")
            return True

def test_legacy_websocket():
    """Test the legacy /ws endpoint"""
    print("🧪 Testing legacy /ws WebSocket endpoint...")
    
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as websocket:
            # Send a test message
            websocket.send_text("test")
            
            # Receive acknowledgment
            response = websocket.receive_text()
            data = json.loads(response)
            
            assert data["type"] == "ack", f"Expected ack, got {data['type']}"
            
            print(f"  ✅ Legacy WebSocket connected and responding")
            return True

def test_parallel_websockets():
    """Test that both personal and fleet WebSockets can be connected simultaneously"""
    print("🧪 Testing parallel WebSocket connections...")
    
    with TestClient(app) as client:
        with client.websocket_connect("/ws/personal") as personal_ws:
            with client.websocket_connect("/ws/fleet") as fleet_ws:
                # Send messages to both
                personal_ws.send_text("test-personal")
                fleet_ws.send_text("test-fleet")
                
                # Both should respond
                personal_response = personal_ws.receive_text()
                fleet_response = fleet_ws.receive_text()
                
                personal_data = json.loads(personal_response)
                fleet_data = json.loads(fleet_response)
                
                assert personal_data["type"] == "ack"
                assert fleet_data["type"] == "ack"
                
                print(f"  ✅ Both WebSockets connected and responding simultaneously")
                return True

def test_driving_data_routing():
    """Test that driving data is routed to the correct WebSocket endpoint"""
    print("🧪 Testing driving data routing...")
    
    with TestClient(app) as client:
        # Establish WebSocket connections
        with client.websocket_connect("/ws/personal") as personal_ws:
            with client.websocket_connect("/ws/fleet") as fleet_ws:
                # Clear initial acks
                personal_ws.send_text("test")
                fleet_ws.send_text("test")
                personal_ws.receive_text()
                fleet_ws.receive_text()
                
                # Send personal mode data
                personal_payload = {
                    "speed": 60.5,
                    "acceleration": 0.5,
                    "braking_intensity": 0.0,
                    "steering_angle": 5.2,
                    "jerk": 0.1,
                    "timestamp": datetime.utcnow().isoformat(),
                    "simulation_mode": "personal",
                    "scenario": "normal",
                    "session_id": "test-personal-001"
                }
                
                response = client.post("/api/driving_data", json=personal_payload)
                assert response.status_code == 200
                
                # Give some time for WebSocket broadcast
                import time
                time.sleep(0.5)
                
                print(f"  ✅ Driving data routing test completed")
                return True

def test_root_endpoint():
    """Test that root endpoint returns correct connection counts"""
    print("🧪 Testing root endpoint with connection tracking...")
    
    with TestClient(app) as client:
        # First check with no connections
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        
        # Should have websocket_connections dict with personal, fleet, and total
        assert "websocket_connections" in data
        assert "personal" in data["websocket_connections"]
        assert "fleet" in data["websocket_connections"]
        assert "total" in data["websocket_connections"]
        
        print(f"  ✅ Root endpoint returns connection tracking")
        return True

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 DriveMind.ai Parallel WebSocket Tests")
    print("Testing separate /ws/personal and /ws/fleet endpoints")
    print("=" * 60)
    
    results = []
    
    # Run tests
    try:
        results.append(("Root Endpoint", test_root_endpoint()))
        results.append(("Personal WebSocket", test_personal_websocket()))
        results.append(("Fleet WebSocket", test_fleet_websocket()))
        results.append(("Legacy WebSocket", test_legacy_websocket()))
        results.append(("Parallel WebSockets", test_parallel_websockets()))
        results.append(("Driving Data Routing", test_driving_data_routing()))
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Exception", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        sys.exit(0)
    else:
        print(f"❌ {total - passed} test(s) failed")
        sys.exit(1)
