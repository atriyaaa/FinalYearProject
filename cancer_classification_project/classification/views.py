import joblib

# Load scaler and label encoder
scaler = joblib.load('models/scaler.pkl')
label_encoder = joblib.load('models/label_encoder.pkl')

# Example of using them for prediction
def preprocess_for_prediction(input_data):
    input_data_scaled = scaler.transform(input_data)  # Scale input data
    return input_data_scaled
