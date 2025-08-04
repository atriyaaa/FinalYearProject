import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import os

# === File paths ===
input_path = '/Users/atriyasmac/Downloads/gene_expression_matrix_with_uuid.csv'
output_path = '/Users/atriyasmac/Downloads/gene_expression_matrix_normalized.csv'

print("📥 Loading raw expression matrix...")
df = pd.read_csv(input_path, index_col=0)

# === Convert all values to numeric ===
print("🧹 Converting all values to numeric...")
df = df.apply(pd.to_numeric, errors='coerce')

# === Drop all-NaN rows/columns ===
print("🧼 Dropping all-NaN rows/columns...")
df.dropna(axis=0, how='all', inplace=True)
df.dropna(axis=1, how='all', inplace=True)

# === Sanity check ===
if df.empty:
    print("❌ Error: Expression matrix is empty after cleaning.")
    exit(1)

# === Log2 transform with pseudocount ===
print("🔁 Applying log2 transformation...")
df_log = np.log2(df + 1)

# === Min-Max scale each gene (row-wise) ===
print("📊 Applying Min-Max scaling...")
scaler = MinMaxScaler()
scaled_array = scaler.fit_transform(df_log.T).T  # scale each gene across samples

df_scaled = pd.DataFrame(
    scaled_array,
    index=df_log.index,
    columns=df_log.columns
)

# === Save normalized matrix ===
df_scaled.to_csv(output_path)
print(f"✅ Normalized matrix saved to: {output_path}")
print("🧪 Final shape:", df_scaled.shape)
