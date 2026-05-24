# 💧 AI-Enabled Data Science Framework for Groundwater Quality Monitoring and Health Hazard Forecasting

**PRODUCT LINK:** [Live Demo](https://drive.google.com/file/d/1eXqHBE5Cw6MvTYNJZwCWQD_Zvpti5Yv_/view?usp=sharing)

---

## 🌐 Project Overview

Groundwater contamination is a critical public health and environmental challenge, particularly in districts like **Cuddalore, Tamil Nadu**, where contamination levels fluctuate with seasons, hydrogeological conditions, and human activity.

This project delivers an **AI-powered, data science–driven framework** to:
- **Predict** Water Quality Index (WQI) and Health Hazard Index (HHI) across blocks and wells
- **Visualize** seasonal and spatial contamination patterns via GIS
- **Classify** groundwater into Good / Moderate / Poor / Highly Polluted categories
- **Recommend** data-driven interventions for sustainable water management

---

## 📦 Installation

**1. Clone or download the project**

**2. Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**3. Run data preprocessing:**
```bash
python data_preprocessing.py
```

**4. Train models:**
```bash
python train_models.py
```

**5. Start Flask application:**
```bash
python app.py
```

**6. Open browser and navigate to:**
```
http://localhost:5000
```

### Optional: Enable GROK Explainability in Analysis Tab

Set these environment variables so the Analysis table can fetch narrative fields per block (Possible Health Impacts, Vulnerable Population, Recommended Action, Recommended Health Intervention):

**Windows PowerShell (current session):**
```powershell
$env:GROK_API_KEY = "<your_api_key>"
$env:GROK_API_URL = "https://your-grok-endpoint"  # POST endpoint returning JSON
python app.py
```

**Make it permanent:**
```powershell
setx GROK_API_KEY "<your_api_key>"
setx GROK_API_URL "https://your-grok-endpoint"
```

**Expected response JSON keys from your endpoint:**
```
possible_impacts               (string or [string])
vulnerable_population          (string or [string])
recommended_action             (string or [string])
recommended_health_intervention (string or [string])
```

---

## 📁 Project Structure

```
projectFolderMohanSir/
├── data_preprocessing.py        # Data loading and preprocessing
├── train_models.py              # Model training scripts
├── app.py                       # Flask application
├── requirements.txt             # Python dependencies
├── templates/
│   └── dashboard.html           # Dashboard UI
├── static/
│   ├── css/
│   │   └── style.css            # Styling
│   └── js/
│       └── dashboard.js         # Dashboard functionality
├── models/                      # Saved ML models
│   ├── rf_classifier.pkl
│   ├── rf_regressor.pkl
│   ├── xgb_classifier.pkl
│   └── xgb_regressor.pkl
└── data/
    ├── 2018 - 2018.csv          # Data files
    ├── 2019 - 2019.csv
    ├── 2020 - 2020.csv
    └── 2021 - 2021.csv
```

---

## 🏗️ System Architecture

<img width="1045" height="634" alt="image" src="https://github.com/user-attachments/assets/f00aab73-7d09-413d-bb46-8bc52a039337" />

---

## 🔬 Methodology

### Step 1 — Data Collection

Seasonal groundwater samples collected block-wise and well-wise across **27 blocks** in Cuddalore district during:
- **Pre-monsoon**
- **Monsoon**
- **Post-monsoon**

### Step 2 — Data Preprocessing

- Removal of missing, inconsistent, and noisy values
- Normalization of physicochemical parameter units
- Feature selection using PCA and Gini impurity
- Version tracking for temporal traceability

### Step 3 — WQI Computation (Formula)

For each water sample *i* and parameter *j*:

```
Sub-index:    Qj = (Cj / Sj) × 100

WQI:          WQIi = Σ(Wj × Qj) / Σ(Wj)
```

| WQI Range | Water Quality Category |
|-----------|------------------------|
| ≤ 50      | ✅ Good                 |
| 51 – 100  | 🟡 Moderate             |
| 101 – 200 | 🟠 Poor                 |
| > 200     | 🔴 Highly Polluted      |

### Step 4 — HHI Computation (Formula)

```
HHIi = Σ (Cij / RfDj)
```

Where `RfDj` = reference dose / maximum safe exposure for contaminant *j* (as per WHO/BIS standards).

### Step 5 — Model Training

**Random Forest Classifier** (for WQI category):
- Bootstrap sampling on seasonal splits
- Gini impurity-based splits
- Majority voting across *k* decision trees
- Hyperparameter tuning via grid search

**XGBoost Regressor** (for HHI score):
- Gradient boosting with learning rate *η*
- L2 regularization (*λ*)
- Optimal leaf weights computed from gradients and hessians
- Cross-validation with RMSE/MAE/R² evaluation

### Step 6 — Visualization

- GIS-based heatmaps for contamination hotspots
- Block-wise and seasonal trend charts
- Interactive web dashboard built in ReactJS

---

## 📊 Dataset

### Primary Dataset

| Field          | Details                                                                         |
|----------------|---------------------------------------------------------------------------------|
| **Source**     | Cuddalore District Groundwater Data (CSV)                                       |
| **Coverage**   | Block-wise & well-wise, 2018–2021                                               |
| **Seasons**    | Pre-monsoon, Monsoon, Post-monsoon                                              |
| **Parameters** | Nitrate (NO₃), Fluoride (F⁻), pH, TDS, Chloride, Hardness, Sulphates, Alkalinity, Iron |
| **Total Wells**| 862                                                                             |
| **Blocks**     | 27                                                                              |

### External Reference Standards

| Dataset                               | Purpose                                      |
|---------------------------------------|----------------------------------------------|
| WHO Drinking Water Quality Guidelines | Permissible limits for WQI/HHI thresholds    |
| CGWB Groundwater Quality Standards    | National-level trend comparison              |
| Block-wise Census / Admin Boundaries  | GIS spatial segmentation                     |

### Derived Outputs

| Output            | Description                                      |
|-------------------|--------------------------------------------------|
| WQI               | Weighted aggregation of physicochemical parameters |
| HHI               | Concentration-to-standard ratio per contaminant  |
| GIS Layers        | IDW/Kriging spatial interpolation                |
| Risk Class Labels | Good / Moderate / Poor / Highly Polluted         |

---

## 🧩 Modules

### Module 1 — Data Acquisition

- Collects seasonal groundwater quality data from district water board reports and field surveys
- Automated integrity checks for missing/inconsistent values
- Contextual metadata logging (sample site, season, block)

---

### Module 2 — Data Preprocessing & Storage

- Filters, imputes, and normalizes raw data
- Feature selection applied before model training
- Cleaned data stored securely in PostgreSQL/MongoDB

---

### Module 3 — AI Prediction

- Random Forest Classifier → WQI category (Good / Moderate / Poor / Highly Polluted)
- XGBoost Regressor → HHI score (continuous)
- Cross-validation + hyperparameter tuning
- Achieved **R² = 0.94**

### Module 4 — API Management Layer

| Endpoint       | Method | Function                          |
|----------------|--------|-----------------------------------|
| `/api/upload`  | POST   | Upload seasonal groundwater CSV   |
| `/api/predict` | POST   | Run WQI/HHI prediction            |
| `/api/stats`   | GET    | Fetch block/season statistics     |
| `/api/status`  | GET    | API health check                  |

- Built with **FastAPI** for async request handling
- HTTPS-secured, data-validated communication

### Module 5 — Visualization & Reporting
- ReactJS dashboard with dynamic WQI/HHI charts
- GIS heatmaps for contamination hotspot identification
- PDF/CSV report export
- Responsive design across all devices
## 🛠️ Implementation

### Quality Monitoring Dashboard

> **Screenshot placeholder:**
> Save Figure 5.1 as `images/dashboard_quality.png`


- Displays **27 blocks** with average HHI = **0.93**
- Quality distribution pie chart (Good / Moderate / Poor / Highly Polluted)
- Pollutant overview bar chart (Chloride, Fluoride, Hardness, Iron, Nitrate, Alkalinity)
- Worst HHI block highlighted: **Veedhachalam (avg. 2.11)**

---

### AI Model Prediction Interface

> **Screenshot placeholder:**
> Save Figure 5.2 as `images/dashboard_prediction.png`


Input parameters accepted:
- pH, TDS (mg/l), Nitrate (mg/l), Fluoride (mg/l), Iron (mg/l), Chloride (mg/l), Hardness (mg/l), Sulphates (mg/l), Alkalinity (mg/l), Total Coliform (MPN/100ml), E. Coli (MPN/100ml)

Sample output:
```
Quality Class:              Good
Health Hazard Index (HHI):  0.19
Risk Level:                 Low
Recommendation:             Water quality is good. Maintain current practices.
```

---

### Seasonal & Spatial Data Charts

Key observations from the charts:
- Block-wise quality distribution across **862 total wells**
- HHI peaks during **pre-monsoon** season and drops in post-monsoon
- Yearly trends (2018–2020) show elevated HHI in 2019 compared to adjacent years

### Health Hazard Risk Visualization
Top 10 Highest-Risk Wells:

| Well ID      | Block           | Village         | Year | Season      | HHI   | Quality        |
|--------------|-----------------|-----------------|------|-------------|-------|----------------|
| L0028239577  | Keerapalayam    | Kothandavilagam | 2019 | Pre-monsoon | 27.21 | Highly Polluted |
| L0028239502  | Keerapalayam    | Kothandavilagam | 2019 | Pre-monsoon | 22.95 | Highly Polluted |
| L0034550580  | Mangalur        | Vinayaganandhal | 2021 | Monsoon     | 15.23 | Highly Polluted |
| L0027819017  | Kattumannarkoil | Agaraputhur     | 2019 | Pre-monsoon | 14.68 | Highly Polluted |
| L0037187428  | Nallur          | Poolambadi      | 2021 | Pre-monsoon | 13.24 | Highly Polluted |

---

## 📈 Results and Discussion

### Model Performance

| Metric                          | Random Forest (WQI) | XGBoost (HHI) |
|---------------------------------|---------------------|---------------|
| **R² Score**                    | 0.94                | 0.95          |
| **Accuracy**                    | High                | —             |
| **RMSE**                        | Low                 | Low           |
| **Correlation (Nitrate → HHI)** | r = 0.88            | r = 0.88      |

### Key Findings

- **Nitrate** was confirmed as the **primary risk driver** (r = 0.88 correlation with HHI)
- High-risk zones: **Annagramam** and **Kurinjipadi** — elevated nitrate and fluoride
- Associated health hazards: **Methemoglobinemia** (blue baby syndrome) and **Skeletal Fluorosis**
- **Pre-monsoon** season consistently showed the highest contamination levels
- ANN and ensemble models effectively captured **non-linear seasonal variations**

### Contamination by Block (Nitrate and Fluoride)

<img width="971" height="600" alt="image" src="https://github.com/user-attachments/assets/073670dd-6a15-4b16-9279-8788c2dd3fb1" />


The bar chart (Fig. 5.5) compares nitrate (mg/L) and fluoride (×30 scaled) concentrations across four major blocks:

| Block       | Nitrate Level        | Fluoride Level | Risk Profile |
|-------------|----------------------|----------------|--------------|
| Annagramam  | High (~60 mg/L)      | Moderate       | Very High    |
| Cuddalore   | Moderate (~50 mg/L)  | Moderate       | High         |
| Panruti     | Moderate (~45 mg/L)  | High           | High         |
| Kurinjipadi | Very High (~65 mg/L) | Very High      | Extreme      |

---

## 🔁 Comparative Analysis

<img width="1002" height="652" alt="image" src="https://github.com/user-attachments/assets/f436005f-8795-4973-b25e-64496120d549" />

### HHI Score Comparison by Block

| Block       | HHI Score | Risk Level          | Primary Contaminant |
|-------------|-----------|---------------------|---------------------|
| Annagramam  | ~0.80     | 🔴 High             | Nitrate             |
| Cuddalore   | ~0.58     | 🟠 Moderate-High    | Chloride, TDS       |
| Panruti     | ~0.48     | 🟡 Moderate         | Fluoride            |
| Kurinjipadi | ~0.92     | 🔴 Very High        | Nitrate + Fluoride  |

### Comparison with Existing Approaches

| Approach                                        | WQI Accuracy | HHI Prediction | Seasonal Analysis | GIS Integration | Real-Time API |
|-------------------------------------------------|:------------:|:--------------:|:-----------------:|:---------------:|:-------------:|
| Manual Testing (Traditional)                    | ❌           | ❌             | ❌                | ❌              | ❌            |
| Static ML Models (Aju et al., 2024)             | ✅           | ❌             | ❌                | ❌              | ❌            |
| Ensemble + Visualization (Gupta & Verma, 2025)  | ✅           | Partial        | ❌                | ❌              | Partial       |
| PCA + WQI (Singh et al., 2024)                  | ✅           | ❌             | ❌                | Partial         | ❌            |
| **This Framework (Ours)**                       | ✅           | ✅             | ✅                | ✅              | ✅            |

**Advantages of this framework:**
- Integrates both WQI and HHI in a single unified pipeline
- Supports multi-season, multi-block spatiotemporal analysis
- Provides real-time predictions via REST API
- GIS-based contamination hotspot visualization
- Explainable outputs with block-wise health recommendations

---

## 🎥 Implementation Video

[![Implementation Demo — Click to Watch](https://img.shields.io/badge/▶%20Watch%20Demo-Google%20Drive-blue?style=for-the-badge&logo=google-drive)](https://drive.google.com/file/d/1eXqHBE5Cw6MvTYNJZwCWQD_Zvpti5Yv_/view?usp=sharing)

**The demo covers:**
- Quality Monitoring Dashboard walkthrough
- Uploading a seasonal groundwater CSV dataset
- Running WQI and HHI predictions via the AI interface
- Viewing block-wise seasonal trend charts
- Exploring the Health Hazard risk visualization table
- Exporting a health risk report (PDF/CSV)
