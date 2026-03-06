import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Play, Globe, Music2 } from 'lucide-react';
import { Button } from '@/components/ui/button';

interface ArtistData {
  artist_name: string;
  bio: string;
  photo_url: string;
  banner_url: string;
  genre: string;
  country: string;
  website: string;
  facebook: string;
  twitter: string;
}

export default function ArtistPage() {
  const { artistName } = useParams();
  const [artist, setArtist] = useState<ArtistData | null>(null);
  const [albums, setAlbums] = useState([]);
  const [tracks, setTracks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchArtistData();
  }, [artistName]);

  async function fetchArtistData() {
    setLoading(true);
    try {
      const response = await fetch(
        `http://localhost:8000/api/artist/${encodeURIComponent(artistName!)}`
      );
      const data = await response.json();
      setArtist(data.artist);
      setAlbums(data.albums || []);
      setTracks(data.tracks || []);
    } catch (error) {
      console.error('Error fetching artist:', error);
    } finally {
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!artist) {
    return (
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-2xl">Artist not found</h1>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Banner */}
      {artist.banner_url && (
        <div 
          className="h-64 bg-cover bg-center relative"
          style={{ backgroundImage: `url(${artist.banner_url})` }}
        >
          <div className="absolute inset-0 bg-gradient-to-b from-transparent to-background"></div>
        </div>
      )}

      <div className="container mx-auto px-4 -mt-32 relative z-10">
        {/* Artist Header */}
        <div className="flex flex-col md:flex-row gap-8 items-start mb-12">
          {artist.photo_url && (
            <img
              src={artist.photo_url}
              alt={artist.artist_name}
              className="w-64 h-64 rounded-lg shadow-2xl object-cover"
            />
          )}
          
          <div className="flex-1">
            <h1 className="text-5xl font-bold mb-2">{artist.artist_name}</h1>
            
            <div className="flex gap-4 mb-4 text-muted-foreground">
              {artist.genre && (
                <span className="flex items-center gap-2">
                  <Music2 className="w-4 h-4" />
                  {artist.genre}
                </span>
              )}
              {artist.country && (
                <span>{artist.country}</span>
              )}
            </div>

            <div className="flex gap-3 mb-6">
              {artist.website && (
                <Button asChild variant="outline">
                  <a href={`https://${artist.website}`} target="_blank" rel="noopener noreferrer">
                    <Globe className="w-4 h-4 mr-2" />
                    Website
                  </a>
                </Button>
              )}
              <Button>
                <Play className="w-4 h-4 mr-2" />
                Play on Spotify
              </Button>
            </div>

            {artist.bio && (
              <div className="prose prose-invert max-w-none">
                <p className="text-muted-foreground leading-relaxed">
                  {artist.bio}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Top Tracks */}
        {tracks.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold mb-6">Top Tracks</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {tracks.slice(0, 6).map((track: any) => (
                <div
                  key={track.track_id}
                  className="flex items-center gap-4 p-4 rounded-lg bg-card hover:bg-accent transition-colors cursor-pointer"
                >
                  <div className="w-12 h-12 rounded bg-primary/10 flex items-center justify-center">
                    <Music2 className="w-6 h-6 text-primary" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="font-semibold truncate">{track.track_name}</h3>
                    <p className="text-sm text-muted-foreground truncate">
                      {track.album_name}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Albums */}
        {albums.length > 0 && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Albums</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {albums.map((album: any) => (
                <div key={album.album_id} className="group cursor-pointer">
                  <div className="aspect-square rounded-lg overflow-hidden mb-3 bg-accent">
                    {album.artwork_url ? (
                      <img
                        src={album.artwork_url}
                        alt={album.album_name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                      />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center">
                        <Music2 className="w-12 h-12 text-muted-foreground" />
                      </div>
                    )}
                  </div>
                  <h3 className="font-semibold text-sm truncate">{album.album_name}</h3>
                  <p className="text-xs text-muted-foreground">{album.year}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}