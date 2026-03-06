import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/hooks/useAuth';
import { savePreferences } from '@/lib/api';
import { useToast } from '@/hooks/use-toast';

const LANGUAGES = ['Tamil', 'Hindi', 'Telugu', 'Malayalam', 'Kannada', 'English'];
const ERAS = ['1950s', '1960s', '1970s', '1980s', '1990s', '2000s', '2010s', '2020s'];
const ARTISTS = [
  'AR Rahman', 'Anirudh Ravichander', 'Ilaiyaraaja', 'Harris Jayaraj',
  'Yuvan Shankar Raja', 'Sid Sriram', 'Devi Sri Prasad', 'S. Thaman'
];

export default function Onboarding() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  const [step, setStep] = useState(1);
  const [selectedLanguages, setSelectedLanguages] = useState<string[]>([]);
  const [selectedEras, setSelectedEras] = useState<string[]>([]);
  const [selectedArtists, setSelectedArtists] = useState<string[]>([]);

  const handleSave = async () => {
    if (!user) return;
    
    if (selectedArtists.length < 3) {
      toast({
        title: 'Select at least 3 artists',
        variant: 'destructive'
      });
      return;
    }

    await savePreferences(user.id, {
      languages: selectedLanguages,
      eras: selectedEras,
      favorite_artists: selectedArtists,
      onboarding_completed: true
    });

    toast({ title: 'Preferences saved!' });
    navigate('/');
  };

  const toggleSelection = (item: string, list: string[], setter: Function) => {
    if (list.includes(item)) {
      setter(list.filter(i => i !== item));
    } else {
      setter([...list, item]);
    }
  };

  return (
    <div className="min-h-screen bg-background flex items-center justify-center p-4">
      <div className="max-w-2xl w-full">
        <h1 className="text-3xl font-bold mb-8">Welcome to Soundlog!</h1>
        
        {step === 1 && (
          <div>
            <h2 className="text-xl mb-4">Select your preferred languages</h2>
            <div className="grid grid-cols-2 gap-3">
              {LANGUAGES.map(lang => (
                <Button
                  key={lang}
                  variant={selectedLanguages.includes(lang) ? 'default' : 'outline'}
                  onClick={() => toggleSelection(lang, selectedLanguages, setSelectedLanguages)}
                >
                  {lang}
                </Button>
              ))}
            </div>
            <div className="flex gap-3 mt-6">
              <Button onClick={() => setStep(2)} disabled={selectedLanguages.length === 0}>
                Next
              </Button>
              <Button variant="ghost" onClick={() => setStep(2)}>Skip</Button>
            </div>
          </div>
        )}

        {step === 2 && (
          <div>
            <h2 className="text-xl mb-4">Select your favorite eras</h2>
            <div className="grid grid-cols-4 gap-3">
              {ERAS.map(era => (
                <Button
                  key={era}
                  variant={selectedEras.includes(era) ? 'default' : 'outline'}
                  onClick={() => toggleSelection(era, selectedEras, setSelectedEras)}
                >
                  {era}
                </Button>
              ))}
            </div>
            <div className="flex gap-3 mt-6">
              <Button onClick={() => setStep(1)} variant="outline">Back</Button>
              <Button onClick={() => setStep(3)} disabled={selectedEras.length === 0}>
                Next
              </Button>
              <Button variant="ghost" onClick={() => setStep(3)}>Skip</Button>
            </div>
          </div>
        )}

        {step === 3 && (
          <div>
            <h2 className="text-xl mb-4">Select at least 3 favorite artists</h2>
            <div className="grid grid-cols-2 gap-3">
              {ARTISTS.map(artist => (
                <Button
                  key={artist}
                  variant={selectedArtists.includes(artist) ? 'default' : 'outline'}
                  onClick={() => toggleSelection(artist, selectedArtists, setSelectedArtists)}
                >
                  {artist}
                </Button>
              ))}
            </div>
            <div className="flex gap-3 mt-6">
              <Button onClick={() => setStep(2)} variant="outline">Back</Button>
              <Button onClick={handleSave} disabled={selectedArtists.length < 3}>
                Complete Setup
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}