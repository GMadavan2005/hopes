import httpx
from app.config import settings

async def get_song_info(artist: str, track: str):
    if not settings.LASTFM_API_KEY:
        return {"play_count": 0, "tags": []}
    
    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getInfo",
        "api_key": settings.LASTFM_API_KEY,
        "artist": artist,
        "track": track,
        "format": "json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(base_url, params=params)
            data = response.json()
            
            if 'track' in data:
                track_data = data['track']
                return {
                    "play_count": int(track_data.get('playcount', 0)),
                    "tags": [tag['name'] for tag in track_data.get('toptags', {}).get('tag', [])[:5]]
                }
    except:
        pass
    
    return {"play_count": 0, "tags": []}

async def get_similar_tracks(artist: str, track: str, limit: int = 5):
    if not settings.LASTFM_API_KEY:
        return []
    
    base_url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        "method": "track.getSimilar",
        "api_key": settings.LASTFM_API_KEY,
        "artist": artist,
        "track": track,
        "limit": limit,
        "format": "json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(base_url, params=params)
            data = response.json()
            
            similar = []
            for track in data.get('similartracks', {}).get('track', []):
                similar.append({
                    "name": track['name'],
                    "artist": track['artist']['name']
                })
            return similar
    except:
        return []