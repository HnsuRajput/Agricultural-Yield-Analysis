# Indian Agricultural Yield Analysis

A comprehensive data-driven web application for analyzing crop yield variability across Indian agro-climatic zones and identifying key factors influencing agricultural productivity. This project provides valuable insights for farmers, agricultural researchers, and policymakers to make informed decisions based on data analytics.

## Project Overview

The Indian Agricultural Yield Analysis application is designed to help users understand the complex relationships between environmental factors and crop yields across different regions of India. By leveraging data science and machine learning techniques, the application provides:

1. **Data-driven insights** into regional agricultural patterns
2. **Predictive models** for estimating crop yields based on environmental parameters
3. **Improvement strategies** tailored to specific regions and crops
4. **Interactive visualizations** for better understanding of agricultural data

The application analyzes relationships between key agricultural factors such as rainfall, irrigation coverage, fertilizer usage, soil types, and seasonal variations to provide actionable insights for optimizing agricultural productivity.

## Agro-Climatic Zones of India

The application is built around India's 15 agro-climatic zones as defined by the Planning Commission of India. These zones are based on soil types, climate, physiography, and cropping patterns:

1. **Western Himalayan Region**: Jammu & Kashmir, Himachal Pradesh, Uttarakhand
   - *Key crops*: Apples, walnuts, barley, maize, wheat
   - *Climate*: Temperate to sub-alpine; cold winters and mild summers

2. **Eastern Himalayan Region**: Arunachal Pradesh, Sikkim, Meghalaya, Assam, Nagaland, Manipur, Mizoram, Tripura
   - *Key crops*: Rice, maize, tea, jute, ginger, pineapple
   - *Climate*: High rainfall; humid subtropical to alpine

3. **Lower Gangetic Plains Region**: West Bengal, parts of Bihar
   - *Key crops*: Rice, jute, sugarcane, potato
   - *Climate*: Tropical humid; high rainfall

4. **Middle Gangetic Plains Region**: Eastern Uttar Pradesh, Bihar
   - *Key crops*: Wheat, rice, pulses, sugarcane
   - *Climate*: Sub-humid; moderate rainfall

5. **Upper Gangetic Plains Region**: Western Uttar Pradesh
   - *Key crops*: Wheat, sugarcane, rice, barley
   - *Climate*: Semi-arid to sub-humid; moderate rainfall

6. **Trans-Gangetic Plains Region**: Punjab, Haryana, Delhi, Chandigarh, Rajasthan (Ganganagar)
   - *Key crops*: Wheat, rice, cotton, sugarcane
   - *Climate*: Semi-arid; low rainfall, extreme summers and winters

7. **Eastern Plateau and Hills Region**: Odisha, Chhattisgarh, parts of Maharashtra
   - *Key crops*: Rice, maize, millet, pulses
   - *Climate*: Sub-humid; hot summers, moderate rainfall

8. **Central Plateau and Hills Region**: Madhya Pradesh, Rajasthan, Uttar Pradesh
   - *Key crops*: Soybean, wheat, gram, jowar
   - *Climate*: Semi-arid; moderate rainfall

9. **Western Plateau and Hills Region**: Maharashtra, Madhya Pradesh, Rajasthan, Gujarat
   - *Key crops*: Cotton, sugarcane, groundnut, pulses
   - *Climate*: Semi-arid; low rainfall

10. **Southern Plateau and Hills Region**: Andhra Pradesh, Karnataka, Tamil Nadu, Maharashtra
    - *Key crops*: Groundnut, millets, cotton, pulses
    - *Climate*: Semi-arid; tropical climate with uneven rainfall

11. **East Coast Plains and Hills Region**: Tamil Nadu, Andhra Pradesh, Odisha, Puducherry
    - *Key crops*: Rice, coconut, sugarcane, cashew
    - *Climate*: Humid tropical; high monsoonal rainfall

12. **West Coast Plains and Ghat Region**: Maharashtra, Goa, Karnataka, Kerala
    - *Key crops*: Coconut, arecanut, rice, spices
    - *Climate*: Tropical humid; heavy monsoon rainfall

13. **Gujarat Plains and Hills Region**: Gujarat
    - *Key crops*: Cotton, groundnut, wheat, bajra
    - *Climate*: Semi-arid to arid; low rainfall

14. **Western Dry Region**: Rajasthan
    - *Key crops*: Bajra, pulses, oilseeds, guar
    - *Climate*: Arid; very low rainfall, extreme temperatures

15. **The Islands Region**: Andaman & Nicobar Islands, Lakshadweep
    - *Key crops*: Coconut, rice, tropical fruits, spices
    - *Climate*: Tropical humid; heavy rainfall

## Features

### Regional Analysis
- Analyze yield trends across different agro-climatic zones
- Identify key factors impacting crop yields in specific regions
- Compare performance of different crops within a region
- Visualize regional yield trends over time

### Crop Analysis
- Understand how specific crops perform across different regions
- Identify optimal growing conditions for each crop
- Analyze factor sensitivity for different crops
- Compare seasonal performance of crops

### Yield Prediction
- Predict crop yields based on environmental parameters
- Use machine learning models trained on historical data
- Adjust parameters to explore different scenarios
- Understand the impact of changing environmental factors

### Improvement Strategies
- Receive data-driven recommendations to improve crop yields
- Get tailored strategies based on regional and crop-specific factors
- Identify high-impact areas for agricultural interventions
- Understand limitations when data is insufficient (e.g., Rice in Central Plains)

## Technical Details

### Data Processing
The application processes agricultural data through several stages:
1. **Data Loading**: Imports crop yield dataset from CSV files
2. **Data Cleaning**: Handles missing values and outliers
3. **Feature Engineering**: Creates derived features for better analysis
4. **Statistical Analysis**: Calculates correlations and factor impacts
5. **Model Training**: Builds predictive models for yield estimation

### Machine Learning Approach
The yield prediction functionality uses:
- Linear Regression models for smaller datasets (< 50 samples)
- Random Forest Regression for larger datasets (≥ 50 samples)
- Feature importance analysis to identify key factors
- Data filtering to create region and crop-specific models
- Correlation analysis to understand relationships between variables

### API Architecture
The application provides a comprehensive REST API built with FastAPI, enabling:
- Easy data retrieval for frontend visualizations
- Programmatic access for external applications
- Flexible filtering of data based on regions, crops, and other parameters
- Detailed error handling and validation

## Tech Stack

- **Backend**: Python 3.9+, FastAPI 0.95.2
- **Data Processing**: Pandas 1.3.5, NumPy 1.21.6, Scikit-learn 1.0.2
- **Data Visualization**: Plotly.js 5.14.1, Matplotlib 3.5.3, Seaborn 0.12.0
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Server**: Uvicorn 0.22.0
- **Development Tools**: Jinja2 3.0.3, python-multipart 0.0.6, joblib 1.1.1

## Project Structure

```
project/
├── app/                      # Main application package
│   ├── api/                  # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py         # API route definitions
│   ├── data/                 # Data storage
│   │   └── crop_yield_dataset.csv  # Agricultural dataset
│   ├── models/               # Data models and analysis
│   │   ├── __init__.py
│   │   ├── data_processor.py # Data processing class
│   │   └── yield_analyzer.py # Yield analysis class
│   ├── static/               # Static files
│   │   ├── css/
│   │   │   └── style.css     # Custom styles
│   │   └── js/
│   │       └── main.js       # Frontend JavaScript
│   ├── templates/            # HTML templates
│   │   └── index.html        # Main dashboard template
│   ├── utils/                # Utility functions
│   │   ├── __init__.py
│   │   ├── helpers.py        # Helper functions
│   │   ├── data_processor.py # Data processing utilities
│   │   └── yield_analyzer.py # Yield analysis utilities
│   └── __init__.py           # App initialization
├── app.py                    # Main FastAPI application file
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── LICENSE                   # License information
└── README.md                 # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/indian-agricultural-yield-analysis.git
cd indian-agricultural-yield-analysis
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
   - Windows:
   ```bash
   venv\Scripts\activate
   ```
   - macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the application:
```bash
python run.py
```

6. Open your browser and navigate to:
```
http://localhost:8000
```

7. Access the interactive API documentation:
```
http://localhost:8000/docs
```

## Usage Guide

### Dashboard Navigation
The application features an intuitive dashboard with four main sections:
1. **Regional Analysis**: Select a region and optionally a crop to analyze regional yield patterns
2. **Crop Analysis**: Select a crop and optionally a region to analyze crop performance
3. **Yield Prediction**: Input environmental parameters to predict crop yields
4. **Improvement Strategies**: Get recommendations for improving yields for specific crops in specific regions

### Known Limitations
- The application may show "No improvement strategies available" for certain region-crop combinations (like Rice in Central Plains) due to:
  - Insufficient data for that specific combination
  - Low correlation between measured factors and yield (impact < 30%)
  - Random data generation patterns in the sample dataset

### Data Sources
The application uses a combination of:
- Historical agricultural yield data
- Weather and climate information
- Irrigation coverage statistics
- Fertilizer usage data
- Soil type classifications

## API Guide

The application provides the following API endpoints:

### Basic Data Endpoints

- **GET /api/regions** - Get all unique agro-climatic zones
- **GET /api/crops** - Get all unique crops
- **GET /api/soil-types** - Get all unique soil types
- **GET /api/seasons** - Get all unique seasons

### Analysis Endpoints

- **GET /api/yield-by-region** - Get average yield by region
  - Query parameters:
    - `crop` (optional): Filter by specific crop

- **GET /api/yield-by-factor** - Get yield data grouped by a specific factor
  - Query parameters:
    - `factor` (required): Factor to group by (e.g., 'Rainfall (mm)', 'Irrigation (%)', 'Fertilizer Use (kg/ha)')
    - `region` (optional): Filter by specific region
    - `crop` (optional): Filter by specific crop

- **GET /api/yield-trend** - Get yield trend over years
  - Query parameters:
    - `region` (optional): Filter by specific region
    - `crop` (optional): Filter by specific crop

- **GET /api/correlation-matrix** - Get correlation matrix between yield and factors
  - Query parameters:
    - `region` (optional): Filter by specific region
    - `crop` (optional): Filter by specific crop

- **GET /api/factor-impact** - Get the impact of each factor on yield
  - Query parameters:
    - `region` (optional): Filter by specific region
    - `crop` (optional): Filter by specific crop

### Insight Endpoints

- **GET /api/regional-insights** - Get comprehensive insights for a specific region
  - Query parameters:
    - `region` (required): Agro-climatic zone
    - `crop` (optional): Filter by specific crop

- **GET /api/crop-insights** - Get comprehensive insights for a specific crop
  - Query parameters:
    - `crop` (required): Crop name
    - `region` (optional): Filter by specific region

- **GET /api/improvement-strategies** - Get strategies to improve yield
  - Query parameters:
    - `region` (required): Agro-climatic zone
    - `crop` (required): Crop name

### Prediction Endpoint

- **POST /api/predict-yield** - Predict yield based on input parameters
  - Request body (JSON):
    ```json
    {
      "region": "Eastern Plateau and Hills",
      "crop": "Wheat",
      "rainfall": 1200.5,
      "irrigation": 85.2,
      "fertilizer": 120.5
    }
    ```
  - Response:
    ```json
    {
      "predicted_yield": 3.45,
      "unit": "tonnes/ha"
    }
    ```

## Example API Usage

### Get Regional Insights

```javascript
// Get insights for rice in the Eastern Plateau and Hills region
fetch('/api/regional-insights?region=Eastern%20Plateau%20and%20Hills&crop=Rice')
  .then(response => response.json())
  .then(data => console.log(data));
```

### Predict Yield

```javascript
// Predict wheat yield in the Trans-Gangetic Plain
fetch('/api/predict-yield', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    region: 'Trans-Gangetic Plain',
    crop: 'Wheat',
    rainfall: 950.5,
    irrigation: 70.8,
    fertilizer: 180.2
  })
})
.then(response => response.json())
.then(data => console.log(data));
```

## Future Enhancements

1. **Enhanced Machine Learning Models**: Implement more sophisticated prediction models like Gradient Boosting or Neural Networks
2. **Time Series Analysis**: Add forecasting capabilities for future yield predictions
3. **Climate Change Impact**: Incorporate climate change scenarios to predict future agricultural patterns
4. **Mobile Application**: Develop a companion mobile app for farmers to access insights in the field
5. **Localization**: Add support for Indian regional languages to improve accessibility

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Indian Council of Agricultural Research (ICAR) for agricultural data
- Ministry of Agriculture & Farmers Welfare for agro-climatic zone classifications
- Planning Commission of India for the agro-climatic regional planning approach
- Agricultural universities and research institutions for domain knowledge
- Open-source community for the fantastic tools and libraries 