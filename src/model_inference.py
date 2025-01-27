import pickle
import numpy as np

# Load the trained model
with open('models/model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

# Load the scaler and label encoder
with open('models/scaler.pkl', 'rb') as scaler_file:
    scaler = pickle.load(scaler_file)
with open('models/label_encoder.pkl', 'rb') as encoder_file:
    encoder = pickle.load(encoder_file)

def predict(data):
    # Preprocess the input data
    scaled_data = scaler.transform(np.array(data).reshape(1, -1))
    # Make predictions
    prediction = model.predict(scaled_data)
    # Decode the prediction to human-readable labels
    return encoder.inverse_transform(prediction)

# Example usage
if __name__ == "__main__":
    sample_data = [5.2, 3.1, 4.5, 2.3]  # Replace with actual input
    print(predict(sample_data))
