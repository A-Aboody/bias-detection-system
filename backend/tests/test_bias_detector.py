"""
Unit tests for BiasDetector model
"""
import pytest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.models.bias_detector import BiasDetector


@pytest.fixture
def detector():
    """Create a BiasDetector instance for testing"""
    return BiasDetector()


class TestBiasDetectorInitialization:
    """Tests for BiasDetector initialization"""

    def test_detector_initializes(self, detector):
        """Test that detector initializes successfully"""
        assert detector is not None
        assert detector.bias_lexicons is not None

    def test_lexicons_loaded(self, detector):
        """Test that lexicons are loaded correctly"""
        assert "gender" in detector.bias_lexicons
        assert "race" in detector.bias_lexicons
        assert "religion" in detector.bias_lexicons
        assert "political" in detector.bias_lexicons
        assert "socioeconomic" in detector.bias_lexicons
        assert "age" in detector.bias_lexicons


class TestGenderBiasDetection:
    """Tests for gender bias detection"""

    def test_neutral_text_no_bias(self, detector):
        """Test that neutral text doesn't flag gender bias"""
        text = "The employee completed the project on time."
        result = detector.detect_lexicon_bias(text)
        assert "gender" not in result["bias_categories"]

    def test_gender_occupation_stereotype(self, detector):
        """Test detection of gender + occupation stereotypes"""
        text = "The female nurse assisted the male doctor with surgery."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "gender" in result["bias_categories"]

    def test_gender_negative_trait_association(self, detector):
        """Test detection of gender + negative trait patterns"""
        text = "Women are emotional and irrational."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "gender" in result["bias_categories"]

    def test_backhanded_compliment(self, detector):
        """Test detection of backhanded compliments"""
        text = "She is surprisingly competent for a woman."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "gender" in result["bias_categories"]


class TestRaceBiasDetection:
    """Tests for racial bias detection"""

    def test_neutral_racial_mention(self, detector):
        """Test that neutral racial mentions don't flag bias"""
        text = "The diverse team included Asian, Black, and White members."
        result = detector.detect_lexicon_bias(text)
        # Might flag slightly, but shouldn't be severe
        if result["has_bias"]:
            assert result["severity"] in ["mild", "none"]

    def test_coded_racial_language(self, detector):
        """Test detection of coded racial language"""
        text = "The inner-city youth were suspected of the crime."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "race" in result["bias_categories"]

    def test_racial_stereotypes(self, detector):
        """Test detection of racial stereotypes"""
        text = "Asian students are naturally gifted at math."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "race" in result["bias_categories"]


class TestReligionBiasDetection:
    """Tests for religious bias detection"""

    def test_neutral_religious_mention(self, detector):
        """Test that neutral religious mentions don't flag"""
        text = "The city has churches, mosques, and temples."
        result = detector.detect_lexicon_bias(text)
        assert "religion" not in result.get("bias_categories", [])

    def test_religious_stereotypes(self, detector):
        """Test detection of religious stereotypes"""
        text = "Muslim immigrants are likely to be terrorists."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "religion" in result["bias_categories"]
        assert result["severity"] in ["moderate", "severe"]


class TestPoliticalBiasDetection:
    """Tests for political bias detection"""

    def test_neutral_political_mention(self, detector):
        """Test that neutral political mentions don't flag"""
        text = "The election featured both Republican and Democratic candidates."
        result = detector.detect_lexicon_bias(text)
        # Might flag mildly, but shouldn't be strong
        if result["has_bias"] and "political" in result["bias_categories"]:
            assert result["severity"] in ["mild", "none"]

    def test_extreme_political_rhetoric(self, detector):
        """Test detection of extreme political rhetoric"""
        text = "Radical leftists are destroying our country."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "political" in result["bias_categories"]


class TestSocioeconomicBiasDetection:
    """Tests for socioeconomic bias detection"""

    def test_neutral_class_mention(self, detector):
        """Test that neutral class mentions don't flag"""
        text = "The study included participants from various economic backgrounds."
        result = detector.detect_lexicon_bias(text)
        assert "socioeconomic" not in result.get("bias_categories", [])

    def test_class_stereotypes(self, detector):
        """Test detection of class-based stereotypes"""
        text = "Poor people are lazy and looking for handouts."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "socioeconomic" in result["bias_categories"]


class TestAgeBiasDetection:
    """Tests for age bias detection"""

    def test_neutral_age_mention(self, detector):
        """Test that neutral age mentions don't flag"""
        text = "The team includes both young and experienced workers."
        result = detector.detect_lexicon_bias(text)
        # Should not flag or be very mild
        if result["has_bias"] and "age" in result["bias_categories"]:
            assert result["severity"] == "mild"

    def test_age_stereotypes_elderly(self, detector):
        """Test detection of age stereotypes about elderly"""
        text = "The elderly worker is too old to learn new technology."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "age" in result["bias_categories"]

    def test_age_stereotypes_millennials(self, detector):
        """Test detection of age stereotypes about young people"""
        text = "Millennials are entitled and lazy."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert "age" in result["bias_categories"]


class TestHighlightTerms:
    """Tests for term highlighting functionality"""

    def test_highlights_biased_terms(self, detector):
        """Test that biased terms are highlighted"""
        text = "The nurse helped the doctor."
        categories = ["gender"]
        highlights = detector.highlight_biased_terms(text, categories)

        assert len(highlights) >= 1
        # Should highlight "nurse" or other gender-associated terms
        terms = [h["term"] for h in highlights]
        assert any(term in ["nurse", "doctor"] for term in terms)

    def test_highlights_sorted_by_position(self, detector):
        """Test that highlights are sorted by position"""
        text = "The elderly nurse was too old to work with the female doctor."
        categories = ["gender", "age"]
        highlights = detector.highlight_biased_terms(text, categories)

        # Check that highlights are in order
        for i in range(len(highlights) - 1):
            assert highlights[i]["start"] <= highlights[i + 1]["start"]


class TestSeverityScoring:
    """Tests for severity scoring"""

    def test_mild_severity(self, detector):
        """Test that mild bias gets appropriate severity"""
        text = "He works as an engineer."
        result = detector.detect_lexicon_bias(text)
        if result["has_bias"]:
            assert result["severity"] == "mild"

    def test_moderate_severity(self, detector):
        """Test that moderate bias gets appropriate severity"""
        text = "Women are naturally better at nursing than engineering."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert result["severity"] in ["mild", "moderate"]

    def test_severe_severity(self, detector):
        """Test that severe bias gets appropriate severity"""
        text = "Muslim refugees are terrorists. The inner-city youth are criminals. Women are stupid and emotional."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert result["severity"] in ["moderate", "severe"]


class TestMultipleBiasCategories:
    """Tests for detecting multiple bias types"""

    def test_multiple_bias_types(self, detector):
        """Test detection of multiple bias categories in one text"""
        text = "The female nurse from the inner-city was surprisingly articulate."
        result = detector.detect_lexicon_bias(text)
        assert result["has_bias"] == True
        assert len(result["bias_categories"]) >= 2


class TestEdgeCases:
    """Tests for edge cases"""

    def test_empty_string(self, detector):
        """Test handling of empty string"""
        result = detector.detect_lexicon_bias("")
        assert result["has_bias"] == False

    def test_very_long_text(self, detector):
        """Test handling of very long text"""
        text = "The weather is nice. " * 1000
        result = detector.detect_lexicon_bias(text)
        # Should complete without error
        assert "has_bias" in result

    def test_special_characters(self, detector):
        """Test handling of special characters"""
        text = "The nurse@#$% helped the doctor!!!"
        result = detector.detect_lexicon_bias(text)
        # Should complete without error
        assert "has_bias" in result

    def test_unicode_text(self, detector):
        """Test handling of unicode characters"""
        text = "The nurse helped the café owner. 你好世界"
        result = detector.detect_lexicon_bias(text)
        # Should complete without error
        assert "has_bias" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
