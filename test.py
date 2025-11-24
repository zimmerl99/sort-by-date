import requests
import json
import time

# API base URL
BASE_URL = "http://127.0.0.1:8002"

def print_test(test_name, passed):
    """Print test result with color"""
    status = "✓ PASSED" if passed else "✗ FAILED"
    print(f"{status}: {test_name}")

def test_root_endpoint():
    """Test 1: Root endpoint responds"""
    print("\n--- Test 1: Root Endpoint ---")
    try:
        response = requests.get(f"{BASE_URL}/")
        passed = response.status_code == 200
        print(f"Response: {response.json()}")
        print_test("Root endpoint accessible", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Root endpoint accessible", False)
        return False

def test_basic_sort():
    """Test 2: Basic date sorting"""
    print("\n--- Test 2: Basic Date Sorting ---")
    data = {
        "dates": ["2025-12-31", "2025-01-15", "2025-06-20", "2025-03-10"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/dates", json=data)
        result = response.json()
        
        expected = ["2025-01-15", "2025-03-10", "2025-06-20", "2025-12-31"]
        passed = (response.status_code == 200 and 
                 result['sorted_dates'] == expected and
                 result['count'] == 4)
        
        print(f"Input: {data['dates']}")
        print(f"Output: {result['sorted_dates']}")
        print(f"Expected: {expected}")
        print_test("Basic date sorting", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Basic date sorting", False)
        return False

def test_mixed_formats():
    """Test 3: Mixed input date formats"""
    print("\n--- Test 3: Mixed Input Formats ---")
    data = {
        "dates": [
            "2025-12-31",
            "01/15/2025",
            "June 20, 2025",
            "2025-03-10"
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/dates", json=data)
        result = response.json()
        
        # All should be sorted chronologically
        expected = ["2025-01-15", "2025-03-10", "2025-06-20", "2025-12-31"]
        passed = (response.status_code == 200 and 
                 result['sorted_dates'] == expected)
        
        print(f"Input: {data['dates']}")
        print(f"Output: {result['sorted_dates']}")
        print(f"Expected: {expected}")
        print_test("Mixed input formats", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Mixed input formats", False)
        return False

def test_custom_output_format():
    """Test 4: Custom output format"""
    print("\n--- Test 4: Custom Output Format ---")
    data = {
        "dates": ["2025-12-31", "2025-01-15", "2025-06-20"],
        "output_format": "%m/%d/%Y"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/dates", json=data)
        result = response.json()
        
        expected = ["01/15/2025", "06/20/2025", "12/31/2025"]
        passed = (response.status_code == 200 and 
                 result['sorted_dates'] == expected)
        
        print(f"Input: {data['dates']}")
        print(f"Output format: {data['output_format']}")
        print(f"Output: {result['sorted_dates']}")
        print(f"Expected: {expected}")
        print_test("Custom output format", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Custom output format", False)
        return False

def test_full_month_names():
    """Test 5: Full month name output"""
    print("\n--- Test 5: Full Month Names Output ---")
    data = {
        "dates": ["2025-01-15", "2025-12-31"],
        "output_format": "%B %d, %Y"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/dates", json=data)
        result = response.json()
        
        expected = ["January 15, 2025", "December 31, 2025"]
        passed = (response.status_code == 200 and 
                 result['sorted_dates'] == expected)
        
        print(f"Output: {result['sorted_dates']}")
        print(f"Expected: {expected}")
        print_test("Full month name output", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Full month name output", False)
        return False

def test_performance():
    """Test 6: Performance with 100 dates"""
    print("\n--- Test 6: Performance Test (100 dates) ---")
    
    # Generate 100 dates
    dates = []
    for i in range(100):
        month = (i % 12) + 1
        day = (i % 28) + 1
        dates.append(f"2025-{month:02d}-{day:02d}")
    
    data = {"dates": dates}
    
    try:
        start_time = time.time()
        response = requests.post(f"{BASE_URL}/dates", json=data)
        end_time = time.time()
        
        duration = end_time - start_time
        result = response.json()
        
        passed = (response.status_code == 200 and 
                 result['count'] == 100 and 
                 duration < 1.0)  # Should complete in under 1 second
        
        print(f"Processed {result['count']} dates")
        print(f"Time taken: {duration:.3f} seconds")
        print(f"Performance requirement: < 1 second")
        print_test("Performance test (100 dates < 1s)", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Performance test", False)
        return False

def test_empty_list():
    """Test 7: Empty date list (should fail gracefully)"""
    print("\n--- Test 7: Empty Date List ---")
    data = {"dates": []}
    
    try:
        response = requests.post(f"{BASE_URL}/dates", json=data)
        passed = response.status_code == 400  # Should return error
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        print_test("Empty list handled correctly", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Empty list handled correctly", False)
        return False

def test_invalid_date():
    """Test 8: Invalid date format"""
    print("\n--- Test 8: Invalid Date Format ---")
    data = {
        "dates": ["2025-01-15", "not-a-date", "2025-12-31"]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/dates", json=data)
        passed = response.status_code == 400  # Should return error
        
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.json()}")
        print_test("Invalid date handled correctly", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Invalid date handled correctly", False)
        return False

def test_consistency():
    """Test 9: Consistency - same input always produces same output"""
    print("\n--- Test 9: Consistency Test ---")
    data = {
        "dates": ["2025-12-31", "01/15/2025", "2025-06-20"],
        "output_format": "%Y-%m-%d"
    }
    
    try:
        # Make the same request 3 times
        results = []
        for i in range(3):
            response = requests.post(f"{BASE_URL}/dates", json=data)
            result = response.json()
            results.append(result['sorted_dates'])
        
        # All results should be identical
        passed = all(r == results[0] for r in results)
        
        print(f"Request made 3 times")
        print(f"Result 1: {results[0]}")
        print(f"Result 2: {results[1]}")
        print(f"Result 3: {results[2]}")
        print_test("Consistency (same input = same output)", passed)
        return passed
    except Exception as e:
        print(f"Error: {e}")
        print_test("Consistency test", False)
        return False

def run_all_tests():
    """Run all tests and print summary"""
    print("=" * 60)
    print("DATE SORTING MICROSERVICE - TEST SUITE")
    print("=" * 60)
    
    tests = [
        test_root_endpoint,
        test_basic_sort,
        test_mixed_formats,
        test_custom_output_format,
        test_full_month_names,
        test_performance,
        test_empty_list,
        test_invalid_date,
        test_consistency
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"Test failed with exception: {e}")
            results.append(False)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    print(f"Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed. Please review above.")
    
    return passed == total

if __name__ == "__main__":
    print("\nMake sure your API is running on http://127.0.0.1:8001")
    print("Start it with: python -m uvicorn your_filename:app --reload --port 8001\n")
    input("Press Enter to start tests...")
    
    run_all_tests()