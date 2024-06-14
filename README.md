# PredictF1Winners
## Overview

This project aims to predict the winner of an F1 race based on various features such as the season, circuit, weather conditions, qualifying time, and grid position. The project was inspired by the Netflix show **Drive to Survive**, which sparked a deeper interest in the complexities and strategies involved in Formula 1 racing.

## Project Motivation

Watching **Drive to Survive** highlighted the intricate details and data-driven decisions that influence race outcomes. This project is an attempt to leverage machine learning to predict race winners, providing insights into the key factors that determine success on the track.

## Features

The following features are used in the prediction model:
- **Season**: The year of the race season.
- **Circuit**: The location where the race is held.
- **Weather Dry**: A binary indicator of whether the weather was dry.
- **Qualifying Time**: The qualifying time of the driver in seconds.
- **Grid Position**: The starting position of the driver on the grid.

## Tools and Technologies

- **Python**: Programming language used for data processing and model development.
- **Pandas**: Library for data manipulation and analysis.
- **Scikit-learn**: Machine learning library used for model training and evaluation.
- **Streamlit**: Framework used to create the web application for predictions.
- **Matplotlib & Seaborn**: Libraries for data visualization.

## Model Training

The model is trained using a logistic regression algorithm with the following steps:
1. Data preprocessing, including feature extraction and encoding.
2. Splitting the data into training and test sets.
3. Scaling the features using `StandardScaler`.
4. Training a logistic regression model.
5. Evaluating the model using cross-validation and hyperparameter tuning.

## Challenges and Future Work

**Challenges**:
- Ensuring the data is clean and well-prepared for training.
- Handling categorical variables effectively.
- Achieving high accuracy in predictions, as current predictions have some inaccuracies.

**Future Work**:
- Improve the model accuracy by exploring other algorithms and feature engineering techniques.
- Expand the feature set to include more relevant data points.
- Continuously tune and validate the model to get it as close to 100% accuracy as possible.

## Example Predictions

Here are some example predictions made by the model:

| Season | Circuit | Weather Dry | Qualifying Time | Grid Position | Predicted Driver |
|--------|---------|-------------|-----------------|---------------|------------------|
| 2023   | Bahrain | Yes         | 270.26          | 3             | sainz            |

*Note: The current model may not always predict accurately. Ongoing improvements and tuning are planned to enhance prediction accuracy.*

## Conclusion

This project is a step towards understanding and predicting F1 race outcomes using machine learning. While the model is not perfect yet, it lays the foundation for further exploration and improvement.
