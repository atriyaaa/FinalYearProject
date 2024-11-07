from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np
import joblib
import os

def load_and_combine_datasets(folder_path):
    all_data = []
    possible_label_columns = ['label', 'target', 'subtype', 'Gene_ID']  # List of possible names for the label column
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            print(f"Loading {file}...")

            try:
                data = pd.read_csv(file_path)
                data.columns = data.columns.str.strip()  # Strip whitespace

                # Find the correct label column in the dataset
                label_column = None
                for col in possible_label_columns:
                    if col in data.columns:
                        label_column = col
                        break

                if label_column:
                    print(f"Using '{label_column}' as the label column for {file}")
                    data.rename(columns={label_column: 'label'}, inplace=True)  # Standardize to 'label'
                    all_data.append(data)
                else:
                    print(f"Warning: No recognized label column found in {file}. Skipping this file.")
            except Exception as e:
                print(f"Error loading {file}: {e}")

    if all_data:
        combined_data = pd.concat(all_data, ignore_index=True)
        return combined_data
    else:
        raise ValueError("No datasets with a recognized label column were found.")

def load_and_preprocess_data(folder_path):
    # Load and combine datasets
    data = load_and_combine_datasets(folder_path)

    # Define features (X) and target label (y)
    X = data.drop(columns=['label'])
    y = data['label']

    # Encode the labels if necessary
    y = y.apply(lambda x: 1 if x == 'positive' else 0)  # Adjust based on your label format

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    return X_train, X_test, y_train, y_test, scaler

def train_model(X_train, y_train):
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

def save_model(model, scaler):
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')

    # Save the trained model
    joblib.dump(model, 'models/breast_cancer_model.pkl')

    # Save the scaler
    joblib.dump(scaler, 'models/scaler.pkl')

if __name__ == '__main__':
    # Specify the folder containing all datasets
    folder_path = 'data'
    
    # Load, combine, and preprocess data
    X_train, X_test, y_train, y_test, scaler = load_and_preprocess_data(folder_path)

    # Train the model
    model = train_model(X_train, y_train)

    # Save the model and scaler
    save_model(model, scaler)

    print("Model and scaler saved successfully in the models folder.")
