# app package initialization
# This file is intentionally empty to make the directory a Python package 

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

# Create FastAPI app instance
app = FastAPI(title="Indian Agricultural Yield Analysis", 
              description="API for analyzing crop yield data across Indian agro-climatic zones")

# Keep the basic endpoints
@app.get("/api")
async def api_root():
    return {"message": "Welcome to the Indian Agricultural Yield Analysis API"}

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"}

# Import data processor and yield analyzer
from app.utils.data_processor import DataProcessor
from app.utils.yield_analyzer import YieldAnalyzer

# Initialize data processor and analyzer
data_processor = DataProcessor()
yield_analyzer = YieldAnalyzer(data_processor)

# Setup API routes
from app.api.routes import setup_routes
setup_routes(app, data_processor, yield_analyzer)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="app/templates")

# Import routes for serving HTML pages
from app.views import setup_views
setup_views(app, templates) 