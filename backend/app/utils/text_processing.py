import re
from typing import List, Dict
import nltk
from collections import Counter

# Download required NLTK data (run once)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

def tokenize_text(text: str) -> List[str]:
    """Tokenize text into words"""
    return re.findall(r'\b\w+\b', text.lower())

def get_sentences(text: str) -> List[str]:
    """Split text into sentences"""
    try:
        return nltk.sent_tokenize(text)
    except:
        # Fallback if NLTK fails
        return re.split(r'[.!?]+', text)

def calculate_text_stats(text: str) -> Dict:
    """Calculate basic statistics about the text"""
    words = tokenize_text(text)
    sentences = get_sentences(text)
    
    return {
        "word_count": len(words),
        "char_count": len(text),
        "sentence_count": len(sentences),
        "avg_word_length": sum(len(word) for word in words) / len(words) if words else 0,
        "avg_sentence_length": len(words) / len(sentences) if sentences else 0
    }

def get_word_frequencies(text: str, top_n: int = 20) -> Dict[str, int]:
    """Get most frequent words in text"""
    words = tokenize_text(text)
    # Filter out common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'was', 'are', 'were'}
    filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
    
    counter = Counter(filtered_words)
    return dict(counter.most_common(top_n))

def clean_text(text: str) -> str:
    """Clean and normalize text"""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep punctuation
    text = re.sub(r'[^\w\s.,!?;:\'-]', '', text)
    return text.strip()

def highlight_terms(text: str, terms: List[str], case_sensitive: bool = False) -> List[Dict]:
    """Find and highlight specific terms in text"""
    highlights = []
    
    for term in terms:
        flags = 0 if case_sensitive else re.IGNORECASE
        pattern = r'\b' + re.escape(term) + r'\b'
        
        for match in re.finditer(pattern, text, flags):
            highlights.append({
                "term": match.group(),
                "start": match.start(),
                "end": match.end(),
                "context": text[max(0, match.start()-30):min(len(text), match.end()+30)]
            })
    
    return sorted(highlights, key=lambda x: x['start'])
