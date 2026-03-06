import httpx
from typing import Optional, Dict, List

# Free API key from documentation
AUDIODB_API_KEY = "123"  # Free test key
BASE_URL = f"https://www.theaudiodb.com/api/v1/json/{AUDIODB_API_KEY}"

async def search_artist(artist_name: str) -> Optional[Dict]:
    """Search for artist by name"""
    url = f"{BASE_URL}/search.php"
    params = {"s": artist_name}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data.get('artists') and len(data['artists']) > 0:
                artist = data['artists'][0]
                return {
                    "artist_id": artist.get('idArtist'),
                    "artist_name": artist.get('strArtist'),
                    "bio": artist.get('strBiographyEN', ''),
                    "bio_short": artist.get('strBiographyEN', '')[:500] + '...' if artist.get('strBiographyEN') else '',
                    "photo_url": artist.get('strArtistThumb'),
                    "logo_url": artist.get('strArtistLogo'),
                    "banner_url": artist.get('strArtistBanner'),
                    "fanart_url": artist.get('strArtistFanart'),
                    "genre": artist.get('strGenre', ''),
                    "style": artist.get('strStyle', ''),
                    "mood": artist.get('strMood', ''),
                    "born": artist.get('intBornYear'),
                    "formed": artist.get('intFormedYear'),
                    "website": artist.get('strWebsite', ''),
                    "facebook": artist.get('strFacebook', ''),
                    "twitter": artist.get('strTwitter', ''),
                    "country": artist.get('strCountry', ''),
                    "label": artist.get('strLabel', ''),
                }
    except Exception as e:
        print(f"AudioDB search error: {e}")
        return None

async def get_artist_by_id(artist_id: str) -> Optional[Dict]:
    """Get detailed artist info by ID"""
    url = f"{BASE_URL}/artist.php"
    params = {"i": artist_id}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data.get('artists'):
                return data['artists'][0]
    except Exception as e:
        print(f"AudioDB get artist error: {e}")
        return None

async def get_artist_albums(artist_id: str) -> List[Dict]:
    """Get all albums by artist ID"""
    url = f"{BASE_URL}/album.php"
    params = {"i": artist_id}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            albums = []
            if data.get('album'):
                for album in data['album']:
                    albums.append({
                        "album_id": album.get('idAlbum'),
                        "album_name": album.get('strAlbum'),
                        "artist_name": album.get('strArtist'),
                        "year": album.get('intYearReleased'),
                        "genre": album.get('strGenre'),
                        "artwork_url": album.get('strAlbumThumb'),
                        "description": album.get('strDescriptionEN', ''),
                        "sales": album.get('intSales'),
                        "score": album.get('intScore'),
                    })
            return albums
    except Exception as e:
        print(f"AudioDB get albums error: {e}")
        return []

async def get_artist_tracks(artist_id: str) -> List[Dict]:
    """Get all tracks by artist ID"""
    url = f"{BASE_URL}/track.php"
    params = {"h": artist_id}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            tracks = []
            if data.get('track'):
                for track in data['track']:
                    tracks.append({
                        "track_id": track.get('idTrack'),
                        "track_name": track.get('strTrack'),
                        "album_name": track.get('strAlbum'),
                        "artist_name": track.get('strArtist'),
                        "genre": track.get('strGenre'),
                        "music_video_url": track.get('strMusicVid'),  # YouTube link
                        "description": track.get('strDescriptionEN', ''),
                        "duration_ms": int(track.get('intDuration', 0)) * 1000 if track.get('intDuration') else None,
                    })
            return tracks
    except Exception as e:
        print(f"AudioDB get tracks error: {e}")
        return []

async def search_album(album_name: str) -> List[Dict]:
    """Search for albums by name"""
    url = f"{BASE_URL}/searchalbum.php"
    params = {"s": album_name}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            albums = []
            if data.get('album'):
                for album in data['album']:
                    albums.append({
                        "album_id": album.get('idAlbum'),
                        "album_name": album.get('strAlbum'),
                        "artist_name": album.get('strArtist'),
                        "year": album.get('intYearReleased'),
                        "artwork_url": album.get('strAlbumThumb'),
                    })
            return albums
    except Exception as e:
        print(f"AudioDB search album error: {e}")
        return []

async def get_music_video(artist_name: str, track_name: str) -> Optional[str]:
    """Get music video URL for a track"""
    # First search for the artist
    artist_data = await search_artist(artist_name)
    if not artist_data:
        return None
    
    # Get all tracks by artist
    tracks = await get_artist_tracks(artist_data['artist_id'])
    
    # Find matching track
    for track in tracks:
        if track_name.lower() in track['track_name'].lower():
            return track.get('music_video_url')
    
    return None

async def get_trending_artists() -> List[Dict]:
    """Get trending artists (uses most loved endpoint)"""
    url = f"{BASE_URL}/trending.php"
    params = {"country": "us", "type": "itunes", "format": "singles"}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(url, params=params)
            data = response.json()
            
            if data.get('trending'):
                return data['trending']
    except:
        pass
    
    return []