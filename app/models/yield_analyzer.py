import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

class YieldAnalyzer:
    """
    Class for analyzing crop yield and providing insights
    """
    
    def __init__(self, data_processor):
        """
        Initialize the YieldAnalyzer with a DataProcessor
        
        Args:
            data_processor: DataProcessor instance
        """
        self.data_processor = data_processor
        self.models = {}
        
    def get_regional_insights(self, region, crop=None):
        """
        Get comprehensive insights for a specific region
        
        Args:
            region (str): Agro-climatic zone
            crop (str, optional): Specific crop to analyze
            
        Returns:
            dict: Dictionary containing regional insights
        """
        insights = {
            'region': region,
            'crop': crop if crop else 'All crops',
            'yield_trend': None,
            'factor_impact': None,
            'recommendations': []
        }
        
        # Get yield trend
        trend_data = self.data_processor.get_yield_trend(region=region, crop=crop)
        if not trend_data.empty:
            insights['yield_trend'] = trend_data.to_dict(orient='records')
            
            # Analyze trend
            if len(trend_data) > 2:
                first_year = trend_data.iloc[0]['Year']
                last_year = trend_data.iloc[-1]['Year']
                first_yield = trend_data.iloc[0]['Average Yield']
                last_yield = trend_data.iloc[-1]['Average Yield']
                
                if last_yield > first_yield:
                    insights['trend_analysis'] = f"Yield has increased by {(last_yield - first_yield):.2f} units from {first_year} to {last_year}."
                    insights['recommendations'].append("Continue with current agricultural practices that have led to yield improvements.")
                else:
                    insights['trend_analysis'] = f"Yield has decreased by {(first_yield - last_yield):.2f} units from {first_year} to {last_year}."
                    insights['recommendations'].append("Review agricultural practices as yields are declining over time.")
        
        # Get factor impact
        factor_impact = self.data_processor.get_factor_impact(region=region, crop=crop)
        if factor_impact:
            insights['factor_impact'] = factor_impact
            
            # Generate recommendations based on factors
            top_factor = max(factor_impact, key=factor_impact.get)
            if top_factor == 'Rainfall (mm)':
                insights['recommendations'].append("Focus on water management strategies as rainfall has the highest impact on yield.")
                if crop:
                    insights['recommendations'].append(f"Consider drought-resistant varieties of {crop} for this region.")
            elif top_factor == 'Irrigation (%)':
                insights['recommendations'].append("Improve irrigation infrastructure as it significantly impacts crop yield.")
                insights['recommendations'].append("Consider drip irrigation or micro-irrigation techniques for efficient water use.")
            elif top_factor == 'Fertilizer Use (kg/ha)':
                insights['recommendations'].append("Optimize fertilizer application as it has the highest impact on yield.")
                insights['recommendations'].append("Consider soil testing to determine precise nutrient requirements.")
        
        # Get soil type analysis
        filters = {'Agro-Climatic Zone': region}
        if crop:
            filters['Crop'] = crop
            
        filtered_df = self.data_processor.filter_data(filters)
        
        if not filtered_df.empty:
            soil_analysis = filtered_df.groupby('Soil Type')[self.data_processor.target_column].mean().sort_values(ascending=False)
            
            if not soil_analysis.empty:
                best_soil = soil_analysis.index[0]
                insights['soil_analysis'] = f"The best soil type for {'this crop' if crop else 'crops'} in this region is {best_soil}."
                insights['recommendations'].append(f"Prioritize cultivation in {best_soil} soil areas for optimal yields.")
        
        return insights
    
    def get_crop_insights(self, crop, region=None):
        """
        Get comprehensive insights for a specific crop
        
        Args:
            crop (str): Crop name
            region (str, optional): Specific region to analyze
            
        Returns:
            dict: Dictionary containing crop insights
        """
        insights = {
            'crop': crop,
            'region': region if region else 'All regions',
            'yield_by_region': None,
            'factor_impact': None,
            'recommendations': []
        }
        
        # Get yield by region
        if not region:
            region_data = self.data_processor.get_yield_by_region(crop=crop)
            if not region_data.empty:
                insights['yield_by_region'] = region_data.to_dict(orient='records')
                
                # Find best and worst regions
                best_region = region_data.iloc[0]['Region']
                worst_region = region_data.iloc[-1]['Region']
                insights['region_analysis'] = f"Best region for {crop} is {best_region}, worst region is {worst_region}."
                insights['recommendations'].append(f"Prioritize {crop} cultivation in {best_region} region.")
        
        # Get factor impact
        factor_impact = self.data_processor.get_factor_impact(region=region, crop=crop)
        if factor_impact:
            insights['factor_impact'] = factor_impact
            
            # Generate recommendations based on factors
            sorted_factors = sorted(factor_impact.items(), key=lambda x: x[1], reverse=True)
            insights['factor_analysis'] = f"The most important factors for {crop} yield are: {sorted_factors[0][0]} ({sorted_factors[0][1]:.1f}%) and {sorted_factors[1][0]} ({sorted_factors[1][1]:.1f}%)."
            
            # Add specific recommendations
            if sorted_factors[0][0] == 'Rainfall (mm)':
                insights['recommendations'].append(f"Ensure adequate water supply for {crop} as it is highly sensitive to rainfall.")
            elif sorted_factors[0][0] == 'Irrigation (%)':
                insights['recommendations'].append(f"Invest in irrigation infrastructure for {crop} cultivation.")
            elif sorted_factors[0][0] == 'Fertilizer Use (kg/ha)':
                insights['recommendations'].append(f"Optimize fertilizer application for {crop} based on soil testing.")
        
        # Get seasonal analysis
        filters = {'Crop': crop}
        if region:
            filters['Agro-Climatic Zone'] = region
            
        filtered_df = self.data_processor.filter_data(filters)
        
        if not filtered_df.empty:
            season_analysis = filtered_df.groupby('Season')[self.data_processor.target_column].mean().sort_values(ascending=False)
            
            if not season_analysis.empty:
                best_season = season_analysis.index[0]
                insights['season_analysis'] = f"The best season for {crop} cultivation is {best_season}."
                insights['recommendations'].append(f"Prioritize {crop} cultivation in {best_season} season.")
        
        return insights
    
    def predict_yield(self, region, crop, rainfall, irrigation, fertilizer):
        """
        Predict yield based on input parameters
        
        Args:
            region (str): Agro-climatic zone
            crop (str): Crop name
            rainfall (float): Rainfall in mm
            irrigation (float): Irrigation percentage
            fertilizer (float): Fertilizer use in kg/ha
            
        Returns:
            float: Predicted yield
        """
        # Create model key
        model_key = f"{region}_{crop}"
        
        # Check if model exists, if not train it
        if model_key not in self.models:
            self._train_model(region, crop)
        
        # If model training failed, return None
        if model_key not in self.models:
            return None
        
        # Prepare input features
        features = np.array([[rainfall, irrigation, fertilizer]])
        
        # Predict yield
        model, scaler = self.models[model_key]
        if scaler:
            features = scaler.transform(features)
            
        predicted_yield = model.predict(features)[0]
        
        return max(0, predicted_yield)
    
    def _train_model(self, region, crop):
        """
        Train a yield prediction model for a specific region and crop
        
        Args:
            region (str): Agro-climatic zone
            crop (str): Crop name
        """
        # Filter data
        filters = {
            'Agro-Climatic Zone': region,
            'Crop': crop
        }
        
        filtered_df = self.data_processor.filter_data(filters)
        
        # Check if we have enough data
        if len(filtered_df) < 10:
            return
        
        # Prepare features and target
        X = filtered_df[self.data_processor.feature_columns].values
        y = filtered_df[self.data_processor.target_column].values
        
        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train model
        if len(filtered_df) >= 50:
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            model = LinearRegression()
            
        model.fit(X_scaled, y)
        
        # Save model
        model_key = f"{region}_{crop}"
        self.models[model_key] = (model, scaler)
        
    def get_improvement_strategies(self, region, crop):
        """
        Get strategies to improve yield for a specific region and crop
        
        Args:
            region (str): Agro-climatic zone
            crop (str): Crop name
            
        Returns:
            list: List of improvement strategies
        """
        strategies = []
        
        # Get factor impact
        factor_impact = self.data_processor.get_factor_impact(region=region, crop=crop)
        
        if not factor_impact:
            return ["Insufficient data to generate improvement strategies."]
        
        # Sort factors by impact
        sorted_factors = sorted(factor_impact.items(), key=lambda x: x[1], reverse=True)
        
        # Generate strategies based on top factors
        for factor, impact in sorted_factors:
            if factor == 'Rainfall (mm)':
                strategies.append({
                    'factor': 'Rainfall',
                    'impact': f"{impact:.1f}%",
                    'strategies': [
                        "Implement rainwater harvesting systems",
                        "Use drought-resistant crop varieties",
                        "Apply mulching to conserve soil moisture",
                        "Construct farm ponds for water storage"
                    ]
                })
            elif factor == 'Irrigation (%)':
                strategies.append({
                    'factor': 'Irrigation',
                    'impact': f"{impact:.1f}%",
                    'strategies': [
                        "Install drip irrigation systems",
                        "Implement precision irrigation scheduling",
                        "Use soil moisture sensors for efficient water use",
                        "Adopt micro-irrigation techniques"
                    ]
                })
            elif factor == 'Fertilizer Use (kg/ha)':
                strategies.append({
                    'factor': 'Fertilizer',
                    'impact': f"{impact:.1f}%",
                    'strategies': [
                        "Conduct soil testing before fertilizer application",
                        "Use balanced NPK fertilizers based on crop requirements",
                        "Apply organic manures to improve soil health",
                        "Adopt precision fertilizer application techniques"
                    ]
                })
        
        # Add general strategies
        strategies.append({
            'factor': 'General',
            'impact': 'Variable',
            'strategies': [
                "Implement crop rotation to maintain soil fertility",
                "Use integrated pest management techniques",
                "Adopt conservation tillage practices",
                "Use quality seeds of improved varieties"
            ]
        })
        
        return strategies 