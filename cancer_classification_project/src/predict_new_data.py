import joblib
import pandas as pd

# === Load trained components ===
model = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/best_model.pkl")
scaler = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/scaler.pkl")
feature_names = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/feature_names.pkl")
try:
    label_encoders = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/label_encoders.pkl")
except:
    label_encoders = None

def predict_new(sample_df):
    # Step 1: Ensure input contains expected features
    missing = [f for f in feature_names if f not in sample_df.columns]
    if missing:
        raise ValueError(f"Missing {len(missing)} features from input: {missing[:5]}...")

    # Step 2: Reorder and subset to match model's training input
    sample_df = sample_df[feature_names]

    # Step 3: Scale
    scaled = scaler.transform(sample_df)

    # Step 4: Predict
    pred = model.predict(scaled)[0]

    # Step 5: Decode class if encoders exist
    if label_encoders and "subtype" in label_encoders:
        pred = label_encoders["subtype"].inverse_transform([pred])[0]

    return pred

if __name__ == "__main__":
    # Load full dataset and select one sample
    df = pd.read_csv("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv")

    # Drop metadata to match input to feature_names
    if "subtype" in df.columns:
        df = df.drop(columns=["subtype"])
    
    # Predict first row
    sample = df.iloc[[0]]
    try:
        result = predict_new(sample)
        print("✅ Predicted Subtype:", result)
    except Exception as e:
        print("❌ Prediction failed:", e)
