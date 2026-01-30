"""
API Testing Script for Customer Support Chatbot
Tests the FastAPI endpoints with sample requests
"""

import requests
import json
import time

# API Configuration
BASE_URL = "http://localhost:8000"
HEALTH_ENDPOINT = f"{BASE_URL}/health"
CHAT_ENDPOINT = f"{BASE_URL}/chat"
INFO_ENDPOINT = f"{BASE_URL}/info"

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def print_header(text):
    """Print formatted header"""
    print(f"\n{BOLD}{BLUE}{'=' * 70}{RESET}")
    print(f"{BOLD}{BLUE}{text}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 70}{RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{GREEN}✓ {text}{RESET}")


def print_error(text):
    """Print error message"""
    print(f"{RED}✗ {text}{RESET}")


def print_info(text):
    """Print info message"""
    print(f"{BLUE}ℹ {text}{RESET}")


def test_health_check():
    """Test health check endpoint"""
    print_header("TEST 1: Health Check")
    
    try:
        response = requests.get(HEALTH_ENDPOINT)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Status: {data['status']}")
            print_success(f"Message: {data['message']}")
            print_success("Health check passed!")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_info_endpoint():
    """Test info endpoint"""
    print_header("TEST 2: Application Info")
    
    try:
        response = requests.get(INFO_ENDPOINT)
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Name: {data['name']}")
            print_success(f"Version: {data['version']}")
            print_success("Info retrieved successfully!")
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_chat_query(query, expected_category=None):
    """Test chat endpoint with a query"""
    print_header(f"TEST: Chat Query")
    print(f"{BOLD}Query:{RESET} {query}")
    
    try:
        payload = {"query": query}
        
        print_info(f"Sending request to {CHAT_ENDPOINT}")
        response = requests.post(CHAT_ENDPOINT, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            print_success(f"Status: OK")
            print_success(f"Category: {data.get('category', 'N/A')}")
            print_success(f"Routed to: {data.get('routed_to', 'N/A')}")
            
            if expected_category and data.get('category') == expected_category:
                print_success(f"Category matches expected: {expected_category}")
            
            print(f"\n{BOLD}Answer:{RESET}")
            print(f"{data.get('answer', 'No answer')}\n")
            
            return True
        else:
            print_error(f"Status code: {response.status_code}")
            print_error(f"Response: {response.text}")
            return False
    
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def test_invalid_query():
    """Test with invalid query"""
    print_header("TEST: Invalid Query (Empty)")
    
    try:
        payload = {"query": "   "}
        
        response = requests.post(CHAT_ENDPOINT, json=payload)
        
        if response.status_code == 422:
            print_success("Validation error caught as expected")
            print_success("Empty queries are properly rejected")
            return True
        else:
            print_error(f"Unexpected status code: {response.status_code}")
            return False
    
    except Exception as e:
        print_error(f"Error: {e}")
        return False


def main():
    """Run all tests"""
    
    print(f"\n{BOLD}{BLUE}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║  Customer Support Chatbot API Test Suite                 ║")
    print("║  Base URL: http://localhost:8000                         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{RESET}\n")
    
    # Wait for server to be ready
    print_info("Waiting for server to be ready...")
    time.sleep(2)
    
    # Track results
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    time.sleep(1)
    
    results.append(("App Info", test_info_endpoint()))
    time.sleep(1)
    
    results.append(("Chat - Products Query", test_chat_query(
        "What is the price of SmartWatch Pro X?",
        expected_category="products"
    )))
    time.sleep(1)
    
    results.append(("Chat - General Query", test_chat_query(
        "What are your support hours?",
        expected_category="general"
    )))
    time.sleep(1)
    
    results.append(("Chat - Unknown Query", test_chat_query(
        "Tell me about quantum computing",
        expected_category="unknown"
    )))
    time.sleep(1)
    
    results.append(("Invalid Query", test_invalid_query()))
    
    # Print summary
    print_header("TEST SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name}: {status}")
    
    print(f"\n{BOLD}Results: {passed}/{total} tests passed{RESET}\n")
    
    if passed == total:
        print_success("All tests passed! ✅")
        return 0
    else:
        print_error(f"{total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    import sys
    exit_code = main()
    sys.exit(exit_code)
