"""
API endpoint tests for bias detection system
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""

    def test_health_check(self):
        """Test health endpoint returns 200"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "model_loaded" in data


class TestDetectEndpoint:
    """Tests for bias detection endpoint"""

    def test_detect_neutral_text(self):
        """Test detection with neutral text"""
        response = client.post(
            "/api/v1/detect",
            json={"text": "The sky is blue and the grass is green."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_bias"] == False
        assert data["severity"] == "none"

    def test_detect_gender_bias(self):
        """Test detection of gender bias"""
        response = client.post(
            "/api/v1/detect",
            json={"text": "The female nurse assisted the male doctor with surgery."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_bias"] == True
        assert "gender" in data["bias_categories"]

    def test_detect_race_bias(self):
        """Test detection of racial bias"""
        response = client.post(
            "/api/v1/detect",
            json={"text": "The inner-city youth were suspected of criminal activity."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_bias"] == True
        assert "race" in data["bias_categories"]

    def test_detect_religion_bias(self):
        """Test detection of religious bias"""
        response = client.post(
            "/api/v1/detect",
            json={"text": "Muslim immigrants are likely to be terrorists."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_bias"] == True
        assert "religion" in data["bias_categories"]

    def test_detect_political_bias(self):
        """Test detection of political bias"""
        response = client.post(
            "/api/v1/detect",
            json={"text": "Radical leftists are destroying our country."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_bias"] == True
        assert "political" in data["bias_categories"]

    def test_detect_socioeconomic_bias(self):
        """Test detection of socioeconomic bias"""
        response = client.post(
            "/api/v1/detect",
            json={"text": "Poor people are lazy and looking for handouts."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_bias"] == True
        assert "socioeconomic" in data["bias_categories"]

    def test_detect_age_bias(self):
        """Test detection of age bias"""
        response = client.post(
            "/api/v1/detect",
            json={"text": "The elderly worker is too old to learn new technology."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_bias"] == True
        assert "age" in data["bias_categories"]

    def test_detect_empty_text(self):
        """Test detection with empty text"""
        response = client.post(
            "/api/v1/detect",
            json={"text": ""}
        )
        assert response.status_code == 422  # Validation error

    def test_detect_with_categories_filter(self):
        """Test detection with category filtering"""
        response = client.post(
            "/api/v1/detect",
            json={
                "text": "The female nurse assisted the male doctor.",
                "categories": ["gender"]
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "gender" in data["bias_categories"]

    def test_detect_multiple_biases(self):
        """Test detection of multiple bias types"""
        response = client.post(
            "/api/v1/detect",
            json={
                "text": "The female nurse from the inner-city was surprisingly competent."
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["has_bias"] == True
        assert len(data["bias_categories"]) >= 2


class TestAnalyzeEndpoint:
    """Tests for comprehensive analysis endpoint"""

    def test_analyze_with_neutral_text(self):
        """Test comprehensive analysis with neutral text"""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "The weather today is pleasant and sunny."}
        )
        assert response.status_code == 200
        data = response.json()
        assert "bias_analysis" in data
        assert "statistics" in data
        assert "recommendations" in data

    def test_analyze_with_biased_text(self):
        """Test comprehensive analysis with biased text"""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "Women are naturally better at nursing than engineering."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["bias_analysis"]["has_bias"] == True
        assert len(data["recommendations"]) > 0

    def test_analyze_statistics_present(self):
        """Test that statistics are included in comprehensive analysis"""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "This is a test sentence with multiple words."}
        )
        assert response.status_code == 200
        data = response.json()
        assert "word_count" in data["statistics"]
        assert "char_count" in data["statistics"]
        assert "sentence_count" in data["statistics"]
        assert data["statistics"]["word_count"] > 0


class TestCategoriesEndpoint:
    """Tests for categories endpoint"""

    def test_get_categories(self):
        """Test retrieval of available bias categories"""
        response = client.get("/api/v1/categories")
        assert response.status_code == 200
        data = response.json()
        assert "categories" in data
        assert isinstance(data["categories"], list)
        assert len(data["categories"]) >= 6

        # Check that all expected categories are present
        category_names = [cat["name"] for cat in data["categories"]]
        assert "gender" in category_names
        assert "race" in category_names
        assert "religion" in category_names
        assert "political" in category_names
        assert "socioeconomic" in category_names
        assert "age" in category_names


class TestValidation:
    """Tests for input validation"""

    def test_missing_text_field(self):
        """Test that missing text field is rejected"""
        response = client.post("/api/v1/detect", json={})
        assert response.status_code == 422

    def test_invalid_category(self):
        """Test that invalid categories are handled gracefully"""
        response = client.post(
            "/api/v1/detect",
            json={
                "text": "Test text",
                "categories": ["invalid_category"]
            }
        )
        # Should still process with valid categories
        assert response.status_code == 200


class TestResponseStructure:
    """Tests for response data structure"""

    def test_detect_response_structure(self):
        """Test that detect response has correct structure"""
        response = client.post(
            "/api/v1/detect",
            json={"text": "The nurse helped the patient."}
        )
        assert response.status_code == 200
        data = response.json()

        # Required fields
        assert "text" in data
        assert "has_bias" in data
        assert "bias_categories" in data
        assert "bias_scores" in data
        assert "severity" in data
        assert "overall_score" in data
        assert "highlights" in data
        assert "timestamp" in data

    def test_analyze_response_structure(self):
        """Test that analyze response has correct structure"""
        response = client.post(
            "/api/v1/analyze",
            json={"text": "Sample text for analysis."}
        )
        assert response.status_code == 200
        data = response.json()

        # Required fields
        assert "text" in data
        assert "bias_analysis" in data
        assert "statistics" in data
        assert "recommendations" in data
        assert "highlights" in data
        assert "timestamp" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
