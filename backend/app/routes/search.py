from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import search_service
from app.models import Song

router = APIRouter()

@router.get("/search")
async def smart_search(q: str, db: Session = Depends(get_db)):
    if not q or len(q.strip()) < 2:
        return {"results": []}

    # Use unified search service
    search_result = await search_service.unified_search(q)

    # Optional: persist returned songs into database for caching
    for song_data in search_result.get('results', [])[:20]:
        existing = db.query(Song).filter(Song.song_id == song_data.get('song_id')).first()
        if not existing and song_data.get('song_id'):
            song = Song(
                song_id=song_data['song_id'],
                song_name=song_data.get('song_name'),
                artist_name=song_data.get('artist_name'),
                album_name=song_data.get('album_name'),
                artwork_url=song_data.get('artwork_url'),
                preview_url=song_data.get('preview_url'),
                release_year=int(song_data.get('release_year')) if song_data.get('release_year') else None,
                era=song_data.get('era'),
                play_count=song_data.get('play_count', 0),
                tags=song_data.get('tags', []),
                duration_ms=song_data.get('duration_ms')
            )
            db.add(song)
    try:
        db.commit()
    except:
        db.rollback()

    return search_result