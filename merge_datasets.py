import os
import pandas as pd

def merge_standardised_datasets(input_dir, output_file):
    """
    Merge all standardised datasets into a single file.

    Args:
        input_dir (str): Directory containing standardised datasets.
        output_file (str): Path to save the merged dataset.

    Returns:
        None
    """
    # Collect all datasets
    datasets = []
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".csv"):  # Only process .csv files
            file_path = os.path.join(input_dir, file_name)
            try:
                # Load the dataset
                df = pd.read_csv(file_path)
                datasets.append(df)
                print(f"Merged: {file_name}")
            except Exception as e:
                print(f"Error reading {file_name}: {e}")

    # Concatenate all datasets
    if datasets:
        merged_data = pd.concat(datasets, ignore_index=True)
        merged_data.to_csv(output_file, index=False)
        print(f"Merged dataset saved to: {output_file}")
    else:
        print("No datasets found to merge!")

# Run the merging process
if __name__ == "__main__":
    input_dir = "standardised_datasets"  # Folder with standardised files
    output_file = "data/merged_dataset.csv"  # Path for the merged dataset
    merge_standardised_datasets(input_dir, output_file)
