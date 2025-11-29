When a request comes in:
```
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
