import pandas as pd
import numpy as np
import json
import os

def format_number(value, decimal_places=2):
    """
    Format a number with specified decimal places
    
    Args:
        value (float): Number to format
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted number
    """
    if pd.isna(value):
        return "N/A"
        
    return f"{value:.{decimal_places}f}"
    
def calculate_percent_change(old_value, new_value):
    """
    Calculate percentage change between two values
    
    Args:
        old_value (float): Original value
        new_value (float): New value
        
    Returns:
        float: Percentage change
    """
    if old_value == 0:
        return float('inf') if new_value > 0 else 0
        
    return ((new_value - old_value) / old_value) * 100
    
def get_trend_direction(values):
    """
    Determine the trend direction from a list of values
    
    Args:
        values (list): List of numerical values
        
    Returns:
        str: 'increasing', 'decreasing', or 'stable'
    """
    if len(values) < 2:
        return 'stable'
        
    # Calculate linear regression slope
    x = np.arange(len(values))
    slope = np.polyfit(x, values, 1)[0]
    
    if abs(slope) < 0.01:
        return 'stable'
    elif slope > 0:
        return 'increasing'
    else:
        return 'decreasing'
        
def generate_color_scale(values, colormap='RdYlGn'):
    """
    Generate a color scale for values
    
    Args:
        values (list): List of numerical values
        colormap (str): Matplotlib colormap name
        
    Returns:
        list: List of hex color codes
    """
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    
    if len(values) == 0:
        return []
        
    # Normalize values between 0 and 1
    min_val = min(values)
    max_val = max(values)
    
    if min_val == max_val:
        normalized = [0.5] * len(values)
    else:
        normalized = [(v - min_val) / (max_val - min_val) for v in values]
    
    # Get colormap
    cmap = plt.get_cmap(colormap)
    
    # Convert to hex colors
    hex_colors = [mcolors.to_hex(cmap(norm)) for norm in normalized]
    
    return hex_colors
    
def save_to_json(data, filename):
    """
    Save data to a JSON file
    
    Args:
        data: Data to save
        filename (str): Filename to save to
    """
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
        
def load_from_json(filename):
    """
    Load data from a JSON file
    
    Args:
        filename (str): Filename to load from
        
    Returns:
        dict: Loaded data
    """
    if not os.path.exists(filename):
        return None
        
    with open(filename, 'r') as f:
        return json.load(f) 