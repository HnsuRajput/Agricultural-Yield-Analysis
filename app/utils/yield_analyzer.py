import numpy as np
from sklearn.linear_model import LinearRegression
from app.utils.helpers import get_trend_direction

class YieldAnalyzer:
    """
    Class for analyzing agricultural yield data
    """
    
    def __init__(self, data_processor):
        """
        Initialize the yield analyzer
        
        Args:
            data_processor: DataProcessor instance
        """
        self.data_processor = data_processor
        
    def get_regional_insights(self, region, crop=None):
        """
        Get comprehensive insights for a specific region
        
        Args:
            region (str): Agro-climatic zone
            crop (str, optional): Crop name
            
        Returns:
            dict: Regional insights
        """
        # Filter data for the region
        data = self.data_processor.data
        region_data = data[data['Agro-Climatic Zone'] == region]
        
        if crop:
            region_data = region_data[region_data['Crop'] == crop]
            
        if len(region_data) == 0:
            return {
                "error": f"No data available for region {region}"
            }
            
        # Calculate average yield
        avg_yield = region_data['Yield (tonnes/ha)'].mean()
        
        # Calculate yield trend
        yield_by_year = region_data.groupby('Year')['Yield (tonnes/ha)'].mean().reset_index()
        trend_direction = get_trend_direction(yield_by_year['Yield (tonnes/ha)'].tolist())
        
        # Get top performing crops
        top_crops = region_data.groupby('Crop')['Yield (tonnes/ha)'].mean().sort_values(ascending=False).head(3)
        
        # Get correlation with factors
        corr_matrix = self.data_processor.get_correlation_matrix(region=region, crop=crop)
        factor_impact = self.data_processor.get_factor_impact(region=region, crop=crop)
        
        # Compile insights
        insights = {
            "region": region,
            "average_yield": round(avg_yield, 2),
            "yield_trend": trend_direction,
            "top_crops": top_crops.index.tolist(),
            "factor_impact": {k: round(v, 2) for k, v in factor_impact.items()}
        }
        
        return insights
    
    def get_crop_insights(self, crop, region=None):
        """
        Get comprehensive insights for a specific crop
        
        Args:
            crop (str): Crop name
            region (str, optional): Agro-climatic zone
            
        Returns:
            dict: Crop insights
        """
        # Filter data for the crop
        data = self.data_processor.data
        crop_data = data[data['Crop'] == crop]
        
        if region:
            crop_data = crop_data[crop_data['Agro-Climatic Zone'] == region]
            
        if len(crop_data) == 0:
            return {
                "error": f"No data available for crop {crop}"
            }
            
        # Calculate average yield
        avg_yield = crop_data['Yield (tonnes/ha)'].mean()
        
        # Calculate yield trend
        yield_by_year = crop_data.groupby('Year')['Yield (tonnes/ha)'].mean().reset_index()
        trend_direction = get_trend_direction(yield_by_year['Yield (tonnes/ha)'].tolist())
        
        # Get top performing regions
        top_regions = crop_data.groupby('Agro-Climatic Zone')['Yield (tonnes/ha)'].mean().sort_values(ascending=False).head(3)
        
        # Get correlation with factors
        corr_matrix = self.data_processor.get_correlation_matrix(region=region, crop=crop)
        factor_impact = self.data_processor.get_factor_impact(region=region, crop=crop)
        
        # Compile insights
        insights = {
            "crop": crop,
            "average_yield": round(avg_yield, 2),
            "yield_trend": trend_direction,
            "top_regions": top_regions.index.tolist(),
            "factor_impact": {k: round(v, 2) for k, v in factor_impact.items()}
        }
        
        return insights
    
    def predict_yield(self, region, crop, rainfall, irrigation, fertilizer):
        """
        Predict yield based on input parameters
        
        Args:
            region (str): Agro-climatic zone
            crop (str): Crop name
            rainfall (float): Rainfall in mm
            irrigation (float): Irrigation percentage
            fertilizer (float): Fertilizer in kg/ha
            
        Returns:
            float: Predicted yield in tonnes/ha
        """
        # Filter data for the region and crop
        data = self.data_processor.data
        filtered_data = data[(data['Agro-Climatic Zone'] == region) & (data['Crop'] == crop)]
        
        if len(filtered_data) < 5:
            return None  # Not enough data for prediction
            
        # Prepare features and target
        X = filtered_data[['Rainfall (mm)', 'Irrigation (%)', 'Fertilizer (kg/ha)']]
        y = filtered_data['Yield (tonnes/ha)']
        
        # Train a simple linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Make prediction
        prediction = model.predict([[rainfall, irrigation, fertilizer]])[0]
        
        return round(max(0.1, prediction), 2)
    
    def get_improvement_strategies(self, region, crop):
        """
        Get strategies to improve yield
        
        Args:
            region (str): Agro-climatic zone
            crop (str): Crop name
            
        Returns:
            list: List of improvement strategies
        """
        # Filter data for the region and crop
        data = self.data_processor.data
        filtered_data = data[(data['Agro-Climatic Zone'] == region) & (data['Crop'] == crop)]
        
        if len(filtered_data) == 0:
            return []
            
        # Get factor impact
        factor_impact = self.data_processor.get_factor_impact(region=region, crop=crop)
        
        # Current average values
        avg_rainfall = filtered_data['Rainfall (mm)'].mean()
        avg_irrigation = filtered_data['Irrigation (%)'].mean()
        avg_fertilizer = filtered_data['Fertilizer (kg/ha)'].mean()
        
        # Generate strategies based on factor impact
        strategies = []
        
        if factor_impact.get('Rainfall (mm)', 0) > 0.3:
            strategies.append({
                "factor": "Rainfall",
                "impact": "High",
                "current_value": round(avg_rainfall, 1),
                "recommendation": "Consider water harvesting techniques to utilize rainfall effectively."
            })
            
        if factor_impact.get('Irrigation (%)', 0) > 0.3:
            strategies.append({
                "factor": "Irrigation",
                "impact": "High",
                "current_value": round(avg_irrigation, 1),
                "recommendation": "Increase irrigation coverage or efficiency through drip irrigation."
            })
            
        if factor_impact.get('Fertilizer (kg/ha)', 0) > 0.3:
            strategies.append({
                "factor": "Fertilizer",
                "impact": "High",
                "current_value": round(avg_fertilizer, 1),
                "recommendation": "Optimize fertilizer application based on soil testing."
            })
            
        return strategies 