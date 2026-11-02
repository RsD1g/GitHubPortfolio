# backend/app/main.py
"""FastAPI application entry point."""
import asyncio
from datetime import datetime
from typing import List

from fastapi import FastAPI, Depends, HTTPException, Header, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .db import engine, async_session, Base
from .models import Repository, RepoSnapshot
from .github import sync_repos, RateLimited
from .config import settings

# Create FastAPI app
app = FastAPI(title="Portfolio API", version="0.1.0")

# Dependency to get async session
async def get_db():
    async with async_session() as session:
        yield session

# Startup event - create tables and run initial sync
@app.on_event("startup")
async def startup():
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created")

    # Run initial synchronization if GITHUB_USERNAME is set
    if settings.GITHUB_USERNAME:
        try:
            print("Running initial repository synchronization...")
            synced = await sync_repos()
            print(f"Initial sync completed: {synced} repositories synchronized")
        except RateLimited as e:
            print(f"Rate limited during initial sync: {e}")
        except Exception as e:
            print(f"Error during initial sync: {e}")
    else:
        print("GITHUB_USERNAME not set, skipping initial synchronization")

# Health check endpoint
@app.get("/api/health", response_class=JSONResponse)
async def health_check():
    return {"status": "ok"}

# Repositories list endpoint
@app.get("/api/repos", response_model=List[dict])
async def get_repos(
    q: Optional[str] = None,
    language: Optional[str] = None,
    sort: str = "pushed",
    db: AsyncSession = Depends(get_db)
):
    query = select(Repository)

    if q:
        # ILIKE search on name and description
        import sqlalchemy
        pattern = f"%{q}%"
        query = query.where(
            sqlalchemy.or_(
                Repository.name.ilike(pattern),
                Repository.description.ilike(pattern)
            )
        )

    if language:
        query = query.where(Repository.language == language)

    if sort == "pushed":
        query = query.order_by(Repository.pushed_at.desc().nulls_last())
    elif sort == "stars":
        query = query.order_by(Repository.stars.desc())
    elif sort == "name":
        query = query.order_by(Repository.name.asc())

    result = await db.execute(query)
    repositories = result.scalars().all()

    # Convert to dict for response
    return [repo.__dict__ for repo in repositories]

# Single repository endpoint
@app.get("/api/repos/{name}", response_model=dict)
async def get_repo(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Repository).where(Repository.name == name))
    repo = result.scalar_one_or_none()
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repo.__dict__

# Repository history endpoint
@app.get("/api/repos/{name}/history", response_model=List[dict])
async def get_repo_history(name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RepoSnapshot).where(RepoSnapshot.repo.has(name=name)).order_by(RepoSnapshot.day)
    )
    snapshots = result.scalars().all()
    return [snap.__dict__ for snap in snapshots]

# Overview stats endpoint
@app.get("/api/stats/overview", response_model=dict)
async def get_overview(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Repository))
    repos = result.scalars().all()

    total_repos = len(repos)
    total_stars = sum(repo.stars for repo in repos)
    total_forks = sum(repo.forks for repo in repos)

    # Get languages and counts
    languages = {}
    for repo in repos:
        if repo.language:
            languages[repo.language] = languages.get(repo.language, 0) + 1

    # Sort languages by count descending
    languages_list = sorted(languages.items(), key=lambda x: x[1], reverse=True)
    languages_sorted = [{"language": lang, "count": count} for lang, count in languages_list]

    return {
        "total_repos": total_repos,
        "total_stars": total_stars,
        "total_forks": total_forks,
        "languages": languages_sorted
    }

# Admin sync endpoint
ADMIN_TOKEN_HASH = settings.ADMIN_TOKEN  # In production, hash this

@app.post("/api/admin/sync",
          status_code=status.HTTP_200_OK if settings.GITHUB_USERNAME else status.HTTP_401_UNAUTHORIZED,
          response_class=JSONResponse)
async def admin_sync(
    authorization: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header required")
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header must start with Bearer")
    token = authorization.split(" ")[1]
    if token != settings.ADMIN_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid admin token")

    try:
        synced = await sync_repos()
        return {"synced": synced}
    except RateLimited as e:
        raise HTTPException(status_code=429, detail=f"Rate limited: {e.reset_seconds} seconds")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))