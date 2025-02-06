from src.data_standardisation import standardise_datasets

if __name__ == "__main__":
    # Input and output directories
    input_dir = "data"  # Directory containing raw datasets
    output_dir = "standardised_datasets"  # Directory for standardised datasets

    # Define the recommended column structure
    standard_columns = [
        "Cancer Type", "Subtype", "ER Status", "PR Status", "HER2 Status",
        "Tumour Stage", "Smoking", "Chemotherapy", "Age", "Gender"
    ]

    # Run the standardisation process
    standardise_datasets(input_dir, output_dir, standard_columns)
