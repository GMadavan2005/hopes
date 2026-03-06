from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Try to create engine with Supabase, but handle failures gracefully
try:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_available = True
    logger.info("✅ Database connection successful")
except Exception as e:
    logger.warning(f"⚠️ Database connection failed: {e}")
    logger.warning("Running in API-only mode. Database features disabled.")
    SessionLocal = None
    db_available = False

Base = declarative_base()

def get_db():
    """Yield database session if available"""
    if not db_available or not SessionLocal:
        logger.warning("Database not available - returning None")
        return None
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()