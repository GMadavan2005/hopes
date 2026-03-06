from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import search, reviews, artists, preferences, trending
from app.database import Base, engine, db_available
import logging

logger = logging.getLogger(__name__)

# Create tables only if database is available
if db_available:
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully")
    except Exception as e:
        logger.warning(f"Could not create tables: {e}")
else:
    logger.warning("⚠️ Skipping table creation - database not available")

app = FastAPI(title="Soundlog Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8081", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(reviews.router, prefix="/api", tags=["reviews"])
app.include_router(artists.router, prefix="/api", tags=["artists"])
app.include_router(preferences.router, prefix="/api", tags=["preferences"])
app.include_router(trending.router, prefix="/api", tags=["trending"])

@app.get("/")
def read_root():
    return {
        "message": "Soundlog Backend API - Running",
        "database": "connected" if db_available else "disconnected (API-only mode)",
        "apis": ["Gemini AI", "MusicBrainz", "Last.fm", "iTunes", "AudioDB"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected" if db_available else "offline"
    }