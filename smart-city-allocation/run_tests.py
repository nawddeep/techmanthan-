#!/usr/bin/env python3
"""
Test Runner
Runs all tests and provides a summary.
"""
import subprocess
import sys

def run_tests():
    """Run all test files"""
    print("="*60)
    print("RUNNING ALL TESTS")
    print("="*60)
    
    test_files = [
        "tests/test_ml_pipeline.py",
        "tests/test_decision_engine.py",
        "tests/test_api_routes.py",
    ]
    
    all_passed = True
    results = {}
    
    for test_file in test_files:
        print(f"\n{'='*60}")
        print(f"Running: {test_file}")
        print('='*60)
        
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short"],
                capture_output=False,
                text=True
            )
            
            results[test_file] = result.returncode == 0
            if result.returncode != 0:
                all_passed = False
                
        except Exception as e:
            print(f"Error running {test_file}: {e}")
            results[test_file] = False
            all_passed = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_file, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{status}: {test_file}")
    
    print("="*60)
    
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("="*60)
        return 0
    else:
        print("❌ SOME TESTS FAILED")
        print("="*60)
        return 1


if __name__ == "__main__":
    sys.exit(run_tests())
