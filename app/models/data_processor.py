import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib
import os

class DataProcessor:
    """
    Class for processing and managing the agricultural yield dataset
    """
    
    def __init__(self, data_path):
        """
        Initialize the DataProcessor with the dataset
        
        Args:
            data_path (str): Path to the CSV dataset
        """
        self.data_path = data_path
        self.df = self._load_data()
        self.feature_columns = ['Rainfall (mm)', 'Irrigation (%)', 'Fertilizer Use (kg/ha)']
        self.target_column = 'crop_yield'
        self.models = {}
        
    def _load_data(self):
        """
        Load the dataset from CSV
        
        Returns:
            pandas.DataFrame: The loaded dataset
        """
        df = pd.read_csv(self.data_path)
        # Basic cleaning
        df = df.dropna()
        return df
    
    def get_unique_values(self, column):
        """
        Get unique values from a column
        
        Args:
            column (str): Column name
            
        Returns:
            list: List of unique values
        """
        return sorted(self.df[column].unique().tolist())
    
    def filter_data(self, filters=None):
        """
        Filter the dataset based on provided filters
        
        Args:
            filters (dict): Dictionary of column-value pairs for filtering
            
        Returns:
            pandas.DataFrame: Filtered dataframe
        """
        if not filters:
            return self.df
            
        filtered_df = self.df.copy()
        
        for column, value in filters.items():
            if value and column in filtered_df.columns:
                filtered_df = filtered_df[filtered_df[column] == value]
                
        return filtered_df
    
    def get_yield_by_region(self, crop=None):
        """
        Get average yield by agro-climatic zone
        
        Args:
            crop (str, optional): Filter by specific crop
            
        Returns:
            pandas.DataFrame: Average yield by region
        """
        filters = {}
        if crop:
            filters['Crop'] = crop
            
        filtered_df = self.filter_data(filters)
        
        region_yield = filtered_df.groupby('Agro-Climatic Zone')[self.target_column].agg(['mean', 'std', 'count']).reset_index()
        region_yield.columns = ['Region', 'Average Yield', 'Std Dev', 'Sample Count']
        
        return region_yield.sort_values('Average Yield', ascending=False)
    
    def get_yield_by_factor(self, factor, region=None, crop=None):
        """
        Get yield data grouped by a specific factor
        
        Args:
            factor (str): Factor column to group by
            region (str, optional): Filter by specific region
            crop (str, optional): Filter by specific crop
            
        Returns:
            pandas.DataFrame: Data grouped by factor
        """
        filters = {}
        if region:
            filters['Agro-Climatic Zone'] = region
        if crop:
            filters['Crop'] = crop
            
        filtered_df = self.filter_data(filters)
        
        if factor not in filtered_df.columns:
            return pd.DataFrame()
            
        # For numerical factors, create bins
        if filtered_df[factor].dtype in [np.float64, np.int64]:
            filtered_df[f'{factor} Bin'] = pd.qcut(filtered_df[factor], 5, duplicates='drop')
            factor = f'{factor} Bin'
            
        factor_yield = filtered_df.groupby(factor)[self.target_column].agg(['mean', 'count']).reset_index()
        factor_yield.columns = [factor, 'Average Yield', 'Sample Count']
        
        return factor_yield.sort_values(factor)
    
    def get_yield_trend(self, region=None, crop=None):
        """
        Get yield trend over years
        
        Args:
            region (str, optional): Filter by specific region
            crop (str, optional): Filter by specific crop
            
        Returns:
            pandas.DataFrame: Yield trend by year
        """
        filters = {}
        if region:
            filters['Agro-Climatic Zone'] = region
        if crop:
            filters['Crop'] = crop
            
        filtered_df = self.filter_data(filters)
        
        yearly_yield = filtered_df.groupby('Year')[self.target_column].agg(['mean', 'std', 'count']).reset_index()
        yearly_yield.columns = ['Year', 'Average Yield', 'Std Dev', 'Sample Count']
        
        return yearly_yield.sort_values('Year')
    
    def get_correlation_matrix(self, region=None, crop=None):
        """
        Get correlation matrix between yield and factors
        
        Args:
            region (str, optional): Filter by specific region
            crop (str, optional): Filter by specific crop
            
        Returns:
            pandas.DataFrame: Correlation matrix
        """
        filters = {}
        if region:
            filters['Agro-Climatic Zone'] = region
        if crop:
            filters['Crop'] = crop
            
        filtered_df = self.filter_data(filters)
        
        numeric_columns = ['Rainfall (mm)', 'Irrigation (%)', 'Fertilizer Use (kg/ha)', self.target_column]
        correlation_matrix = filtered_df[numeric_columns].corr()
        
        return correlation_matrix
    
    def get_factor_impact(self, region=None, crop=None):
        """
        Get the impact of each factor on yield
        
        Args:
            region (str, optional): Filter by specific region
            crop (str, optional): Filter by specific crop
            
        Returns:
            dict: Factor impact scores
        """
        filters = {}
        if region:
            filters['Agro-Climatic Zone'] = region
        if crop:
            filters['Crop'] = crop
            
        filtered_df = self.filter_data(filters)
        
        if len(filtered_df) < 10:
            return {}
            
        X = filtered_df[self.feature_columns]
        y = filtered_df[self.target_column]
        
        # Train a simple linear regression model
        model = LinearRegression()
        model.fit(X, y)
        
        # Get feature importance
        importance = dict(zip(self.feature_columns, model.coef_))
        
        # Normalize to sum to 100%
        total = sum(abs(val) for val in importance.values())
        if total > 0:
            for key in importance:
                importance[key] = abs(importance[key]) / total * 100
                
        return importance 