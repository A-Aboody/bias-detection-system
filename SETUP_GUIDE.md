# Bias Detection System - Setup Guide

## 📋 Complete File Structure

```
bias-detection-system/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                     # FastAPI application entry point
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   └── bias_detector.py        # Bias detection model class
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── detection.py            # API route handlers
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── text_processing.py      # Text utilities
│   │   │   └── metrics.py              # Metric calculations
│   │   └── data/
│   │       └── bias_lexicons.json      # Bias term lexicons
│   ├── requirements.txt                # Python dependencies
│   ├── .env                            # Backend configuration
│   └── README.md                       # Backend documentation
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx              # App header component
│   │   │   ├── BiasAnalyzer.jsx        # Main analysis interface
│   │   │   └── ResultsDisplay.jsx      # Results visualization
│   │   ├── services/
│   │   │   └── api.js                  # API client service
│   │   ├── App.jsx                     # Main app component
│   │   ├── main.jsx                    # React entry point
│   │   └── index.css                   # Global styles
│   ├── public/                         # Static assets
│   ├── index.html                      # HTML template
│   ├── package.json                    # Node dependencies
│   ├── vite.config.js                  # Vite configuration
│   ├── tailwind.config.js              # Tailwind CSS config
│   ├── postcss.config.js               # PostCSS config
│   ├── .env                            # Frontend configuration
│   └── README.md                       # Frontend documentation
│
├── notebooks/
│   └── dataset_exploration.ipynb       # Jupyter notebook for data exploration
│
├── data/
│   ├── raw/                            # Raw datasets
│   ├── processed/                      # Processed data
│   └── results/                        # Analysis results
│
├── .gitignore                          # Git ignore rules
└── README.md                           # Main project documentation
```

## 🚀 Step-by-Step Setup Instructions

### Step 1: Extract the Project

Extract the `bias-detection-system` folder to your desired location.

### Step 2: Backend Setup

1. **Open Terminal/Command Prompt** and navigate to the backend directory:
   ```bash
   cd bias-detection-system/backend
   ```

2. **Create a Python virtual environment**:
   ```bash
   # On Windows:
   python -m venv venv
   venv\Scripts\activate

   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download NLTK data**:
   ```bash
   python -c "import nltk; nltk.download('punkt')"
   ```

5. **Verify the backend works**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   You should see:
   ```
   INFO:     Uvicorn running on http://0.0.0.0:8000
   INFO:     Application startup complete.
   ```

6. **Test the API** by visiting:
   - http://localhost:8000 (API root)
   - http://localhost:8000/docs (Swagger UI)

### Step 3: Frontend Setup

1. **Open a NEW Terminal/Command Prompt** (keep the backend running!) and navigate to the frontend:
   ```bash
   cd bias-detection-system/frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```
   
   This might take a few minutes.

3. **Start the development server**:
   ```bash
   npm run dev
   ```
   
   You should see:
   ```
   VITE v5.0.0  ready in XXX ms
   
   ➜  Local:   http://localhost:5173/
   ➜  Network: use --host to expose
   ```

4. **Open your browser** and go to: http://localhost:5173

### Step 4: Test the System

1. You should see the Bias Detection System interface
2. Try the example texts or enter your own
3. Click "Analyze" to see the results
4. Toggle between "Quick" and "Detailed" analysis modes

## 🔧 Configuration

### Backend Configuration (backend/.env)
```
PORT=8000
HOST=0.0.0.0
DEBUG=True
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
DEFAULT_MODEL=distilbert-base-uncased
MAX_TEXT_LENGTH=10000
```

### Frontend Configuration (frontend/.env)
```
VITE_API_URL=http://localhost:8000
```

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📊 Working with the BEADs Dataset

### In Jupyter Notebook

1. **Install Jupyter** (if not already installed):
   ```bash
   pip install jupyter
   ```

2. **Start Jupyter**:
   ```bash
   cd notebooks
   jupyter notebook
   ```

3. **Open** `dataset_exploration.ipynb`

4. **Run the cells** to explore the BEADs dataset

### In Python Script

```python
from datasets import load_dataset

# Load BEADs dataset
dataset = load_dataset("shainar/BEAD")

# Explore the data
print(dataset)
for example in dataset['train'][:5]:
    print(example)
```

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**: Make sure you activated the virtual environment and ran `pip install -r requirements.txt`

**Problem**: Port 8000 already in use
**Solution**: 
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Frontend Issues

**Problem**: `npm install` fails
**Solution**: 
1. Delete `node_modules` and `package-lock.json`
2. Run `npm install` again

**Problem**: Port 5173 already in use
**Solution**: Edit `vite.config.js` and change the port:
```javascript
server: {
  port: 5174,  // Change to different port
  ...
}
```

**Problem**: Backend connection error
**Solution**: 
1. Make sure backend is running at http://localhost:8000
2. Check `.env` file has correct `VITE_API_URL`
3. Clear browser cache and reload

### Dataset Issues

**Problem**: BEADs dataset download fails
**Solution**:
```bash
# Try with cache disabled
from datasets import load_dataset
dataset = load_dataset("shainar/BEAD", download_mode="force_redownload")
```

## 🎯 Next Steps for Development

### For Abdula (Backend):
1. ✅ Backend structure is ready
2. Test all API endpoints with sample data
3. Integrate BEADs dataset loading
4. Add database for storing analysis history (optional)
5. Implement batch processing endpoint

### For Ali (Frontend):
1. ✅ Frontend structure is ready
2. Test UI with various text inputs
3. Add file upload feature
4. Improve mobile responsiveness
5. Add export functionality (CSV/JSON)

### For Chance (ML/Models):
1. Run `dataset_exploration.ipynb` notebook
2. Fine-tune transformer models on BEADs
3. Evaluate model performance
4. Integrate trained models into backend
5. Create model comparison functionality

### For Ghina (Documentation):
1. ✅ Initial documentation is ready
2. Document API endpoints with examples
3. Create user guide with screenshots
4. Prepare presentation slides
5. Write analysis report

## 📚 Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **React Documentation**: https://react.dev/
- **Vite Documentation**: https://vitejs.dev/
- **TailwindCSS**: https://tailwindcss.com/
- **Hugging Face Datasets**: https://huggingface.co/docs/datasets/
- **BEADs Paper**: https://arxiv.org/abs/2406.04220

## 💡 Tips

1. **Always keep both backend and frontend running** during development
2. **Use two terminal windows** - one for backend, one for frontend
3. **Check browser console** (F12) for frontend errors
4. **Check terminal output** for backend errors
5. **Save your work frequently** and commit to Git regularly

## 🤝 Team Collaboration

### Git Workflow
```bash
# Initial setup (done once)
git init
git remote add origin <your-repo-url>

# Regular workflow
git pull origin main              # Get latest changes
git checkout -b feature-name      # Create feature branch
# Make your changes
git add .
git commit -m "Description"
git push origin feature-name      # Push your branch
# Create pull request on GitHub
```

### Branch Naming Convention
- `backend/feature-name` - Backend features
- `frontend/feature-name` - Frontend features
- `ml/feature-name` - ML/model features
- `docs/feature-name` - Documentation

## ✅ Verification Checklist

Before considering setup complete, verify:

- [ ] Backend starts without errors at http://localhost:8000
- [ ] API documentation accessible at http://localhost:8000/docs
- [ ] Frontend starts without errors at http://localhost:5173
- [ ] Sample text analysis works correctly
- [ ] Both "Quick" and "Detailed" modes function
- [ ] Text highlighting displays properly
- [ ] No console errors in browser (F12)
- [ ] BEADs dataset can be loaded in notebook
- [ ] All team members can run the project

## 📞 Support

If you encounter issues:
1. Check this setup guide carefully
2. Review the troubleshooting section
3. Check the individual README files (backend/README.md, frontend/README.md)
4. Ask team members in your group chat

---

**Happy coding! 🚀**
