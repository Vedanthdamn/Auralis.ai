#!/usr/bin/env python3
"""
Quick test to verify async changes work correctly
"""
import asyncio
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

async def test_ml_service_async():
    """Test that ML service calculate_score is async"""
    print("🧪 Testing ML Service async implementation...")
    
    from services.ml_service import MLService
    from models.schemas import DrivingData
    from datetime import datetime
    
    ml_service = MLService()
    
    # Create test driving data
    test_data = DrivingData(
        speed=60.5,
        acceleration=0.5,
        braking_intensity=0.0,
        steering_angle=5.2,
        jerk=0.1,
        timestamp=datetime.utcnow(),
        simulation_mode="personal",
        scenario="normal",
        session_id="test-001"
    )
    
    # Test async calculate_score
    score = await ml_service.calculate_score(test_data)
    
    print(f"  ✅ ML Service async calculate_score works! Score: {score:.2f}/10")
    assert 0 <= score <= 10, f"Score {score} out of range"
    return True

async def test_simulator_async():
    """Test that simulator is async"""
    print("🧪 Testing Simulator async implementation...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simulation'))
    from drive_simulator import DrivingSimulator
    
    # Create simulator but don't run full simulation
    simulator = DrivingSimulator(api_url="http://localhost:8000/api")
    
    # Verify methods are async
    import inspect
    assert inspect.iscoroutinefunction(simulator.run_simulation), "run_simulation should be async"
    assert inspect.iscoroutinefunction(simulator.send_telemetry), "send_telemetry should be async"
    
    print(f"  ✅ Simulator methods are properly async!")
    return True

async def test_concurrent_scoring():
    """Test that multiple ML scoring operations can run concurrently"""
    print("🧪 Testing concurrent ML scoring...")
    
    from services.ml_service import MLService
    from models.schemas import DrivingData
    from datetime import datetime
    
    ml_service = MLService()
    
    # Create multiple test data points
    test_data_list = [
        DrivingData(
            speed=60.0 + i * 5,
            acceleration=0.5 + i * 0.1,
            braking_intensity=0.0,
            steering_angle=5.0,
            jerk=0.1,
            timestamp=datetime.utcnow(),
            simulation_mode="personal",
            scenario="normal",
            session_id=f"test-concurrent-{i}"
        )
        for i in range(5)
    ]
    
    # Run scoring concurrently
    start = asyncio.get_event_loop().time()
    scores = await asyncio.gather(*[ml_service.calculate_score(data) for data in test_data_list])
    end = asyncio.get_event_loop().time()
    
    print(f"  ✅ Scored {len(scores)} data points concurrently in {end - start:.3f}s")
    print(f"     Scores: {[f'{s:.1f}' for s in scores]}")
    
    for score in scores:
        assert 0 <= score <= 10, f"Score {score} out of range"
    
    return True

async def main():
    print("="*60)
    print("🚗 DriveMind.ai Async Implementation Tests")
    print("="*60)
    print()
    
    results = []
    
    try:
        results.append(("ML Service Async", await test_ml_service_async()))
        results.append(("Simulator Async", await test_simulator_async()))
        results.append(("Concurrent Scoring", await test_concurrent_scoring()))
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        results.append(("Exception", False))
    
    # Summary
    print()
    print("="*60)
    print("📊 Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print()
    print("="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All async implementation tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
