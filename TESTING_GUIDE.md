# 🧪 Comprehensive Testing Guide for TechGear Electronics Chatbot

## Quick Start

### 1. Manual Testing (Single Query)
```bash
# Basic query
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What smartwatches do you have?"}'

# Or use the test script
python test_chatbot.py --single "What smartwatches do you have?"
```

### 2. Quick Test Suite (5-6 queries)
```bash
python test_chatbot.py --quick
```

### 3. Full Test Suite (100+ queries)
```bash
python test_chatbot.py
```

---

## 📋 Test Categories & Sample Questions

### 1. **Product Queries** (General Product Lists)
Test if the chatbot can retrieve product categories correctly.

✅ **Try these:**
```bash
# Smartwatches
"What smartwatches do you have?"
"Show me all smartwatches"
"List your wearable devices"

# Laptops
"What laptops are available?"
"Show me all laptops"
"Do you have gaming laptops?"

# Earbuds
"What wireless earbuds do you sell?"
"List all audio products"
"Show me earbuds with noise cancellation"

# Other categories
"What cameras do you have?"
"Show me power banks"
"List all drones"
"What smart home devices are available?"
```

**Expected Result:** Should list relevant products from that category

---

### 2. **Specific Product Features**
Test detailed information extraction from product descriptions.

✅ **Try these:**
```bash
"Tell me about the SmartWatch Pro X features"
"What are the specifications of SmartWatch Classic Gold?"
"What's included with the TrueSound Pro earbuds?"
"What's the battery life of SmartWatch Pro X?"
"Is the ActionCam Pro waterproof?"
"What sensors does the SmartWatch have?"
```

**Expected Result:** Should return specific features, specs, and capabilities

---

### 3. **Price Queries**
Test price information retrieval.

✅ **Try these:**
```bash
"How much does the SmartWatch Pro X cost?"
"What's the price of TrueSound Pro earbuds?"
"How much is the UltraBook Pro 15?"
"Price of PowerMax 20000 power bank?"
"What are your cheapest products?"
"What's the most expensive smartwatch?"
```

**Expected Result:** Should return accurate pricing from product info

---

### 4. **Comparison Queries**
Test multi-product comparison and differentiation.

✅ **Try these:**
```bash
"Compare SmartWatch Pro X and SmartWatch Classic Gold"
"What's the difference between TrueSound Pro and TrueSound Bass earbuds?"
"Which smartwatch has better battery life?"
"Compare all your laptops"
"What's better: SmartWatch Pro X or SmartWatch Ultra Sport?"
```

**Expected Result:** Should compare features and highlight differences

---

### 5. **Availability & Stock Queries**
Test inventory information retrieval.

✅ **Try these:**
```bash
"Is the SmartWatch Pro X in stock?"
"What products are available now?"
"Are all smartwatches in stock?"
"Which items are out of stock?"
"When will SmartWatch Classic Gold be available?"
```

**Expected Result:** Should return stock status from product_info.txt

---

### 6. **Policy Queries** (Returns, Warranty, Shipping)
Test company policy information retrieval.

✅ **Try these:**
```bash
# Return Policy
"What is your return policy?"
"How long do I have to return a product?"
"Can I return opened items?"
"What's your refund policy?"

# Warranty
"What warranty do you offer?"
"How long is the warranty on smartwatches?"
"What does the warranty cover?"

# Shipping
"Do you offer free shipping?"
"What are your delivery options?"
"How long does shipping take?"

# Other Policies
"Do you have a price match guarantee?"
"What are your customer support hours?"
```

**Expected Result:** Should return accurate policy information

---

### 7. **Technical Specifications**
Test retrieval of detailed technical specs.

✅ **Try these:**
```bash
"What processor does the UltraBook Pro have?"
"How much RAM does the gaming laptop have?"
"What's the screen size of SmartWatch Pro X?"
"What Bluetooth version do the earbuds use?"
"What's the camera resolution on the drone?"
"What's the refresh rate of the gaming monitor?"
"How many USB ports on the laptop?"
```

**Expected Result:** Should extract specific technical details

---

### 8. **Category-Level Queries**
Test broad category information.

✅ **Try these:**
```bash
"What wearable devices do you sell?"
"Show me all audio products"
"What computing devices are available?"
"List all smart home products"
"What photography equipment do you have?"
"Show me all mobile accessories"
```

**Expected Result:** Should list all products in that category

---

### 9. **Feature-Based Searches**
Test filtering by specific features.

✅ **Try these:**
```bash
"Which products have water resistance?"
"What devices have GPS tracking?"
"Which laptops have touchscreens?"
"What products have wireless charging?"
"Which earbuds have active noise cancellation?"
"What devices work with Alexa?"
"Which cameras shoot 4K video?"
"What smartwatches have heart rate monitors?"
```

**Expected Result:** Should filter and return matching products

---

### 10. **Conversational/Intent-Based Queries**
Test natural language understanding.

✅ **Try these:**
```bash
"I need a smartwatch for running"
"Looking for a laptop for gaming"
"Want earbuds for the gym"
"Need a gift for a photographer"
"Best product for home office setup"
"Something for outdoor activities"
"Device for fitness tracking"
"Recommend a product for music lovers"
```

**Expected Result:** Should understand intent and recommend relevant products

---

### 11. **Complex Multi-Part Queries**
Test handling of queries with multiple conditions.

✅ **Try these:**
```bash
"What smartwatches have GPS AND heart rate monitoring?"
"Do you have laptops with 16GB RAM AND SSD storage?"
"Which products come with a 2-year warranty?"
"What earbuds have noise cancellation AND long battery life?"
"I want a 4K monitor with high refresh rate"
"Show me waterproof cameras under $500"
"Which smartwatch has the best battery life and is water resistant?"
```

**Expected Result:** Should handle multiple conditions and return matching products

---

### 12. **Support/Escalation Queries**
Test routing to human support.

✅ **Try these:**
```bash
"I need help with my order"
"My product is defective"
"How do I track my order?"
"I want to cancel my order"
"Need to speak to customer service"
"File a complaint"
"Product not working properly"
"I have a billing issue"
```

**Expected Result:** Should route to escalation and provide support contact info

---

### 13. **Edge Cases & Invalid Queries**
Test fallback handling and error scenarios.

✅ **Try these:**
```bash
# Out of scope
"What's the weather today?"
"Tell me a joke"
"Who is the president?"
"What's 2+2?"

# Non-existent products
"Do you sell phone cases?"
"Do you have car accessories?"
"Do you sell furniture?"

# Ambiguous queries
"Show me products"
"What do you have?"
"Tell me something"

# Gibberish
"asdfghjkl"
"xyz123abc"
```

**Expected Result:** Should handle gracefully with appropriate fallback responses

---

## 🎯 Key Testing Scenarios

### Scenario 1: Product Discovery Journey
```bash
1. "What smartwatches do you have?"
2. "Tell me about the SmartWatch Pro X features"
3. "How much does it cost?"
4. "Is it in stock?"
5. "What's your return policy?"
```

### Scenario 2: Comparison Shopping
```bash
1. "Show me all earbuds"
2. "Compare TrueSound Pro and TrueSound Bass"
3. "Which one has better battery life?"
4. "How much does TrueSound Pro cost?"
```

### Scenario 3: Feature-Based Search
```bash
1. "Which products have water resistance?"
2. "Tell me more about the waterproof smartwatch"
3. "Does it have GPS?"
4. "What's the warranty?"
```

### Scenario 4: Problem Resolution
```bash
1. "I need help with my order"
2. "How do I return a product?"
3. "What's your refund policy?"
```

---

## 📊 Performance Metrics to Track

### ✅ Success Metrics
- **Response Accuracy**: Does it return correct information?
- **Response Time**: Is it under 5 seconds?
- **Context Relevance**: Are retrieved chunks relevant?
- **Completeness**: Does it answer the full question?
- **Category Classification**: Is the query classified correctly?

### ⚠️ Failure Patterns to Watch
- Returns "Information not available" for valid products
- Incorrect product information
- Mixing up product details
- Routing errors (wrong node)
- Slow responses (>10 seconds)
- API errors or timeouts

---

## 🚀 Running Automated Tests

### Quick Test (5-6 queries)
```bash
python test_chatbot.py --quick
```
**Tests:** Product query, features, price, policy, invalid query

### Full Test Suite (100+ queries)
```bash
python test_chatbot.py
```
**Tests:** All 14 categories with multiple queries each

### Single Query Test
```bash
python test_chatbot.py --single "Your question here"
```

---

## 📈 Expected Results

### Good Performance:
- ✅ 95%+ success rate on product queries
- ✅ 90%+ success rate on feature queries
- ✅ 100% success rate on policy queries
- ✅ Average response time: 2-5 seconds
- ✅ Proper routing (products → rag_responder, support → escalation)

### Areas That May Need Improvement:
- ⚠️ Complex multi-condition queries
- ⚠️ Ambiguous questions
- ⚠️ Comparison queries (may need better prompting)
- ⚠️ Price queries for specific products (if not explicitly in chunks)

---

## 🔧 Troubleshooting

If tests fail:

1. **Check server is running**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check logs**
   ```bash
   tail -f /tmp/server_log.txt
   ```

3. **Verify embeddings exist**
   ```bash
   ls -la chroma_db/
   ```

4. **Test single query**
   ```bash
   python test_chatbot.py --single "What smartwatches do you have?"
   ```

---

## 📝 Sample Test Commands

```bash
# Test product retrieval
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" \
  -d '{"query": "What smartwatches do you have?"}'

# Test features
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" \
  -d '{"query": "Tell me about SmartWatch Pro X features"}'

# Test policy
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" \
  -d '{"query": "What is your return policy?"}'

# Test edge case
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" \
  -d '{"query": "What is the weather?"}'
```

---

## 🎓 Test Results Analysis

After running tests, check:

1. **test_results_TIMESTAMP.json** - Detailed results
2. Response time statistics
3. Success rate by category
4. Failed queries (investigate why)

---

**Happy Testing! 🚀**
