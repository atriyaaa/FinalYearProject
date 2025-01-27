# import joblib
# from django.shortcuts import render

# # Load scaler and label encoder
# scaler = joblib.load('models/scaler.pkl')
# label_encoder = joblib.load('models/label_encoder.pkl')

# # Example of using them for prediction
# def preprocess_for_prediction(input_data):
#     input_data_scaled = scaler.transform(input_data)  # Scale input data
#     return input_data_scaled


# def predict_cancer_type(request):
#     # Sample response; replace with your actual view code
#     return render(request, 'classification/index.html')

import os
import joblib
from django.conf import settings
from django.shortcuts import render

# Define paths based on BASE_DIR
scaler_path = os.path.join(settings.BASE_DIR, 'models', 'scaler.pkl')
label_encoder_path = os.path.join(settings.BASE_DIR, 'models', 'label_encoder.pkl')

# Load scaler and label encoder
scaler = joblib.load(scaler_path)
label_encoder = joblib.load(label_encoder_path)

def preprocess_for_prediction(input_data):
    input_data_scaled = scaler.transform(input_data)
    return input_data_scaled

def predict_cancer_type(request):
    return render(request, 'classification/index.html')
