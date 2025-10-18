# Tests Directory

This directory contains integration and validation tests for the Auralis.ai system.

## Test Files

- **test_async_changes.py** - Tests for async implementation and concurrency
- **test_backend_validation.py** - Backend API validation tests
- **test_integration_parallel.py** - Parallel integration tests for multiple components
- **test_parallel_dashboard_simulation.py** - Tests for concurrent dashboard simulations
- **test_parallel_simulators.py** - Tests for running multiple simulators in parallel
- **test_structure.py** - Repository structure validation tests

## Running Tests

To run all tests:
```bash
cd tests
python test_structure.py
python test_backend_validation.py
# etc.
```

Or run specific tests:
```bash
python tests/test_parallel_simulators.py --duration 10
```

## Note

These are integration tests that verify the system works correctly under various conditions, including concurrent operations and parallel data streaming.
