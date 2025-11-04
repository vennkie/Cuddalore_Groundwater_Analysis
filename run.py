"""
Main script to run the complete groundwater quality analysis system
"""
import os
import sys

def main():
    print("="*70)
    print("GROUNDWATER QUALITY ANALYSIS SYSTEM")
    print("="*70)
    
    # Step 1: Data Preprocessing
    print("\n[1/4] Starting data preprocessing...")
    print("-" * 70)
    try:
        os.system("python data_preprocessing.py")
        print("✓ Data preprocessing completed!")
    except Exception as e:
        print(f"✗ Error in data preprocessing: {e}")
        return
    
    # Step 2: Model Training
    print("\n[2/4] Starting model training...")
    print("-" * 70)
    try:
        os.system("python train_models.py")
        print("✓ Model training completed!")
    except Exception as e:
        print(f"✗ Error in model training: {e}")
        return
    
    # Step 3: Check if models exist
    print("\n[3/4] Verifying models...")
    print("-" * 70)
    models_exist = all([
        os.path.exists("models/rf_classifier.pkl"),
        os.path.exists("models/rf_regressor.pkl"),
        os.path.exists("models/xgb_classifier.pkl"),
        os.path.exists("models/xgb_regressor.pkl")
    ])
    
    if models_exist:
        print("✓ All models verified!")
    else:
        print("✗ Some models are missing!")
        print("Please run train_models.py manually")
        return
    
    # Step 4: Start Flask App
    print("\n[4/4] Starting Flask application...")
    print("-" * 70)
    print("✓ Flask app is starting...")
    print("✓ Open your browser and navigate to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70)
    
    try:
        os.system("python app.py")
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
    except Exception as e:
        print(f"\n✗ Error starting Flask app: {e}")

if __name__ == "__main__":
    main()

