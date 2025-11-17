from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import detection
import os

app = FastAPI(
    title="Bias Detection API",
    description="API for detecting bias in AI-generated text",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(detection.router, prefix="/api/v1", tags=["detection"])

@app.get("/")
async def root():
    return {
        "message": "Bias Detection API",
        "version": "1.0.0",
        "endpoints": {
            "detect": "/api/v1/detect",
            "analyze": "/api/v1/analyze",
            "health": "/api/v1/health"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
