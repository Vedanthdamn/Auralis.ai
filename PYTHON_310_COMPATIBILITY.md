# Python 3.10 Compatibility

## Overview
This document describes the changes made to ensure Python 3.10+ compatibility in the Auralis.ai backend.

## Issue
The original code used `asyncio.timeout()` which was introduced in Python 3.11. This caused compatibility issues when running on Python 3.10.

## Solution
Replaced `asyncio.timeout()` with `asyncio.wait_for()` which has been available since Python 3.7 and provides equivalent functionality.

### Before (Python 3.11+ only)
```python
async with asyncio.timeout(2.0):
    async with semaphore:
        score = ml_service.calculate_score(data)
```

### After (Python 3.10+ compatible)
```python
async def _acquire_and_calculate_score(semaphore, ml_service, data):
    """Helper function to acquire semaphore and calculate score"""
    async with semaphore:
        # Note: calculate_score() is a synchronous method
        score = ml_service.calculate_score(data)
        return score

# Usage:
score = await asyncio.wait_for(
    _acquire_and_calculate_score(semaphore, ml_service, data),
    timeout=2.0
)
```

## Key Changes

### 1. Helper Function Pattern
When multiple `await` statements need to be executed within a timeout, wrap them in an async helper function. This is the recommended pattern for `asyncio.wait_for()`.

### 2. Error Handling
Both `asyncio.timeout()` and `asyncio.wait_for()` raise `asyncio.TimeoutError` when the timeout is exceeded, so the exception handling remains the same.

### 3. Files Modified
- `backend/app/routes.py`: Updated the `/api/driving_data` endpoint to use Python 3.10 compatible timeout handling

## Testing
All changes have been tested and verified:
- ✅ Single requests work correctly
- ✅ Concurrent requests (10+) work without errors
- ✅ Timeout behavior functions as expected
- ✅ No Python 3.11+ specific features remain in the codebase

## Minimum Python Version
The backend now requires **Python 3.10+** (previously required Python 3.11+).

## See Also
- [Python asyncio.wait_for() documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for)
- Test files: `backend/test_timeout_compatibility.py`, `backend/test_routes.py`
