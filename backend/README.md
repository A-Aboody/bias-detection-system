# Backend API

FastAPI backend for bias detection.

## Setup

**Prerequisites:** Python 3.8+

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt')"
```

3. Run the server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Access at http://localhost:8000

**API Docs:** http://localhost:8000/docs

## API Endpoints

**POST /api/v1/detect** - Quick bias detection
```json
{
  "text": "Your text here",
  "categories": ["gender", "race"]  // optional
}
```

**POST /api/v1/analyze** - Comprehensive analysis with statistics

**GET /api/v1/categories** - List available categories

**GET /api/v1/health** - Health check

## Detection

The system detects 6 bias categories using lexicon-based pattern matching:
- Gender, Race, Religion, Political, Socioeconomic, Age

Severity levels: Mild (0-0.35), Moderate (0.35-0.65), Severe (0.65-1.0)

## Testing

```bash
pytest
```
