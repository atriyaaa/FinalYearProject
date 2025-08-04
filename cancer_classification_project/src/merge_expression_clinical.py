
import pandas as pd

# Paths
expr_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/ovarian/tcga_ov_expression_matrix_with_barcodes.csv"
clinical_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/ovarian/tcga_ov_clinical.csv"
output_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/ovarian/merged_ovarian.csv"

# Load data
expr_df = pd.read_csv(expr_path)
clinical_df = pd.read_csv(clinical_path)

# Transpose gene expression matrix
expr_df = expr_df.set_index("gene_id").T.reset_index()
expr_df = expr_df.rename(columns={"index": "barcode"})  # matches clinical's sample_id

# Merge
merged_df = pd.merge(clinical_df, expr_df, on="barcode", how="inner")

# Move 'barcode' and clinical columns to the front
clinical_columns = ["barcode", "sex", "age_at_diagnosis", "vital_status", "subtype"]
gene_columns = [col for col in merged_df.columns if col not in clinical_columns]
merged_df = merged_df[clinical_columns + gene_columns]

# Save
merged_df.to_csv(output_path, index=False)
print("✅ Merged file with reordered columns saved.")

