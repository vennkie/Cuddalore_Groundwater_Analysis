from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd
import numpy as np
import os
import json
from collections import Counter
try:
    import requests
except Exception:
    requests = None

app = Flask(__name__)

# Load models
models = {}
try:
    models['rf_classifier'] = joblib.load('models/rf_classifier.pkl')
    models['xgb_regressor'] = joblib.load('models/xgb_regressor.pkl')
    print("Models loaded successfully!")
except Exception as e:
    print(f"Error loading models: {e}")
    models = {}

# Load processed data for dashboard
df_processed = None
try:
    df_processed = pd.read_csv('processed_data.csv')
    print("Processed data loaded successfully!")
except Exception as e:
    print(f"Error loading data: {e}")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get overall statistics for the dashboard"""
    if df_processed is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    stats = {
        'total_samples': len(df_processed),
        'total_blocks': df_processed['BlockName'].nunique(),
        'years': sorted(df_processed['Year'].unique().tolist()),
        'quality_distribution': df_processed['Quality_Class'].value_counts().to_dict(),
        'avg_hhi': float(df_processed['HHI'].mean()),
        'max_hhi': float(df_processed['HHI'].max()),
        'min_hhi': float(df_processed['HHI'].min()),
    }
    
    return jsonify(stats)

@app.route('/api/blocks')
def get_blocks():
    """Get list of all blocks"""
    if df_processed is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    blocks = df_processed['BlockName'].unique().tolist()
    return jsonify(blocks)

@app.route('/api/block_stats/<block_name>')
def get_block_stats(block_name):
    """Get statistics for a specific block"""
    if df_processed is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    block_data = df_processed[df_processed['BlockName'] == block_name]
    
    if len(block_data) == 0:
        return jsonify({'error': 'Block not found'}), 404
    
    stats = {
        'block_name': block_name,
        'total_samples': len(block_data),
        'quality_distribution': block_data['Quality_Class'].value_counts().to_dict(),
        'avg_hhi': float(block_data['HHI'].mean()),
        'seasonal_data': block_data.groupby('Season')['HHI'].agg(['mean', 'count']).to_dict('index'),
        'yearly_data': block_data.groupby('Year')['HHI'].mean().to_dict(),
    }
    
    return jsonify(stats)

@app.route('/api/season_trends')
def get_season_trends():
    """Get seasonal trends"""
    if df_processed is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    trends = df_processed.groupby(['Year', 'Season']).agg({
        'HHI': 'mean',
        'Quality_Class': lambda x: (x == 'Good').sum()
    }).reset_index()
    
    return jsonify(trends.to_dict('records'))

def _risk_category_from_hhi(hhi_value: float) -> str:
    if hhi_value < 0.5:
        return "Low"
    if hhi_value < 1.0:
        return "Moderate"
    if hhi_value < 2.0:
        return "High"
    return "Severe"

def _wqi_category_for_block(block_df: pd.DataFrame) -> str:
    # Use majority class
    counts = block_df['Quality_Class'].value_counts()
    return counts.idxmax() if not counts.empty else "Unknown"

def _default_health_text(avg_nitrate: float, avg_fluoride: float, risk: str):
    impacts = []
    vulnerable = []
    actions = []
    interventions = []

    if avg_nitrate >= 45:
        impacts.append("Risk of Blue Baby Syndrome (methemoglobinemia)")
        vulnerable.append("Infants, Pregnant Women")
        actions.append("Alternate supply + nitrate removal treatment")
        interventions.append("Health screening; awareness on nitrate-safe water")
    if avg_fluoride >= 1.5:
        impacts.append("Dental/Skeletal fluorosis risk")
        vulnerable.append("Children, Elderly")
        actions.append("Defluoridation + alternate safe supply")
        interventions.append("Dental checkups; distribute fluoride-safe water")
    if not impacts:
        impacts.append("Possible gastrointestinal irritation; monitor contaminants")
        vulnerable.append("General Population")
        actions.append("Continue monitoring and basic treatment")
        interventions.append("Routine water quality testing")

    # Deduplicate and join
    return (
        ", ".join(sorted(set(impacts))),
        ", ".join(sorted(set(vulnerable))),
        ", ".join(sorted(set(actions))),
        ", ".join(sorted(set(interventions))),
    )

def _call_groq_api(payload: dict) -> dict:
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    api_key = "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"
    if not api_url or not api_key or requests is None:
        return {}
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        model = os.environ.get("GROQ_MODEL", "llama-3.1-70b-versatile")

        system_prompt = (
            "You are a groundwater health assistant."
            " Read the provided water quality context and respond ONLY with a compact JSON"
            " containing keys: possible_impacts, vulnerable_population, recommended_action,"
            " recommended_health_intervention. Do not include extra text."
        )

        user_content = (
            "Context:\n" + json.dumps(payload, ensure_ascii=False) +
            "\n\nReturn JSON with exactly these keys."
        )

        body = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "temperature": 0.2,
        }

        resp = requests.post(api_url, headers=headers, data=json.dumps(body), timeout=15)
        if resp.status_code != 200:
            return {}

        data = resp.json()
        choices = data.get("choices", [])
        if not choices:
            return {}
        content = choices[0].get("message", {}).get("content", "").strip()
        if not content:
            return {}
        # Try to parse JSON from content
        try:
            parsed = json.loads(content)
            if isinstance(parsed, dict):
                return parsed
            return {}
        except Exception:
            return {}
    except Exception:
        return {}

@app.route('/api/analysis_table')
def get_analysis_table():
    if df_processed is None:
        return jsonify({'error': 'Data not loaded'}), 500

    groups = df_processed.groupby('BlockName', dropna=False)
    rows = []
    for block, gdf in groups:
        num_wells = gdf['WellID'].nunique() if 'WellID' in gdf.columns else len(gdf)
        avg_nitrate = float(gdf['Nitrate'].mean()) if 'Nitrate' in gdf.columns else 0.0
        avg_fluoride = float(gdf['Fluoride'].mean()) if 'Fluoride' in gdf.columns else 0.0
        hhi_mean = float(gdf['HHI'].mean()) if 'HHI' in gdf.columns else 0.0
        risk_cat = _risk_category_from_hhi(hhi_mean)
        wqi_cat = _wqi_category_for_block(gdf)

        # Default messages
        impacts, vulnerable, action, intervention = _default_health_text(avg_nitrate, avg_fluoride, risk_cat)

        # Optional GROQ explainability
        groq_payload = {
            "task": "groundwater_health_explainability",
            "block": str(block),
            "avg_nitrate": avg_nitrate,
            "avg_fluoride": avg_fluoride,
            "wqi_category": wqi_cat,
            "hhi": hhi_mean,
            "risk_category": risk_cat,
            "instructions": "Return JSON with keys: possible_impacts, vulnerable_population, recommended_action, recommended_health_intervention"
        }
        groq_resp = _call_groq_api(groq_payload)
        if groq_resp:
            possible_impacts = groq_resp.get('possible_impacts', "Groq response missing field: possible_impacts")
            vulnerable_population = groq_resp.get('vulnerable_population', "Groq response missing field: vulnerable_population")
            recommended_action = groq_resp.get('recommended_action', "Groq response missing field: recommended_action")
            recommended_health_intervention = groq_resp.get('recommended_health_intervention', "Groq response missing field: recommended_health_intervention")
            groq_status = "ok"
        else:
            # Strict Groq requirement: no local fallback content
            possible_impacts = "Groq unavailable"
            vulnerable_population = "Groq unavailable"
            recommended_action = "Groq unavailable"
            recommended_health_intervention = "Groq unavailable"
            groq_status = "unavailable"

        rows.append({
            "Block": str(block),
            "Wells": int(num_wells),
            "AvgNitrate": round(avg_nitrate, 2),
            "AvgFluoride": round(avg_fluoride, 2),
            "WQI": wqi_cat,
            "HHI": round(hhi_mean, 2),
            "Risk": risk_cat,
            "PossibleImpacts": possible_impacts,
            "VulnerablePopulation": vulnerable_population,
            "RecommendedAction": recommended_action,
            "RecommendedHealthIntervention": recommended_health_intervention,
            "GroqStatus": groq_status,
        })

    # Sort by risk severity then HHI desc
    severity_order = {"Severe": 3, "High": 2, "Moderate": 1, "Low": 0}
    rows.sort(key=lambda r: (severity_order.get(r["Risk"], 0), r["HHI"]), reverse=True)
    return jsonify(rows)

@app.route('/api/pollutant_data')
def get_pollutant_data():
    """Get pollutant concentration data"""
    if df_processed is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    pollutants = ['pH', 'TDS', 'Nitrate', 'Fluoride', 'Iron', 'Chloride', 'Hardness', 'Sulphates']
    
    pollutant_stats = {}
    for pollutant in pollutants:
        if pollutant in df_processed.columns:
            pollutant_stats[pollutant] = {
                'mean': float(df_processed[pollutant].mean()),
                'max': float(df_processed[pollutant].max()),
                'min': float(df_processed[pollutant].min()),
                'std': float(df_processed[pollutant].std())
            }
    
    return jsonify(pollutant_stats)

@app.route('/predict', methods=['POST'])
def predict():
    """Predict water quality from input parameters"""
    if not models:
        return jsonify({'error': 'Models not loaded'}), 500
    
    try:
        # Get input data
        data = request.json
        
        # Create feature array
        features = np.array([[
            float(data.get('pH', 7.0)),
            float(data.get('TDS', 0)),
            float(data.get('Nitrate', 0)),
            float(data.get('Fluoride', 0)),
            float(data.get('Iron', 0)),
            float(data.get('Chloride', 0)),
            float(data.get('Hardness', 0)),
            float(data.get('Sulphates', 0)),
            float(data.get('Alkalinity', 0)),
            float(data.get('Total_Coliform', 0)),
            float(data.get('E.Coli', 0)),
            float(data.get('Turbidity', 0)),
            float(data.get('Manganese', 0)),
            float(data.get('BlockName_encoded', 0)),
            float(data.get('Season_encoded', 0)),
            float(data.get('Year', 2020)),
        ]])
        
        # Predict: RF for classification, XGB for regression
        quality_class = models['rf_classifier'].predict(features)[0]
        hhi = models['xgb_regressor'].predict(features)[0]
        
        # Get probabilities for classification
        proba = models['rf_classifier'].predict_proba(features)[0]
        classes = models['rf_classifier'].classes_
        
        probabilities = {str(cls): float(prob) for cls, prob in zip(classes, proba)}
        
        # Determine risk level based on HHI
        if hhi < 0.5:
            risk_level = "Low"
        elif hhi < 1.0:
            risk_level = "Moderate"
        elif hhi < 2.0:
            risk_level = "High"
        else:
            risk_level = "Very High"
        
        # Get violations
        violations = []
        standards = {
            'pH': (6.5, 8.5),
            'TDS': 500,
            'Nitrate': 45,
            'Fluoride': 1.5,
            'Iron': 0.3,
            'Chloride': 250,
            'Hardness': 200,
        }
        
        for param, value in data.items():
            if param in standards:
                if isinstance(standards[param], tuple):
                    if value < standards[param][0] or value > standards[param][1]:
                        violations.append(f"{param}: {value} (acceptable range: {standards[param][0]}-{standards[param][1]})")
                else:
                    if value > standards[param]:
                        violations.append(f"{param}: {value} (max allowed: {standards[param]})")
        
        result = {
            'quality_class': quality_class,
            'hhi': float(hhi),
            'risk_level': risk_level,
            'probabilities': probabilities,
            'violations': violations,
            'recommendations': get_recommendations(quality_class, violations)
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def get_recommendations(quality_class, violations):
    """Get recommendations based on quality class and violations"""
    recommendations = []
    
    if quality_class == 'Good':
        recommendations.append("✓ Water quality is good. Maintain current practices.")
        recommendations.append("Continue regular monitoring.")
    
    elif quality_class == 'Moderate':
        recommendations.append("⚠ Water quality is moderate. Review treatment processes.")
        recommendations.append("Implement additional filtration if needed.")
    
    elif quality_class == 'Poor':
        recommendations.append("⚠ Water quality is poor. Immediate action required.")
        recommendations.append("Install reverse osmosis or advanced filtration system.")
        recommendations.append("Consider alternative water sources.")
    
    elif quality_class == 'Highly Polluted':
        recommendations.append("🚨 Water is highly polluted. Not suitable for consumption.")
        recommendations.append("Stop using this water source immediately.")
        recommendations.append("Install comprehensive treatment system or find alternative source.")
        recommendations.append("Conduct detailed water quality audit.")
    
    if violations:
        recommendations.append("")
        recommendations.append("Specific issues to address:")
        recommendations.extend(violations[:5])  # Limit to 5 violations
    
    return recommendations

@app.route('/api/top_risky_wells')
def get_top_risky_wells():
    """Get top 10 wells with highest HHI"""
    if df_processed is None:
        return jsonify({'error': 'Data not loaded'}), 500
    
    # Get top risky wells
    top_risky = df_processed.nlargest(10, 'HHI')[
        ['WellID', 'BlockName', 'VillageName', 'Year', 'Season', 'HHI', 'Quality_Class']
    ]
    
    return jsonify(top_risky.to_dict('records'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)

