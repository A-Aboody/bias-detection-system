# Frontend

React interface for bias detection system.

## Tech Stack

React 18, Vite, TailwindCSS, Axios

## Setup

**Prerequisites:** Node.js 18+

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Create `.env` file:
```bash
echo "VITE_API_URL=http://localhost:8000" > .env
```

3. Run development server:
```bash
npm run dev
```

Access at http://localhost:5173

## Build

```bash
npm run build
```

Output: `dist/` directory

## Features

**Two Analysis Modes:**
- Quick: Fast detection with highlights
- Detailed: Full analysis with statistics and recommendations

**Category Selection:** Filter specific bias types to check

**Export:** Download results as JSON or text report

**Text Highlighting:** Color-coded biased terms in original text

## Components

**BiasAnalyzer** - Main interface for text input and analysis

**ResultsDisplay** - Shows analysis results with visualizations

**Header** - Application header with status indicator

## API Integration

The app connects to the backend API at `http://localhost:8000` (configurable via `.env`).

Endpoints: `/api/v1/detect`, `/api/v1/analyze`, `/api/v1/categories`, `/api/v1/health`
