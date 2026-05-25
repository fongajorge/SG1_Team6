import pandas as pd
import numpy as np
import pickle
from ml_model import linear_regression, scaler as sc

def prepare_and_train():
    csv_filename = 'clean_dataset.csv'
    print(f"Loading dataset: {csv_filename}...")
    df = pd.read_csv(csv_filename)
    
    # Define our features and our target
    feature_columns = ['Temperature_C', 'Humidity_percent', 'Irradiance_Wm2'] 
    target_column = 'Solar_Generation_kW'
    
    X_raw = df[feature_columns].values
    y = df[target_column].values
    
    # ---------------------------------------------------------
    # 2. DATA SCALING
    # ---------------------------------------------------------
    print("\nScaling features...")
    scaler = sc()
    X_scaled = scaler.fit_transform(X_raw)
    
    # ---------------------------------------------------------
    # 3. TRAINING THE MODEL
    # ---------------------------------------------------------
    print("Training Custom Linear Regression Model...")
    model = linear_regression(learning_rate=0.01, iterations=1500)
    model.fit(X_scaled, y)
    
    print("Training complete!")
    print(f"Final Weights: {model.weights}")
    print(f"Final Bias: {model.bias}")
    
    # ---------------------------------------------------------
    # 4. SAVE THE BRAIN
    # ---------------------------------------------------------
    with open('trained_brain.pkl', 'wb') as f:
        pickle.dump({'model': model, 'scaler': scaler}, f)
    print("\nModel and Scaler successfully saved to 'trained_brain.pkl'.")
    print("The Brain is ready for the transplant!")

if __name__ == "__main__":
    prepare_and_train()