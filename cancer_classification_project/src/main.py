
from preprocess_data import preprocess_data
from train_model import train_model
from evaluation import evaluate_model
from model_inference_predictor import predict
from xai import explain_model

import pandas as pd
import joblib
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def main():
    try:
        print("🚀 Starting full pipeline...")

        # Step 1: Preprocess data
        print("🔄 Preprocessing data...")
        preprocess_data()

        # Step 2: Load cleaned dataset
        dataset_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv"
        df = pd.read_csv(dataset_path)
        print(f"📦 Loaded dataset with {df.shape[0]} rows and {df.shape[1]} columns")

        # Step 3: Remove rare subtypes
        subtype_counts = df["subtype"].value_counts()
        valid_subtypes = subtype_counts[subtype_counts > 1].index
        df = df[df["subtype"].isin(valid_subtypes)]

        # Step 4: Split features and labels
        y = df["subtype"]
        X = df.drop(columns=["subtype"])

        # Step 5: Encode string subtype labels into integers
        label_enc = LabelEncoder()
        label_enc.fit(y)
        y_encoded = label_enc.transform(y)

        # ✅ Save the properly encoded label encoder
        model_dir = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models"
        os.makedirs(model_dir, exist_ok=True)
        joblib.dump({"subtype": label_enc}, os.path.join(model_dir, "label_encoders.pkl"))
        print(f"✅ Saved label encoder with classes: {list(label_enc.classes_)}")

        # Step 6: Train/test split
        print("🔀 Splitting train/test sets...")
        X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42)

        # Step 7: Train model
        print("🔧 Training models...")
        train_model(X_train, y_train)

        # Step 8: Load saved components
        feature_names = joblib.load(os.path.join(model_dir, "feature_names.pkl"))
        scaler = joblib.load(os.path.join(model_dir, "scaler.pkl"))
        pca = joblib.load(os.path.join(model_dir, "pca.pkl"))
        best_model = joblib.load(os.path.join(model_dir, "best_model.pkl"))

        # Step 9: Apply PCA transformation
        print("📉 Applying PCA transformation...")
        X_train_scaled = scaler.transform(X_train[feature_names])
        X_test_scaled = scaler.transform(X_test[feature_names])
        X_train_pca = pca.transform(X_train_scaled)
        X_test_pca = pca.transform(X_test_scaled)

        # Step 10: Evaluate model
        print("📊 Evaluating model...")
        evaluate_model(best_model, X_test_pca, y_test, feature_names=[f"PC{i+1}" for i in range(X_test_pca.shape[1])])

        # Step 11: Explain model with SHAP
        print("🧠 Running XAI...")
        explain_model(best_model, X_train_pca, X_test_pca, feature_names=[f"PC{i+1}" for i in range(X_train_pca.shape[1])])

        # Step 12: Predict one sample
        print("🔮 Making predictions...")
        sample = X_test.iloc[[0]]
        sample_scaled = scaler.transform(sample[feature_names])
        sample_pca = pca.transform(sample_scaled)
        result = predict(sample_pca, best_model)

        print(f"✅ Predicted subtype: {result['subtype']}, Cancer type: {result['cancer_type']}")
        print("✅ Pipeline completed successfully!")

    except Exception as e:
        import traceback
        print(f"❌ Error in pipeline: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
