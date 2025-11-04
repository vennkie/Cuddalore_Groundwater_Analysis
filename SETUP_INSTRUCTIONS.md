# Quick Setup Instructions

## 📋 Prerequisites

- Python 3.8 or higher
- All 4 CSV files in the project directory (2018, 2019, 2020, 2021)

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
Open terminal/command prompt in the project folder and run:
```bash
pip install -r requirements.txt
```

### Step 2: Process Data and Train Models
Run the main script:
```bash
python run.py
```

OR run manually:
```bash
python data_preprocessing.py
python train_models.py
python app.py
```

### Step 3: Access Dashboard
Open your browser and go to:
```
http://localhost:5000
```

## 📊 What Each Script Does

### 1. data_preprocessing.py
- Loads all 4 CSV files (2018-2021)
- Parses parameter strings
- Extracts features (pH, TDS, Nitrate, etc.)
- Calculates HHI (Health Hazard Index)
- Creates quality classifications
- Saves to `processed_data.csv`

### 2. train_models.py
- Loads processed data
- Trains Random Forest Classifier
- Trains Random Forest Regressor
- Trains XGBoost Classifier
- Trains XGBoost Regressor
- Saves models to `models/` folder

### 3. app.py
- Loads trained models
- Creates Flask server
- Provides API endpoints
- Serves dashboard UI

## 🎯 Dashboard Features

Once running, you'll see:

### Overview Tab
- Total samples, blocks, year range
- Average HHI
- Quality distribution chart
- Pollutant overview chart

### Analysis Tab
- Select blocks from dropdown
- Block-wise quality charts
- Seasonal HHI trends
- Yearly trends

### Prediction Tab
- Enter water parameters
- Get instant predictions
- Quality class prediction
- Health Hazard Index
- Risk level assessment
- Actionable recommendations

### Risk Zones Tab
- Top 10 risky wells table
- Highest HHI values
- Block and season info

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Install requirements
```bash
pip install -r requirements.txt
```

### Issue: CSV files not found
**Solution**: Ensure all 4 CSV files are in the project root:
- 2018 - 2018.csv
- 2019 - 2019.csv
- 2020 - 2020.csv
- 2021 - 2021.csv

### Issue: Models not loading
**Solution**: Run training script
```bash
python train_models.py
```

### Issue: Port 5000 already in use
**Solution**: Change port in app.py
```python
app.run(debug=True, port=5001)  # Use different port
```

## 📝 Expected Runtime

- Data preprocessing: ~5-10 minutes (depending on CSV size)
- Model training: ~2-5 minutes
- Flask app starts: Instant

## 💡 Tips

1. First run will take longer due to data processing
2. Models are saved in `models/` folder (reuse for faster startup)
3. Keep CSV files in the root directory
4. Check console for any errors

## 📊 Output Files

After running, you'll have:
- `processed_data.csv` - Cleaned and processed data
- `models/rf_classifier.pkl` - Random Forest Classifier
- `models/rf_regressor.pkl` - Random Forest Regressor
- `models/xgb_classifier.pkl` - XGBoost Classifier
- `models/xgb_regressor.pkl` - XGBoost Regressor

## 🎉 Success!

Once you see "Running on http://127.0.0.1:5000" in the console, your dashboard is ready!

