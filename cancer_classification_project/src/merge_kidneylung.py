

import pandas as pd

# === File paths ===
expr_files = [
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/lung/tcga_luad_expression_matrix_with_barcodes.csv",
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/lung/tcga_lusc_expression_matrix_with_barcodes.csv"
]

clinical_files = [
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/lung/tcga_luad_clinical.csv",
    "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/lung/tcga_lusc_clinical.csv"
]

output_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/lung/merged_lung.csv"

# === Load and combine clinical files ===
clinical_dfs = [pd.read_csv(f) for f in clinical_files]
clinical_df = pd.concat(clinical_dfs, ignore_index=True)
if "uuid" in clinical_df.columns:
    clinical_df = clinical_df.drop(columns=["uuid"])
clinical_df["barcode"] = clinical_df["barcode"].astype(str).str.strip().str.upper().str[:12]

# === Load and transpose expression files ===
expr_dfs = []
for path in expr_files:
    df = pd.read_csv(path)
    df = df.rename(columns={df.columns[0]: "gene"})
    df = df.set_index("gene").T.reset_index()
    df = df.rename(columns={"index": "barcode"})
    df["barcode"] = df["barcode"].astype(str).str.strip().str.upper().str[:12]
    expr_dfs.append(df)

expr_df = pd.concat(expr_dfs, ignore_index=True)

# === Merge clinical and expression ===
merged_df = pd.merge(clinical_df, expr_df, on="barcode", how="inner")

# === Save final merged lung dataset ===
merged_df.to_csv(output_path, index=False)
print("✅ Lung data merged and formatted correctly.")
