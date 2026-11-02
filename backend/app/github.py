# backend/app/github.py
"""GitHub API client and synchronization logic."""
import asyncio
import json
from datetime import datetime
from typing import List, Optional
from urllib.parse import urlparse, parse_qs

import httpx
from sqlalchemy import select, insert, update
from sqlalchemy.exc import HTTPError
from .db import engine, async_session
from .models import Repository, RepoSnapshot
from .config import settings
from asyncpg import postgresql

# Custom exception for rate limiting
class RateLimited(Exception):
    def __init__(self, reset_seconds: int):
        super().__init__(f"Rate limited, reset in {reset_seconds} seconds")
        self.reset_seconds = reset_seconds

# Rate limiting client
class GitHubClient:
    API_BASE = "https://api.github.com"

    def __init__(self):
        self.http_client = httpx.AsyncClient(
            timeout=30.0,
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )

    async def close(self):
        await self.http_client.aclose()

    async def get_user_repos(self, username: str) -> List[dict]:
        """Fetch all public repos for a user with pagination."""
        if not username:
            raise ValueError("GitHub username must be provided")

        repos = []
        url = f"{self.API_BASE}/users/{username}/repos"
        params = {
            "per_page": 100,
            "type": "owner",
            "sort": "pushed",
        }

        while url:
            # Check ETag for conditional request
            etag = None
            if settings.GITHUB_TOKEN:
                # Try to get ETag from Redis (not implemented here)
                pass

            response = await self.http_client.get(url, params=params)
            if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
                reset_time = int(response.headers.get("X-RateLimit-Reset", "0"))
                raise RateLimited(reset_time - int(asyncio.get_event_loop().time()))
            elif response.status_code == 429:
                reset_time = int(response.headers.get("X-RateLimit-Reset", "0"))
                raise RateLimited(reset_time - int(asyncio.get_event_loop().time()))
            elif response.status_code == 304:
                # Not modified, skip processing
                pass
            elif response.status_code != 200:
                raise HTTPError(f"GitHub API error: {response.status_code} - {response.text}")

            data = response.json()
            repos.extend(data)

            # Handle pagination via Link header
            link_header = response.headers.get("Link", "")
            if link_header:
                # Parse next URL from Link header
                # Example: <https://api.github.com/user/repos?page=2>; rel="next"
                next_url = None
                for part in link_header.split(","):
                    if 'rel="next"' in part:
                        next_url = part[part.find('<')+1:part.find('>')]
                        break
                if next_url:
                    # Extract URL and params
                    parsed = urlparse(next_url)
                    url = parsed.geturl()
                    # Update params with query parameters from the next URL
                    qs = parse_qs(parsed.query)
                    params.update({k: v[0] for k, v in qs.items()})
                    continue

            break  # No more pages

        return repos

    async def get_repo_details(self, owner: str, repo_name: str) -> dict:
        """Fetch details for a specific repository."""
        url = f"{self.API_BASE}/repos/{owner}/{repo_name}"
        response = await self.http_client.get(url)
        if response.status_code == 404:
            raise ValueError(f"Repository {owner}/{repo_name} not found")
        if response.status_code == 403 and response.headers.get("X-RateLimit-Remaining") == "0":
            reset_time = int(response.headers.get("X-RateLimit-Reset", "0"))
            raise RateLimited(reset_time - int(asyncio.get_event_loop().time()))
        elif response.status_code == 429:
            reset_time = int(response.headers.get("X-RateLimit-Reset", "0"))
            raise RateLimited(reset_time - int(asyncio.get_event_loop().time()))
        elif response.status_code == 304:
            return {}
        elif response.status_code != 200:
            raise HTTPError(f"GitHub API error: {response.status_code} - {response.text}")

        return response.json()

    async def close(self):
        await self.http_client.aclose()

# Rate limiting wrapper for repository sync
async def sync_repos(username: Optional[str] = None) -> int:
    """
    Synchronize repositories from GitHub to the database.
    Returns the number of repositories synced.
    """
    client = GitHubClient()
    try:
        if username is None:
            # Use GITHUB_USERNAME from config if set
            username = settings.GITHUB_USERNAME
        if not username:
            raise ValueError("GITHUB_USERNAME is not set in configuration")

        print(f"Starting synchronization for GitHub user: {username}")
        repos_data = await client.get_user_repos(username)
        print(f"Found {len(repos_data)} repositories on GitHub")

        # Get or create repository IDs in DB
        async with async_session() as session:
            # Create mapping of github_id to repository ID
            existing_repos = await session.execute(
                select(Repository.github_id).where(Repository.github_id.in_([r['id'] for r in repos_data]))
            )
            existing_ids = {row[0] for row in existing_repos}
            new_repos_data = [r for r in repos_data if r['id'] not in existing_ids]
            print(f"Syncing {len(new_repos_data)} new repositories")

            # Process each repository
            synced_count = 0
            for repo_info in new_repos_data:
                # Skip forks and archived repos
                if repo_info.get('fork') or repo_info.get('archived'):
                    continue

                # Parse pushed_at timestamp
                pushed_at = None
                if repo_info.get('pushed_at'):
                    # Replace 'Z' with '+00:00' for proper parsing
                    pushed_at_str = repo_info['pushed_at'].replace('Z', '+00:00')
                    try:
                        pushed_at = datetime.fromisoformat(pushed_at_str)
                    except ValueError:
                        pushed_at = datetime.utcnow()

                # Create or update repository
                stmt = insert(Repository).values(
                    github_id=repo_info['id'],
                    name=repo_info['name'],
                    full_name=repo_info.get('full_name'),
                    description=repo_info.get('description'),
                    html_url=repo_info['html_url'],
                    homepage=repo_info.get('homepage'),
                    language=repo_info.get('language'),
                    topics=repo_info.get('topics'),
                    stars=repo_info.get('stargazers_count', 0),
                    forks=repo_info.get('forks_count', 0),
                    open_issues=repo_info.get('open_issues_count', 0),
                    pushed_at=pushed_at,
                ).on_conflict_do_update(
                    index_elements=[Repository.github_id],
                    set_={
                        Repository.name: repo_info['name'],
                        Repository.full_name: repo_info.get('full_name'),
                        Repository.description: repo_info.get('description'),
                        Repository.html_url: repo_info['html_url'],
                        Repository.homepage: repo_info.get('homepage'),
                        Repository.language: repo_info.get('language'),
                        Repository.topics: repo_info.get('topics'),
                        Repository.stars: repo_info.get('stargazers_count', 0),
                        Repository.forks: repo_info.get('forks_count', 0),
                        Repository.open_issues: repo_info.get('open_issues_count', 0),
                        Repository.pushed_at: pushed_at,
                    }
                )
                result = await session.execute(stmt)
                synced_count += 1

                # Create daily snapshot
                day = datetime.utcnow().date()
                snapshot_stmt = insert(RepoSnapshot).values(
                    repo_id=result.inserted_id if result.inserted_id else result.last_opened_id(),
                    day=day,
                    stars=repo_info.get('stargazers_count', 0),
                    forks=repo_info.get('forks_count', 0),
                )
                await session.execute(snapshot_stmt)

            await session.commit()
            print(f"Synchronization complete: {synced_count} repositories processed")
            return synced_count

    except RateLimited as e:
        print(f"Rate limit exceeded: {e}")
        raise
    except Exception as e:
        print(f"Error during synchronization: {e}")
        raise
    finally:
        await client.close()