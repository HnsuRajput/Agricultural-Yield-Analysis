// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initApp();
});

// Global variables
let regions = [];
let crops = [];

// Initialize the application
function initApp() {
    // Fetch regions and crops
    fetchRegions();
    fetchCrops();
    
    // Set up event listeners
    setupEventListeners();
}

// Fetch regions from API
function fetchRegions() {
    fetch('/api/regions')
        .then(response => response.json())
        .then(data => {
            regions = data;
            populateRegionSelects(data);
        })
        .catch(error => console.error('Error fetching regions:', error));
}

// Fetch crops from API
function fetchCrops() {
    fetch('/api/crops')
        .then(response => response.json())
        .then(data => {
            crops = data;
            populateCropSelects(data);
        })
        .catch(error => console.error('Error fetching crops:', error));
}

// Populate all region select dropdowns
function populateRegionSelects(regions) {
    const regionSelects = [
        document.getElementById('region-select'),
        document.getElementById('crop-region-select'),
        document.getElementById('pred-region-select'),
        document.getElementById('strategy-region-select')
    ];
    
    regionSelects.forEach(select => {
        if (select) {
            // Clear existing options
            select.innerHTML = '';
            
            // Add default option
            const defaultOption = document.createElement('option');
            defaultOption.value = '';
            defaultOption.textContent = 'Select Region';
            select.appendChild(defaultOption);
            
            // Add region options
            regions.forEach(region => {
                const option = document.createElement('option');
                option.value = region;
                option.textContent = region;
                select.appendChild(option);
            });
        }
    });
}

// Populate all crop select dropdowns
function populateCropSelects(crops) {
    const cropSelects = [
        document.getElementById('region-crop-select'),
        document.getElementById('crop-select'),
        document.getElementById('pred-crop-select'),
        document.getElementById('strategy-crop-select')
    ];
    
    cropSelects.forEach(select => {
        if (select) {
            // Clear existing options except the first one (All Crops)
            if (select.id === 'region-crop-select' || select.id === 'crop-region-select') {
                select.innerHTML = '';
                const allOption = document.createElement('option');
                allOption.value = '';
                allOption.textContent = 'All Crops';
                select.appendChild(allOption);
            } else {
                select.innerHTML = '';
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'Select Crop';
                select.appendChild(defaultOption);
            }
            
            // Add crop options
            crops.forEach(crop => {
                const option = document.createElement('option');
                option.value = crop;
                option.textContent = crop;
                select.appendChild(option);
            });
        }
    });
}

// Set up event listeners
function setupEventListeners() {
    // Regional analysis
    const analyzeRegionBtn = document.getElementById('analyze-region-btn');
    if (analyzeRegionBtn) {
        analyzeRegionBtn.addEventListener('click', analyzeRegion);
    }
    
    // Crop analysis
    const analyzeCropBtn = document.getElementById('analyze-crop-btn');
    if (analyzeCropBtn) {
        analyzeCropBtn.addEventListener('click', analyzeCrop);
    }
    
    // Yield prediction
    const predictionForm = document.getElementById('prediction-form');
    if (predictionForm) {
        predictionForm.addEventListener('submit', predictYield);
    }
    
    // Improvement strategies
    const getStrategiesBtn = document.getElementById('get-strategies-btn');
    if (getStrategiesBtn) {
        getStrategiesBtn.addEventListener('click', getImprovementStrategies);
    }
}

// Analyze region
function analyzeRegion() {
    const region = document.getElementById('region-select').value;
    const crop = document.getElementById('region-crop-select').value;
    
    if (!region) {
        alert('Please select a region');
        return;
    }
    
    // Show loading state
    document.getElementById('region-yield-trend').innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading-spinner"></div></div>';
    document.getElementById('region-factor-impact').innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading-spinner"></div></div>';
    document.getElementById('region-insights').innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading-spinner"></div></div>';
    
    // Fetch yield trend
    fetchYieldTrend(region, crop, 'region-yield-trend');
    
    // Fetch factor impact
    fetchFactorImpact(region, crop, 'region-factor-impact');
    
    // Fetch regional insights
    fetchRegionalInsights(region, crop);
}

// Analyze crop
function analyzeCrop() {
    const crop = document.getElementById('crop-select').value;
    const region = document.getElementById('crop-region-select').value;
    
    if (!crop) {
        alert('Please select a crop');
        return;
    }
    
    // Show loading state
    document.getElementById('crop-yield-by-region').innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading-spinner"></div></div>';
    document.getElementById('crop-factor-impact').innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading-spinner"></div></div>';
    document.getElementById('crop-insights').innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading-spinner"></div></div>';
    
    // Fetch yield by region
    fetchYieldByRegion(crop, 'crop-yield-by-region');
    
    // Fetch factor impact
    fetchFactorImpact(region, crop, 'crop-factor-impact');
    
    // Fetch crop insights
    fetchCropInsights(crop, region);
}

// Predict yield
function predictYield(event) {
    event.preventDefault();
    
    const region = document.getElementById('pred-region-select').value;
    const crop = document.getElementById('pred-crop-select').value;
    const rainfall = document.getElementById('rainfall-input').value;
    const irrigation = document.getElementById('irrigation-input').value;
    const fertilizer = document.getElementById('fertilizer-input').value;
    
    if (!region || !crop || !rainfall || !irrigation || !fertilizer) {
        alert('Please fill all fields');
        return;
    }
    
    const url = '/api/predict-yield';
    const data = {
        region: region,
        crop: crop,
        rainfall: parseFloat(rainfall),
        irrigation: parseFloat(irrigation),
        fertilizer: parseFloat(fertilizer)
    };
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('prediction-result').innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        ${data.error}
                    </div>
                `;
            } else {
                document.getElementById('prediction-result').innerHTML = `
                    <div class="prediction-result">
                        <h4>Predicted Yield</h4>
                        <div class="prediction-value">${data.predicted_yield.toFixed(2)}</div>
                        <div class="prediction-unit">${data.unit}</div>
                    </div>
                    <div class="mt-3">
                        <p>For ${crop} in ${region} with:</p>
                        <ul class="list-unstyled">
                            <li>Rainfall: ${rainfall} mm</li>
                            <li>Irrigation: ${irrigation}%</li>
                            <li>Fertilizer: ${fertilizer} kg/ha</li>
                        </ul>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error predicting yield:', error);
            document.getElementById('prediction-result').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    An error occurred while predicting yield. Please try again.
                </div>
            `;
        });
}

// Get improvement strategies
function getImprovementStrategies() {
    const region = document.getElementById('strategy-region-select').value;
    const crop = document.getElementById('strategy-crop-select').value;
    
    if (!region || !crop) {
        alert('Please select both region and crop');
        return;
    }
    
    // Show loading state
    document.getElementById('strategies-container').innerHTML = '<div class="d-flex justify-content-center align-items-center h-100"><div class="loading-spinner"></div></div>';
    
    const url = `/api/improvement-strategies?region=${encodeURIComponent(region)}&crop=${encodeURIComponent(crop)}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                document.getElementById('strategies-container').innerHTML = `
                    <div class="alert alert-info" role="alert">
                        No improvement strategies available for ${crop} in ${region}.
                    </div>
                `;
                return;
            }
            
            let strategiesHTML = `
                <h6>Improvement Strategies for ${crop} in ${region}</h6>
                <div class="strategies-list">
            `;
            
            data.forEach(strategy => {
                strategiesHTML += `
                    <div class="strategy-card">
                        <h6>${strategy.factor}</h6>
                        <p><strong>Impact:</strong> ${strategy.impact}</p>
                        <p><strong>Current Value:</strong> ${strategy.current_value}</p>
                        <p><strong>Recommendation:</strong> ${strategy.recommendation}</p>
                    </div>
                `;
            });
            
            strategiesHTML += '</div>';
            
            document.getElementById('strategies-container').innerHTML = strategiesHTML;
        })
        .catch(error => {
            console.error('Error fetching improvement strategies:', error);
            document.getElementById('strategies-container').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    An error occurred while fetching improvement strategies. Please try again.
                </div>
            `;
        });
}

// Fetch yield trend
function fetchYieldTrend(region, crop, elementId) {
    let url = `/api/yield-trend?region=${encodeURIComponent(region)}`;
    if (crop) {
        url += `&crop=${encodeURIComponent(crop)}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                document.getElementById(elementId).innerHTML = `
                    <div class="alert alert-info" role="alert">
                        No yield trend data available for the selected parameters.
                    </div>
                `;
                return;
            }
            
            // Extract data from API response
            const years = data.map(item => item.Year);
            const yields = data.map(item => item['Yield (tonnes/ha)']);
            
            // Create trace for the chart
            const traces = [
                {
                    x: years,
                    y: yields,
                    type: 'scatter',
                    mode: 'lines+markers',
                    name: 'Average Yield',
                    line: {
                        color: '#28a745',
                        width: 2
                    },
                    marker: {
                        size: 8,
                        color: '#28a745'
                    }
                }
            ];
            
            const layout = {
                title: `Yield Trend for ${crop || 'All Crops'} in ${region}`,
                xaxis: {
                    title: 'Year'
                },
                yaxis: {
                    title: 'Yield (tonnes/ha)'
                },
                margin: {
                    l: 50,
                    r: 50,
                    b: 50,
                    t: 50,
                    pad: 4
                },
                hovermode: 'closest'
            };
            
            Plotly.newPlot(elementId, traces, layout, {responsive: true});
        })
        .catch(error => {
            console.error('Error fetching yield trend:', error);
            document.getElementById(elementId).innerHTML = `
                <div class="alert alert-danger" role="alert">
                    An error occurred while fetching yield trend. Please try again.
                </div>
            `;
        });
}

// Fetch yield by region
function fetchYieldByRegion(crop, elementId) {
    const url = `/api/yield-by-region?crop=${encodeURIComponent(crop)}`;
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) {
                document.getElementById(elementId).innerHTML = `
                    <div class="alert alert-info" role="alert">
                        No yield data available for the selected crop.
                    </div>
                `;
                return;
            }
            
            // Sort data by yield
            data.sort((a, b) => b['Yield (tonnes/ha)'] - a['Yield (tonnes/ha)']);
            
            const regions = data.map(item => item['Agro-Climatic Zone']);
            const yields = data.map(item => item['Yield (tonnes/ha)']);
            
            const trace = {
                x: regions,
                y: yields,
                type: 'bar',
                marker: {
                    color: '#28a745'
                }
            };
            
            const layout = {
                title: `Average Yield of ${crop} by Region`,
                xaxis: {
                    title: 'Region',
                    tickangle: -45
                },
                yaxis: {
                    title: 'Yield (tonnes/ha)'
                },
                margin: {
                    l: 50,
                    r: 50,
                    b: 150,
                    t: 50,
                    pad: 4
                }
            };
            
            Plotly.newPlot(elementId, [trace], layout, {responsive: true});
        })
        .catch(error => {
            console.error('Error fetching yield by region:', error);
            document.getElementById(elementId).innerHTML = `
                <div class="alert alert-danger" role="alert">
                    An error occurred while fetching yield by region. Please try again.
                </div>
            `;
        });
}

// Fetch factor impact
function fetchFactorImpact(region, crop, elementId) {
    let url = '/api/factor-impact';
    const params = [];
    
    if (region) {
        params.push(`region=${encodeURIComponent(region)}`);
    }
    
    if (crop) {
        params.push(`crop=${encodeURIComponent(crop)}`);
    }
    
    if (params.length > 0) {
        url += '?' + params.join('&');
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (Object.keys(data).length === 0) {
                document.getElementById(elementId).innerHTML = `
                    <div class="alert alert-info" role="alert">
                        No factor impact data available for the selected parameters.
                    </div>
                `;
                return;
            }
            
            const factors = Object.keys(data);
            const impacts = Object.values(data);
            
            const trace = {
                x: factors,
                y: impacts,
                type: 'bar',
                marker: {
                    color: '#28a745'
                }
            };
            
            const layout = {
                title: `Factor Impact on Yield`,
                xaxis: {
                    title: 'Factor'
                },
                yaxis: {
                    title: 'Impact (%)'
                },
                margin: {
                    l: 50,
                    r: 50,
                    b: 100,
                    t: 50,
                    pad: 4
                }
            };
            
            Plotly.newPlot(elementId, [trace], layout, {responsive: true});
        })
        .catch(error => console.error('Error fetching factor impact:', error));
}

// Fetch regional insights
function fetchRegionalInsights(region, crop) {
    let url = `/api/regional-insights?region=${encodeURIComponent(region)}`;
    
    if (crop) {
        url += `&crop=${encodeURIComponent(crop)}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('region-insights').innerHTML = `
                    <div class="alert alert-warning" role="alert">
                        ${data.error}
                    </div>
                `;
                return;
            }
            
            let insightsHTML = `
                <h6>Insights for ${data.region}</h6>
                <p><strong>Average Yield:</strong> ${data.average_yield} tonnes/ha</p>
                <p><strong>Yield Trend:</strong> ${data.yield_trend}</p>
            `;
            
            if (data.top_crops && data.top_crops.length > 0) {
                insightsHTML += `
                    <p><strong>Top Performing Crops:</strong></p>
                    <ul>
                        ${data.top_crops.map(crop => `<li>${crop}</li>`).join('')}
                    </ul>
                `;
            }
            
            if (data.factor_impact) {
                insightsHTML += `
                    <p><strong>Factor Impact:</strong></p>
                    <ul>
                        ${Object.entries(data.factor_impact).map(([factor, impact]) => 
                            `<li>${factor}: ${impact.toFixed(2)}</li>`).join('')}
                    </ul>
                `;
            }
            
            document.getElementById('region-insights').innerHTML = insightsHTML;
        })
        .catch(error => {
            console.error('Error fetching regional insights:', error);
            document.getElementById('region-insights').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    An error occurred while fetching regional insights. Please try again.
                </div>
            `;
        });
}

// Fetch crop insights
function fetchCropInsights(crop, region) {
    let url = `/api/crop-insights?crop=${encodeURIComponent(crop)}`;
    
    if (region) {
        url += `&region=${encodeURIComponent(region)}`;
    }
    
    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('crop-insights').innerHTML = `
                    <div class="alert alert-warning" role="alert">
                        ${data.error}
                    </div>
                `;
                return;
            }
            
            let insightsHTML = `
                <h6>Insights for ${data.crop}</h6>
                <p><strong>Average Yield:</strong> ${data.average_yield} tonnes/ha</p>
                <p><strong>Yield Trend:</strong> ${data.yield_trend}</p>
            `;
            
            if (data.top_regions && data.top_regions.length > 0) {
                insightsHTML += `
                    <p><strong>Top Performing Regions:</strong></p>
                    <ul>
                        ${data.top_regions.map(region => `<li>${region}</li>`).join('')}
                    </ul>
                `;
            }
            
            if (data.factor_impact) {
                insightsHTML += `
                    <p><strong>Factor Impact:</strong></p>
                    <ul>
                        ${Object.entries(data.factor_impact).map(([factor, impact]) => 
                            `<li>${factor}: ${impact.toFixed(2)}</li>`).join('')}
                    </ul>
                `;
            }
            
            document.getElementById('crop-insights').innerHTML = insightsHTML;
        })
        .catch(error => {
            console.error('Error fetching crop insights:', error);
            document.getElementById('crop-insights').innerHTML = `
                <div class="alert alert-danger" role="alert">
                    An error occurred while fetching crop insights. Please try again.
                </div>
            `;
        });
} 