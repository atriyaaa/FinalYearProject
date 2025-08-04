import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import os

# === Paths ===
data_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv"
output_dir = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/plots"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# === Load data ===
df = pd.read_csv(data_path)

# === Separate features and labels ===
metadata_cols = ["barcode", "subtype", "sex", "vital_status", "age"]
X = df.drop(columns=metadata_cols, errors="ignore")
y = df["subtype"]

# === PCA ===
print("🔍 Running PCA...")
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X)

plt.figure(figsize=(10, 7))
sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=y, palette="tab10", s=60, alpha=0.8)
plt.title("PCA - 2D Projection of Gene Expression")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend(title="Subtype", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "pca_2d.png"))
plt.show()

# === t-SNE ===
print("🔍 Running t-SNE (this might take a few minutes)...")
tsne = TSNE(n_components=2, random_state=42, perplexity=30, n_iter=1000)
X_tsne = tsne.fit_transform(X)

plt.figure(figsize=(10, 7))
sns.scatterplot(x=X_tsne[:, 0], y=X_tsne[:, 1], hue=y, palette="tab10", s=60, alpha=0.8)
plt.title("t-SNE - 2D Projection of Gene Expression")
plt.xlabel("t-SNE1")
plt.ylabel("t-SNE2")
plt.legend(title="Subtype", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "tsne_2d.png"))
plt.show()
