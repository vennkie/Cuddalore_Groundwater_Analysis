# System Workflow

## 🔄 Complete Workflow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   1. DATA PREPROCESSING                      │
│              (data_preprocessing.py)                         │
├─────────────────────────────────────────────────────────────┤
│  Input: 4 CSV files (2018, 2019, 2020, 2021)              │
│  ↓ Parse parameter strings                                  │
│  ↓ Extract features (pH, TDS, Nitrate, etc.)               │
│  ↓ Calculate HHI                                           │
│  ↓ Classify quality                                         │
│  Output: processed_data.csv                                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   2. MODEL TRAINING                         │
│                (train_models.py)                             │
├─────────────────────────────────────────────────────────────┤
│  Load: processed_data.csv                                   │
│  ↓                                                           │
│  Split: Train/Test (80/20)                                  │
│  ↓                                                           │
│  Train Classification Models:                                │
│    • Random Forest Classifier                               │
│    • XGBoost Classifier                                     │
│  ↓                                                           │
│  Train Regression Models:                                    │
│    • Random Forest Regressor                                │
│    • XGBoost Regressor                                       │
│  ↓                                                           │
│  Evaluate & Save                                            │
│  Output: 4 model files in models/ folder                    │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                   3. WEB APPLICATION                        │
│                     (app.py)                                │
├─────────────────────────────────────────────────────────────┤
│  Load: Trained models                                       │
│  ↓                                                           │
│  Serve: Interactive Dashboard                               │
│    • Overview Statistics                                    │
│    • Block-wise Analysis                                    │
│    • Real-time Predictions                                  │
│    • Risk Zone Identification                               │
│  ↓                                                           │
│  Provide: API Endpoints                                     │
│    GET /api/stats                                           │
│    GET /api/blocks                                          │
│    GET /api/block_stats/<block>                             │
│    POST /predict                                            │
│  Output: Live Dashboard (http://localhost:5000)             │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Data Flow

### Input → Processing → Output

```
CSV Files → Parse → Extract Features → Calculate Targets
                                 ↓
                    [Classification + Regression]
                                 ↓
                        Train Models → Save
                                 ↓
                          Load Models → Flask App
                                 ↓
                          User Input → Predict
                                 ↓
                         Display Results
```

## 🎯 User Journey

### Scenario 1: View Dashboard
```
User opens → Dashboard loads → Overview tab
    ↓
Views statistics → Quality charts → Pollutant analysis
```

### Scenario 2: Analyze Block
```
User selects → Analysis tab → Chooses block
    ↓
Views block stats → Seasonal trends → Yearly data
```

### Scenario 3: Make Prediction
```
User navigates → Prediction tab → Enters parameters
    ↓
Submits form → Flask processes → Returns results
    ↓
Views quality class → HHI value → Risk level → Recommendations
```

### Scenario 4: Check Risk Zones
```
User navigates → Risk Zones tab → Views table
    ↓
Sees top 10 risky wells → HHI values → Quality classes
```

## 🔧 Technical Architecture

```
┌──────────────┐
│   User       │
│  Browser     │
└──────┬───────┘
       │ HTTP Requests
       ↓
┌──────────────────────────────────────┐
│         Flask Application            │
│  ┌────────────────────────────┐     │
│  │  Routes & API Endpoints    │     │
│  └────────────────────────────┘     │
│  ┌────────────────────────────┐     │
│  │  Load Models               │     │
│  │  - rf_classifier.pkl        │     │
│  │  - rf_regressor.pkl         │     │
│  │  - xgb_classifier.pkl       │     │
│  │  - xgb_regressor.pkl        │     │
│  └────────────────────────────┘     │
│  ┌────────────────────────────┐     │
│  │  Load Data                  │     │
│  │  - processed_data.csv       │     │
│  └────────────────────────────┘     │
└──────────────────────────────────────┘
       │
       ↓
┌──────────────────────────────────────┐
│      Templates & Static Files        │
│  - dashboard.html                     │
│  - style.css                         │
│  - dashboard.js                      │
│  - Chart.js (CDN)                    │
└──────────────────────────────────────┘
```

## 📝 Execution Order

### First Time Setup:
```
1. Install dependencies
   $ pip install -r requirements.txt

2. Process data
   $ python data_preprocessing.py
   
3. Train models
   $ python train_models.py

4. Run application
   $ python app.py
```

### Subsequent Runs:
```
Quick Start:
$ python app.py
(Models are already trained and saved)
```

### Using Automation:
```
$ python run.py
(Runs all steps automatically)
```

## 🎨 Dashboard Tabs Flow

```
┌────────────────────────────────────────────────────┐
│                    DASHBOARD                        │
├────────────────────────────────────────────────────┤
│  Overview | Analysis | Prediction | Risk Zones     │
└────────────────────────────────────────────────────┘
    ↓         ↓            ↓             ↓
  Stats   Block      Input →   Risky
  Charts  Analysis   Predict    Wells
  HHI     Trends     Results    Table
```

## 🔄 Prediction Flow

```
Input Form → Extract Values → Create Feature Array
                                    ↓
                            Load Models
                                    ↓
                    [Classification + Regression]
                                    ↓
                    Get Quality Class + HHI
                                    ↓
                    Calculate Risk Level
                                    ↓
                    Generate Recommendations
                                    ↓
                    Display Results + Charts
```

## 💾 File Dependencies

```
data_preprocessing.py
    ↓ creates
processed_data.csv
    ↓ used by
train_models.py
    ↓ creates
models/*.pkl
    ↓ loaded by
app.py
    ↓ serves
templates/dashboard.html
    ↓ uses
static/css/style.css
static/js/dashboard.js
```

## ✨ Key Features Flow

1. **Data Preprocessing**
   - Reads CSV files
   - Parses parameter strings
   - Calculates HHI
   - Creates quality classes

2. **Model Training**
   - Prepares features
   - Trains classification models
   - Trains regression models
   - Saves models

3. **Web Application**
   - Loads models
   - Provides dashboard
   - Handles predictions
   - Shows results

4. **User Interaction**
   - Views statistics
   - Analyzes blocks
   - Makes predictions
   - Reviews risk zones

---

**End-to-end AI-powered groundwater quality analysis system!** 🌊

