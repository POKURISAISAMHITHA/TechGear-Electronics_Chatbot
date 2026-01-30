"""
Simple API Test - Uses only stdlib (no external dependencies needed)
Tests the FastAPI endpoints after manual server startup
"""

import json
import urllib.request
import urllib.error
import time
import sys

# Configuration
BASE_URL = "http://localhost:8000"

# Colors
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'


def make_request(method, endpoint, data=None):
    """Make HTTP request using stdlib"""
    url = f"{BASE_URL}{endpoint}"
    
    try:
        if method == "GET":
            req = urllib.request.Request(url, method="GET")
        elif method == "POST":
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method="POST"
            )
        
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read())
    
    except urllib.error.HTTPError as e:
        return e.code, {"error": str(e)}
    except Exception as e:
        return None, {"error": str(e)}


def test_health():
    """Test health endpoint"""
    print(f"\n{BOLD}{BLUE}TEST 1: Health Check{RESET}")
    status, data = make_request("GET", "/health")
    
    if status == 200:
        print(f"{GREEN}✓ Status: {data.get('status')}{RESET}")
        print(f"{GREEN}✓ Message: {data.get('message')}{RESET}")
        return True
    else:
        print(f"{RED}✗ Failed with status {status}{RESET}")
        return False


def test_chat():
    """Test chat endpoint"""
    print(f"\n{BOLD}{BLUE}TEST 2: Chat Endpoint{RESET}")
    
    payload = {"query": "What is the price of SmartWatch Pro X?"}
    status, data = make_request("POST", "/chat", payload)
    
    if status == 200:
        print(f"{GREEN}✓ Answer: {data.get('answer')[:80]}...{RESET}")
        print(f"{GREEN}✓ Category: {data.get('category')}{RESET}")
        print(f"{GREEN}✓ Routed to: {data.get('routed_to')}{RESET}")
        return True
    else:
        print(f"{RED}✗ Failed with status {status}{RESET}")
        if 'error' in data:
            print(f"{RED}✗ Error: {data.get('error')}{RESET}")
        return False


def test_info():
    """Test info endpoint"""
    print(f"\n{BOLD}{BLUE}TEST 3: Info Endpoint{RESET}")
    status, data = make_request("GET", "/info")
    
    if status == 200:
        print(f"{GREEN}✓ Name: {data.get('name')}{RESET}")
        print(f"{GREEN}✓ Version: {data.get('version')}{RESET}")
        return True
    else:
        print(f"{RED}✗ Failed with status {status}{RESET}")
        return False


def main():
    """Run tests"""
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}FastAPI Backend Tests (Simplified){RESET}")
    print(f"{BOLD}{BLUE}Server must be running at http://localhost:8000{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}")
    
    print(f"\n{BOLD}Instructions to start server:{RESET}")
    print("  cd /home/labuser/Customer_support_chatbot")
    print("  python -m uvicorn main:app --host 0.0.0.0 --port 8000")
    print("\nOr in another terminal while keeping this script ready...")
    
    # Quick connectivity check
    print(f"\n{BOLD}Checking server connectivity...{RESET}")
    status, _ = make_request("GET", "/health")
    
    if status is None:
        print(f"{RED}✗ Cannot connect to http://localhost:8000{RESET}")
        print(f"{RED}Make sure the server is running!{RESET}")
        return 1
    
    # Run tests
    results = [
        ("Health Check", test_health()),
        ("Chat Endpoint", test_chat()),
        ("Info Endpoint", test_info()),
    ]
    
    # Summary
    print(f"\n{BOLD}{BLUE}{'='*60}{RESET}")
    print(f"{BOLD}{BLUE}Test Summary{RESET}")
    print(f"{BOLD}{BLUE}{'='*60}{RESET}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status_text = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {test_name}: {status_text}")
    
    print(f"\n{BOLD}Results: {passed}/{total} tests passed{RESET}\n")
    
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
