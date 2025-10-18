#!/usr/bin/env python3
"""
Comprehensive integration test to verify the timeout fix.

This script simulates the exact scenario from the problem statement:
- Running both Personal and Fleet simulators simultaneously
- Sending data at high frequency (1-second intervals)
- Verifying no timeouts occur

Before the fix, this would produce:
  ⏳ Request timeout, retrying...
  ❌ Request timeout after 3 attempts

After the fix, both simulators should stream data continuously without errors.
"""
import asyncio
import aiohttp
import time
from datetime import datetime

BACKEND_URL = "http://localhost:8000/api"

async def send_driving_data(session: aiohttp.ClientSession, mode: str, iteration: int):
    """Send a single driving data point"""
    data = {
        "speed": 60.0 + (iteration % 40),
        "acceleration": 0.5 + (iteration % 3) * 0.3,
        "braking_intensity": 0.1 if iteration % 5 == 0 else 0.0,
        "steering_angle": 5.0 + (iteration % 10) - 5,
        "jerk": 0.1,
        "timestamp": datetime.utcnow().isoformat(),
        "simulation_mode": mode,
        "scenario": "normal",
        "session_id": f"test-{mode}-session"
    }
    
    try:
        async with session.post(f"{BACKEND_URL}/driving_data", json=data, timeout=aiohttp.ClientTimeout(total=5)) as response:
            if response.status == 200:
                result = await response.json()
                return True, result.get('score', 0)
            else:
                return False, f"HTTP {response.status}"
    except asyncio.TimeoutError:
        return False, "TIMEOUT"
    except Exception as e:
        return False, str(e)

async def simulate_mode(mode: str, duration: int = 30, update_interval: float = 1.0):
    """Simulate a single mode (personal or fleet)"""
    mode_emoji = "🚗" if mode == 'personal' else "🚕"
    print(f"{mode_emoji} Starting {mode.upper()} simulator (duration: {duration}s, interval: {update_interval}s)")
    
    successes = 0
    failures = 0
    timeouts = 0
    scores = []
    
    start_time = time.time()
    iteration = 0
    
    async with aiohttp.ClientSession() as session:
        while time.time() - start_time < duration:
            success, result = await send_driving_data(session, mode, iteration)
            
            if success:
                successes += 1
                scores.append(result)
                status = "✅"
            else:
                failures += 1
                if result == "TIMEOUT":
                    timeouts += 1
                    status = "⏳ TIMEOUT"
                else:
                    status = f"❌ {result}"
            
            elapsed = time.time() - start_time
            print(f"{mode_emoji} [{mode.upper():8s}] #{iteration:3d} | Elapsed: {elapsed:5.1f}s | {status}")
            
            iteration += 1
            
            # Wait for next update
            await asyncio.sleep(update_interval)
    
    # Summary
    total = successes + failures
    success_rate = (successes / total * 100) if total > 0 else 0
    avg_score = sum(scores) / len(scores) if scores else 0
    
    print(f"\n{mode_emoji} {mode.upper()} Summary:")
    print(f"   Total Requests: {total}")
    print(f"   Successes: {successes} ({success_rate:.1f}%)")
    print(f"   Failures: {failures}")
    print(f"   Timeouts: {timeouts}")
    if scores:
        print(f"   Average Score: {avg_score:.2f}/10")
    
    return {
        'mode': mode,
        'total': total,
        'successes': successes,
        'failures': failures,
        'timeouts': timeouts,
        'success_rate': success_rate,
        'avg_score': avg_score
    }

async def check_backend_health():
    """Check if backend is running and healthy"""
    print("🔍 Checking backend health...")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{BACKEND_URL.replace('/api', '')}/health", timeout=aiohttp.ClientTimeout(total=5)) as response:
                if response.status == 200:
                    health = await response.json()
                    print(f"✅ Backend is healthy")
                    print(f"   ML Service: {health['services']['ml_service']}")
                    print(f"   Supabase: {health['services']['supabase_service']}")
                    return True
                else:
                    print(f"❌ Backend returned status {response.status}")
                    return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        print(f"   Make sure backend is running on http://localhost:8000")
        return False

async def main():
    print("="*80)
    print("🧪 COMPREHENSIVE ASYNC CONCURRENCY TEST")
    print("="*80)
    print("\nThis test simulates the exact scenario that was causing timeouts:")
    print("  - Two simulators (Personal & Fleet) running simultaneously")
    print("  - High-frequency updates (1-second intervals)")
    print("  - Continuous operation for 30+ seconds")
    print()
    print("EXPECTED RESULT (with async fix):")
    print("  ✅ Both simulators should complete without timeouts")
    print("  ✅ Success rate should be 100% for both")
    print("  ✅ No '⏳ TIMEOUT' messages should appear")
    print()
    print("=" * 80)
    print()
    
    # Check backend
    if not await check_backend_health():
        print("\n⚠️  Please start the backend first:")
        print("   cd backend && uvicorn main:app --host 0.0.0.0 --port 8000")
        return 1
    
    print("\n" + "="*80)
    print("🚀 Starting parallel simulation test (30 seconds)...")
    print("="*80)
    print()
    
    # Run both simulators concurrently
    start_time = time.time()
    
    results = await asyncio.gather(
        simulate_mode('personal', duration=30, update_interval=1.0),
        simulate_mode('fleet', duration=30, update_interval=1.0),
        return_exceptions=True
    )
    
    end_time = time.time()
    total_duration = end_time - start_time
    
    # Analyze results
    print("\n" + "="*80)
    print("📊 TEST RESULTS")
    print("="*80)
    
    if isinstance(results[0], Exception) or isinstance(results[1], Exception):
        print("❌ TEST FAILED - One or both simulators crashed")
        if isinstance(results[0], Exception):
            print(f"   Personal: {results[0]}")
        if isinstance(results[1], Exception):
            print(f"   Fleet: {results[1]}")
        return 1
    
    personal_result = results[0]
    fleet_result = results[1]
    
    print(f"\n⏱️  Total Duration: {total_duration:.2f}s (expected ~30s)")
    print()
    
    # Personal results
    print("🚗 PERSONAL Mode:")
    print(f"   Total Requests: {personal_result['total']}")
    print(f"   Success Rate: {personal_result['success_rate']:.1f}%")
    print(f"   Timeouts: {personal_result['timeouts']}")
    print(f"   Average Score: {personal_result['avg_score']:.2f}/10")
    
    # Fleet results
    print("\n🚕 FLEET Mode:")
    print(f"   Total Requests: {fleet_result['total']}")
    print(f"   Success Rate: {fleet_result['success_rate']:.1f}%")
    print(f"   Timeouts: {fleet_result['timeouts']}")
    print(f"   Average Score: {fleet_result['avg_score']:.2f}/10")
    
    # Overall assessment
    print("\n" + "="*80)
    print("🎯 ASSESSMENT")
    print("="*80)
    
    all_pass = True
    
    # Check for timeouts
    total_timeouts = personal_result['timeouts'] + fleet_result['timeouts']
    if total_timeouts == 0:
        print("✅ NO TIMEOUTS - Async implementation is working correctly!")
    else:
        print(f"❌ {total_timeouts} TIMEOUT(S) DETECTED - Async implementation may have issues")
        all_pass = False
    
    # Check success rates
    min_success_rate = 95.0  # Allow for occasional network issues
    if personal_result['success_rate'] >= min_success_rate and fleet_result['success_rate'] >= min_success_rate:
        print(f"✅ SUCCESS RATES GOOD - Both modes above {min_success_rate}%")
    else:
        print(f"❌ LOW SUCCESS RATE - One or both modes below {min_success_rate}%")
        all_pass = False
    
    # Check timing (should be ~30s, not 60s which would indicate sequential execution)
    if 28 <= total_duration <= 35:
        print(f"✅ PARALLEL EXECUTION CONFIRMED - Completed in ~30s (not ~60s)")
    else:
        print(f"⚠️  TIMING UNUSUAL - Expected ~30s, got {total_duration:.1f}s")
        # Don't fail on this, could be slow system
    
    # Check request counts
    expected_requests = 28  # ~30 seconds at 1/second minus a few
    if personal_result['total'] >= expected_requests and fleet_result['total'] >= expected_requests:
        print(f"✅ REQUEST COUNTS GOOD - Both modes sent {expected_requests}+ requests")
    else:
        print(f"⚠️  LOW REQUEST COUNT - Expected {expected_requests}+, got {personal_result['total']} and {fleet_result['total']}")
    
    print("\n" + "="*80)
    if all_pass:
        print("✅✅✅ ALL TESTS PASSED! ✅✅✅")
        print("\nThe async concurrency implementation is working correctly!")
        print("Both Personal and Fleet simulators can run simultaneously without timeouts.")
    else:
        print("❌❌❌ SOME TESTS FAILED ❌❌❌")
        print("\nPlease review the results above and check:")
        print("  1. Backend is fully started and not overloaded")
        print("  2. All async changes are properly deployed")
        print("  3. Network connection is stable")
    print("="*80)
    
    return 0 if all_pass else 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        exit(1)
