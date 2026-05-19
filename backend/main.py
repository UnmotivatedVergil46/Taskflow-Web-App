from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

from config import init_db, is_using_memory
import auth_routes
import task_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api/auth", tags=["auth"])
app.include_router(task_routes.router, prefix="/api/tasks", tags=["tasks"])

@app.get("/api/health")
async def health_check():
    storage_type = "in-memory" if is_using_memory() else "mysql"
    return {
        "status": "ok",
        "storage": storage_type,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    print(f"\n[OK] Todo API server running on http://localhost:{port}")
    print(f"[DB] Storage: {'In-Memory (no MySQL)' if is_using_memory() else 'MySQL'}")
    print(f"[OK] Health check: http://localhost:{port}/api/health\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
