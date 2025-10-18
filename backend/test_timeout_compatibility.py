#!/usr/bin/env python3
"""
Test script to verify asyncio.wait_for works correctly as replacement for asyncio.timeout
This tests Python 3.10 compatibility
"""
import asyncio
import sys

async def test_wait_for_with_success():
    """Test that wait_for works when operation completes in time"""
    print("🧪 Test 1: wait_for with successful completion")
    
    async def quick_operation():
        await asyncio.sleep(0.1)
        return "success"
    
    try:
        result = await asyncio.wait_for(quick_operation(), timeout=1.0)
        assert result == "success"
        print("✅ Test passed: wait_for completed successfully")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_wait_for_with_timeout():
    """Test that wait_for raises TimeoutError when operation takes too long"""
    print("\n🧪 Test 2: wait_for with timeout")
    
    async def slow_operation():
        await asyncio.sleep(2.0)
        return "too slow"
    
    try:
        result = await asyncio.wait_for(slow_operation(), timeout=0.5)
        print(f"❌ Test failed: Should have raised TimeoutError, got result: {result}")
        return False
    except asyncio.TimeoutError:
        print("✅ Test passed: wait_for raised TimeoutError as expected")
        return True
    except Exception as e:
        print(f"❌ Test failed with unexpected error: {e}")
        return False

async def test_wait_for_with_semaphore():
    """Test that wait_for works with semaphore acquisition"""
    print("\n🧪 Test 3: wait_for with semaphore")
    
    semaphore = asyncio.Semaphore(1)
    
    async def acquire_and_work(sem, delay=0.1):
        async with sem:
            await asyncio.sleep(delay)
            return "done"
    
    try:
        # First acquisition should succeed
        result = await asyncio.wait_for(acquire_and_work(semaphore, 0.1), timeout=1.0)
        assert result == "done"
        print("✅ Test passed: wait_for with semaphore completed successfully")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def test_wait_for_with_nested_operations():
    """Test that wait_for works with multiple awaits inside"""
    print("\n🧪 Test 4: wait_for with nested async operations")
    
    async def complex_operation():
        await asyncio.sleep(0.05)
        result1 = await asyncio.sleep(0.05)
        await asyncio.sleep(0.05)
        return "complex_done"
    
    try:
        result = await asyncio.wait_for(complex_operation(), timeout=1.0)
        assert result == "complex_done"
        print("✅ Test passed: wait_for with nested operations completed successfully")
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

async def run_all_tests():
    """Run all timeout compatibility tests"""
    print("=" * 60)
    print("🐍 Testing Python 3.10+ asyncio.wait_for compatibility")
    print(f"Python version: {sys.version}")
    print("=" * 60)
    
    results = []
    
    results.append(await test_wait_for_with_success())
    results.append(await test_wait_for_with_timeout())
    results.append(await test_wait_for_with_semaphore())
    results.append(await test_wait_for_with_nested_operations())
    
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All compatibility tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
