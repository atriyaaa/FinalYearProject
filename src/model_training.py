import os
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report
import pandas as pd
import joblib

# Define BASE_DIR to construct absolute paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
folder_path = os.path.join(BASE_DIR, 'data')

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
                label_column = next((col for col in possible_label_columns if col in data.columns), None)
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

    # Encode labels for multi-class classification
    le = LabelEncoder()
    y = le.fit_transform(y)

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Ensure the models directory exists
    if not os.path.exists('models'):
        os.makedirs('models')

    # Save label encoder and scaler for later use
    joblib.dump(scaler, 'models/scaler.pkl')
    joblib.dump(le, 'models/label_encoder.pkl')

    return X_train, X_test, y_train, y_test, scaler, le

def train_model(X_train, y_train, model_type='random_forest'):
    if model_type == 'random_forest':
        model = RandomForestClassifier(random_state=42)
    elif model_type == 'logistic_regression':
        model = LogisticRegression(max_iter=1000, random_state=42)
    else:
        raise ValueError("Unsupported model type. Choose 'random_forest' or 'logistic_regression'.")

    model.fit(X_train, y_train)
    return model

def save_model(model):
    # Create models directory if it doesn't exist
    if not os.path.exists('models'):
        os.makedirs('models')

    # Save the trained model
    joblib.dump(model, 'models/cancer_model.pkl')
    print("Model saved successfully in the models folder.")

if __name__ == '__main__':
    # Load, combine, and preprocess data
    X_train, X_test, y_train, y_test, scaler, le = load_and_preprocess_data(folder_path)

    # Train the model
    model = train_model(X_train, y_train, model_type='random_forest')

    # Save the model and scaler
    save_model(model)

    # Evaluate model performance
    y_pred = model.predict(X_test)
    print("\nModel Evaluation:\n")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
