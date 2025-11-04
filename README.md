# Groundwater Quality Analysis Dashboard

An AI-powered data science framework for monitoring and predicting groundwater quality in Cuddalore District (2018-2021).

## 📋 Project Overview

This project focuses on analyzing groundwater quality data to:
- Monitor water quality variations across seasons and blocks
- Predict potential health hazards based on contaminant levels
- Support decision-making for water management and public health policies

## 🎯 Features

- **Data Analysis**: Comprehensive analysis of 4 years of groundwater quality data
- **Machine Learning Models**: Classification and Regression models for quality prediction
- **Interactive Dashboard**: Real-time visualization and predictions
- **Risk Assessment**: Health Hazard Index (HHI) calculation
- **Predictive Analytics**: Water quality prediction based on water parameters

## 📊 Data Parameters

### Physicochemical Parameters:
- pH, TDS, EC
- Nitrate, Fluoride, Iron
- Hardness, Chloride, Sulphate

### Biological Parameters:
- E. coli, Total Coliform

### Spatio-temporal Factors:
- Block name, Well ID
- Depth (8m pre-monsoon / 12m monsoon / 2m post-monsoon)
- Seasonal data (Pre-monsoon, Monsoon, Post-monsoon)

## 🛠️ Tech Stack

- **Backend**: Flask (Python)
- **ML Models**: Random Forest, XGBoost (scikit-learn)
- **Frontend**: HTML, CSS, JavaScript
- **Visualization**: Chart.js
 - **Explainability (optional)**: External GROK API via HTTP

## 📦 Installation

1. **Clone or download the project**

2. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run data preprocessing:**
```bash
python data_preprocessing.py
```

4. **Train models:**
```bash
python train_models.py
```

5. **Start Flask application:**
```bash
python app.py
```

6. **Open browser and navigate to:**
```
http://localhost:5000
```

### Optional: Enable GROK explainability in Analysis tab

Set these environment variables so the Analysis table can fetch narrative fields per block (Possible Health Impacts, Vulnerable Population, Recommended Action, Recommended Health Intervention):

Windows PowerShell (current session):
```powershell
$env:GROK_API_KEY = "<your_api_key>"
$env:GROK_API_URL = "https://your-grok-endpoint"  # POST endpoint returning JSON
python app.py
```

Make it permanent:
```powershell
setx GROK_API_KEY "<your_api_key>"
setx GROK_API_URL "https://your-grok-endpoint"
```

Expected response JSON keys from your endpoint:
- `possible_impacts` (string or [string])
- `vulnerable_population` (string or [string])
- `recommended_action` (string or [string])
- `recommended_health_intervention` (string or [string])

## 📁 Project Structure

```
projectFolderMohanSir/
├── data_preprocessing.py    # Data loading and preprocessing
├── train_models.py          # Model training scripts
├── app.py                   # Flask application
├── requirements.txt         # Python dependencies
├── templates/
│   └── dashboard.html      # Dashboard UI
├── static/
│   ├── css/
│   │   └── style.css       # Styling
│   └── js/
│       └── dashboard.js    # Dashboard functionality
├── models/                 # Saved ML models
│   ├── rf_classifier.pkl
│   ├── rf_regressor.pkl
│   ├── xgb_classifier.pkl
│   └── xgb_regressor.pkl
└── 2018 - 2018.csv         # Data files
    2019 - 2019.csv
    2020 - 2020.csv
    2021 - 2021.csv
```

## 🚀 Usage

### Dashboard Tabs

1. **Overview**: Overall statistics and quality distribution
2. **Analysis**: Block-wise analysis and seasonal trends
   - Includes a table: Block, #Wells, Avg Nitrate, Avg Fluoride, WQI, HHI, Risk Category
   - Plus four narrative fields (AI-generated if GROK configured): Possible Health Impacts, Vulnerable Population, Recommended Action, Recommended Health Intervention
3. **Prediction**: Predict water quality from input parameters
4. **Risk Zones**: Identify high-risk wells and areas

### Making Predictions

1. Navigate to the "Prediction" tab
2. Enter water quality parameters:
   - pH, TDS, Nitrate, Fluoride, Iron
   - Chloride, Hardness, Sulphates
   - Alkalinity, Total Coliform, E. Coli
3. Click "Predict Quality"
4. View results:
   - Quality Class (Good/Moderate/Poor/Highly Polluted)
   - Health Hazard Index (HHI)
   - Risk Level
   - Recommendations

## 📈 Model Performance

### Classification Model
- Random Forest Classifier for quality categorization
- Accuracy and detailed classification metrics

### Regression Model
- Random Forest Regressor for HHI prediction
- RMSE, MAE, and R² scores

## 🎨 Dashboard Features

- **Interactive Charts**: Quality distribution, pollutant analysis
- **Block-wise Analysis**: Detailed statistics per block
  - API: `GET /api/analysis_table` (feeds the analysis table)
- **Seasonal Trends**: HHI trends across seasons
- **Risk Assessment**: Top 10 risky wells identification
- **Real-time Predictions**: Instant quality predictions

## 📊 Output

- Water quality classification
- Health Hazard Index (HHI)
- Violation detection
- Personalized recommendations
- Visual analytics and charts
 - Analysis table per block with health and action recommendations (with or without GROK)

## 🔍 Health Hazard Index (HHI)

HHI is calculated based on WHO/BIS standards:
- **Low Risk**: HHI < 0.5
- **Moderate Risk**: 0.5 ≤ HHI < 1.0
- **High Risk**: 1.0 ≤ HHI < 2.0
- **Very High Risk**: HHI ≥ 2.0

## 📝 Quality Classification

- **Excellent**: WQI < 25
- **Good**: 25 ≤ WQI < 50
- **Poor**: 50 ≤ WQI < 75
- **Very Poor**: 75 ≤ WQI < 100
- **Unsuitable**: WQI ≥ 100

## 🤝 Contributing

This is a research project for groundwater quality monitoring in Cuddalore District.

## 📄 License

Project developed for groundwater quality research.

## 👥 Authors

Developed for the groundwater quality analysis research project.

---

**Note**: Ensure all CSV data files are in the project root directory before running preprocessing.

---

## 🌐 Running on an external device (same Wi‑Fi/LAN)

Goal: Open the dashboard on your phone or another PC on the same network.

### Option A: Quick (edit run host in code temporarily)
In `app.py`, change the last line to bind to all interfaces:
```python
app.run(debug=True, host="0.0.0.0", port=5000)
```
Then run:
```bash
python app.py
```
Find your PC's local IP (e.g., 192.168.1.20) and open on another device:
```
http://192.168.1.20:5000
```

### Option B: Without editing code (use Flask runner)
```powershell
set FLASK_APP=app.py   # on Windows cmd
# or
$env:FLASK_APP = "app.py"  # on PowerShell

flask run --host=0.0.0.0 --port=5000
```
Open from another device via `http://<your-PC-LAN-IP>:5000`.

### Windows Firewall
- On first run, allow Python through Windows Firewall (Private networks).
- If blocked, open Windows Security → Firewall → Allow an app → Allow `python.exe` for Private.

### Notes
- All devices must be on the same network.
- Use Private/Trusted network, not Public Wi‑Fi.
- For production/Internet exposure, use a WSGI server (e.g., gunicorn via WSL) and a reverse proxy.

