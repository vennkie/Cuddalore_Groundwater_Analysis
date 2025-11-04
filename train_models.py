import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import xgboost as xgb
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns

def load_processed_data():
    """Load the processed data"""
    print("Loading processed data...")
    df = pd.read_csv("processed_data.csv")
    print(f"Data shape: {df.shape}")
    return df

def prepare_features(df):
    """Prepare features and targets for model training"""
    print("\nPreparing features...")
    
    # Select feature columns (numeric only for now)
    feature_cols = ['pH', 'TDS', 'Nitrate', 'Fluoride', 'Iron', 'Chloride', 
                   'Hardness', 'Sulphates', 'Sulphates', 'Alkalinity', 
                   'Total_Coliform', 'E.Coli', 'Turbidity', 'Manganese']
    
    # Add categorical encoding
    df['BlockName_encoded'] = pd.Categorical(df['BlockName']).codes
    df['Season_encoded'] = pd.Categorical(df['Season']).codes
    df['TypeOfSource_encoded'] = pd.Categorical(df['TypeOfSource']).codes
    
    # Select features
    X_cols = feature_cols + ['BlockName_encoded', 'Season_encoded', 'Year']
    
    # Remove rows with missing values in key features
    df_clean = df.dropna(subset=feature_cols)
    
    # Fill remaining NaN with 0
    df_clean = df_clean.fillna(0)
    
    # Prepare X and y
    X = df_clean[X_cols]
    
    # Classification target
    y_class = df_clean['Quality_Class']
    
    # Regression target
    y_reg = df_clean['HHI']
    
    print(f"Feature shape: {X.shape}")
    print(f"\nTarget distribution:")
    print(y_class.value_counts())
    print(f"\nHHI statistics:")
    print(f"Mean: {y_reg.mean():.2f}, Std: {y_reg.std():.2f}")
    print(f"Min: {y_reg.min():.2f}, Max: {y_reg.max():.2f}")
    
    return X, y_class, y_reg, df_clean

def train_classification_model(X_train, y_train, X_test, y_test):
    """Train classification model"""
    print("\n" + "="*50)
    print("TRAINING CLASSIFICATION MODEL")
    print("="*50)
    
    # Train Random Forest
    print("\nTraining Random Forest Classifier...")
    rf_model = RandomForestClassifier(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    rf_model.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = rf_model.predict(X_train)
    y_test_pred = rf_model.predict(X_test)
    
    # Evaluation
    print("\nTraining Accuracy:", accuracy_score(y_train, y_train_pred))
    print("Test Accuracy:", accuracy_score(y_test, y_test_pred))
    print("\nClassification Report:")
    print(classification_report(y_test, y_test_pred))
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_test_pred)
    print("\nConfusion Matrix:")
    print(cm)
    
    # Feature Importance
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10))
    
    return rf_model, feature_importance

def train_regression_model(X_train, y_train, X_test, y_test):
    """Train regression model"""
    print("\n" + "="*50)
    print("TRAINING REGRESSION MODEL")
    print("="*50)
    
    # Train Random Forest Regressor
    print("\nTraining Random Forest Regressor...")
    rf_regressor = RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    rf_regressor.fit(X_train, y_train)
    
    # Predictions
    y_train_pred = rf_regressor.predict(X_train)
    y_test_pred = rf_regressor.predict(X_test)
    
    # Evaluation
    print("\nTraining Metrics:")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_train, y_train_pred)):.2f}")
    print(f"MAE: {mean_absolute_error(y_train, y_train_pred):.2f}")
    print(f"R²: {r2_score(y_train, y_train_pred):.2f}")
    
    print("\nTest Metrics:")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_test_pred)):.2f}")
    print(f"MAE: {mean_absolute_error(y_test, y_test_pred):.2f}")
    print(f"R²: {r2_score(y_test, y_test_pred):.2f}")
    
    # Feature Importance
    feature_importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf_regressor.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 10 Important Features:")
    print(feature_importance.head(10))
    
    return rf_regressor, feature_importance

def train_xgboost_classifier(X_train, y_train, X_test, y_test):
    """Train XGBoost classification model"""
    print("\n" + "="*50)
    print("TRAINING XGBOOST CLASSIFIER")
    print("="*50)
    
    # Encode labels
    label_dict = {'Good': 0, 'Moderate': 1, 'Poor': 2, 'Highly Polluted': 3}
    y_train_encoded = y_train.map(label_dict)
    y_test_encoded = y_test.map(label_dict)
    
    # Train XGBoost
    xgb_model = xgb.XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    
    xgb_model.fit(X_train, y_train_encoded)
    
    # Predictions
    y_test_pred = xgb_model.predict(X_test)
    
    # Convert back to labels
    reverse_label_dict = {v: k for k, v in label_dict.items()}
    y_test_pred_labels = pd.Series([reverse_label_dict[pred] for pred in y_test_pred])
    y_test_labels = y_test.map(label_dict).map(reverse_label_dict)
    
    # Evaluation
    print("Test Accuracy:", accuracy_score(y_test_labels, y_test_pred_labels))
    print("\nClassification Report:")
    print(classification_report(y_test_labels, y_test_pred_labels))
    
    return xgb_model, label_dict

def train_xgboost_regressor(X_train, y_train, X_test, y_test):
    """Train XGBoost regression model"""
    print("\n" + "="*50)
    print("TRAINING XGBOOST REGRESSOR")
    print("="*50)
    
    # Train XGBoost
    xgb_regressor = xgb.XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    )
    
    xgb_regressor.fit(X_train, y_train)
    
    # Predictions
    y_test_pred = xgb_regressor.predict(X_test)
    
    # Evaluation
    print("\nTest Metrics:")
    print(f"RMSE: {np.sqrt(mean_squared_error(y_test, y_test_pred)):.2f}")
    print(f"MAE: {mean_absolute_error(y_test, y_test_pred):.2f}")
    print(f"R²: {r2_score(y_test, y_test_pred):.2f}")
    
    return xgb_regressor

def save_models(rf_classifier, rf_regressor, xgb_classifier, xgb_regressor, feature_importance_clf, feature_importance_reg):
    """Save trained models and results"""
    print("\n" + "="*50)
    print("SAVING MODELS")
    print("="*50)
    
    # Create models directory
    os.makedirs("models", exist_ok=True)
    
    # Save models
    joblib.dump(rf_classifier, "models/rf_classifier.pkl")
    print("Saved: models/rf_classifier.pkl")
    
    joblib.dump(rf_regressor, "models/rf_regressor.pkl")
    print("Saved: models/rf_regressor.pkl")
    
    joblib.dump(xgb_classifier, "models/xgb_classifier.pkl")
    print("Saved: models/xgb_classifier.pkl")
    
    joblib.dump(xgb_regressor, "models/xgb_regressor.pkl")
    print("Saved: models/xgb_regressor.pkl")
    
    # Save feature importance
    feature_importance_clf.to_csv("models/feature_importance_clf.csv", index=False)
    feature_importance_reg.to_csv("models/feature_importance_reg.csv", index=False)
    
    print("\nAll models and results saved successfully!")

def main():
    """Main training function"""
    print("=" * 50)
    print("GROUNDWATER QUALITY MODEL TRAINING")
    print("=" * 50)
    
    # Load data
    df = load_processed_data()
    
    # Prepare features
    X, y_class, y_reg, df_clean = prepare_features(df)
    
    # Split data
    X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
        X, y_class, y_reg, test_size=0.2, random_state=42, stratify=y_class
    )
    
    print(f"\nTrain size: {len(X_train)}, Test size: {len(X_test)}")
    
    # Train models
    rf_classifier, feat_imp_clf = train_classification_model(X_train, y_class_train, X_test, y_class_test)
    rf_regressor, feat_imp_reg = train_regression_model(X_train, y_reg_train, X_test, y_reg_test)
    xgb_classifier, label_dict = train_xgboost_classifier(X_train, y_class_train, X_test, y_class_test)
    xgb_regressor = train_xgboost_regressor(X_train, y_reg_train, X_test, y_reg_test)
    
    # Save everything
    save_models(rf_classifier, rf_regressor, xgb_classifier, xgb_regressor, feat_imp_clf, feat_imp_reg)
    
    print("\n" + "="*50)
    print("TRAINING COMPLETE!")
    print("="*50)
    
    return rf_classifier, rf_regressor, xgb_classifier, xgb_regressor

if __name__ == "__main__":
    models = main()

