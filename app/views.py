from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

def setup_views(app, templates):
    """
    Set up routes for serving HTML pages
    
    Args:
        app: FastAPI application
        templates: Jinja2Templates instance
    """
    
    @app.get("/", response_class=HTMLResponse)
    async def index(request: Request):
        """Serve the main dashboard page"""
        return templates.TemplateResponse("index.html", {"request": request}) 