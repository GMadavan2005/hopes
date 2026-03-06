from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Try to create engine with Supabase, then verify connectivity by opening a test connection.
# If anything fails we fall back to API-only mode.
try:
    engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
    # sessionmaker can be created even if the database is unreachable; test by connecting
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        db_available = True
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        logger.info("✅ Database connection successful")
    except Exception as conn_err:
        logger.warning(f"⚠️ Database ping failed: {conn_err}")
        logger.warning("Running in API-only mode. Database features disabled.")
        SessionLocal = None
        db_available = False
except Exception as e:
    logger.warning(f"⚠️ Failed to configure database engine: {e}")
    logger.warning("Running in API-only mode. Database features disabled.")
    SessionLocal = None
    db_available = False

Base = declarative_base()

def get_db():
    """Yield database session if available. Always yield once for FastAPI dependency.
    If the database is unavailable, yields None and downstream code must check.
    """
    if not db_available or not SessionLocal:
        logger.warning("Database not available - yielding None session")
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()