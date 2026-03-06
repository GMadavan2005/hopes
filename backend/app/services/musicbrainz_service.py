import httpx
from typing import List, Dict

async def search_songs(query: str, artist: str = None, limit: int = 20) -> List[Dict]:
    base_url = "https://musicbrainz.org/ws/2/recording"
    
    search_query = query
    if artist:
        search_query = f'recording:"{query}" AND artist:"{artist}"'
    
    params = {
        "query": search_query,
        "fmt": "json",
        "limit": limit
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(base_url, params=params)
            data = response.json()
            
            songs = []
            for recording in data.get('recordings', []):
                artist_name = "Unknown Artist"
                if recording.get('artist-credit'):
                    artist_name = recording['artist-credit'][0]['name']
                
                release_year = None
                if recording.get('first-release-date'):
                    try:
                        release_year = int(recording['first-release-date'][:4])
                    except:
                        pass
                
                songs.append({
                    "song_id": recording['id'],
                    "song_name": recording['title'],
                    "artist_name": artist_name,
                    "release_year": release_year,
                    "era": identify_era(release_year) if release_year else None,
                    "tags": [tag['name'] for tag in recording.get('tags', [])[:5]],
                    "length_ms": recording.get('length', 0)
                })
            
            return songs
    except Exception as e:
        print(f"MusicBrainz error: {e}")
        return []

def identify_era(year: int) -> str:
    if not year:
        return None
    
    era_map = {
        (1950, 1959): "1950s",
        (1960, 1969): "1960s",
        (1970, 1979): "1970s",
        (1980, 1989): "1980s",
        (1990, 1999): "1990s",
        (2000, 2009): "2000s",
        (2010, 2019): "2010s",
        (2020, 2029): "2020s"
    }
    
    for (start, end), era in era_map.items():
        if start <= year <= end:
            return era
    return None

async def get_artist_info(artist_name: str) -> Dict:
    base_url = "https://musicbrainz.org/ws/2/artist"
    params = {
        "query": f'artist:"{artist_name}"',
        "fmt": "json",
        "limit": 1
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(base_url, params=params)
            data = response.json()
            
            if data.get('artists'):
                artist = data['artists'][0]
                return {
                    "artist_id": artist['id'],
                    "artist_name": artist['name'],
                    "type": artist.get('type', ''),
                    "tags": [tag['name'] for tag in artist.get('tags', [])[:10]]
                }
    except:
        pass
    
    return {}