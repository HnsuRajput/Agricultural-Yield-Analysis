import pandas as pd
import numpy as np
import os
from app.utils.helpers import calculate_percent_change, get_trend_direction

class DataProcessor:
    """
    Class for processing agricultural yield data
    """
    
    def __init__(self):
        """Initialize the data processor with sample data"""
        # In a real application, this would load data from a database or CSV file
        # For now, we'll create some sample data
        self.data = self._load_sample_data()
        
        # Define column name mappings for API parameters
        self.column_mappings = {
            'Rainfall': 'Rainfall (mm)',
            'Irrigation': 'Irrigation (%)',
            'Fertilizer': 'Fertilizer (kg/ha)',
            'Yield': 'Yield (tonnes/ha)',
            'Year': 'Year',
            'Region': 'Agro-Climatic Zone',
            'Crop': 'Crop',
            'Soil': 'Soil Type',
            'Season': 'Season'
        }
        
    def _load_sample_data(self):
        """Load sample agricultural data"""
        # Check if we have actual data files
        data_path = os.path.join('app', 'data', 'agricultural_data.csv')
        if os.path.exists(data_path):
            return pd.read_csv(data_path)
        
        # Create sample data if no file exists
        regions = ['Northern Plains', 'Eastern Plains', 'Central Plains', 
                  'Western Dry', 'Southern Plains', 'Coastal Region', 'Hill Region']
        crops = ['Rice', 'Wheat', 'Maize', 'Sugarcane', 'Cotton', 'Pulses']
        soil_types = ['Alluvial', 'Black', 'Red', 'Laterite', 'Arid']
        seasons = ['Kharif', 'Rabi', 'Zaid']
        years = list(range(2010, 2023))
        
        # Generate random data
        data_rows = []
        for region in regions:
            for crop in crops:
                for year in years:
                    # Only include some combinations to make data more realistic
                    if np.random.random() > 0.3:
                        rainfall = np.random.normal(900, 300)
                        irrigation = np.random.normal(60, 20)
                        fertilizer = np.random.normal(150, 50)
                        
                        # Make yield dependent on factors
                        base_yield = np.random.normal(3, 1)
                        rainfall_effect = 0.001 * (rainfall - 600)
                        irrigation_effect = 0.01 * irrigation
                        fertilizer_effect = 0.005 * fertilizer
                        
                        yield_value = max(0.5, base_yield + rainfall_effect + 
                                         irrigation_effect + fertilizer_effect)
                        
                        # Add some yearly trends
                        yield_value += (year - 2010) * 0.05 * np.random.normal(1, 0.2)
                        
                        data_rows.append({
                            'Year': year,
                            'Agro-Climatic Zone': region,
                            'Crop': crop,
                            'Soil Type': np.random.choice(soil_types),
                            'Season': np.random.choice(seasons),
                            'Rainfall (mm)': round(rainfall, 1),
                            'Irrigation (%)': round(irrigation, 1),
                            'Fertilizer (kg/ha)': round(fertilizer, 1),
                            'Yield (tonnes/ha)': round(yield_value, 2)
                        })
        
        return pd.DataFrame(data_rows)
    
    def get_unique_values(self, column):
        """Get unique values from a column"""
        return sorted(self.data[column].unique().tolist())
    
    def get_yield_by_region(self, crop=None):
        """Get average yield by region"""
        query = self.data
        if crop:
            query = query[query['Crop'] == crop]
            
        return query.groupby('Agro-Climatic Zone')['Yield (tonnes/ha)'].mean().reset_index()
    
    def get_yield_by_factor(self, factor, region=None, crop=None):
        """Get yield data grouped by a specific factor"""
        query = self.data
        if region:
            query = query[query['Agro-Climatic Zone'] == region]
        if crop:
            query = query[query['Crop'] == crop]
            
        # Map the factor name to the actual column name if needed
        actual_factor = self.column_mappings.get(factor, factor)
        
        # Check if the column exists
        if actual_factor not in query.columns:
            # Return empty result with proper structure
            return pd.DataFrame({actual_factor: [], 'Yield (tonnes/ha)': []})
            
        return query.groupby(actual_factor)['Yield (tonnes/ha)'].mean().reset_index()
    
    def get_yield_trend(self, region=None, crop=None):
        """Get yield trend over years"""
        query = self.data
        if region:
            query = query[query['Agro-Climatic Zone'] == region]
        if crop:
            query = query[query['Crop'] == crop]
            
        return query.groupby('Year')['Yield (tonnes/ha)'].mean().reset_index()
    
    def get_correlation_matrix(self, region=None, crop=None):
        """Get correlation matrix between yield and factors"""
        query = self.data
        if region:
            query = query[query['Agro-Climatic Zone'] == region]
        if crop:
            query = query[query['Crop'] == crop]
            
        numeric_columns = ['Rainfall (mm)', 'Irrigation (%)', 
                          'Fertilizer (kg/ha)', 'Yield (tonnes/ha)']
        return query[numeric_columns].corr()
    
    def get_factor_impact(self, region=None, crop=None):
        """Get the impact of each factor on yield"""
        corr_matrix = self.get_correlation_matrix(region, crop)
        yield_corr = corr_matrix['Yield (tonnes/ha)'].drop('Yield (tonnes/ha)')
        
        # Convert to dictionary
        return yield_corr.to_dict() 