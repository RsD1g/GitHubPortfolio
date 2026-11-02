# backend/app/models.py
"""SQLAlchemy models for the portfolio database."""
from sqlalchemy import Column, Date, Integer, String, JSON, BigInteger, Boolean, Timestamptz, Numeric
from sqlalchemy.orm import relationship
from .db import Base
from typing import List, Optional
from datetime import date

class Repository(Base):
    __tablename__ = "repositories"

    id: BigInteger = Column(BigInteger, primary_key=True, index=True)
    github_id: BigInteger = Column(BigInteger, unique=True, index=True, nullable=False)
    name: String = Column(String, unique=True, index=True, nullable=False)
    full_name: String = Column(String, nullable=True)
    description: String = Column(String, nullable=True)
    html_url: String = Column(String, nullable=False)
    homepage: String = Column(String, nullable=True)
    language: String = Column(String, nullable=True, index=True)
    topics: String = Column(JSON, nullable=True)  # JSON list of topics
    stars: Integer = Column(Integer, nullable=False, default=0)
    forks: Integer = Column(Integer, nullable=False, default=0)
    open_issues: Integer = Column(Integer, nullable=False, default=0)
    pushed_at: Timestamptz = Column(Timestamptz, nullable=True)

    # Relationships
    snapshots: List["RepoSnapshot"] = relationship("RepoSnapshot", back_populates="repo", cascade="all, delete-orphan")

class RepoSnapshot(Base):
    __tablename__ = "repo_snapshots"

    id: BigInteger = Column(BigInteger, primary_key=True, index=True)
    repo_id: BigInteger = Column(BigInteger,
                                 ForeignKey("repositories.id", ondelete="CASCADE"),
                                 index=True, nullable=False)
    day: Date = Column(Date, index=True, nullable=False)
    stars: Integer = Column(Integer, nullable=False, default=0)
    forks: Integer = Column(Integer, nullable=False, default=0)

    repo: Repository = relationship("Repository", back_populates="snapshots")

# Unique constraint on (repo_id, day)
__table_args__ = (Column('repo_id', 'repo_id', index=True),)