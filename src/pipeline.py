from data_preprocessing import preprocess_data
from model_training import train_model
from evaluation import evaluate_model
from model_inference import predict

def main():
    # Preprocess the data
    X_train, X_test, y_train, y_test = preprocess_data('data/dataset.csv')

    # Train the model
    model = train_model(X_train, y_train)

    # Evaluate the model
    evaluate_model(model, X_test, y_test)

    # Predict for new data
    sample_data = [5.2, 3.1, 4.5, 2.3]
    print(f"Predicted class: {predict(sample_data)}")

if __name__ == "__main__":
    main()
