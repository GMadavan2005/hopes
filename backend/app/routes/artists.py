from fastapi import APIRouter, Depends
from app.services import audiodb_service
from app.database import get_db
from app.models import Artist
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/artist/{artist_name}")
async def get_artist(artist_name: str, db: Session = Depends(get_db)):
    # Search AudioDB
    artist_data = await audiodb_service.search_artist(artist_name)
    
    if not artist_data:
        return {"error": "Artist not found"}
    
    # Get albums and tracks
    artist_id = artist_data['artist_id']
    albums = await audiodb_service.get_artist_albums(artist_id)
    tracks = await audiodb_service.get_artist_tracks(artist_id)
    
    # Save to database
    existing = db.query(Artist).filter(Artist.artist_id == artist_id).first()
    if not existing:
        artist = Artist(
            artist_id=artist_id,
            artist_name=artist_data['artist_name'],
            bio=artist_data['bio'],
            photo_url=artist_data['photo_url'],
            genres=[artist_data['genre']] if artist_data.get('genre') else []
        )
        db.add(artist)
        try:
            db.commit()
        except:
            db.rollback()
    
    return {
        "artist": artist_data,
        "albums": albums,
        "tracks": tracks
    }