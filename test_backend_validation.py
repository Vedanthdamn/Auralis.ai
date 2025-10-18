#!/usr/bin/env python3
"""
Quick validation script to ensure backend can start without errors
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all backend modules can be imported"""
    print("🧪 Testing backend imports...")
    
    try:
        print("  - Importing main...")
        from main import app
        print("  ✅ main.app imported successfully")
        
        print("  - Importing routes...")
        from app.routes import router
        print("  ✅ app.routes imported successfully")
        
        print("  - Importing ML service...")
        from services.ml_service import MLService
        print("  ✅ services.ml_service imported successfully")
        
        print("  - Importing schemas...")
        from models.schemas import DrivingData
        print("  ✅ models.schemas imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_app_structure():
    """Test that FastAPI app is properly configured"""
    print("\n🧪 Testing FastAPI app structure...")
    
    try:
        from main import app
        
        # Check routes are included
        routes = [route.path for route in app.routes]
        print(f"  - Found {len(routes)} routes")
        
        # Check for key routes
        key_routes = ['/api/driving_data', '/health', '/ws/personal', '/ws/fleet']
        for route in key_routes:
            if any(route in r for r in routes):
                print(f"  ✅ Route {route} exists")
            else:
                print(f"  ⚠️  Route {route} might be missing")
        
        # Check lifespan is configured
        if app.router.lifespan_context:
            print("  ✅ Lifespan context configured")
        else:
            print("  ⚠️  Lifespan context not found")
        
        return True
    except Exception as e:
        print(f"❌ App structure test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_async_methods():
    """Test that key methods are async"""
    print("\n🧪 Testing async method signatures...")
    
    try:
        from services.ml_service import MLService
        import inspect
        
        ml_service = MLService()
        
        # Check calculate_score is async
        if inspect.iscoroutinefunction(ml_service.calculate_score):
            print("  ✅ MLService.calculate_score is async")
        else:
            print("  ❌ MLService.calculate_score is NOT async")
            return False
        
        # Check Ollama methods are async
        if inspect.iscoroutinefunction(ml_service._generate_ollama_feedback):
            print("  ✅ MLService._generate_ollama_feedback is async")
        else:
            print("  ❌ MLService._generate_ollama_feedback is NOT async")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Async methods test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("="*60)
    print("🔍 Backend Validation Tests")
    print("="*60)
    print()
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("App Structure", test_app_structure()))
    results.append(("Async Methods", test_async_methods()))
    
    print("\n" + "="*60)
    print("📊 Validation Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("\n" + "="*60)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ Backend validation complete - ready to run!")
        return 0
    else:
        print(f"❌ {total - passed} validation test(s) failed")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
