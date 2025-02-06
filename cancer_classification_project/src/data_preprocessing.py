import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

def preprocess_data(input_file, output_file):
    """
    Preprocess the merged dataset:
    - Handle missing values
    - Encode categorical variables
    - Scale numerical features

    Args:
        input_file (str): Path to the merged dataset.
        output_file (str): Path to save the preprocessed dataset.

    Returns:
        None
    """
    # Load dataset
    df = pd.read_csv(input_file)

    # Handle missing values
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Tumour Stage"] = df["Tumour Stage"].fillna(0)
    df["Subtype"] = df["Subtype"].fillna("Unknown")
    df["Smoking"] = df["Smoking"].fillna("Unknown")

    # Encode categorical features
    label_encoder = LabelEncoder()
    df["Subtype"] = label_encoder.fit_transform(df["Subtype"])
    df["Gender"] = label_encoder.fit_transform(df["Gender"])
    df["Smoking"] = label_encoder.fit_transform(df["Smoking"])

    # Scale numerical features
    scaler = StandardScaler()
    df[["Age", "Tumour Stage"]] = scaler.fit_transform(df[["Age", "Tumour Stage"]])

    # Save preprocessed dataset
    df.to_csv(output_file, index=False)
    print(f"Preprocessed dataset saved to: {output_file}")

# Example usage
if __name__ == "__main__":
    preprocess_data("data/merged_dataset.csv", "data/preprocessed_dataset.csv")
