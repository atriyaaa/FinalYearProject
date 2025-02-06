from data_preprocessing import preprocess_data
from model_training import train_model
from evaluation import evaluate_model
from model_inference import predict


def main():
    try:
        print("Starting pipeline...")

        # Step 1: Preprocess the data
        print("Preprocessing data...")
        X_train, X_test, y_train, y_test = preprocess_data('data/merged_dataset.csv')

        # Step 2: Train the model
        print("Training the model...")
        model = train_model(X_train, y_train)

        # Step 3: Evaluate the model
        print("Evaluating the model...")
        evaluate_model(model, X_test, y_test)

        # Step 4: Predict for new data
        print("Making predictions for new data...")
        sample_data = [[5.2, 3.1, 4.5, 2.3]]  # Example new data
        predicted_class = predict(model, sample_data)
        print(f"Predicted class: {predicted_class}")

        print("Pipeline completed successfully!")

    except Exception as e:
        print(f"An error occurred in the pipeline: {e}")


if __name__ == "__main__":
    main()
