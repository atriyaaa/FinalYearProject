import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Streamlit page config
st.set_page_config(page_title="Cancer Subtype Predictor", layout="wide")
st.title("🧬 Multi-Cancer Subtype Classification (with Explainable AI)")

st.write("Upload your gene expression CSV file (same format as training data):")
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    # Load uploaded data (do NOT set index_col=0)
    df = pd.read_csv(uploaded_file)
    st.write("### Uploaded Data Preview:")
    st.write(df.head())

    # Load model, scaler and selected features
    model = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/new_model.pkl")
    scaler = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/scaler.pkl")
    selected_indices = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/feature_indices.pkl")

    # Prepare data
    if 'vital_status' in df.columns:
        st.warning("'vital_status' column found in uploaded data and will be removed.")
        df = df.drop(columns=['vital_status'])

    # Check and align columns
    if hasattr(scaler, 'feature_names_in_'):
        scaler_feature_names = scaler.feature_names_in_
        missing_cols = [col for col in scaler_feature_names if col not in df.columns]
        extra_cols = [col for col in df.columns if col not in scaler_feature_names]

        if missing_cols:
            st.warning(f"Uploaded file is missing {len(missing_cols)} columns. Filling them with zeros.")
            for col in missing_cols:
                df[col] = 0.0

        if extra_cols:
            st.warning(f"Uploaded file has {len(extra_cols)} extra columns. They will be removed.")
            df = df.drop(columns=extra_cols)

        # Make sure order is correct
        df = df[scaler_feature_names]

    # Scale the data
    scaled_data = scaler.transform(df)

    # Select only model features
    selected_data = scaled_data[:, selected_indices]

    # Predict
    predictions = model.predict(selected_data)

    # Show predictions
    st.write("### Prediction Results:")
    result_df = df.copy()
    result_df["Predicted Class"] = predictions
    st.dataframe(result_df.head())  # Show only head for readability

    st.success("✅ Prediction completed successfully!")
else:
    st.info("Please upload a CSV file to continue.")
