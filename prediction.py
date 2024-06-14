import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score
from sklearn.model_selection import train_test_split

def score_classification(model, X_test, y_test):
    prediction_df = pd.DataFrame(model.predict_proba(X_test), columns=['proba_0', 'proba_1'])
    prediction_df['actual'] = y_test.reset_index(drop=True)
    prediction_df.sort_values('proba_1', ascending=False, inplace=True)
    prediction_df.reset_index(inplace=True, drop=True)
    prediction_df['predicted'] = prediction_df.index
    prediction_df['predicted'] = prediction_df['predicted'].map(lambda x: 1 if x == 0 else 0)
    return precision_score(prediction_df['actual'], prediction_df['predicted'])

if __name__ == "__main__":
    df = pd.read_csv('data/final_data.csv')

    # Drop the url column
    if 'url' in df.columns:
        df = df.drop(columns=['url'])

    # Classification
    df['podium'] = df['podium'].map(lambda x: 1 if x == 1 else 0)
    X = df.drop(['driver', 'podium'], axis=1)
    y = df['podium']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X_train.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X_test.columns)

    # Logistic Regression
    model = LogisticRegression(max_iter=10000, random_state=42)
    model.fit(X_train, y_train)
    model_score = score_classification(model, X_test, y_test)

    # check the model score
    print(f'Logistic Regression Model Precision Score: {model_score}')
