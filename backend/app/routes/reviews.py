from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services import gemini_service
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter()

class ReviewAnalysisRequest(BaseModel):
    text: str

@router.post("/analyze-review")
async def analyze_review(request: ReviewAnalysisRequest):
    sentiment = await gemini_service.analyze_review_sentiment(request.text)
    
    return {
        "text": request.text,
        "sentiment": sentiment,
        "is_toxic": "toxic" in request.text.lower() or "hate" in request.text.lower()
    }