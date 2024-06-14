import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import re
import pickle

# Function to extract circuit from URL
def extract_circuit(url):
    match = re.search(r'wiki/(\d+_(.+?)_Grand_Prix)', url)
    if match:
        return match.group(2).replace('_', ' ')
    return "Unknown"

if __name__ == "__main__":
    df = pd.read_csv('data/final_data.csv')

    # Extract circuit from URL
    df['circuit'] = df['url'].apply(extract_circuit)

    # Print column names to debug
    print("Columns in the dataset:", df.columns)

    # Key features to focus on
    key_features = ['season', 'circuit', 'weather_dry', 'qualifying_time', 'grid', 'driver']

    # Check if all key features are present in the dataframe
    missing_features = [feature for feature in key_features if feature not in df.columns]
    if missing_features:
        raise KeyError(f"Missing features in the dataset: {missing_features}")

    df = df[key_features]

    # Prepare the data for training
    X = df.drop(['driver'], axis=1)
    y = df['driver']

    # Encode categorical features
    X = pd.get_dummies(X, columns=['circuit'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

    # Logistic Regression
    model = LogisticRegression(max_iter=10000, random_state=42, multi_class='multinomial')
    model.fit(X_train, y_train)

    # Save the model and scaler
    with open('model/driver_model.pkl', 'wb') as model_file:
        pickle.dump(model, model_file)
    with open('model/scaler.pkl', 'wb') as scaler_file:
        pickle.dump(scaler, scaler_file)
