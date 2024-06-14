import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle
import re

# Function to load data
def load_data():
    return pd.read_csv('data/final_data.csv')

# Function to load model and scaler
def load_model_and_scaler():
    with open('model/driver_model.pkl', 'rb') as model_file:
        model = pickle.load(model_file)
    with open('model/scaler.pkl', 'rb') as scaler_file:
        scaler = pickle.load(scaler_file)
    return model, scaler

# Function to extract circuit from URL
def extract_circuit(url):
    match = re.search(r'wiki/(\d+_(.+?)_Grand_Prix)', url)
    if match:
        return match.group(2).replace('_', ' ')
    return "Unknown"

# Function to prepare the test data
def prepare_test_data(df, key_features, training_columns):
    # Extract circuit from URL
    df['circuit'] = df['url'].apply(extract_circuit)
    df = df[key_features]

    # Encode categorical features
    df = pd.get_dummies(df, columns=['circuit'])

    # Ensure the columns match the training data
    for col in training_columns:
        if col not in df.columns:
            df[col] = 0

    df = df[training_columns]  # Reorder columns to match training data
    return df

# Load data, model and scaler
df = load_data()
model, scaler = load_model_and_scaler()

# Key features used for prediction
key_features = ['season', 'circuit', 'weather_dry', 'qualifying_time', 'grid', 'driver']

# Prepare the training data to get the columns
df['circuit'] = df['url'].apply(extract_circuit)
df = df[key_features]
X_train = pd.get_dummies(df.drop(columns=['driver']), columns=['circuit'])

# Load test cases
test_cases = [
    {
        'season': 2023,
        'circuit': 'Bahrain',
        'weather_dry': 1,
        'qualifying_time': 270.26,
        'grid': 3,
        'driver': 'max_verstappen'
    },
    # Add more test cases here
]

# Prepare test input
test_input_df = pd.DataFrame(test_cases)
actual_results = test_input_df['driver']
test_input_df.drop(columns=['driver'], inplace=True)

# Encode categorical features
test_input_df = pd.get_dummies(test_input_df, columns=['circuit'])

# Ensure the columns match the training data
for col in X_train.columns:
    if col not in test_input_df.columns:
        test_input_df[col] = 0

test_input_df = test_input_df[X_train.columns]  # Reorder columns to match training data

# Scale the input
scaled_test_input = scaler.transform(test_input_df)

# Make predictions
predictions = model.predict(scaled_test_input)

# Compare actual and predicted results
comparison_df = pd.DataFrame({'Actual': actual_results, 'Predicted': predictions})
print(comparison_df)

# Evaluate accuracy
accuracy = (comparison_df['Actual'] == comparison_df['Predicted']).mean()
print(f"Accuracy: {accuracy:.2f}")
