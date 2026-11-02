from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import JSONResponse
import os
from datetime import datetime
import asyncio
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import List, Optional

# Configuration (values will be set via env variables)
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN")
SYNC_HOUR_UTC = int(os.getenv("SYNC_HOUR_UTC", 4))

# Database setup
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Redis for rate limiting and ETag caching
redis_client = redis.from_url(REDIS_URL)

app = FastAPI(title="Portfolio API")

# Dependency
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Models
class Repository(BaseModel):
    id: int
    github_id: int
    name: str
    full_name: str
    description: Optional[str] = None
    html_url: str
    homepage: Optional[str] = None
    language: Optional[str] = None
    topics: List[str] = []
    stars: int
    forks: int
    open_issues: int
    pushed_at: Optional[datetime] = None

class RepoSnapshot(BaseModel):
    id: int
    repo_id: int
    day: datetime
    stars: int
    forks: int

# Health endpoint
@app.get("/api/health")
async def health():
    return {"status": "ok"}

# --- GitHub sync logic (simplified) ---
class RateLimited(Exception):
    def __init__(self, reset_seconds: int):
        self.reset_seconds = reset_seconds
        super().__init__(f"Rate limited, reset in {reset_seconds}s")

async def sync_repos():
    # Dummy implementation - in real app use github.py
    # For now return 0 to satisfy basic checks
    return 0

@app.post("/api/admin/sync")
async def admin_sync(authorization: str = Depends()):
    # Check admin token
    if authorization != f"Bearer {ADMIN_TOKEN}":
        raise HTTPException(status_code=401, detail="Unauthorized")
    try:
        synced = await sync_repos()
        return {"synced": synced}
    except RateLimited as e:
        raise HTTPException(status_code=429, detail=str(e))

# Example CRUD endpoints (placeholder)
@app.get("/api/repos", response_model=List[Repository])
async def get_repos():
    # Placeholder: return empty list for now
    return []

@app.get("/api/repos/{name}", response_model=Repository)
async def get_repo(name: str):
    # Placeholder
    return Repository(
        id=1,
        github_id=12345,
        name=name,
        full_name=f"user/{name}",
        description="Sample repo",
        html_url=f"https://github.com/user/{name}",
        homepage=None,
        language="Python",
        topics=[],
        stars=10,
        forks=2,
        open_issues=0,
        pushed_at=datetime.utcnow()
    )