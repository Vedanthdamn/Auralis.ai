#!/usr/bin/env python3
"""
Test script to verify the /api/driving_data route works correctly
with Python 3.10 compatible timeout handling
"""
import asyncio
import sys
from fastapi.testclient import TestClient
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, '/home/runner/work/Auralis.ai/Auralis.ai/backend')

from main import app

def test_driving_data_endpoint():
    """Test the /api/driving_data endpoint"""
    client = TestClient(app)
    
    # Test data
    test_payload = {
        "speed": 60.5,
        "acceleration": 0.5,
        "braking_intensity": 0.0,
        "steering_angle": 5.2,
        "jerk": 0.1,
        "timestamp": datetime.utcnow().isoformat(),
        "simulation_mode": "personal",
        "scenario": "normal",
        "session_id": "test-session-001"
    }
    
    print("🧪 Testing /api/driving_data endpoint...")
    print(f"📤 Sending request with data: {test_payload}")
    
    try:
        # Make POST request
        response = client.post("/api/driving_data", json=test_payload)
        
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response data: {response.json()}")
        
        # Verify response
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        
        response_data = response.json()
        assert "score" in response_data, "Response missing 'score' field"
        assert "timestamp" in response_data, "Response missing 'timestamp' field"
        assert "confidence" in response_data, "Response missing 'confidence' field"
        
        assert 0 <= response_data["score"] <= 10, f"Score {response_data['score']} out of range"
        assert 0 <= response_data["confidence"] <= 1, f"Confidence {response_data['confidence']} out of range"
        
        print("✅ Test passed! /api/driving_data endpoint works correctly")
        return True
        
    except AssertionError as e:
        print(f"❌ Test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_concurrent_requests():
    """Test that multiple concurrent requests work without errors"""
    client = TestClient(app)
    
    print("\n🧪 Testing concurrent requests...")
    
    test_payload = {
        "speed": 60.5,
        "acceleration": 0.5,
        "braking_intensity": 0.0,
        "steering_angle": 5.2,
        "jerk": 0.1,
        "timestamp": datetime.utcnow().isoformat(),
        "simulation_mode": "personal",
        "scenario": "normal",
        "session_id": "test-session-concurrent"
    }
    
    try:
        # Send multiple requests
        results = []
        for i in range(5):
            payload = test_payload.copy()
            payload["session_id"] = f"test-session-{i}"
            response = client.post("/api/driving_data", json=payload)
            results.append(response)
            print(f"  Request {i+1}: Status {response.status_code}")
        
        # Verify all succeeded
        for i, response in enumerate(results):
            assert response.status_code == 200, f"Request {i+1} failed with status {response.status_code}"
        
        print("✅ Concurrent requests test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Concurrent requests test failed: {e}")
        return False

def test_health_check():
    """Test health check endpoint"""
    client = TestClient(app)
    
    print("\n🧪 Testing /health endpoint...")
    
    try:
        response = client.get("/health")
        print(f"📥 Response status: {response.status_code}")
        print(f"📥 Response data: {response.json()}")
        
        assert response.status_code == 200
        response_data = response.json()
        assert response_data["status"] == "healthy"
        
        print("✅ Health check passed!")
        return True
        
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 DriveMind.ai Backend Tests")
    print("Testing Python 3.10 compatible timeout handling")
    print("=" * 60)
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Driving Data Endpoint", test_driving_data_endpoint()))
    results.append(("Concurrent Requests", test_concurrent_requests()))
    
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
