from fastapi import APIRouter, Depends
from app.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.models import TrendingCache
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/trending/{language}")
async def get_trending(language: str, db: Session = Depends(get_db)):
    # Check cache (refresh every hour)
    cache = db.query(TrendingCache).filter(
        TrendingCache.language == language
    ).first()
    
    if cache and (datetime.utcnow() - cache.cached_at) < timedelta(hours=1):
        return {"language": language, "song_ids": cache.song_ids}
    
    # Query actual trending songs
    query = text("""
        SELECT sr.song_id, sr.song_name, sr.artist_name, sr.artwork_url,
               COUNT(*) as review_count,
               AVG(sr.rating) as avg_rating
        FROM song_reviews sr
        JOIN songs s ON sr.song_id = s.song_id
        WHERE s.language = :language
          AND sr.created_at > NOW() - INTERVAL '7 days'
        GROUP BY sr.song_id, sr.song_name, sr.artist_name, sr.artwork_url
        ORDER BY review_count DESC, avg_rating DESC
        LIMIT 20
    """)
    
    result = db.execute(query, {"language": language})
    trending_songs = [dict(row._mapping) for row in result]
    song_ids = [song['song_id'] for song in trending_songs]
    
    # Update cache
    if cache:
        cache.song_ids = song_ids
        cache.cached_at = datetime.utcnow()
    else:
        cache = TrendingCache(
            language=language,
            song_ids=song_ids
        )
        db.add(cache)
    
    db.commit()
    
    return {
        "language": language,
        "songs": trending_songs
    }