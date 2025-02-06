import os
import pandas as pd
import numpy as np

def standardise_datasets(input_dir, output_dir, standard_columns):
    """
    Standardise all datasets to a unified format, filling irrelevant columns with NaN.

    Args:
        input_dir (str): Directory containing raw datasets.
        output_dir (str): Directory to save standardised datasets.
        standard_columns (list): List of columns in the recommended format.

    Returns:
        None
    """
    os.makedirs(output_dir, exist_ok=True)

    # Minimal log: Display detected files
    print(f"Looking for datasets in: {input_dir}")
    files = os.listdir(input_dir)
    print(f"Files found: {len(files)} files")

    for file_name in files:
        if file_name.endswith((".csv", ".tsv")):
            file_path = os.path.join(input_dir, file_name)
            sep = "," if file_name.endswith(".csv") else "\t"

            try:
                # Load dataset
                df = pd.read_csv(file_path, sep=sep)

                # Assign cancer type
                if "breast" in file_name.lower():
                    cancer_type = "Breast"
                elif "lung" in file_name.lower():
                    cancer_type = "Lung"
                else:
                    cancer_type = "Unknown"

                df["Cancer Type"] = cancer_type

                # Standardise columns
                df = df.reindex(columns=standard_columns, fill_value=np.nan)

                # Save standardised dataset
                output_file = os.path.splitext(file_name)[0] + ".csv"
                output_path = os.path.join(output_dir, output_file)
                df.to_csv(output_path, index=False, na_rep="N/A")

                # Minimal log: File processed
                print(f"Processed: {file_name}")

            except Exception as e:
                print(f"Error processing {file_name}: {e}")
