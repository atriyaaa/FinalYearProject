# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler, LabelEncoder

# def load_data(filepath):
#     data = pd.read_csv(filepath)
#     return data

# def preprocess_data(data, label_column='label'):
#     X = data.drop(columns=[label_column])
#     y = data[label_column]
    
#     # Encode labels
#     le = LabelEncoder()
#     y = le.fit_transform(y)

    # # Split data
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # # Scale features
    # scaler = StandardScaler()
    # X_train = scaler.fit_transform(X_train)
    # X_test = scaler.transform(X_test)

    # return X_train, X_test, y_train, y_test, scaler, le


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

def load_data(filepath):
    """
    Load data from a CSV file.

    Parameters:
    filepath (str): Path to the CSV file.

    Returns:
    pd.DataFrame: Loaded data as a pandas DataFrame.
    """
    data = pd.read_csv(filepath)
    return data

def preprocess_data(data, label_column='label', scaler_path='scaler.pkl', encoder_path='label_encoder.pkl'):
    """
    Preprocess data by encoding labels, splitting into train/test sets, and scaling features.

    Parameters:
    data (pd.DataFrame): The input data.
    label_column (str): The name of the column containing the target labels.
    scaler_path (str): Path to save the fitted scaler.
    encoder_path (str): Path to save the fitted label encoder.

    Returns:
    tuple: Scaled training and test data (X_train, X_test), training and test labels (y_train, y_test),
           and the fitted scaler and label encoder.
    """
    # Separate features and labels
    X = data.drop(columns=[label_column])
    y = data[label_column]
    
    # Encode labels
    le = LabelEncoder()
    y = le.fit_transform(y)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Save scaler and label encoder for later use
    joblib.dump(scaler, scaler_path)
    joblib.dump(le, encoder_path)

    return X_train, X_test, y_train, y_test, scaler, le
