"""
Database configuration and connection management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import NullPool
import os
from typing import Generator

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/prize2pride_german"
)

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Disable pooling for development
    echo=False,  # Set to True for SQL debugging
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
    }
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection for database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_db():
    """
    Initialize database tables
    """
    Base.metadata.create_all(bind=engine)

def drop_db():
    """
    Drop all database tables (use with caution!)
    """
    Base.metadata.drop_all(bind=engine)

# ============================================================================
# CONNECTION TESTING
# ============================================================================

def test_connection():
    """
    Test database connection
    """
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return {"status": "connected", "result": result.fetchone()}
    except Exception as e:
        return {"status": "error", "error": str(e)}
