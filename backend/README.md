# Bias Detection System - Backend

FastAPI-based backend for detecting bias in AI-generated text.

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download NLTK data:
```python
python -c "import nltk; nltk.download('punkt')"
```

### Running the Server

Start the development server:
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Health Check
```
GET /health
```

### Detect Bias
```
POST /api/v1/detect
Content-Type: application/json

{
  "text": "Your text here",
  "categories": ["gender", "race"]  // optional
}
```

**Response:**
```json
{
  "text": "Your text here",
  "has_bias": true,
  "bias_categories": ["gender"],
  "bias_scores": {
    "gender": 0.6
  },
  "severity": "moderate",
  "overall_score": 0.6,
  "highlights": [
    {
      "term": "example",
      "category": "gender",
      "start": 10,
      "end": 17
    }
  ],
  "timestamp": "2025-11-16T10:30:00"
}
```

### Comprehensive Analysis
```
POST /api/v1/analyze
Content-Type: application/json

{
  "text": "Your text here",
  "model_name": "distilbert-base-uncased"  // optional
}
```

### Get Available Categories
```
GET /api/v1/categories
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models/
│   │   ├── __init__.py
│   │   └── bias_detector.py    # Bias detection model
│   ├── routes/
│   │   ├── __init__.py
│   │   └── detection.py        # API routes
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── text_processing.py  # Text utilities
│   │   └── metrics.py          # Metric calculations
│   └── data/
│       └── bias_lexicons.json  # Bias lexicons
├── requirements.txt
├── .env
└── README.md
```

## Bias Detection Methods

### Lexicon-Based Detection
Uses predefined lexicons of biased terms and patterns to identify:
- Gender bias
- Racial bias
- Religious bias
- Political bias
- Socioeconomic bias
- Age bias

### Scoring System
- **Mild**: 0.0 - 0.3
- **Moderate**: 0.3 - 0.6
- **Severe**: 0.6 - 1.0

## Development

### Adding New Bias Categories

Edit `app/data/bias_lexicons.json` to add new categories:
```json
{
  "new_category": {
    "terms": ["term1", "term2"],
    "stereotypes": ["stereotype1"]
  }
}
```

Then add detection logic in `app/models/bias_detector.py`.

### Testing

```bash
# Install pytest
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

## Team Assignments

- **Abdula Ameen**: Backend development, API implementation, model integration
- **Ali Zahr**: Frontend development
- **Chance Inosencio**: Model training and evaluation
- **Ghina Albabbili**: Documentation and analysis

## License

MIT License
