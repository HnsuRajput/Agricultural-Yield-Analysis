from flask import render_template, jsonify
from app import app, data_processor

@app.route('/')
def index():
    """Render the main dashboard page"""
    return render_template('index.html')

@app.route('/regions')
def get_regions():
    """Get all unique agro-climatic zones"""
    regions = data_processor.get_unique_values('Agro-Climatic Zone')
    return jsonify(regions)

@app.route('/crops')
def get_crops():
    """Get all unique crops"""
    crops = data_processor.get_unique_values('Crop')
    return jsonify(crops) 