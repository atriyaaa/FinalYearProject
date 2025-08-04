import pandas as pd
import joblib

# Load scaler and model
scaler = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/scaler.pkl")
model = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/model.pkl")

# Load merged dataset
df = pd.read_csv("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/merged_dataset.csv", index_col=0)

# Align sample with expected features
expected_features = scaler.feature_names_in_
df_filtered = df[expected_features]

# Select a sample (you can change .iloc[0] to any other index)
sample = df_filtered.iloc[0]

# Scale the sample
scaled_sample = scaler.transform([sample])

# Predict
predicted = model.predict(scaled_sample)

print("Predicted class:", predicted[0])
