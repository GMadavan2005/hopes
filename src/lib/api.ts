const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000/api';

export async function smartSearch(query: string) {
  const response = await fetch(`${BACKEND_URL}/search?q=${encodeURIComponent(query)}`);
  if (!response.ok) throw new Error('Search failed');
  return response.json();
}

export async function analyzeReview(text: string) {
  const response = await fetch(`${BACKEND_URL}/analyze-review`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  });
  return response.json();
}

export async function getArtistInfo(artistName: string) {
  const response = await fetch(`${BACKEND_URL}/artist/${encodeURIComponent(artistName)}`);
  return response.json();
}

export async function savePreferences(userId: string, prefs: any) {
  const response = await fetch(`${BACKEND_URL}/preferences`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, ...prefs })
  });
  return response.json();
}

export async function getPreferences(userId: string) {
  const response = await fetch(`${BACKEND_URL}/preferences/${userId}`);
  return response.json();
}

export async function getForYou(userId: string) {
  const response = await fetch(`${BACKEND_URL}/for-you/${userId}`);
  return response.json();
}

export async function getTrending(language: string) {
  const response = await fetch(`${BACKEND_URL}/trending/${language}`);
  return response.json();
}