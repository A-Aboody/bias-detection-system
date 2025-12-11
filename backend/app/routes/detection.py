from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict
from app.models.bias_detector import bias_detector
import json
from datetime import datetime
import re

router = APIRouter()

VALID_CATEGORIES = ["gender", "race", "religion", "political", "socioeconomic", "age"]

class DetectionRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Text to analyze for bias")
    categories: Optional[List[str]] = Field(default=None, description="Specific bias categories to check")

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        """Validate text input"""
        if not v or not v.strip():
            raise ValueError("Text cannot be empty or only whitespace")
        # Remove excessive whitespace
        v = re.sub(r'\s+', ' ', v.strip())
        return v

    @field_validator('categories')
    @classmethod
    def validate_categories(cls, v):
        """Validate category list"""
        if v is not None:
            if not isinstance(v, list):
                raise ValueError("Categories must be a list")
            if len(v) == 0:
                raise ValueError("Categories list cannot be empty")
            invalid = [cat for cat in v if cat not in VALID_CATEGORIES]
            if invalid:
                raise ValueError(f"Invalid categories: {', '.join(invalid)}. Valid categories are: {', '.join(VALID_CATEGORIES)}")
        return v

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

    Args:
        request: DetectionRequest with text and optional categories

    Returns:
        DetectionResponse with bias analysis results

    Raises:
        HTTPException: If an error occurs during detection
    """
    try:
        # Validate text length
        if len(request.text) > 10000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text exceeds maximum length of 10,000 characters"
            )

        # Run lexicon-based detection
        results = bias_detector.detect_lexicon_bias(request.text)

        # Filter by requested categories if specified
        if request.categories:
            filtered_categories = [
                cat for cat in results["bias_categories"]
                if cat in request.categories
            ]
            filtered_scores = {
                cat: score for cat, score in results["bias_scores"].items()
                if cat in request.categories
            }
            results["bias_categories"] = filtered_categories
            results["bias_scores"] = filtered_scores
            results["has_bias"] = len(filtered_categories) > 0

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

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during bias detection. Please try again."
        )

@router.post("/analyze")
async def comprehensive_analysis(request: AnalysisRequest):
    """
    Perform comprehensive bias analysis including detailed metrics

    Args:
        request: AnalysisRequest with text and optional model name

    Returns:
        Comprehensive analysis including statistics, bias analysis, and recommendations

    Raises:
        HTTPException: If an error occurs during analysis
    """
    try:
        # Validate text length
        if len(request.text) > 10000:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Text exceeds maximum length of 10,000 characters"
            )

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

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during comprehensive analysis. Please try again."
        )

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
    categories_info = []
    descriptions = {
        "gender": "Gender-based stereotypes and imbalances",
        "race": "Racial and ethnic bias",
        "religion": "Religious bias and stereotypes",
        "political": "Political bias and loaded language",
        "socioeconomic": "Socioeconomic stereotypes and class bias",
        "age": "Age-based stereotypes and discrimination"
    }

    for cat in bias_detector.bias_lexicons.keys():
        categories_info.append({
            "name": cat,
            "description": descriptions.get(cat, "No description available")
        })

    return {
        "categories": categories_info
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
        elif category == "age":
            recommendations.append(
                "Avoid age-based stereotypes and assumptions about capabilities based on age."
            )

    if results["severity"] == "severe":
        recommendations.append(
            "High bias detected. Consider significant revision of the text."
        )
    elif results["severity"] == "moderate":
        recommendations.append(
            "Moderate bias detected. Review highlighted terms and consider alternative phrasing."
        )

    return recommendations
