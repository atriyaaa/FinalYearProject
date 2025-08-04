import pandas as pd

# === File paths ===
coad_expr_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/colorectal/tcga_coad_expression_matrix_with_barcodes.csv"
read_expr_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/colorectal/tcga_read_expression_matrix_with_barcodes.csv"
clinical_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/colorectal/tcga_coadread_clinical.csv"
output_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/colorectal/merged_colorectal.csv"

# === Load expression datasets and transpose them ===
coad_expr = pd.read_csv(coad_expr_path)
read_expr = pd.read_csv(read_expr_path)

# Transpose and fix headers
coad_expr = coad_expr.set_index("gene_id").T.reset_index().rename(columns={"index": "barcode"})
read_expr = read_expr.set_index("gene_id").T.reset_index().rename(columns={"index": "barcode"})

# Combine COAD and READ expressions
expr_df = pd.concat([coad_expr, read_expr], axis=0)
expr_df["barcode"] = expr_df["barcode"].str[:12].str.upper()

# === Load and clean clinical data ===
clinical_df = pd.read_csv(clinical_path)
clinical_df["barcode"] = clinical_df["barcode"].astype(str).str[:12].str.upper()

# === Merge clinical with expression ===
merged_df = pd.merge(clinical_df, expr_df, on="barcode", how="inner")

# === Save to CSV ===
merged_df.to_csv(output_path, index=False)
print(f"✅ Merged colorectal clinical and expression data saved to:\n{output_path}")
