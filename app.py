# Main application file
# Import the Flask app from the app package
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Optional, List, Dict, Any
import json
import os

# Import our custom modules
from app.models.data_processor import DataProcessor
from app.models.yield_analyzer import YieldAnalyzer
from app.api.routes import setup_routes

# Initialize FastAPI app
app = FastAPI(
    title="Indian Agricultural Yield Analysis",
    description="Analyze crop yield variability across Indian agro-climatic zones",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Load the data processor and analyzer
data_processor = DataProcessor('app/data/crop_yield_dataset.csv')
yield_analyzer = YieldAnalyzer(data_processor)

# Set up API routes
setup_routes(app, data_processor, yield_analyzer)

# Main routes
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main dashboard page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/regions", response_model=List[str])
async def get_regions():
    """Get all unique agro-climatic zones"""
    regions = data_processor.get_unique_values('Agro-Climatic Zone')
    return regions

@app.get("/crops", response_model=List[str])
async def get_crops():
    """Get all unique crops"""
    crops = data_processor.get_unique_values('Crop')
    return crops

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 