import pandas as pd
import numpy as np
import re
from datetime import datetime

def parse_parameter_string(param_string):
    """Parse parameter strings like 'Nitrate[14.000 mg/l]' to extract values"""
    if pd.isna(param_string):
        return {}
    
    params = {}
    # Pattern to match ParameterName[Value Unit]
    pattern = r'(\w+(?:\s+\w+)*)\[([\d.]+)\s*([^\]]+)?\]'
    
    matches = re.finditer(pattern, param_string)
    for match in matches:
        param_name = match.group(1).strip()
        value = float(match.group(2))
        params[param_name] = value
    
    return params

def extract_year_from_date(date_str):
    """Extract year from date string"""
    try:
        if pd.notna(date_str):
            date_obj = datetime.strptime(str(date_str), "%d/%m/%Y")
            return date_obj.year
        return None
    except:
        return None

def determine_season(date_str):
    """Determine season based on month"""
    try:
        if pd.isna(date_str):
            return "Unknown"
        date_obj = datetime.strptime(str(date_str), "%d/%m/%Y")
        month = date_obj.month
        if month in [12, 1, 2, 3, 4, 5]:  # Dec-May: Pre-monsoon
            return "Pre-monsoon"
        elif month in [6, 7, 8, 9]:  # Jun-Sep: Monsoon
            return "Monsoon"
        else:  # Oct-Nov: Post-monsoon
            return "Post-monsoon"
    except:
        return "Unknown"

def calculate_wqi_class(wqi_score):
    """Classify water quality based on WQI score"""
    if wqi_score < 25:
        return "Excellent"
    elif wqi_score < 50:
        return "Good"
    elif wqi_score < 75:
        return "Poor"
    elif wqi_score < 100:
        return "Very Poor"
    else:
        return "Unsuitable"

def calculate_hhi(parameters):
    """Calculate Health Hazard Index based on contaminant levels"""
    # WHO/BIS standards
    standards = {
        'pH': {'min': 6.5, 'max': 8.5},
        'TDS': {'max': 500},
        'Nitrate': {'max': 45},
        'Fluoride': {'max': 1.5},
        'Iron': {'max': 0.3},
        'Chloride': {'max': 250},
        'Hardness': {'max': 200},
        'Sulphates': {'max': 200},
        'Alkalinity': {'max': 120},
        'Total Coliform': {'max': 0},
        'E.Coli': {'max': 0}
    }
    
    hhi = 0
    violations = []
    
    for param, value in parameters.items():
        param_key = param.split()[0]  # Get first word to match standards
        if param_key in standards:
            std = standards[param_key]
            
            # Check violation
            violation = 0
            if 'max' in std:
                # Handle division by zero for cases where max is 0
                if std['max'] == 0 and value > 0:
                    violation = value  # Count any presence as violation
                    hhi += violation
                    violations.append(f"{param}: {value:.2f} (should be 0)")
                elif std['max'] > 0 and value > std['max']:
                    violation = (value / std['max']) - 1
                    hhi += violation
                    violations.append(f"{param}: {value:.2f} (limit: {std['max']})")
            
            if 'min' in std and std['min'] > 0:
                if value < std['min']:
                    violation = 1 - (value / std['min'])
                    hhi += violation
                    violations.append(f"{param}: {value:.2f} (limit: {std['min']}-{std.get('max', 'inf')})")
    
    return max(0, hhi), violations

def load_and_process_data():
    """Load all CSV files and process them"""
    print("Loading CSV files...")
    
    all_data = []
    
    for year in [2018, 2019, 2020, 2021]:
        filename = f"{year} - {year}.csv"
        print(f"Processing {filename}...")
        
        df = pd.read_csv(filename)
        df['Year'] = year
        
        # Extract year from LabTestingDate
        df['TestYear'] = df['LabTestingDate'].apply(extract_year_from_date)
        
        # Determine season
        df['Season'] = df['LabTestingDate'].apply(determine_season)
        
        all_data.append(df)
    
    # Combine all data
    df_combined = pd.concat(all_data, ignore_index=True)
    print(f"Total records: {len(df_combined)}")
    
    return df_combined

def extract_features(df):
    """Extract features from the combined dataframe"""
    print("Extracting features from data...")
    
    features_list = []
    
    for idx, row in df.iterrows():
        if idx % 1000 == 0:
            print(f"Processing row {idx}/{len(df)}")
        
        # Extract parameters
        above_params = parse_parameter_string(row.get('AbovePMandatory', ''))
        below_params = parse_parameter_string(row.get('BelowPMandatory', ''))
        above_emerging = parse_parameter_string(row.get('AbovePEmerging', ''))
        below_emerging = parse_parameter_string(row.get('BelowPEmerging', ''))
        
        # Combine all parameters
        all_params = {**above_params, **below_params, **above_emerging, **below_emerging}
        
        # Initialize feature dict
        features = {
            'Row': row.get('row', idx),
            'BlockName': row.get('BlockName', ''),
            'Year': row.get('Year', row.get('TestYear', 2020)),
            'Season': row.get('Season', 'Unknown'),
            'VillageName': row.get('VillageName', ''),
            'HabitationName': row.get('HabitationName', ''),
            'WellID': row.get('Testid', ''),
            'TypeOfSource': row.get('TypeOfSource', ''),
            'SampleName': row.get('SampleName', ''),
        }
        
        # Extract numeric parameters
        numeric_params = ['pH', 'TDS', 'Nitrate', 'Fluoride', 'Iron', 'Chloride', 
                         'Hardness', 'Sulphates', 'Sulphates', 'Alkalinity', 
                         'Total Coliform', 'E.Coli', 'E.Coli', 'Turbidity', 'Manganese']
        
        for param in numeric_params:
            # Try to find parameter in all_params
            param_key = None
            for key in all_params.keys():
                if param.lower() in key.lower() or key.lower() in param.lower():
                    param_key = key
                    break
            
            if param_key:
                features[param.replace(' ', '_')] = all_params[param_key]
            else:
                features[param.replace(' ', '_')] = 0
        
        features_list.append(features)
    
    feature_df = pd.DataFrame(features_list)
    print(f"Extracted {len(feature_df)} feature records")
    
    return feature_df

def create_targets(feature_df):
    """Create classification and regression targets"""
    print("Creating targets...")
    
    # Calculate HHI for regression target
    hhi_scores = []
    quality_classes = []
    
    for idx, row in feature_df.iterrows():
        params = {
            'pH': row.get('pH', 7.0),
            'TDS': row.get('TDS', 0),
            'Nitrate': row.get('Nitrate', 0),
            'Fluoride': row.get('Fluoride', 0),
            'Iron': row.get('Iron', 0),
            'Chloride': row.get('Chloride', 0),
            'Hardness': row.get('Hardness', 0),
            'Sulphates': row.get('Sulphates', 0),
            'Total Coliform': row.get('Total_Coliform', 0),
            'E.Coli': row.get('E.Coli', 0)
        }
        
        hhi, _ = calculate_hhi(params)
        hhi_scores.append(hhi)
        
        # Classification based on HHI and WHO standards
        violations = []
        
        # Check pH
        ph = params.get('pH', 7)
        if ph < 6.5 or ph > 8.5:
            violations.append('pH')
        
        # Check major pollutants with WHO limits
        if params.get('Nitrate', 0) > 45:
            violations.append('Nitrate')
        if params.get('Fluoride', 0) > 1.5:
            violations.append('Fluoride')
        if params.get('Iron', 0) > 0.3:
            violations.append('Iron')
        if params.get('Chloride', 0) > 250:
            violations.append('Chloride')
        if params.get('TDS', 0) > 500:
            violations.append('TDS')
        if params.get('Hardness', 0) > 200:
            violations.append('Hardness')
        if params.get('Sulphates', 0) > 200:
            violations.append('Sulphates')
        if params.get('Total Coliform', 0) > 0:
            violations.append('Coliform')
        if params.get('E.Coli', 0) > 0:
            violations.append('E.Coli')
        
        # Classify based on HHI and violations
        if hhi == 0 and len(violations) == 0:
            quality_classes.append("Good")
        elif hhi < 0.5 and len(violations) <= 1:
            quality_classes.append("Good")
        elif hhi < 1.5 and len(violations) <= 3:
            quality_classes.append("Moderate")
        elif hhi < 3.0:
            quality_classes.append("Poor")
        else:
            quality_classes.append("Highly Polluted")
    
    feature_df['HHI'] = hhi_scores
    feature_df['Quality_Class'] = quality_classes
    
    print(f"HHI range: {min(hhi_scores):.2f} - {max(hhi_scores):.2f}")
    print(f"Quality class distribution:")
    print(feature_df['Quality_Class'].value_counts())
    
    return feature_df

def main():
    """Main preprocessing function"""
    print("=" * 50)
    print("GROUNDWATER QUALITY DATA PREPROCESSING")
    print("=" * 50)
    
    # Load data
    df_combined = load_and_process_data()
    
    # Extract features
    feature_df = extract_features(df_combined)
    
    # Create targets
    feature_df = create_targets(feature_df)
    
    # Save processed data
    output_file = "processed_data.csv"
    feature_df.to_csv(output_file, index=False)
    print(f"\nProcessed data saved to: {output_file}")
    
    print(f"\nShape: {feature_df.shape}")
    print(f"Columns: {list(feature_df.columns)}")
    
    return feature_df

if __name__ == "__main__":
    df_processed = main()

