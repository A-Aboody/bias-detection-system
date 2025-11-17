from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from app.models.bias_detector import bias_detector
import json
from datetime import datetime

router = APIRouter()

class DetectionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to analyze for bias")
    categories: Optional[List[str]] = Field(default=None, description="Specific bias categories to check")

class DetectionResponse(BaseModel):
    text: str
    has_bias: bool
    bias_categories: List[str]
    bias_scores: Dict[str, float]
    severity: str
    overall_score: Optional[float] = None
    highlights: List[Dict]
    timestamp: str

class AnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000)
    model_name: Optional[str] = Field(default=None, description="Specific model to use")

@router.post("/detect", response_model=DetectionResponse)
async def detect_bias(request: DetectionRequest):
    """
    Detect bias in provided text using lexicon-based approach
    """
    try:
        # Run lexicon-based detection
        results = bias_detector.detect_lexicon_bias(request.text)
        
        # Get highlights for flagged categories
        highlights = []
        if results["has_bias"]:
            highlights = bias_detector.highlight_biased_terms(
                request.text, 
                results["bias_categories"]
            )
        
        response = DetectionResponse(
            text=request.text,
            has_bias=results["has_bias"],
            bias_categories=results["bias_categories"],
            bias_scores=results["bias_scores"],
            severity=results["severity"],
            overall_score=results.get("overall_score"),
            highlights=highlights,
            timestamp=datetime.now().isoformat()
        )
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during detection: {str(e)}")

@router.post("/analyze")
async def comprehensive_analysis(request: AnalysisRequest):
    """
    Perform comprehensive bias analysis including detailed metrics
    """
    try:
        # Lexicon-based detection
        lexicon_results = bias_detector.detect_lexicon_bias(request.text)
        
        # Get highlights
        highlights = []
        if lexicon_results["has_bias"]:
            highlights = bias_detector.highlight_biased_terms(
                request.text,
                lexicon_results["bias_categories"]
            )
        
        # Calculate additional metrics
        word_count = len(request.text.split())
        char_count = len(request.text)
        
        # Generate recommendations
        recommendations = _generate_recommendations(lexicon_results)
        
        response = {
            "text": request.text,
            "statistics": {
                "word_count": word_count,
                "char_count": char_count,
                "sentence_count": request.text.count('.') + request.text.count('!') + request.text.count('?')
            },
            "bias_analysis": {
                "has_bias": lexicon_results["has_bias"],
                "categories": lexicon_results["bias_categories"],
                "scores": lexicon_results["bias_scores"],
                "severity": lexicon_results["severity"],
                "overall_score": lexicon_results.get("overall_score", 0)
            },
            "highlights": highlights,
            "recommendations": recommendations,
            "timestamp": datetime.now().isoformat()
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during analysis: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Check if the detection service is running properly
    """
    return {
        "status": "healthy",
        "service": "bias-detection",
        "version": "1.0.0",
        "lexicons_loaded": len(bias_detector.bias_lexicons),
        "model_loaded": bias_detector.model is not None
    }

@router.get("/categories")
async def get_bias_categories():
    """
    Get list of available bias categories
    """
    return {
        "categories": list(bias_detector.bias_lexicons.keys()),
        "descriptions": {
            "gender": "Gender-based stereotypes and imbalances",
            "race": "Racial and ethnic bias",
            "religion": "Religious bias and stereotypes",
            "political": "Political bias and loaded language",
            "socioeconomic": "Socioeconomic stereotypes and class bias"
        }
    }

def _generate_recommendations(results: Dict) -> List[str]:
    """Generate recommendations based on detected bias"""
    recommendations = []
    
    if not results["has_bias"]:
        return ["No significant bias detected. The text appears balanced."]
    
    for category in results["bias_categories"]:
        if category == "gender":
            recommendations.append(
                "Consider using gender-neutral language or ensuring balanced representation of all genders."
            )
        elif category == "race":
            recommendations.append(
                "Review racial or ethnic references to ensure they are relevant and non-stereotypical."
            )
        elif category == "religion":
            recommendations.append(
                "Ensure religious references are neutral and avoid stereotypical associations."
            )
        elif category == "political":
            recommendations.append(
                "Consider using more neutral language and presenting multiple perspectives."
            )
        elif category == "socioeconomic":
            recommendations.append(
                "Avoid stereotypes related to socioeconomic status and class."
            )
    
    if results["severity"] == "severe":
        recommendations.append(
            "⚠️ High bias detected. Consider significant revision of the text."
        )
    
    return recommendations
