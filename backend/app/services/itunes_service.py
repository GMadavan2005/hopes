import httpx

async def search_itunes(term: str, artist: str = None, limit: int = 10):
    base_url = "https://itunes.apple.com/search"
    
    search_term = f"{term} {artist}" if artist else term
    
    params = {
        "term": search_term,
        "media": "music",
        "entity": "song",
        "limit": limit
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(base_url, params=params)
            data = response.json()
            
            results = []
            for track in data.get('results', []):
                results.append({
                    "song_id": str(track['trackId']),
                    "song_name": track['trackName'],
                    "artist_name": track['artistName'],
                    "album_name": track.get('collectionName', ''),
                    "artwork_url": track.get('artworkUrl100', '').replace('100x100', '600x600'),
                    "preview_url": track.get('previewUrl', ''),
                    "duration_ms": track.get('trackTimeMillis', 0),
                    "release_year": track.get('releaseDate', '')[:4] if track.get('releaseDate') else None
                })
            
            return results
    except Exception as e:
        print(f"iTunes error: {e}")
        return []