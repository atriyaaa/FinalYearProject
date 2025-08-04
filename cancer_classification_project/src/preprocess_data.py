
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib

def preprocess_data():
    input_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_merged.csv"
    output_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv"

    df = pd.read_csv(input_path)
    print(f"📥 Original dataset size: {df.shape[0]} rows, {df.shape[1]} columns")

    # ✅ Drop only rows with missing critical info (not all NaNs)
    required_cols = ["subtype", "age", "sex"]
    df = df.dropna(subset=required_cols)
    df = df[df["subtype"].notna()]
    df = df[~df["subtype"].isin(["Unknown"])]

    print(f"✅ After filtering null/unknown subtypes: {df.shape[0]} rows")

    # === Target and metadata
    target_col = "subtype"
    metadata_cols = ["barcode", "subtype", "sex", "vital_status", "age", "tumor_stage"]

    # === Expression features
    X = df.drop(columns=metadata_cols, errors="ignore")

    # Optionally re-add simple clinical features
    if "sex" in df.columns:
        X["sex"] = df["sex"].map({"male": 1, "female": 0})
    if "age" in df.columns:
        X["age"] = df["age"]

    # Fill any remaining NaNs in features
    X = X.fillna(0)

    # === Scale
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # === Combine and save
    final_df = pd.DataFrame(X_scaled, columns=X.columns)
    final_df[target_col] = df[target_col].values

    final_df.to_csv(output_path, index=False)
    joblib.dump(scaler, "scaler.pkl")

    print("✅ Final preprocessed dataset saved:", output_path)
    print("🧬 Final shape:", final_df.shape)
    print("✅ Subtype counts:\n", final_df["subtype"].value_counts())

if __name__ == "__main__":
    preprocess_data()
