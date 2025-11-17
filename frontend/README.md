# Bias Detection System - Frontend

React-based frontend for the Bias Detection System, providing an intuitive interface for analyzing text bias.

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **TailwindCSS** - Utility-first CSS framework
- **Axios** - HTTP client
- **Lucide React** - Icon library

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create `.env` file (if not exists):
```bash
echo "VITE_API_URL=http://localhost:8000" > .env
```

### Running the Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

### Preview Production Build

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx           # App header
│   │   ├── BiasAnalyzer.jsx     # Main analysis component
│   │   └── ResultsDisplay.jsx   # Results visualization
│   ├── services/
│   │   └── api.js               # API client
│   ├── App.jsx                  # Main app component
│   ├── main.jsx                 # Entry point
│   └── index.css                # Global styles
├── public/                      # Static assets
├── index.html                   # HTML template
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Features

### Two Analysis Modes

1. **Quick Detection**
   - Fast lexicon-based analysis
   - Immediate results
   - Basic bias categories

2. **Detailed Analysis**
   - Comprehensive bias analysis
   - Text statistics
   - Actionable recommendations
   - Detailed metrics

### Bias Categories Detected

- 🚺 **Gender** - Gender stereotypes and imbalances
- 🌍 **Race** - Racial and ethnic bias
- ⛪ **Religion** - Religious bias and stereotypes
- 🗳️ **Political** - Political bias and loaded language
- 💰 **Socioeconomic** - Class-based stereotypes
- 👴 **Age** - Age-related bias

### Key Components

#### BiasAnalyzer
Main component for text input and analysis control:
- Text input area
- Example texts
- Analysis mode toggle
- Real-time character count
- Error handling

#### ResultsDisplay
Visualizes analysis results:
- Overall bias status
- Severity indicators
- Category breakdown
- Text highlighting
- Score visualizations
- Recommendations

#### Header
Application header with branding and status indicator.

## API Integration

The frontend communicates with the backend API through the `services/api.js` module:

### Endpoints Used

```javascript
// Detect bias
POST /api/v1/detect
{
  "text": "string",
  "categories": ["gender", "race"] // optional
}

// Comprehensive analysis
POST /api/v1/analyze
{
  "text": "string",
  "model_name": "string" // optional
}

// Get categories
GET /api/v1/categories

// Health check
GET /api/v1/health
```

## Styling

### TailwindCSS Configuration

Custom colors defined in `tailwind.config.js`:
- Primary (blue shades)
- Danger (red shades)
- Warning (yellow shades)
- Success (green shades)

### Custom Animations

- Fade-in effect for results
- Highlight hover effects
- Loading spinners
- Smooth transitions

## Error Handling

The application handles various error states:
- Backend connection errors
- API request failures
- Invalid input handling
- Empty text validation

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Development Tips

### Hot Reload
Vite provides instant hot module replacement (HMR) during development.

### Component Development
Each component is self-contained with its own logic and styling.

### Adding New Features
1. Create new component in `src/components/`
2. Add API method in `src/services/api.js`
3. Import and use in `App.jsx` or other components

## Team Assignments

- **Ali Zahr**: Frontend development, UI/UX design
- **Abdula Ameen**: Backend integration, API client
- **Chance Inosencio**: Model integration support
- **Ghina Albabbili**: Documentation, content

## Troubleshooting

### Backend Connection Issues
Ensure the backend is running at `http://localhost:8000`. Check the `.env` file for correct API URL.

### Build Errors
Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

### Port Already in Use
Change the port in `vite.config.js` or kill the process using port 5173.

## License

MIT License
