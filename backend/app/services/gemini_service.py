import google.generativeai as genai
from app.config import settings
import json
import re
from typing import List, Dict, Optional

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    # Use Gemini 1.5 Flash - FASTEST and FREE
    model = genai.GenerativeModel(
        'gemini-1.5-flash',
        generation_config={
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
    )
else:
    model = None
    print("WARNING: GEMINI_API_KEY not set - sentiment analysis and recommendations disabled")

# ==========================================
# SEARCH QUERY PARSING
# ==========================================

async def parse_search_query(query: str) -> dict:
    """
    Parse user search query and extract structured information
    """
    
    if not model:
        # Fallback parsing without Gemini
        return {
            "artist_name": None,
            "song_name": None,
            "language": None,
            "genre": None,
            "era": None,
            "search_query": query,
            "mood": None
        }
    
    prompt = f"""You are a music search expert specializing in Indian music.

User searched: "{query}"

Analyze this query and return a JSON object with these fields:
{{
  "artist_name": "Full artist name if mentioned, else null",
  "song_name": "Song title if mentioned, else null",
  "language": "Tamil/Hindi/Telugu/Malayalam/Kannada/English if detected, else null",
  "genre": "Genre/mood if mentioned, else null",
  "era": "Decade if mentioned, else null",
  "search_query": "Cleaned search term for API",
  "mood": "Emotional tone if detected, else null"
}}

ABBREVIATIONS:
- arr, ar rahman → AR Rahman
- anirudh, ani → Anirudh Ravichander
- harris → Harris Jayaraj
- ilayaraja, raja → Ilaiyaraaja
- yuvan → Yuvan Shankar Raja
- sid sriram → Sid Sriram
- dsp → Devi Sri Prasad
- thaman → S. Thaman

Return ONLY the JSON object, no markdown.
"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        
        parsed = json.loads(text)
        return {
            "artist_name": parsed.get("artist_name"),
            "song_name": parsed.get("song_name"),
            "language": parsed.get("language"),
            "genre": parsed.get("genre"),
            "era": parsed.get("era"),
            "search_query": parsed.get("search_query", query),
            "mood": parsed.get("mood")
        }
        
    except Exception as e:
        print(f"Gemini parsing error: {e}")
        return {
            "artist_name": None,
            "song_name": None,
            "language": None,
            "genre": None,
            "era": None,
            "search_query": query,
            "mood": None
        }

# ==========================================
# SENTIMENT ANALYSIS
# ==========================================

async def analyze_review_sentiment(review_text: str) -> Dict:
    """
    Analyze review sentiment and detect toxicity
    """
    
    if not review_text or len(review_text.strip()) < 3:
        return {
            "sentiment": "neutral",
            "is_toxic": False,
            "confidence": 0.0,
            "reasoning": "No text provided"
        }
    
    if not model:
        # Fallback keyword-based detection
        text_lower = review_text.lower()
        positive_words = ['fire', 'banger', 'amazing', 'love', 'best', 'masterpiece', 'goat', 'incredible', 'beautiful']
        negative_words = ['bad', 'boring', 'skip', 'worst', 'terrible', 'trash', 'hate', 'awful']
        toxic_words = ['stupid', 'idiot', 'garbage']
        
        is_toxic = any(word in text_lower for word in toxic_words)
        
        if any(word in text_lower for word in positive_words):
            sentiment = 'positive'
        elif any(word in text_lower for word in negative_words):
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            "sentiment": sentiment,
            "is_toxic": is_toxic,
            "confidence": 0.6,
            "reasoning": "Keyword-based fallback"
        }
    
    prompt = f"""Analyze this music review for sentiment.

Review: "{review_text}"

Return a JSON object:
{{
  "sentiment": "positive/negative/neutral",
  "is_toxic": true/false,
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation"
}}

RULES:
- Positive: fire, banger, amazing, masterpiece, love, best, incredible
- Negative: bad, boring, skip, worst, terrible, trash
- Neutral: everything else
- Toxic: hate speech, slurs, extreme negativity toward people

Return ONLY JSON.
"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        
        result = json.loads(text)
        return {
            "sentiment": result.get("sentiment", "neutral"),
            "is_toxic": result.get("is_toxic", False),
            "confidence": float(result.get("confidence", 0.5)),
            "reasoning": result.get("reasoning", "")
        }
        
    except Exception as e:
        print(f"Sentiment analysis error: {e}")
        # Fallback
        text_lower = review_text.lower()
        positive_words = ['fire', 'banger', 'amazing', 'love', 'best', 'masterpiece', 'goat']
        negative_words = ['bad', 'boring', 'skip', 'worst', 'terrible', 'trash']
        
        if any(word in text_lower for word in positive_words):
            sentiment = 'positive'
        elif any(word in text_lower for word in negative_words):
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            "sentiment": sentiment,
            "is_toxic": False,
            "confidence": 0.6,
            "reasoning": "Keyword fallback"
        }

# ==========================================
# PERSONALIZED RECOMMENDATIONS
# ==========================================

async def generate_for_you_recommendations(preferences: Dict, limit: int = 20) -> List[Dict]:
    """
    Generate personalized song recommendations
    """
    
    if not model:
        return []
    
    prompt = f"""You are a music recommendation expert for Indian music.

User preferences:
- Languages: {', '.join(preferences.get('languages', [])) or 'Any'}
- Favorite eras: {', '.join(preferences.get('eras', [])) or 'Any'}
- Favorite artists: {', '.join(preferences.get('favorite_artists', [])) or 'None'}
- Genres: {', '.join(preferences.get('genres', [])) or 'Any'}

Generate {limit} song recommendations.

Return a JSON array:
[
  {{
    "song_name": "Title",
    "artist_name": "Artist",
    "language": "Tamil/Hindi/etc",
    "era": "1990s/2000s/etc",
    "reason": "Why recommended"
  }}
]

Return ONLY the JSON array.
"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        
        recommendations = json.loads(text)
        return recommendations
        
    except Exception as e:
        print(f"Recommendation error: {e}")
        return []

# ==========================================
# SONG SIMILARITY
# ==========================================

async def find_similar_songs(song_name: str, artist_name: str, limit: int = 10) -> List[str]:
    """Find similar songs"""
    
    if not model:
        return []
    
    prompt = f"""Find {limit} songs similar to "{song_name}" by {artist_name}.

Return a JSON array of song names:
["Song 1", "Song 2", ...]

Return ONLY the JSON array.
"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        
        similar = json.loads(text)
        return similar
        
    except:
        return []

# ==========================================
# PLAYLIST GENERATION
# ==========================================

async def generate_playlist(theme: str, limit: int = 20) -> Dict:
    """Generate a themed playlist"""
    
    if not model:
        return {"playlist_name": theme, "description": "", "songs": []}
    
    prompt = f"""Create a {limit}-song {theme} playlist.

Return JSON:
{{
  "playlist_name": "Title",
  "description": "Description",
  "songs": [{{"song_name": "Title", "artist_name": "Artist"}}]
}}

Return ONLY JSON.
"""
    
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        text = re.sub(r'```json\s*', '', text)
        text = re.sub(r'```\s*$', '', text)
        
        return json.loads(text)
        
    except:
        return {"playlist_name": theme, "description": "", "songs": []}

# ==========================================
# BATCH REVIEW ANALYSIS
# ==========================================

async def batch_analyze_reviews(reviews: List[str]) -> List[Dict]:
    """Analyze multiple reviews efficiently"""
    
    if not reviews or not model:
        return [{"sentiment": "neutral", "is_toxic": False} for _ in reviews]
    
    try:
        results = []
        for review in reviews:
            result = await analyze_review_sentiment(review)
            results.append({
                "sentiment": result.get("sentiment", "neutral"),
                "is_toxic": result.get("is_toxic", False)
            })
        return results
        
    except:
        return [{"sentiment": "neutral", "is_toxic": False} for _ in reviews]
