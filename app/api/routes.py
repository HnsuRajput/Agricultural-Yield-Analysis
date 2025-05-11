from fastapi import APIRouter, Query, HTTPException, Body
from fastapi.responses import JSONResponse
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

class YieldPredictionInput(BaseModel):
    region: str
    crop: str
    rainfall: float
    irrigation: float
    fertilizer: float

def setup_routes(app, data_processor, yield_analyzer):
    """
    Set up all API routes
    
    Args:
        app: FastAPI application
        data_processor: DataProcessor instance
        yield_analyzer: YieldAnalyzer instance
    """
    
    @app.get("/api/regions", response_model=List[str])
    async def api_regions():
        """Get all unique agro-climatic zones"""
        regions = data_processor.get_unique_values('Agro-Climatic Zone')
        return regions
    
    @app.get("/api/crops", response_model=List[str])
    async def api_crops():
        """Get all unique crops"""
        crops = data_processor.get_unique_values('Crop')
        return crops
    
    @app.get("/api/soil-types", response_model=List[str])
    async def api_soil_types():
        """Get all unique soil types"""
        soil_types = data_processor.get_unique_values('Soil Type')
        return soil_types
    
    @app.get("/api/seasons", response_model=List[str])
    async def api_seasons():
        """Get all unique seasons"""
        seasons = data_processor.get_unique_values('Season')
        return seasons
    
    @app.get("/api/yield-by-region", response_model=List[Dict[str, Any]])
    async def api_yield_by_region(crop: Optional[str] = None):
        """Get average yield by region"""
        data = data_processor.get_yield_by_region(crop=crop)
        return data.to_dict(orient='records')
    
    @app.get("/api/yield-by-factor", response_model=List[Dict[str, Any]])
    async def api_yield_by_factor(
        factor: str = Query(..., description="Factor to group by"),
        region: Optional[str] = None,
        crop: Optional[str] = None
    ):
        """Get yield data grouped by a specific factor"""
        if not factor:
            raise HTTPException(status_code=400, detail="Factor parameter is required")
        
        try:
            # Check if factor is valid
            valid_factors = list(data_processor.column_mappings.keys()) + list(data_processor.column_mappings.values())
            if factor not in valid_factors:
                return JSONResponse(
                    status_code=400,
                    content={
                        "error": f"Invalid factor: {factor}",
                        "valid_factors": list(data_processor.column_mappings.keys())
                    }
                )
                
            data = data_processor.get_yield_by_factor(factor, region=region, crop=crop)
            return data.to_dict(orient='records')
        except Exception as e:
            return JSONResponse(
                status_code=500,
                content={"error": f"An error occurred: {str(e)}"}
            )
    
    @app.get("/api/yield-trend", response_model=List[Dict[str, Any]])
    async def api_yield_trend(
        region: Optional[str] = None,
        crop: Optional[str] = None
    ):
        """Get yield trend over years"""
        data = data_processor.get_yield_trend(region=region, crop=crop)
        return data.to_dict(orient='records')
    
    @app.get("/api/correlation-matrix", response_model=Dict[str, Dict[str, float]])
    async def api_correlation_matrix(
        region: Optional[str] = None,
        crop: Optional[str] = None
    ):
        """Get correlation matrix between yield and factors"""
        data = data_processor.get_correlation_matrix(region=region, crop=crop)
        return data.to_dict()
    
    @app.get("/api/factor-impact", response_model=Dict[str, float])
    async def api_factor_impact(
        region: Optional[str] = None,
        crop: Optional[str] = None
    ):
        """Get the impact of each factor on yield"""
        data = data_processor.get_factor_impact(region=region, crop=crop)
        return data
    
    @app.get("/api/regional-insights", response_model=Dict[str, Any])
    async def api_regional_insights(
        region: str = Query(..., description="Agro-climatic zone"),
        crop: Optional[str] = None
    ):
        """Get comprehensive insights for a specific region"""
        if not region:
            raise HTTPException(status_code=400, detail="Region parameter is required")
            
        insights = yield_analyzer.get_regional_insights(region, crop=crop)
        return insights
    
    @app.get("/api/crop-insights", response_model=Dict[str, Any])
    async def api_crop_insights(
        crop: str = Query(..., description="Crop name"),
        region: Optional[str] = None
    ):
        """Get comprehensive insights for a specific crop"""
        if not crop:
            raise HTTPException(status_code=400, detail="Crop parameter is required")
            
        insights = yield_analyzer.get_crop_insights(crop, region=region)
        return insights
    
    @app.post("/api/predict-yield", response_model=Dict[str, Any])
    async def api_predict_yield(data: YieldPredictionInput):
        """Predict yield based on input parameters"""
        predicted_yield = yield_analyzer.predict_yield(
            data.region,
            data.crop,
            data.rainfall,
            data.irrigation,
            data.fertilizer
        )
        
        if predicted_yield is None:
            raise HTTPException(status_code=400, detail="Insufficient data to make prediction")
            
        return {
            "predicted_yield": predicted_yield,
            "unit": "tonnes/ha"
        }
    
    @app.get("/api/improvement-strategies", response_model=List[Dict[str, Any]])
    async def api_improvement_strategies(
        region: str = Query(..., description="Agro-climatic zone"),
        crop: str = Query(..., description="Crop name")
    ):
        """Get strategies to improve yield"""
        if not region or not crop:
            raise HTTPException(status_code=400, detail="Both region and crop parameters are required")
            
        strategies = yield_analyzer.get_improvement_strategies(region, crop)
        return strategies 