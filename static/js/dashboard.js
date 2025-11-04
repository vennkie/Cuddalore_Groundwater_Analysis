// Global chart variables
let qualityChart, pollutantChart, blockQualityChart, seasonChart, yearlyChart, probabilityChart;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    loadBlocks();
    loadTopRiskyWells();
    
    // Setup form submission
    document.getElementById('prediction-form').addEventListener('submit', handlePrediction);
});

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + '-tab').classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
    
    // Load data for specific tab
    if (tabName === 'analysis') {
        loadAnalysisData();
        loadAnalysisTable();
    }
}

// Load overview statistics
async function loadStats() {
    try {
        const response = await fetch('/api/stats');
        const data = await response.json();
        
        // Update stat cards
        document.getElementById('total-samples').textContent = data.total_samples.toLocaleString();
        document.getElementById('total-blocks').textContent = data.total_blocks;
        document.getElementById('avg-hhi').textContent = data.avg_hhi.toFixed(2);
        
        // Create quality distribution chart
        createQualityChart(data.quality_distribution);
        
        // Load pollutant data
        loadPollutantData();
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Create quality distribution pie chart
function createQualityChart(data) {
    const ctx = document.getElementById('qualityChart').getContext('2d');
    
    const labels = Object.keys(data);
    const values = Object.values(data);
    const colors = {
        'Good': '#28a745',
        'Moderate': '#ffc107',
        'Poor': '#fd7e14',
        'Highly Polluted': '#dc3545'
    };
    
    if (qualityChart) qualityChart.destroy();
    
    qualityChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: labels.map(l => colors[l] || '#999')
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Water Quality Distribution'
                }
            }
        }
    });
}

// Load pollutant data
async function loadPollutantData() {
    try {
        const response = await fetch('/api/pollutant_data');
        const data = await response.json();
        
        const pollutants = Object.keys(data).slice(0, 6); // Top 6 pollutants
        const means = pollutants.map(p => data[p].mean);
        
        createPollutantChart(pollutants, means);
        
    } catch (error) {
        console.error('Error loading pollutant data:', error);
    }
}

// Create pollutant bar chart
function createPollutantChart(labels, data) {
    const ctx = document.getElementById('pollutantChart').getContext('2d');
    
    if (pollutantChart) pollutantChart.destroy();
    
    pollutantChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Concentration',
                data: data,
                backgroundColor: 'rgba(102, 126, 234, 0.8)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Average Pollutant Concentrations'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Load blocks dropdown
async function loadBlocks() {
    try {
        const response = await fetch('/api/blocks');
        const blocks = await response.json();
        
        const selector = document.getElementById('block-selector');
        blocks.forEach(block => {
            const option = document.createElement('option');
            option.value = block;
            option.textContent = block;
            selector.appendChild(option);
        });
        
        selector.addEventListener('change', function() {
            if (this.value) {
                loadBlockStats(this.value);
            }
        });
        
    } catch (error) {
        console.error('Error loading blocks:', error);
    }
}

// Load analysis data
async function loadAnalysisData() {
    await loadBlocks();
    loadSeasonTrends();
}

// Load analysis table data (block-wise summary)
async function loadAnalysisTable() {
    try {
        const response = await fetch('/api/analysis_table');
        const rows = await response.json();

        const tbody = document.querySelector('#analysis-table tbody');
        tbody.innerHTML = '';

        rows.forEach(r => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${r.Block}</td>
                <td style="text-align:right;">${r.Wells}</td>
                <td style="text-align:right;">${r.AvgNitrate?.toFixed(1)}</td>
                <td style="text-align:right;">${r.AvgFluoride?.toFixed(1)}</td>
                <td>${r.WQI}</td>
                <td style="text-align:right;">${r.HHI?.toFixed(2)}</td>
                <td><b class="risk-${r.Risk.toLowerCase().replace(/\s+/g,'-')}">${r.Risk}</b></td>
                <td>${Array.isArray(r.PossibleImpacts) ? r.PossibleImpacts.join('; ') : r.PossibleImpacts}</td>
                <td>${Array.isArray(r.VulnerablePopulation) ? r.VulnerablePopulation.join('; ') : r.VulnerablePopulation}</td>
                <td>${Array.isArray(r.RecommendedAction) ? r.RecommendedAction.join('; ') : r.RecommendedAction}</td>
                <td>${Array.isArray(r.RecommendedHealthIntervention) ? r.RecommendedHealthIntervention.join('; ') : r.RecommendedHealthIntervention}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (err) {
        console.error('Error loading analysis table:', err);
    }
}

// Load block statistics
async function loadBlockStats(blockName) {
    try {
        const response = await fetch(`/api/block_stats/${encodeURIComponent(blockName)}`);
        const data = await response.json();
        
        // Create block quality chart
        createBlockQualityChart(data.quality_distribution);
        
        // Create season chart
        createSeasonChart(data.seasonal_data);
        
        // Create yearly chart
        createYearlyChart(data.yearly_data);
        
    } catch (error) {
        console.error('Error loading block stats:', error);
    }
}

// Create block quality chart
function createBlockQualityChart(data) {
    const ctx = document.getElementById('blockQualityChart').getContext('2d');
    
    if (blockQualityChart) blockQualityChart.destroy();
    
    const labels = Object.keys(data);
    const values = Object.values(data);
    const colors = {
        'Good': '#28a745',
        'Moderate': '#ffc107',
        'Poor': '#fd7e14',
        'Highly Polluted': '#dc3545'
    };
    
    blockQualityChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: labels.map(l => colors[l] || '#999')
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Create season chart
function createSeasonChart(data) {
    const ctx = document.getElementById('seasonChart').getContext('2d');
    
    const seasons = Object.keys(data);
    const hhiValues = seasons.map(s => data[s].mean);
    
    if (seasonChart) seasonChart.destroy();
    
    seasonChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: seasons,
            datasets: [{
                label: 'Average HHI',
                data: hhiValues,
                borderColor: 'rgba(102, 126, 234, 1)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Create yearly chart
function createYearlyChart(data) {
    const ctx = document.getElementById('yearlyChart').getContext('2d');
    
    const years = Object.keys(data);
    const hhiValues = Object.values(data);
    
    if (yearlyChart) yearlyChart.destroy();
    
    yearlyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: years,
            datasets: [{
                label: 'Average HHI',
                data: hhiValues,
                backgroundColor: 'rgba(118, 75, 162, 0.8)',
                borderColor: 'rgba(118, 75, 162, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// Load season trends
async function loadSeasonTrends() {
    try {
        const response = await fetch('/api/season_trends');
        const data = await response.json();
        
        // Process and create chart if needed
        console.log('Season trends:', data);
        
    } catch (error) {
        console.error('Error loading season trends:', error);
    }
}

// Load top risky wells
async function loadTopRiskyWells() {
    try {
        const response = await fetch('/api/top_risky_wells');
        const wells = await response.json();
        
        const tbody = document.querySelector('#risky-wells-table tbody');
        tbody.innerHTML = '';
        
        wells.forEach(well => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${well.WellID || '-'}</td>
                <td>${well.BlockName || '-'}</td>
                <td>${well.VillageName || '-'}</td>
                <td>${well.Year || '-'}</td>
                <td>${well.Season || '-'}</td>
                <td>${well.HHI ? well.HHI.toFixed(2) : '-'}</td>
                <td><span class="quality-${well.Quality_Class?.toLowerCase().replace(' ', '-')}">${well.Quality_Class || '-'}</span></td>
            `;
            tbody.appendChild(row);
        });
        
    } catch (error) {
        console.error('Error loading risky wells:', error);
    }
}

// Handle prediction form submission
async function handlePrediction(event) {
    event.preventDefault();
    
    // Collect form data
    const formData = {
        pH: parseFloat(document.getElementById('pH').value),
        TDS: parseFloat(document.getElementById('TDS').value),
        Nitrate: parseFloat(document.getElementById('Nitrate').value),
        Fluoride: parseFloat(document.getElementById('Fluoride').value),
        Iron: parseFloat(document.getElementById('Iron').value),
        Chloride: parseFloat(document.getElementById('Chloride').value),
        Hardness: parseFloat(document.getElementById('Hardness').value),
        Sulphates: parseFloat(document.getElementById('Sulphates').value),
        Alkalinity: parseFloat(document.getElementById('Alkalinity').value),
        Total_Coliform: parseFloat(document.getElementById('Total_Coliform').value),
        'E.Coli': parseFloat(document.getElementById('E.Coli').value),
        BlockName_encoded: 0,
        Season_encoded: 0,
        Year: 2020
    };
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const result = await response.json();
        
        if (result.error) {
            alert('Error: ' + result.error);
            return;
        }
        
        displayResults(result);
        
    } catch (error) {
        console.error('Error making prediction:', error);
        alert('Error making prediction. Please try again.');
    }
}

// Display prediction results
function displayResults(result) {
    // Show results section
    document.getElementById('results-section').style.display = 'block';
    
    // Update result values
    document.getElementById('quality-class').textContent = result.quality_class;
    document.getElementById('quality-class').className = `result-value quality-${result.quality_class.toLowerCase().replace(' ', '-')}`;
    
    document.getElementById('hhi-value').textContent = result.hhi.toFixed(2);
    
    const riskLevel = result.risk_level;
    document.getElementById('risk-level').textContent = riskLevel;
    document.getElementById('risk-level').className = `result-value risk-${riskLevel.toLowerCase().replace(' ', '-')}`;
    
    // Create probability chart
    createProbabilityChart(result.probabilities);
    
    // Display recommendations
    displayRecommendations(result.recommendations);
}

// Create probability chart
function createProbabilityChart(probabilities) {
    const ctx = document.getElementById('probabilityChart').getContext('2d');
    
    const labels = Object.keys(probabilities);
    const values = Object.values(probabilities);
    
    if (probabilityChart) probabilityChart.destroy();
    
    probabilityChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Probability',
                data: values,
                backgroundColor: labels.map(l => {
                    if (l === 'Good') return '#28a745';
                    if (l === 'Moderate') return '#ffc107';
                    if (l === 'Poor') return '#fd7e14';
                    return '#dc3545';
                })
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 1
                }
            }
        }
    });
}

// Display recommendations
function displayRecommendations(recommendations) {
    const ul = document.getElementById('recommendations-list');
    ul.innerHTML = '';
    
    recommendations.forEach(rec => {
        const li = document.createElement('li');
        li.textContent = rec;
        ul.appendChild(li);
    });
}

