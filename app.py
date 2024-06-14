import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle
import re

# Function to load data
@st.cache_data
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

# Main function to run the app
def main():
    st.title("F1 Race Winner Prediction")

    df = load_data()
    model, scaler = load_model_and_scaler()

    # Extract circuit from URL
    df['circuit'] = df['url'].apply(extract_circuit)

    # Drop the url column and focus on key features
    key_features = ['season', 'circuit', 'weather_dry', 'qualifying_time', 'grid']
    df = df[key_features]

    st.write("Data Preview:")
    st.write(df.head())

    # Prediction Section
    st.header("Make a Prediction")
    input_data = []

    # Input for Season
    season = st.number_input("Input value for season", value=2024, step=1, min_value=int(df['season'].min()))
    input_data.append(season)

    # Input for Circuit
    circuits = df['circuit'].unique()
    circuit = st.selectbox("Select Circuit", options=circuits)
    input_data.extend([1 if c == circuit else 0 for c in circuits])

    # Input for Weather
    weather = st.selectbox("Is it dry?", options=["Yes", "No"])
    weather_dry = 1 if weather == "Yes" else 0
    input_data.append(weather_dry)

    # Input for Qualifying Time
    min_time = 70.342
    max_time = 2146.249
    qualifying_time = st.number_input("Input value for qualifying time (seconds)", min_value=min_time, max_value=max_time, value=float(df['qualifying_time'].mean()))
    input_data.append(qualifying_time)

    # Input for Grid Position
    min_grid = int(df['grid'].min())
    max_grid = int(df['grid'].max())
    grid = st.slider("Input value for grid position", min_value=min_grid, max_value=max_grid, value=int(df['grid'].mean()))
    input_data.append(grid)

    if st.button("Predict"):
        # Ensure all input values are correctly formatted
        formatted_input = np.array(input_data).reshape(1, -1)
        formatted_input = scaler.transform(formatted_input)
        prediction = model.predict(formatted_input)
        st.write(f"Prediction: Driver - {prediction[0]}")

if __name__ == "__main__":
    main()
