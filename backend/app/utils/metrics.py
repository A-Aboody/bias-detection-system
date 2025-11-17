from typing import Dict, List
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix

def calculate_bias_severity(scores: Dict[str, float]) -> str:
    """
    Calculate overall bias severity based on category scores
    
    Args:
        scores: Dictionary of bias category scores
        
    Returns:
        Severity level: 'none', 'mild', 'moderate', or 'severe'
    """
    if not scores:
        return 'none'
    
    max_score = max(scores.values())
    avg_score = sum(scores.values()) / len(scores)
    
    # Weighted combination of max and average
    combined_score = 0.6 * max_score + 0.4 * avg_score
    
    if combined_score < 0.25:
        return 'mild'
    elif combined_score < 0.5:
        return 'moderate'
    else:
        return 'severe'

def calculate_overall_bias_score(scores: Dict[str, float], weights: Dict[str, float] = None) -> float:
    """
    Calculate weighted overall bias score
    
    Args:
        scores: Dictionary of bias category scores
        weights: Optional custom weights for each category
        
    Returns:
        Overall bias score (0-1)
    """
    if not scores:
        return 0.0
    
    if weights is None:
        # Default equal weights
        weights = {category: 1.0 for category in scores.keys()}
    
    weighted_sum = sum(scores[cat] * weights.get(cat, 1.0) for cat in scores)
    total_weight = sum(weights.get(cat, 1.0) for cat in scores)
    
    return round(weighted_sum / total_weight, 3)

def calculate_category_distribution(detections: List[Dict]) -> Dict[str, int]:
    """
    Calculate distribution of bias categories across multiple detections
    
    Args:
        detections: List of detection results
        
    Returns:
        Dictionary with category counts
    """
    distribution = {}
    
    for detection in detections:
        for category in detection.get('bias_categories', []):
            distribution[category] = distribution.get(category, 0) + 1
    
    return distribution

def calculate_detection_metrics(y_true: List[int], y_pred: List[int]) -> Dict[str, float]:
    """
    Calculate classification metrics for bias detection
    
    Args:
        y_true: True labels (0 = no bias, 1 = bias)
        y_pred: Predicted labels
        
    Returns:
        Dictionary with precision, recall, f1, and accuracy
    """
    try:
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        
        # Calculate accuracy
        correct = sum(1 for true, pred in zip(y_true, y_pred) if true == pred)
        accuracy = correct / len(y_true) if y_true else 0
        
        # Confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        
        return {
            'precision': round(precision, 3),
            'recall': round(recall, 3),
            'f1_score': round(f1, 3),
            'accuracy': round(accuracy, 3),
            'confusion_matrix': cm.tolist()
        }
    except Exception as e:
        return {
            'error': str(e),
            'precision': 0,
            'recall': 0,
            'f1_score': 0,
            'accuracy': 0
        }

def calculate_bias_density(text_length: int, bias_count: int) -> float:
    """
    Calculate bias density (bias instances per 100 words)
    
    Args:
        text_length: Length of text in words
        bias_count: Number of biased instances detected
        
    Returns:
        Bias density score
    """
    if text_length == 0:
        return 0.0
    
    return round((bias_count / text_length) * 100, 2)

def aggregate_scores(scores_list: List[Dict[str, float]]) -> Dict[str, float]:
    """
    Aggregate bias scores from multiple analyses
    
    Args:
        scores_list: List of score dictionaries
        
    Returns:
        Aggregated average scores per category
    """
    if not scores_list:
        return {}
    
    # Get all unique categories
    all_categories = set()
    for scores in scores_list:
        all_categories.update(scores.keys())
    
    # Calculate averages
    aggregated = {}
    for category in all_categories:
        values = [scores.get(category, 0) for scores in scores_list]
        aggregated[category] = round(np.mean(values), 3)
    
    return aggregated

def calculate_confidence_interval(scores: List[float], confidence: float = 0.95) -> tuple:
    """
    Calculate confidence interval for a list of scores
    
    Args:
        scores: List of numerical scores
        confidence: Confidence level (default 0.95)
        
    Returns:
        Tuple of (lower_bound, upper_bound)
    """
    if not scores:
        return (0, 0)
    
    mean = np.mean(scores)
    std = np.std(scores)
    n = len(scores)
    
    # Calculate margin of error
    z_score = 1.96 if confidence == 0.95 else 2.576  # for 95% or 99%
    margin = z_score * (std / np.sqrt(n))
    
    return (round(mean - margin, 3), round(mean + margin, 3))
