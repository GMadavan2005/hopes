from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from app.database import get_db
from app.models import UserPreferences
from sqlalchemy.orm import Session
from app.services import gemini_service

router = APIRouter()

class PreferencesUpdate(BaseModel):
    user_id: str
    languages: List[str] = []
    eras: List[str] = []
    favorite_artists: List[str] = []
    genres: List[str] = []
    onboarding_completed: bool = False

@router.post("/preferences")
async def save_preferences(prefs: PreferencesUpdate, db: Session = Depends(get_db)):
    existing = db.query(UserPreferences).filter(
        UserPreferences.user_id == prefs.user_id
    ).first()
    
    if existing:
        existing.languages = prefs.languages
        existing.eras = prefs.eras
        existing.favorite_artists = prefs.favorite_artists
        existing.genres = prefs.genres
        existing.onboarding_completed = prefs.onboarding_completed
    else:
        new_prefs = UserPreferences(
            user_id=prefs.user_id,
            languages=prefs.languages,
            eras=prefs.eras,
            favorite_artists=prefs.favorite_artists,
            genres=prefs.genres,
            onboarding_completed=prefs.onboarding_completed
        )
        db.add(new_prefs)
    
    db.commit()
    return {"message": "Preferences saved"}

@router.get("/preferences/{user_id}")
async def get_preferences(user_id: str, db: Session = Depends(get_db)):
    prefs = db.query(UserPreferences).filter(
        UserPreferences.user_id == user_id
    ).first()
    
    if not prefs:
        return {
            "languages": [],
            "eras": [],
            "favorite_artists": [],
            "genres": [],
            "onboarding_completed": False
        }
    
    return {
        "languages": prefs.languages,
        "eras": prefs.eras,
        "favorite_artists": prefs.favorite_artists,
        "genres": prefs.genres,
        "onboarding_completed": prefs.onboarding_completed
    }

@router.get("/for-you/{user_id}")
async def get_for_you(user_id: str, db: Session = Depends(get_db)):
    prefs = db.query(UserPreferences).filter(
        UserPreferences.user_id == user_id
    ).first()
    
    if not prefs or not prefs.onboarding_completed:
        return {"songs": []}
    
    preferences_dict = {
        "languages": prefs.languages,
        "eras": prefs.eras,
        "favorite_artists": prefs.favorite_artists,
        "genres": prefs.genres
    }
    
    song_suggestions = await gemini_service.generate_for_you_songs(preferences_dict)
    
    return {"songs": song_suggestions}