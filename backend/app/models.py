from sqlalchemy import Column, String, Integer, Boolean, ARRAY, Text, DateTime, Float, Date
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid
from datetime import datetime

class Song(Base):
    __tablename__ = "songs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    song_id = Column(String, unique=True, nullable=False)
    song_name = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)
    album_name = Column(String)
    artwork_url = Column(String)
    preview_url = Column(String)
    release_year = Column(Integer)
    era = Column(String)
    language = Column(String)
    genre = Column(String)
    play_count = Column(Integer, default=0)
    tags = Column(ARRAY(String))
    duration_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Artist(Base):
    __tablename__ = "artists"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    artist_id = Column(String, unique=True, nullable=False)
    artist_name = Column(String, nullable=False)
    bio = Column(Text)
    photo_url = Column(String)
    genres = Column(ARRAY(String))
    created_at = Column(DateTime, default=datetime.utcnow)

class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    languages = Column(ARRAY(String), default=[])
    eras = Column(ARRAY(String), default=[])
    favorite_artists = Column(ARRAY(String), default=[])
    genres = Column(ARRAY(String), default=[])
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class TrendingCache(Base):
    __tablename__ = "trending_cache"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    language = Column(String, unique=True, nullable=False)
    song_ids = Column(ARRAY(String), nullable=False)
    cached_at = Column(DateTime, default=datetime.utcnow)