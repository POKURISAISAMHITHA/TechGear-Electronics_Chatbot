# 🔄 RAG Update Workflow - Quick Reference

## When to Update RAG:
- ✅ Added new products to `product_info.txt`
- ✅ Modified product prices, features, or specifications
- ✅ Changed product availability/stock status
- ✅ Updated company policies (return, warranty, shipping)
- ✅ Added new product categories
- ✅ Removed discontinued products

---

## 🚀 3-Step Update Process:

### Step 1: Edit Product Information
```bash
# Open and edit the product file
nano product_info.txt
# or
code product_info.txt
```

### Step 2: Regenerate Embeddings (MANDATORY!)
```bash
cd /home/labuser/TechGear-Electronics_Chatbot
source .venv/bin/activate
python embed_and_store.py
```

**Expected Output:**
```
✅ Text loaded successfully
✅ Created XXX chunks
✅ Embeddings stored in ChromaDB
```

### Step 3: Restart the Server
```bash
# Option A: Kill and restart
pkill -f "uvicorn main:app"
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Option B: Background restart
pkill -f "uvicorn main:app"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 > /tmp/server_log.txt 2>&1 &
```

---

## ⚠️ IMPORTANT: Don't Skip Step 2!

**Why regenerating embeddings is critical:**
- The chatbot uses vector embeddings stored in ChromaDB
- If you edit `product_info.txt` but don't run `embed_and_store.py`:
  ❌ Chatbot will still return OLD information
  ❌ New products won't be found
  ❌ Updated prices won't show up
  ❌ RAG will be out of sync

**After running `embed_and_store.py`:**
- ✅ All new products are searchable
- ✅ Updated information is retrieved correctly
- ✅ Vector database matches your product catalog
- ✅ RAG system is synchronized

---

## 🧪 Verify RAG is Updated

After updating, test with a query about your new/updated product:

```bash
# Test new product
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the price of [NEW_PRODUCT_NAME]?"}'

# Test updated information
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "Tell me about [UPDATED_PRODUCT]"}'
```

If you get correct information → ✅ RAG is updated!  
If you get old information → ❌ Run `embed_and_store.py` again

---

## 📊 Check Embeddings Status

```bash
# Check number of chunks in ChromaDB
python -c "
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import os
from dotenv import load_dotenv

load_dotenv()
embeddings = GoogleGenerativeAIEmbeddings(
    model='models/embedding-001',
    google_api_key=os.getenv('GEMINI_API_KEY')
)
vectorstore = Chroma(
    persist_directory='chroma_db',
    embedding_function=embeddings,
    collection_name='product_info'
)
print(f'Total chunks in ChromaDB: {vectorstore._collection.count()}')
"
```

---

## 🔧 Troubleshooting

### Issue: "Chatbot returns old product information"
**Solution:**
```bash
python embed_and_store.py
pkill -f "uvicorn main:app"
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### Issue: "New products not found"
**Solution:**
1. Check `product_info.txt` - is the product there?
2. Run `embed_and_store.py` - did it complete successfully?
3. Check chunk count - did it increase?
4. Restart server

### Issue: "Embeddings not updating"
**Solution:**
```bash
# Delete old embeddings
rm -rf chroma_db/

# Regenerate from scratch
python embed_and_store.py

# Restart server
pkill -f "uvicorn main:app"
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 📝 Example Update Workflow

### Scenario: Adding 10 New Smartwatches

```bash
# 1. Edit product file
nano product_info.txt
# Add your 10 new smartwatch products

# 2. Save and regenerate embeddings
python embed_and_store.py
# Output should show: "Created XXX chunks" (number should increase)

# 3. Restart server
pkill -f "uvicorn main:app"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# 4. Test new products
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What smartwatches do you have?"}'
# Should now include your 10 new watches!
```

---

## ⏱️ Update Frequency Recommendations

| Update Type | Frequency | Action Required |
|-------------|-----------|-----------------|
| **Price Changes** | Daily/Weekly | Regenerate embeddings |
| **New Products** | As needed | Regenerate embeddings |
| **Stock Status** | Real-time* | Regenerate embeddings |
| **Policy Updates** | Monthly/Quarterly | Regenerate embeddings |
| **Seasonal Changes** | Quarterly | Regenerate embeddings |

\* For real-time stock updates, consider integrating with a live inventory API instead of static text file.

---

## 🎯 Best Practices

1. **Always backup before major updates:**
   ```bash
   cp product_info.txt product_info_backup_$(date +%Y%m%d).txt
   ```

2. **Keep track of changes:**
   - Document what you updated
   - Note the date and reason
   - Keep version history

3. **Test after every update:**
   - Run at least 3-5 test queries
   - Verify new products are found
   - Check updated information is correct

4. **Monitor server logs:**
   ```bash
   tail -f /tmp/server_log.txt
   ```

5. **Automate if possible:**
   - Create a script to update → regenerate → restart
   - Schedule regular updates
   - Set up monitoring alerts

---

## 🚨 Critical Reminders

⚠️ **NEVER skip `embed_and_store.py` after updating products!**

⚠️ **Always restart the server after regenerating embeddings!**

⚠️ **Test before deploying to production!**

⚠️ **Keep backups of your `product_info.txt`!**

⚠️ **Monitor the server logs for errors!**

---

## 📞 Quick Help

If something's not working:
1. Check server is running: `ps aux | grep uvicorn`
2. Check logs: `tail -100 /tmp/server_log.txt`
3. Verify embeddings: Check `chroma_db/` directory exists
4. Test API: `curl http://localhost:8000/health`
5. Regenerate everything: Delete `chroma_db/`, run `embed_and_store.py`, restart server

---

**Remember: Product updates → Regenerate embeddings → Restart server → Test!**

**Last Updated:** February 2, 2026
