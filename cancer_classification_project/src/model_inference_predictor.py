
# import pandas as pd
# import joblib
# import numpy as np

# from sklearn.base import BaseEstimator

# # Load pre-trained components
# model = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/best_model.pkl")
# scaler = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/scaler.pkl")
# label_encoders = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/label_encoders.pkl")

# def predict(input_sample: pd.DataFrame) -> str:
#     """
#     Predict cancer subtype from gene expression sample.
#     input_sample: pd.DataFrame with same structure as training features (genes as columns).
#     """
#     # Preprocess
#     input_scaled = scaler.transform(input_sample)
    
#     # Predict
#     pred_class = model.predict(input_scaled)[0]
    
#     # Decode prediction
#     decoded_class = label_encoders["subtype"].inverse_transform([pred_class])[0]
#     return decoded_class


import joblib
import numpy as np
from sklearn.base import BaseEstimator

# Subtype to cancer mapping
SUBTYPE_TO_CANCER = {
    "BRCA_LumA": "Breast", "BRCA_LumB": "Breast", "BRCA_Her2": "Breast", "BRCA_Basal": "Breast", "BRCA_Normal": "Breast",
    "LUAD": "Lung", "LUSC": "Lung",
    "Clear Cell": "Kidney", "Papillary": "Kidney", "Chromophobe": "Kidney",
    "Prostate Adenocarcinoma, Acinar Type": "Prostate", "Prostate Adenocarcinoma, Other Subtype": "Prostate",
    "STAGE I": "Colorectal", "STAGE II": "Colorectal", "STAGE III": "Colorectal", "STAGE IV": "Colorectal",
    "STAGE IA": "Colorectal", "STAGE IB": "Colorectal", "STAGE IIA": "Colorectal", "STAGE IIB": "Colorectal", "STAGE IIC": "Colorectal",
    "STAGE IIIA": "Colorectal", "STAGE IIIB": "Colorectal", "STAGE IIIC": "Colorectal", "STAGE IVA": "Colorectal", "STAGE IVB": "Colorectal"
}

def predict(pca_input: np.ndarray, model: BaseEstimator) -> dict:
    # 🔄 Load label encoder only when needed (after main.py saves it)
    label_encoders = joblib.load("/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/label_encoders.pkl")
    label_encoder = label_encoders["subtype"]

    pred_class = model.predict(pca_input)[0]
    decoded_subtype = label_encoder.inverse_transform([pred_class])[0]
    cancer_type = SUBTYPE_TO_CANCER.get(decoded_subtype, "Unknown")

    print(f"🔍 DEBUG: Predicted class = {pred_class}")
    print(f"🔍 DEBUG: Decoded subtype = {decoded_subtype}")
    print(f"🔍 DEBUG: Cancer type = {cancer_type}")

    return {
        "subtype": decoded_subtype,
        "cancer_type": cancer_type
    }
