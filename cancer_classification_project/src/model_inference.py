import os
import pickle
import numpy as np

# Load the trained model, scaler, and label encoder
def load_model_assets():
    try:
        # Load the model
        with open('models/model.pkl', 'rb') as model_file:
            model = pickle.load(model_file)

        # Load the scaler
        with open('models/scaler.pkl', 'rb') as scaler_file:
            scaler = pickle.load(scaler_file)

        # Load the label encoder
        with open('models/label_encoder.pkl', 'rb') as encoder_file:
            encoder = pickle.load(encoder_file)

        print("Model, scaler, and label encoder loaded successfully.")
        return model, scaler, encoder

    except FileNotFoundError as e:
        print(f"Error: {e}. Ensure all required files (model.pkl, scaler.pkl, label_encoder.pkl) exist in the 'models' directory.")
        raise


# Prediction function
def predict(data):
    # Load model, scaler, and encoder
    model, scaler, encoder = load_model_assets()

    # Verify input data shape
    if len(data) != scaler.mean_.shape[0]:
        raise ValueError(f"Expected {scaler.mean_.shape[0]} features, but got {len(data)} features.")

    # Preprocess the input data
    scaled_data = scaler.transform(np.array(data).reshape(1, -1))

    # Make predictions
    prediction = model.predict(scaled_data)

    # Decode the prediction to human-readable labels
    return encoder.inverse_transform(prediction)[0]


# Example usage
if __name__ == "__main__":
    # Replace with actual input data
    sample_data = [5.2, 3.1, 4.5, 2.3]  # Ensure this matches the feature count
    try:
        predicted_class = predict(sample_data)
        print(f"Predicted class: {predicted_class}")
    except Exception as e:
        print(f"An error occurred during prediction: {e}")
