"""
Database Configuration
---------------------
Attempts to connect to MySQL using environment variables.
If MySQL is unavailable, falls back to an in-memory store.
"""

import os
from sqlalchemy import create_engine, event, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool
from typing import List, Dict, Any, Optional
from datetime import datetime

# Database URL
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "todo_app")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = None
SessionLocal = None
use_memory = False

# In-memory fallback store
class MemoryStore:
    def __init__(self):
        self.users = []
        self.tasks = []
        self._user_id = 1
        self._task_id = 1
    
    def reset(self):
        self.users = []
        self.tasks = []
        self._user_id = 1
        self._task_id = 1

memory_store = MemoryStore()

async def init_db():
    """Initialize database connection or fallback to memory."""
    global engine, SessionLocal, use_memory
    
    try:
        engine = create_engine(
            DATABASE_URL,
            poolclass=QueuePool,
            pool_size=10,
            max_overflow=20,
            echo=False
        )
        
        # Test connection
        with engine.begin() as conn:
            conn.execute(text("SELECT 1"))
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        # Create tables
        from models import Base
        Base.metadata.create_all(bind=engine)
        
        print("[OK] Connected to MySQL database")
        use_memory = False
    except Exception as e:
        print(f"[WARN] MySQL connection failed: {str(e)}")
        print("[INFO] Falling back to in-memory storage")
        use_memory = True
        SessionLocal = None

def get_db():
    """Get database session for dependency injection."""
    if use_memory:
        yield None
        return
    if SessionLocal is None:
        raise RuntimeError("Database not initialized")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def is_using_memory() -> bool:
    """Check if using in-memory storage."""
    return use_memory

def query_memory(sql: str, params: List[Any] = None) -> Any:
    """Execute query on in-memory store."""
    if params is None:
        params = []
    
    normalized = sql.strip().upper()
    
    # INSERT INTO users
    if normalized.startswith("INSERT INTO USERS"):
        user = {
            "id": memory_store._user_id,
            "username": params[0],
            "password_hash": params[1],
            "created_at": datetime.utcnow(),
        }
        memory_store.users.append(user)
        memory_store._user_id += 1
        return {"insertId": user["id"]}
    
    # SELECT * FROM users WHERE username
    if normalized.startswith("SELECT") and "USERS" in normalized and "USERNAME" in normalized:
        return [u for u in memory_store.users if u["username"] == params[0]]
    
    # INSERT INTO tasks
    if normalized.startswith("INSERT INTO TASKS"):
        task = {
            "id": memory_store._task_id,
            "user_id": params[0],
            "title": params[1],
            "due_date": params[2],
            "completed": False,
            "created_at": datetime.utcnow(),
        }
        memory_store.tasks.append(task)
        memory_store._task_id += 1
        return {"insertId": task["id"]}
    
    # SELECT * FROM tasks WHERE user_id
    if normalized.startswith("SELECT") and "TASKS" in normalized and "USER_ID" in normalized and "AND" not in normalized:
        return [t for t in memory_store.tasks if t["user_id"] == params[0]]
    
    # SELECT * FROM tasks WHERE id AND user_id
    if normalized.startswith("SELECT") and "TASKS" in normalized and "AND" in normalized:
        return [t for t in memory_store.tasks if t["id"] == params[0] and t["user_id"] == params[1]]
    
    # UPDATE tasks
    if normalized.startswith("UPDATE TASKS"):
        task_id = params[-2]
        user_id = params[-1]
        for i, t in enumerate(memory_store.tasks):
            if t["id"] == task_id and t["user_id"] == user_id:
                if "TITLE" in normalized and "DUE_DATE" in normalized and "COMPLETED" in normalized:
                    memory_store.tasks[i]["title"] = params[0]
                    memory_store.tasks[i]["due_date"] = params[1]
                    memory_store.tasks[i]["completed"] = params[2]
                elif "COMPLETED" in normalized:
                    memory_store.tasks[i]["completed"] = params[0]
                return {"affectedRows": 1}
        return {"affectedRows": 0}
    
    # DELETE FROM tasks
    if normalized.startswith("DELETE FROM TASKS"):
        initial_len = len(memory_store.tasks)
        memory_store.tasks = [
            t for t in memory_store.tasks 
            if not (t["id"] == params[0] and t["user_id"] == params[1])
        ]
        return {"affectedRows": initial_len - len(memory_store.tasks)}
    
    return []
