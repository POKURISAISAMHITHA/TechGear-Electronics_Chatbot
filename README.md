# 🤖 TechGear Customer Support Chatbot

```
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║          🚀 TechGear Customer Support Chatbot - AI Powered! 🚀          ║
║                                                                          ║
║   Intelligent • Conversational • RAG-Powered • Production-Ready         ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
```

> 💡 **A production-ready AI-powered customer support chatbot** built with FastAPI, LangGraph, and Google Gemini AI. Features intelligent query classification, RAG (Retrieval-Augmented Generation), and natural conversation handling for TechGear product support.

---

<div align="center">

![Version](https://img.shields.io/badge/version-1.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.10+-green?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=for-the-badge)
![Status](https://img.shields.io/badge/status-Production%20Ready-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

</div>

---

## ✨ Features & Capabilities

### 🎯 Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 🤖 **Intelligent Classification** | Auto-categorizes queries into products, returns, general, or unknown | ✅ |
| 💬 **Natural Conversations** | Handles greetings ("hi", "hello"), acknowledgments, and friendly responses | ✅ |
| 📦 **Product Intelligence** | Detailed specs, pricing, warranty, and feature information | ✅ |
| ❓ **Yes/No Detection** | Smart detection and proper formatting of yes/no questions | ✅ |
| 🧠 **RAG System** | Context-aware responses using ChromaDB embeddings & Gemini | ✅ |
| 👤 **Human Escalation** | Routes complex queries to support team seamlessly | ✅ |
| 🎨 **Beautiful Web UI** | Modern, responsive chat interface with real-time updates | ✅ |
| 📡 **REST API** | Easy integration with external systems (FastAPI) | ✅ |
| 🛡️ **Error Handling** | Graceful fallbacks and comprehensive error recovery | ✅ |

### 🛠️ Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    ARCHITECTURE                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🌐 Frontend (Web UI)                                       │
│  ├── HTML/CSS/JavaScript (Vanilla)                          │
│  └── Real-time Chat Interface                              │
│                                                             │
│  ⚡ API Layer (FastAPI)                                     │
│  ├── REST Endpoints                                         │
│  └── Request/Response Validation (Pydantic)                │
│                                                             │
│  🧠 LLM Orchestration (LangGraph)                           │
│  ├── Query Classification Node                              │
│  ├── RAG Responder Node                                     │
│  └── Escalation Node                                        │
│                                                             │
│  🤖 AI/ML Layer                                             │
│  ├── Google Gemini (LLM)                                    │
│  ├── Google Embeddings (models/embedding-001)               │
│  └── LangChain (Framework)                                  │
│                                                             │
│  💾 Data Layer                                              │
│  ├── ChromaDB (Vector Store)                                │
│  └── product_info.txt (Knowledge Base)                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Key Technologies:**
- 🐍 **Python 3.10+** - Programming Language
- ⚡ **FastAPI 0.109.0** - Web Framework
- 🤖 **Google Gemini** - LLM Engine
- 🧠 **LangGraph 1.0.7** - Workflow Orchestration
- 🔗 **LangChain 1.2.7** - AI Framework
- 🗄️ **ChromaDB 0.4.24** - Vector Database
- 🚀 **Uvicorn** - ASGI Server

---

## 🎨 User Interface Showcase

### 💬 Sample Chat Conversations

#### Example 1: Product Information Query

```
╔════════════════════════════════════════════════════════════════╗
║           TechGear Customer Support Chat                       ║
╚════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  👤 You: What is the price of SmartWatch Pro X?               │
│                                                                │
│  🤖 Bot: SmartWatch Pro X: Price ₹15,999 | AMOLED             │
│           display, 14-day battery, fitness tracking, water    │
│           resistant, sleep monitoring | Standard warranty:    │
│           1 year, Extended: 2 years (₹2,999)                 │
│                                                                │
│  👤 You: Can I return it within 30 days?                      │
│                                                                │
│  🤖 Bot: No, return window is 7 days (from purchase)         │
│                                                                │
│  👤 You: ok thanks!                                           │
│                                                                │
│  🤖 Bot: Thank you! Hope my response was helpful. Feel        │
│           free to ask if you have any other questions! 😊    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

#### Example 2: Greeting & Product Listing

```
╔════════════════════════════════════════════════════════════════╗
║           TechGear Customer Support Chat                       ║
╚════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  👤 You: Hi! What products do you sell?                       │
│                                                                │
│  🤖 Bot: Hi! How can I help you today?                        │
│           SmartWatch Pro X, Wireless Earbuds Elite,           │
│           Power Bank Ultra                                    │
│                                                                │
│  👤 You: Tell me about the earbuds                            │
│                                                                │
│  🤖 Bot: Wireless Earbuds Elite: Price ₹7,999 | Active       │
│           noise cancellation, premium sound, 20-hour battery,│
│           water resistant | Standard warranty: 1 year,       │
│           Extended: 2 years (₹1,999)                         │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

#### Example 3: Technical Support

```
╔════════════════════════════════════════════════════════════════╗
║           TechGear Customer Support Chat                       ║
╚════════════════════════════════════════════════════════════════╝

┌────────────────────────────────────────────────────────────────┐
│                                                                │
│  👤 You: How long does the smartwatch battery last?           │
│                                                                │
│  🤖 Bot: SmartWatch Pro X has a 14-day battery life. The      │
│           battery duration depends on usage patterns and      │
│           features enabled.                                   │
│                                                                │
│  👤 You: Is it water resistant?                               │
│                                                                │
│  🤖 Bot: Yes, SmartWatch Pro X is water resistant and can     │
│           be used during swimming and water sports.           │
│                                                                │
│  👤 You: What about warranty coverage?                        │
│                                                                │
│  🤖 Bot: SmartWatch Pro X comes with standard 1-year         │
│           warranty covering manufacturing defects. Extended   │
│           warranty available for ₹2,999 (2 years).            │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### 🖥️ Web Interface Preview

```
┌─────────────────────────────────────────────────────────────────┐
│  🌐 http://localhost:8000                          ✕ ☐ ⛶        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│          ╔═════════════════════════════════════════╗            │
│          ║  🚀 TechGear Support Assistant          ║            │
│          ║  Status: 🟢 Online                       ║            │
│          ╚═════════════════════════════════════════╝            │
│                                                                 │
│          ╔═════════════════════════════════════════╗            │
│          ║ Chat History                            ║            │
│          ├─────────────────────────────────────────┤            │
│          ║                                         ║            │
│          ║  🤖 Bot:                               ║            │
│          ║  Hi! How can I help you today? 😊      ║            │
│          ║                                         ║            │
│          ║  👤 You:                                ║            │
│          ║  What is the price of smartwatch?      ║            │
│          ║  14:32 PM                              ║            │
│          ║                                         ║            │
│          ║  🤖 Bot:                               ║            │
│          ║  SmartWatch Pro X: Price ₹15,999       ║            │
│          ║  AMOLED display, 14-day battery...     ║            │
│          ║  14:32 PM                              ║            │
│          ║                                         ║            │
│          ║  [Bot is typing... ⌛]                  ║            │
│          ║                                         ║            │
│          ╚═════════════════════════════════════════╝            │
│                                                                 │
│          ╔═════════════════════════════════════════╗            │
│          ║ 📝 Type your message...                 ║            │
│          ║ [Max 1000 characters]          [Send →] ║            │
│          ╚═════════════════════════════════════════╝            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 🎯 Query Classification Flow

```
                    📝 User Query
                         │
                         ▼
            ┌─────────────────────────┐
            │  Gemini Classifier      │
            │  (with Fallback)        │
            └────────────┬────────────┘
                         │
        ┌────────────────┼────────────────┐
        │                │                │
        ▼                ▼                ▼
   ┌─────────┐    ┌─────────────┐    ┌─────────┐
   │ Products│    │   General   │    │ Unknown │
   │ Returns │    │ Greetings   │    │  Queries│
   │ Features│    │Acknowledgmts│    │         │
   └────┬────┘    └──────┬──────┘    └────┬────┘
        │                │                │
        ▼                ▼                ▼
   ┌─────────────┐  ┌──────────────┐  ┌────────────┐
   │ RAG Chain   │  │ Response     │  │ Escalation │
   │ ChromaDB    │  │ Mapping      │  │ to Human   │
   │ Retrieval   │  │              │  │            │
   └────────┬────┘  └──────┬───────┘  └────────┬───┘
            │              │                   │
            └──────────────┼───────────────────┘
                           │
                           ▼
                    🤖 Response to User
```

---

## 📋 Prerequisites

- 🐍 Python 3.10+
- 🔑 Google Gemini API Key
- 📦 pip (Python package manager)

### Get Google Gemini API Key
1. Visit [🔗 Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy your API key to `.env` file

---

## 🚀 Quick Start (7 Steps)

### Step 1️⃣: Clone Repository
```bash
git clone https://github.com/yourusername/TECHGEAR-CHATBOT.git
cd TECHGEAR-CHATBOT
```

### Step 2️⃣: Setup Environment
```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# On Windows use: .venv\Scripts\activate
```

### Step 3️⃣: Install Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements_api.txt
```

### Step 4️⃣: Configure API Key
```bash
# Create .env file with your Gemini API key
cat > .env << EOF
GEMINI_API_KEY=your_api_key_here
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=False
EOF
```

### Step 5️⃣: Setup Embeddings
```bash
# Run once to create and store embeddings
python embed_and_store.py
```

### Step 6️⃣: Start Server
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Step 7️⃣: Open Chat UI
```
🌐 Open browser: http://localhost:8000
```

---

## 📁 Project Structure

```
TECHGEAR-CHATBOT/
│
├── 🔧 Core Application
│   ├── main.py                    ← FastAPI backend & UI server
│   ├── langgraph_workflow.py      ← LangGraph production workflow
│   ├── rag_chain.py               ← RAG implementation
│   └── embed_and_store.py         ← Embedding pipeline
│
├── 🎨 Frontend
│   └── index.html                 ← Web chat UI (served by FastAPI)
│
├── 📚 Knowledge Base
│   └── product_info.txt           ← Product information
│
├── 🗄️ Data
│   └── chroma_db/                 ← Vector database (auto-created)
│
├── ⚙️ Configuration
│   ├── .env                       ← API credentials (create this)
│   ├── .gitignore                 ← Git ignore rules
│   ├── requirements.txt           ← Core dependencies
│   └── requirements_api.txt       ← API dependencies
│
├── 📖 Documentation
│   ├── README.md                  ← This file
│   ├── CONVERSATION_FEATURES.md   ← Feature guide
│   ├── FASTAPI_COMPLETE.md        ← API documentation
│   ├── LANGGRAPH_GUIDE.md         ← Workflow guide
│   └── UI_GUIDE.md                ← UI documentation
│
└── 🧪 Testing
    └── test_api.py                ← API test suite
```

---

## 🧪 Testing & Validation

### ✅ Run Full Test Suite
```bash
# Terminal 1: Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Terminal 2: Run tests
python test_api.py
```

### ✅ Expected Test Results
```
╔════════════════════════════════════════════╗
║          🧪 TEST RESULTS                   ║
╠════════════════════════════════════════════╣
║ ✅ Health Check........................ PASS ║
║ ✅ App Info........................... PASS ║
║ ✅ Chat - Products Query............. PASS ║
║ ✅ Chat - General Query.............. PASS ║
║ ✅ Chat - Unknown Query.............. PASS ║
║ ✅ Invalid Query..................... PASS ║
╠════════════════════════════════════════════╣
║ 📊 Results: 6/6 tests passed ✅           ║
║ ⏱️  Total Time: ~2.5 seconds              ║
╚════════════════════════════════════════════╝
```

### 🔍 Manual Testing
```bash
# Health check
curl -X GET http://localhost:8000/health

# Product query
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the price of SmartWatch Pro X?"}'

# Greeting
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "hi"}'

# API docs (Swagger UI)
open http://localhost:8000/docs
```

---

## 📡 API Endpoints Documentation

### 1️⃣ Health Check
```
GET /health
```
**Description:** Check if chatbot service is running

**Response:**
```json
{
  "status": "healthy",
  "message": "Chatbot service is running",
  "timestamp": "2026-01-30T14:32:00Z"
}
```

**Example:**
```bash
curl http://localhost:8000/health
```

### 2️⃣ Chat Endpoint (Main)
```
POST /chat
```
**Description:** Send query to chatbot and get response

**Request:**
```json
{
  "query": "What is the price of SmartWatch Pro X?"
}
```

**Response:**
```json
{
  "response": "SmartWatch Pro X: Price ₹15,999 | AMOLED display, 14-day battery, fitness tracking, water resistant, sleep monitoring | Standard warranty: 1 year, Extended: 2 years (₹2,999)",
  "category": "products",
  "timestamp": "2026-01-30T14:32:15Z"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the price of SmartWatch Pro X?"}'
```

### 3️⃣ Info Endpoint
```
GET /info
```
**Description:** Get chatbot information

**Response:**
```json
{
  "name": "TechGear Support Bot",
  "version": "1.0.0",
  "description": "AI-powered customer support chatbot",
  "features": [
    "Product information",
    "Price queries",
    "Warranty support",
    "Order tracking",
    "Returns policy",
    "Technical support"
  ]
}
```

### 4️⃣ UI Endpoint
```
GET /
```
**Description:** Serve web chat interface

**Returns:** HTML page with embedded CSS and JavaScript

---

## 🎯 Conversation Examples

### 💬 Example 1: Product Information
```
USER → What is the price of SmartWatch Pro X?
BOT  → SmartWatch Pro X: Price ₹15,999 | AMOLED display,
       14-day battery, fitness tracking, water resistant,
       sleep monitoring | Standard warranty: 1 year,
       Extended: 2 years (₹2,999)

USER → What features does it have?
BOT  → AMOLED display, 14-day battery life, fitness
       tracking with heart rate, water resistant (50m),
       sleep monitoring, GPS tracking

USER → What is the warranty?
BOT  → 1 year standard warranty included. Extended
       warranty (2 years) available for ₹2,999
```

### 👋 Example 2: Natural Conversation
```
USER → hi there!
BOT  → Hi! How can I help you today?

USER → Tell me about your smartwatch
BOT  → SmartWatch Pro X: Price ₹15,999 | AMOLED display,
       14-day battery, fitness tracking, water resistant,
       sleep monitoring | Standard warranty: 1 year,
       Extended: 2 years (₹2,999)

USER → thanks that's helpful
BOT  → Thank you! Hope my response was helpful. Feel
       free to ask if you have any other questions! 😊
```

### 📦 Example 3: Product Catalog
```
USER → What products do you sell?
BOT  → SmartWatch Pro X, Wireless Earbuds Elite,
       Power Bank Ultra

USER → Tell me about the earbuds
BOT  → Wireless Earbuds Elite: Price ₹7,999 | Active
       noise cancellation, premium sound, 20-hour
       battery, water resistant | Standard warranty:
       1 year, Extended: 2 years (₹1,999)
```

### ❓ Example 4: Yes/No Questions
```
USER → Can I return within 30 days?
BOT  → No, return window is 7 days (from purchase)

USER → Is it water resistant?
BOT  → Yes, water resistant up to 50m and suitable
       for swimming and water sports

USER → Do you offer expedited shipping?
BOT  → Yes, expedited shipping available. Standard:
       3-5 days, Express: 1-2 days (+₹500)
```

### 🔧 Example 5: Support & Troubleshooting
```
USER → How do I reset my smartwatch?
BOT  → To reset: Press and hold the side button for
       10 seconds until you see the power menu. Select
       Reset. This will erase all data.

USER → The battery drains quickly
BOT  → Try: Disable continuous heart rate monitoring,
       reduce screen brightness, enable battery saver
       mode. If issue persists, contact support.

USER → When are you available?
BOT  → Available 24/7 via chat. Phone support:
       Mon-Fri 9AM-6PM IST. Email us anytime.
```

---

## 🔐 Security Features

```
┌──────────────────────────────────────────┐
│      🔒 Security Implementations         │
├──────────────────────────────────────────┤
│                                          │
│ ✅ Environment variables (.env)         │
│    - API keys never exposed in code      │
│    - .gitignore protects credentials     │
│                                          │
│ ✅ Input validation (Pydantic)          │
│    - Query length: max 1000 chars        │
│    - Type checking                       │
│    - Request validation                  │
│                                          │
│ ✅ CORS middleware                      │
│    - Cross-origin access controlled      │
│                                          │
│ ✅ Error handling                        │
│    - No sensitive data in error msgs     │
│    - Proper HTTP status codes            │
│                                          │
│ ✅ Rate limiting ready                  │
│    - Can be added via middleware          │
│                                          │
└──────────────────────────────────────────┘
```

---

## 🌐 Deployment

### 🐳 Docker Deployment

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir -r requirements_api.txt

COPY . .

ENV GEMINI_API_KEY=$GEMINI_API_KEY
ENV API_HOST=0.0.0.0
ENV API_PORT=8000

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### ☁️ Cloud Deployment Options

**AWS (EC2/Lambda)**
```bash
# Deploy to AWS Lambda
pip install zappa
zappa init
zappa deploy production
```

**Heroku**
```bash
# Deploy to Heroku
heroku create your-chatbot
git push heroku main
```

**Google Cloud (Cloud Run)**
```bash
# Deploy to Cloud Run
gcloud run deploy techgear-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key
```

---

## 🐛 Troubleshooting

### Issue: "GEMINI_API_KEY not found"
**Solution:** Create `.env` file with your API key
```bash
cat > .env << EOF
GEMINI_API_KEY=your_api_key_here
EOF
```

### Issue: "Port 8000 already in use"
**Solution:** Use a different port
```bash
python -m uvicorn main:app --port 8001
```

### Issue: "ChromaDB connection failed"
**Solution:** Reinstall ChromaDB
```bash
pip install --upgrade chromadb
```

### Issue: "Module not found"
**Solution:** Install all dependencies
```bash
pip install -r requirements.txt
pip install -r requirements_api.txt
```

---

## 📊 Project Statistics

- **Code Lines**: 2000+
- **Documentation**: 2400+ lines
- **Test Cases**: 6 comprehensive tests
- **Features**: 10+ core features
- **API Endpoints**: 4 endpoints
- **Response Types**: 20+ different conversation patterns

---

## 🎯 Roadmap

### Phase 2 (Coming Soon)
- [ ] User authentication / session persistence
- [ ] Conversation history storage
- [ ] Message reactions (👍, 👎)
- [ ] Quick reply buttons
- [ ] Markdown support in responses

### Phase 3 (Future)
- [ ] Voice input / speech recognition
- [ ] Real-time message streaming
- [ ] Conversation sharing via link
- [ ] Admin panel
- [ ] Analytics dashboard

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 💬 Support

For issues, questions, or suggestions:
- Open an Issue on GitHub
- Email: support@techgear.com
- Hours: Mon-Sat, 9AM-6PM IST

---

## 🎉 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- LLM: [Google Generative AI](https://ai.google.dev/)
- Workflow: [LangGraph](https://github.com/langchain-ai/langgraph)
- Embeddings: [ChromaDB](https://www.trychroma.com/)

---

**Made with ❤️ for better customer support**

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║     🎉 Ready to deploy? Go to GitHub and push your code! 🚀   ║
║                                                                ║
║        git add .                                               ║
║        git commit -m "Initial commit: TechGear Chatbot"       ║
║        git push origin main                                    ║
║                                                                ║
║     Share your amazing chatbot with the world! ⭐            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```
