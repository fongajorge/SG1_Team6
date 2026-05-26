import pandas as pd
import numpy as np
import os
import sys
import pickle


# Point Python to the simulator/src/ folder to find ml_model.py
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', 'simulator', 'src')
sys.path.append(src_path)

from ml_model import linear_regression, scaler

# Helper function to calculate R-squared for evaluation
def calculate_r2(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    if ss_tot == 0: return 0
    return 1 - (ss_res / ss_tot)

print("Starting Automated Grid Search for the Best ML Brain...")

# ---------------------------------------------------------
# 1. LOAD DATA (Dynamic path to the simulator folder)
# ---------------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
# Points to GreenGridSim/simulator/clean_dataset.csv
data_path = os.path.join(current_dir, '..', 'simulator', 'clean_dataset.csv')

df = pd.read_csv(data_path)
X = df[['Temperature_C', 'Humidity_percent', 'Irradiance_Wm2']].values
y = df['Solar_Generation_kW'].values

# ---------------------------------------------------------
# 2. SCALE FEATURES
# ---------------------------------------------------------
scaler = scaler()
X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------------
# 3. HYPERPARAMETER GRID SEARCH
# ---------------------------------------------------------
# We will test 9 different combinations of parameters
learning_rates = [0.01, 0.05, 0.1]
iterations_list = [1000, 3000, 5000]

best_r2 = -float('inf')
best_model = None
best_params = {}

for lr in learning_rates:
    for iters in iterations_list:
        print(f"Testing Learning Rate: {lr} | Iterations: {iters}...")
        
        # Train
        model = linear_regression(learning_rate=lr, iterations=iters)
        model.fit(X_scaled, y)
        
        # Evaluate
        y_pred = model.predict(X_scaled)
        r2 = calculate_r2(y, y_pred)
        
        print(f"  -> R^2 Score: {r2:.4f}")
        
        # Save the winner
        if r2 > best_r2:
            best_r2 = r2
            best_model = model
            best_params = {'lr': lr, 'iterations': iters}

print("\n" + "="*50)
print(f"WINNING COMBINATION FOUND!")
print(f"Learning Rate: {best_params['lr']}")
print(f"Iterations: {best_params['iterations']}")
print(f"Top R^2 Accuracy: {best_r2:.4f}")
print("="*50 + "\n")

# ---------------------------------------------------------
# 4. DEPLOY THE WINNING BRAIN TO THE SIMULATION
# ---------------------------------------------------------
target_dir = os.path.join(current_dir, '..', 'simulator', 'src')
os.makedirs(target_dir, exist_ok=True)
pkl_path = os.path.join(target_dir, 'trained_brain.pkl')

with open(pkl_path, 'wb') as f:
    pickle.dump({'model': best_model, 'scaler': scaler}, f)

print(f"Best model successfully saved directly to: {pkl_path}")
print("The Brain is automatically in position for the simulation!")
