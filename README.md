# 📚 Bookstore REST API

A clean, minimal REST API for a digital bookstore, built using FastAPI.

---

## ⚙️ Features

- ➕ Add, 🔍 View, 📝 Update, 🗑️ Delete books
- 💡 JSON input/output
- 🛡️ Validated using Pydantic models
- 🚀 Swagger documentation at `/docs`

---

## 🚀 How to Run

1. Install dependencies:

```bash
pip install fastapi uvicorn


```
When a Request comes in:
1. Request hits uvicorn server
   ↓
2. Uvicorn forwards to FastAPI app (main.py)
   ↓
3. FastAPI checks which router handles this URL
   ↓
4. Router calls the appropriate function (routes.py)
   ↓
5. Function calls database (database.py)
   ↓
6. Database validates with models (models.py)
   ↓
7. Response flows back up the chain


# ✅ Key Concepts

- How to build APIs using FastAPI
- Defining routes for CRUD operations
- Using Pydantic for validation
- Structuring JSON response
- Error handling and status codes in backend

---
