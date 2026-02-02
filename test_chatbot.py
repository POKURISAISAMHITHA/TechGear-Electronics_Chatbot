#!/usr/bin/env python3
"""
Automated Test Suite for TechGear Electronics Chatbot
Tests various query types to validate RAG system performance
"""

import requests
import json
import time
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Configuration
API_URL = "http://localhost:8000/chat"
TEST_QUERIES_FILE = "test_queries.json"

class ChatbotTester:
    def __init__(self, api_url):
        self.api_url = api_url
        self.results = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "response_times": [],
            "category_results": {}
        }
    
    def test_query(self, query, category="general"):
        """Send a single query to the chatbot and return results"""
        try:
            start_time = time.time()
            response = requests.post(
                self.api_url,
                json={"query": query},
                timeout=30
            )
            end_time = time.time()
            response_time = end_time - start_time
            
            self.results["response_times"].append(response_time)
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "status": "success",
                    "query": query,
                    "answer": result.get("answer", ""),
                    "category": result.get("category", "unknown"),
                    "routed_to": result.get("routed_to", "unknown"),
                    "response_time": response_time
                }
            else:
                return {
                    "status": "failed",
                    "query": query,
                    "error": f"HTTP {response.status_code}",
                    "response_time": response_time
                }
        
        except requests.exceptions.ConnectionError:
            return {
                "status": "error",
                "query": query,
                "error": "Connection refused - Server not running?"
            }
        except Exception as e:
            return {
                "status": "error",
                "query": query,
                "error": str(e)
            }
    
    def run_test_category(self, category_name, queries):
        """Run all tests in a category"""
        print(f"\n{'='*80}")
        print(f"{Fore.CYAN}Testing: {category_name.upper().replace('_', ' ')}")
        print(f"{'='*80}")
        
        category_results = []
        
        for i, query in enumerate(queries, 1):
            print(f"\n{Fore.YELLOW}[{i}/{len(queries)}] Query: {query}")
            
            result = self.test_query(query, category_name)
            category_results.append(result)
            self.results["total_tests"] += 1
            
            if result["status"] == "success":
                self.results["passed"] += 1
                print(f"{Fore.GREEN}✓ SUCCESS")
                print(f"{Fore.WHITE}Answer: {result['answer'][:150]}...")
                print(f"Category: {result['category']} | Routed to: {result['routed_to']}")
                print(f"Response time: {result['response_time']:.2f}s")
            elif result["status"] == "failed":
                self.results["failed"] += 1
                print(f"{Fore.RED}✗ FAILED: {result['error']}")
            else:
                self.results["errors"] += 1
                print(f"{Fore.RED}✗ ERROR: {result['error']}")
            
            # Small delay to avoid overwhelming the server
            time.sleep(0.5)
        
        self.results["category_results"][category_name] = category_results
        return category_results
    
    def run_all_tests(self, test_file):
        """Run all test categories from JSON file"""
        try:
            with open(test_file, 'r') as f:
                test_data = json.load(f)
            
            print(f"\n{Fore.MAGENTA}{'='*80}")
            print(f"{Fore.MAGENTA}TechGear Electronics Chatbot - Test Suite")
            print(f"{Fore.MAGENTA}{'='*80}")
            print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            
            for category, data in test_data["test_queries"].items():
                description = data.get("description", "")
                queries = data.get("queries", [])
                
                print(f"\n{Fore.BLUE}Category: {category}")
                print(f"{Fore.WHITE}Description: {description}")
                
                self.run_test_category(category, queries)
            
            self.print_summary()
            
        except FileNotFoundError:
            print(f"{Fore.RED}Error: Test file '{test_file}' not found")
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Invalid JSON in test file")
    
    def run_quick_test(self):
        """Run a quick subset of important tests"""
        quick_tests = {
            "Product Query": [
                "What smartwatches do you have?",
                "Show me all laptops"
            ],
            "Feature Query": [
                "Tell me about the SmartWatch Pro X features"
            ],
            "Price Query": [
                "How much does the UltraBook Pro 15 cost?"
            ],
            "Policy Query": [
                "What is your return policy?"
            ],
            "Invalid Query": [
                "What's the weather today?"
            ]
        }
        
        print(f"\n{Fore.MAGENTA}{'='*80}")
        print(f"{Fore.MAGENTA}TechGear Electronics Chatbot - Quick Test")
        print(f"{Fore.MAGENTA}{'='*80}\n")
        
        for category, queries in quick_tests.items():
            self.run_test_category(category.lower().replace(" ", "_"), queries)
        
        self.print_summary()
    
    def print_summary(self):
        """Print test results summary"""
        print(f"\n\n{Fore.MAGENTA}{'='*80}")
        print(f"{Fore.MAGENTA}TEST RESULTS SUMMARY")
        print(f"{Fore.MAGENTA}{'='*80}\n")
        
        total = self.results["total_tests"]
        passed = self.results["passed"]
        failed = self.results["failed"]
        errors = self.results["errors"]
        
        print(f"{Fore.WHITE}Total Tests: {total}")
        print(f"{Fore.GREEN}✓ Passed: {passed} ({passed/total*100:.1f}%)" if total > 0 else "No tests run")
        print(f"{Fore.RED}✗ Failed: {failed} ({failed/total*100:.1f}%)" if total > 0 else "")
        print(f"{Fore.RED}✗ Errors: {errors} ({errors/total*100:.1f}%)" if total > 0 else "")
        
        if self.results["response_times"]:
            avg_time = sum(self.results["response_times"]) / len(self.results["response_times"])
            min_time = min(self.results["response_times"])
            max_time = max(self.results["response_times"])
            
            print(f"\n{Fore.CYAN}Response Time Statistics:")
            print(f"{Fore.WHITE}  Average: {avg_time:.2f}s")
            print(f"{Fore.WHITE}  Min: {min_time:.2f}s")
            print(f"{Fore.WHITE}  Max: {max_time:.2f}s")
        
        # Category breakdown
        print(f"\n{Fore.CYAN}Results by Category:")
        for category, results in self.results["category_results"].items():
            success_count = sum(1 for r in results if r["status"] == "success")
            total_count = len(results)
            success_rate = (success_count / total_count * 100) if total_count > 0 else 0
            print(f"{Fore.WHITE}  {category.replace('_', ' ').title()}: {success_count}/{total_count} ({success_rate:.1f}%)")
        
        print(f"\n{Fore.MAGENTA}{'='*80}\n")
        
        # Save results to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        results_file = f"test_results_{timestamp}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"{Fore.GREEN}Results saved to: {results_file}\n")

def main():
    """Main function"""
    import sys
    
    tester = ChatbotTester(API_URL)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        print(f"{Fore.YELLOW}Running quick test suite...")
        tester.run_quick_test()
    elif len(sys.argv) > 1 and sys.argv[1] == "--single":
        if len(sys.argv) < 3:
            print(f"{Fore.RED}Usage: python test_chatbot.py --single \"Your query here\"")
            return
        query = " ".join(sys.argv[2:])
        print(f"\n{Fore.CYAN}Testing single query: {query}\n")
        result = tester.test_query(query)
        if result["status"] == "success":
            print(f"{Fore.GREEN}✓ SUCCESS")
            print(f"\n{Fore.WHITE}Query: {result['query']}")
            print(f"Answer: {result['answer']}")
            print(f"Category: {result['category']}")
            print(f"Routed to: {result['routed_to']}")
            print(f"Response time: {result['response_time']:.2f}s\n")
        else:
            print(f"{Fore.RED}✗ {result['status'].upper()}: {result.get('error', 'Unknown error')}\n")
    else:
        print(f"{Fore.YELLOW}Running full test suite...")
        tester.run_all_tests(TEST_QUERIES_FILE)

if __name__ == "__main__":
    main()
