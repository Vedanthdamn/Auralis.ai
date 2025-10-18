#!/usr/bin/env python3
"""
Test script to simulate running both Personal and Fleet simulators
in parallel to verify no timeout or blocking issues
"""
import asyncio
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'simulation'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from drive_simulator import DrivingSimulator

async def run_personal_simulator(duration: int = 10):
    """Run personal simulator for testing"""
    print("🚗 Starting PERSONAL simulator...")
    simulator = DrivingSimulator(api_url="http://localhost:8000/api")
    
    try:
        await simulator.run_simulation(
            duration=duration,
            update_interval=1.0,
            simulation_mode='personal'
        )
    except Exception as e:
        print(f"❌ Personal simulator error: {e}")
        return False
    
    return True

async def run_fleet_simulator(duration: int = 10):
    """Run fleet simulator for testing"""
    print("🚕 Starting FLEET simulator...")
    simulator = DrivingSimulator(api_url="http://localhost:8000/api")
    
    try:
        await simulator.run_simulation(
            duration=duration,
            update_interval=1.0,
            simulation_mode='fleet'
        )
    except Exception as e:
        print(f"❌ Fleet simulator error: {e}")
        return False
    
    return True

async def test_parallel_simulators(duration: int = 10):
    """Run both simulators in parallel"""
    print("="*70)
    print("🧪 Testing Parallel Simulator Execution")
    print("="*70)
    print(f"\n⚠️  Note: This test requires the backend to be running!")
    print(f"   Start backend with: cd backend && uvicorn main:app --host 0.0.0.0 --port 8000")
    print(f"\n📊 Running both simulators for {duration} seconds...\n")
    
    # Run both simulators concurrently
    start = asyncio.get_event_loop().time()
    
    results = await asyncio.gather(
        run_personal_simulator(duration),
        run_fleet_simulator(duration),
        return_exceptions=True
    )
    
    end = asyncio.get_event_loop().time()
    elapsed = end - start
    
    print("\n" + "="*70)
    print("📊 Test Results")
    print("="*70)
    
    personal_success = results[0] if not isinstance(results[0], Exception) else False
    fleet_success = results[1] if not isinstance(results[1], Exception) else False
    
    if isinstance(results[0], Exception):
        print(f"❌ Personal simulator exception: {results[0]}")
    elif personal_success:
        print("✅ Personal simulator completed successfully")
    else:
        print("❌ Personal simulator failed")
    
    if isinstance(results[1], Exception):
        print(f"❌ Fleet simulator exception: {results[1]}")
    elif fleet_success:
        print("✅ Fleet simulator completed successfully")
    else:
        print("❌ Fleet simulator failed")
    
    print(f"\n⏱️  Total elapsed time: {elapsed:.2f}s (expected ~{duration}s)")
    print(f"   Expected range: {duration}s to {duration + 2}s")
    
    # Check if execution time is reasonable (within expected duration + some margin)
    timing_ok = duration <= elapsed <= (duration + 3)
    
    if timing_ok:
        print("✅ Execution timing is reasonable (simulators ran in parallel)")
    else:
        print("⚠️  Execution timing seems off (possible sequential execution or other issues)")
    
    all_success = personal_success and fleet_success and timing_ok
    
    print("\n" + "="*70)
    if all_success:
        print("✅ PARALLEL EXECUTION TEST PASSED!")
        print("   Both simulators can run concurrently without timeout")
    else:
        print("❌ PARALLEL EXECUTION TEST FAILED")
        if not (personal_success and fleet_success):
            print("   One or both simulators encountered errors")
        if not timing_ok:
            print("   Timing suggests possible blocking or other issues")
    print("="*70)
    
    return 0 if all_success else 1

async def test_without_backend():
    """Test that simulators handle backend being offline gracefully"""
    print("="*70)
    print("🧪 Testing Simulator Behavior Without Backend")
    print("="*70)
    print("\nThis test verifies simulators handle connection errors gracefully\n")
    
    # Use a fake URL that won't respond
    simulator = DrivingSimulator(api_url="http://localhost:9999/api")
    
    print("🚗 Running short simulation with unreachable backend...")
    
    try:
        # Run for just 5 seconds to test error handling
        await simulator.run_simulation(
            duration=5,
            update_interval=1.0,
            simulation_mode='personal'
        )
        
        print("\n✅ Simulator handled missing backend gracefully")
        print("   (Expected to see connection errors, but no crashes)")
        return True
        
    except Exception as e:
        print(f"\n❌ Simulator crashed when backend unavailable: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test parallel simulator execution')
    parser.add_argument('--duration', type=int, default=10, 
                       help='Test duration in seconds (default: 10)')
    parser.add_argument('--skip-backend-test', action='store_true',
                       help='Skip test requiring backend')
    parser.add_argument('--offline-only', action='store_true',
                       help='Only run offline test (no backend needed)')
    
    args = parser.parse_args()
    
    if args.offline_only:
        # Only test offline behavior
        success = await test_without_backend()
        return 0 if success else 1
    
    if not args.skip_backend_test:
        # Main parallel test (requires backend)
        exit_code = await test_parallel_simulators(args.duration)
        return exit_code
    else:
        print("⚠️  Skipping backend test as requested")
        # Just test offline behavior
        success = await test_without_backend()
        return 0 if success else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
