import asyncio
from typing import List, Dict
from app.services import (
    gemini_service,
    musicbrainz_service,
    lastfm_service,
    itunes_service,
    audiodb_service
)

async def unified_search(query: str) -> Dict:
    """
    Master search function that combines all APIs
    Returns enriched song data with ALL available information
    """
    
    # Step 1: Parse query with Gemini AI
    parsed = await gemini_service.parse_search_query(query)
    
    # Step 2: Search all sources in parallel
    results = await asyncio.gather(
        musicbrainz_service.search_songs(
            parsed['search_query'],
            parsed.get('artist_name'),
            limit=15
        ),
        itunes_service.search_itunes(
            parsed['search_query'],
            parsed.get('artist_name'),
            limit=10
        ),
        return_exceptions=True
    )
    
    musicbrainz_results = results[0] if not isinstance(results[0], Exception) else []
    itunes_results = results[1] if not isinstance(results[1], Exception) else []
    
    # Step 3: Merge and deduplicate
    merged_songs = {}
    
    # Prefer iTunes for artwork and preview
    for song in itunes_results:
        key = f"{song['song_name']}_{song['artist_name']}".lower().replace(' ', '')
        merged_songs[key] = song
    
    # Add MusicBrainz data
    for song in musicbrainz_results:
        key = f"{song['song_name']}_{song['artist_name']}".lower().replace(' ', '')
        if key not in merged_songs:
            merged_songs[key] = song
        else:
            # Enrich existing entry
            merged_songs[key].update({
                'tags': song.get('tags', []),
                'era': song.get('era') or merged_songs[key].get('era'),
                'release_year': song.get('release_year') or merged_songs[key].get('release_year')
            })
    
    # Step 4: Enrich top 10 results with Last.fm and AudioDB
    enriched_songs = []
    for i, (key, song) in enumerate(list(merged_songs.items())[:10]):
        # Get Last.fm data
        lastfm_task = lastfm_service.get_song_info(
            song['artist_name'],
            song['song_name']
        )
        
        # Get AudioDB artist data (cache by artist)
        audiodb_task = audiodb_service.search_artist(song['artist_name'])
        
        lastfm_data, audiodb_data = await asyncio.gather(
            lastfm_task,
            audiodb_task,
            return_exceptions=True
        )
        
        # Merge Last.fm data
        if not isinstance(lastfm_data, Exception):
            song['play_count'] = lastfm_data.get('play_count', 0)
            existing_tags = song.get('tags', [])
            new_tags = lastfm_data.get('tags', [])
            song['tags'] = list(set(existing_tags + new_tags))[:10]
        
        # Add AudioDB artist info
        if not isinstance(audiodb_data, Exception) and audiodb_data:
            song['artist_bio'] = audiodb_data.get('bio_short', '')
            song['artist_photo'] = audiodb_data.get('photo_url', '')
            song['artist_genre'] = audiodb_data.get('genre', '')
        
        # Detect language from tags
        if not song.get('language'):
            song['language'] = detect_language_from_tags(song.get('tags', []))
        
        enriched_songs.append(song)
    
    # Step 5: Apply Gemini filters
    filtered_songs = enriched_songs
    
    if parsed.get('era'):
        filtered_songs = [s for s in filtered_songs if s.get('era') == parsed['era']]
    
    if parsed.get('language'):
        lang_lower = parsed['language'].lower()
        filtered_songs = [
            s for s in filtered_songs 
            if s.get('language') and lang_lower in s['language'].lower()
        ]
    
    return {
        "query": query,
        "parsed": parsed,
        "total": len(filtered_songs),
        "results": filtered_songs
    }

def detect_language_from_tags(tags: List[str]) -> str:
    """Detect language from tags"""
    tag_str = ' '.join(tags).lower()
    
    language_keywords = {
        'Tamil': ['tamil', 'kollywood', 'chennai'],
        'Hindi': ['hindi', 'bollywood', 'mumbai'],
        'Telugu': ['telugu', 'tollywood', 'hyderabad'],
        'Malayalam': ['malayalam', 'mollywood', 'kerala'],
        'Kannada': ['kannada', 'sandalwood', 'karnataka'],
    }
    
    for language, keywords in language_keywords.items():
        if any(kw in tag_str for kw in keywords):
            return language
    
    return None