from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np

# Load the model and scaler
model = joblib.load('models/breast_cancer_model.pkl')
scaler = joblib.load('models/scaler.pkl')

# Initialize the Flask app
app = Flask(__name__)

# Serve the HTML form
@app.route('/')
def home():
    return render_template('index.html')  # This will look for 'index.html' in a 'templates' folder

# Define the prediction endpoint that handles form submissions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the form as a list of numbers
        data = [float(x) for x in request.form.values()]  # Convert form values to floats
        
        # Convert data to numpy array and reshape it for the model
        data = np.array(data).reshape(1, -1)
        
        # Scale the data using the previously saved scaler
        scaled_data = scaler.transform(data)
        
        # Make a prediction using the loaded model
        prediction = model.predict(scaled_data)
        
        # Display the result on the webpage
        return render_template('index.html', prediction_text=f'Predicted Class: {int(prediction[0])}')
    
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
