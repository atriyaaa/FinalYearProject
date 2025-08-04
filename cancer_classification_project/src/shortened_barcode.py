import pandas as pd

# Load gene expression matrix (already has full barcodes from API)
expr_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/breast/tcga_brca_expression_matrix_with_barcodes.csv"
expr_df = pd.read_csv(expr_path)

# 🔧 Shorten TCGA barcodes to 12-character patient ID
def shorten_barcode(barcode):
    return barcode[:12] if barcode.startswith("TCGA") else barcode

# Apply shortening (skip first column which is gene name)
expr_df.columns = [expr_df.columns[0]] + [shorten_barcode(col) for col in expr_df.columns[1:]]

# Save the shortened version
output_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/breast/tcga_brca_expression_matrix_with_barcodes.csv"
expr_df.to_csv(output_path, index=False)

print("✅ Shortened barcodes to patient-level IDs and saved.")
