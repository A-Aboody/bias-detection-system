"""
Test script for bias detection
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.models.bias_detector import bias_detector

# Test cases
test_cases = [
    {
        "name": "Neutral text with gender pronouns",
        "text": "He went to the store. She bought groceries. They had a good day.",
        "expected_bias": False
    },
    {
        "name": "Gender stereotype - female nurse",
        "text": "The female nurse assisted the male doctor with the surgery.",
        "expected_bias": True,
        "expected_categories": ["gender"]
    },
    {
        "name": "Gender stereotype - male engineer",
        "text": "He is an excellent engineer, while she makes a great secretary.",
        "expected_bias": True,
        "expected_categories": ["gender"]
    },
    {
        "name": "Racial stereotype",
        "text": "The inner-city youth were suspected of the crime.",
        "expected_bias": True,
        "expected_categories": ["race"]
    },
    {
        "name": "Neutral mention of race",
        "text": "The study included participants of various ethnicities including Asian, Black, and White individuals.",
        "expected_bias": False
    },
    {
        "name": "Religious stereotype",
        "text": "Muslim extremist terrorists attacked the building.",
        "expected_bias": True,
        "expected_categories": ["religion"]
    },
    {
        "name": "Neutral religious mention",
        "text": "The church, mosque, and temple are all places of worship.",
        "expected_bias": False
    },
    {
        "name": "Socioeconomic stereotype",
        "text": "Poor people are lazy and uneducated.",
        "expected_bias": True,
        "expected_categories": ["socioeconomic"]
    },
    {
        "name": "Neutral socioeconomic mention",
        "text": "The program serves both wealthy and poor communities.",
        "expected_bias": False
    },
    {
        "name": "Political loaded language",
        "text": "The radical liberal activist extremists are destroying our country.",
        "expected_bias": True,
        "expected_categories": ["political"]
    },
    {
        "name": "Gender attribute stereotype - contrast",
        "text": "girls are stupid whereas men are really smart",
        "expected_bias": True,
        "expected_categories": ["gender"]
    },
    {
        "name": "Gender negative trait",
        "text": "Women are too emotional to lead.",
        "expected_bias": True,
        "expected_categories": ["gender"]
    },
    {
        "name": "Mild - occupation with possessive pronouns",
        "text": "The software engineer reviewed his code while the secretary organized her files.",
        "expected_bias": True,
        "expected_categories": ["gender"],
        "expected_severity": "mild"
    },
    {
        "name": "Moderate - gendered abilities",
        "text": "Women are naturally better at nursing and teaching, while men excel in engineering and leadership roles.",
        "expected_bias": True,
        "expected_categories": ["gender"],
        "expected_severity": "moderate"
    },
    {
        "name": "Severe - backhanded compliment + help needed",
        "text": "The female CEO was surprisingly competent, unlike most women in business. She must have had help from the male executives to get there.",
        "expected_bias": True,
        "expected_categories": ["gender"],
        "expected_severity": "severe"
    }
]

def run_tests():
    print("=" * 80)
    print("BIAS DETECTION TEST SUITE")
    print("=" * 80)

    passed = 0
    failed = 0

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"Text: \"{test['text']}\"")

        result = bias_detector.detect_lexicon_bias(test['text'])

        print(f"\nResults:")
        print(f"  Has Bias: {result['has_bias']}")
        print(f"  Categories: {result['bias_categories']}")
        print(f"  Scores: {result['bias_scores']}")
        print(f"  Severity: {result['severity']}")
        print(f"  Overall Score: {result.get('overall_score', 'N/A')}")

        # Check if test passed
        test_passed = True
        if result['has_bias'] != test['expected_bias']:
            print(f"\n  [FAIL] Expected has_bias={test['expected_bias']}, got {result['has_bias']}")
            test_passed = False
        else:
            print(f"\n  [OK] Bias detection correct")

        if 'expected_categories' in test and test['expected_bias']:
            if not any(cat in result['bias_categories'] for cat in test['expected_categories']):
                print(f"  [FAIL] Expected categories {test['expected_categories']}, got {result['bias_categories']}")
                test_passed = False
            else:
                print(f"  [OK] Categories correct")

        if 'expected_severity' in test and test['expected_bias']:
            if result['severity'] != test['expected_severity']:
                print(f"  [FAIL] Expected severity '{test['expected_severity']}', got '{result['severity']}'")
                test_passed = False
            else:
                print(f"  [OK] Severity correct")

        if test_passed:
            passed += 1
            print("  [PASSED]")
        else:
            failed += 1
            print("  [FAILED]")

        print("-" * 80)

    print(f"\n{'=' * 80}")
    print(f"SUMMARY: {passed} passed, {failed} failed out of {len(test_cases)} tests")
    print(f"Success rate: {(passed/len(test_cases)*100):.1f}%")
    print(f"{'=' * 80}\n")

if __name__ == "__main__":
    run_tests()
