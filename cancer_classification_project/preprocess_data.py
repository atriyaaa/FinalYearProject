from src.data_preprocessing import preprocess_pipeline

# File paths for the datasets
file_paths = {
    "breast": "data/breast_cancer.csv",
    "lung": "data/lung_cancer.csv",
    "ovarian": "data/ovarian_cancer.csv"
}

# Preprocess datasets
harmonised_data, scalers, label_encoder = preprocess_pipeline(file_paths)

# Save the processed dataset
harmonised_data.to_csv("data/harmonised_data.csv", index=False)

# Save the scalers and label encoder for later use
import joblib

joblib.dump(scalers, "models/scalers.pkl")
joblib.dump(label_encoder, "models/label_encoder.pkl")

print("Preprocessing complete. Harmonised dataset saved to 'data/harmonised_data.csv'.")
