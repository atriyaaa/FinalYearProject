import pandas as pd
import numpy as np
import joblib
from sklearn.decomposition import PCA
import os

def rebuild_pca(n_components=50):  # Set default to 50 to match the expected model input
    """
    Rebuilds PCA model based on the current dataset and saved feature list.
    This is useful when there's a mismatch between dataset features and the PCA model.
    
    Parameters:
    -----------
    n_components : int, default=50
        Number of components to keep. Should match what the model expects.
    """
    print("🔧 Rebuilding PCA model...")
    
    # Paths
    dataset_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv"
    feature_names_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/feature_names.pkl"
    pca_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/pca.pkl"
    
    # Load the dataset
    df = pd.read_csv(dataset_path)
    y = df["subtype"]
    X = df.drop(columns=["subtype"])
    
    # Check if feature_names file exists
    if os.path.exists(feature_names_path):
        feature_names = joblib.load(feature_names_path)
        print(f"📋 Loaded {len(feature_names)} feature names from saved file")
        
        # Check for missing columns
        missing_cols = [col for col in feature_names if col not in X.columns]
        if missing_cols:
            print(f"⚠️ Warning: {len(missing_cols)} columns missing from current dataset")
            # Remove missing columns from feature names
            feature_names = [col for col in feature_names if col in X.columns]
            print(f"ℹ️ Using {len(feature_names)} available features")
            
        # Filter to only include saved features
        X = X[feature_names]
    else:
        # No saved feature names - use all except metadata columns
        print("⚠️ No saved feature names found. Using all gene features.")
        # If you have known metadata columns, exclude them
        metadata_cols = ['age', 'sex']  # Add any other non-gene columns
        feature_names = [col for col in X.columns if col not in metadata_cols]
        X = X[feature_names]
        
        # Save these feature names
        joblib.dump(feature_names, feature_names_path)
        print(f"💾 Saved {len(feature_names)} feature names")
    
    # Apply PCA with exactly n_components
    print(f"🧮 Applying PCA with {n_components} components")
    pca = PCA(n_components=n_components, random_state=42)
    pca.fit(X)
    
    # Save the PCA model
    joblib.dump(pca, pca_path)
    print(f"✅ PCA model rebuilt and saved to: {pca_path}")
    print(f"📊 Explained variance ratio: {sum(pca.explained_variance_ratio_):.2%}")
    
    return pca

if __name__ == "__main__":
    # You can change this value if needed, but it should match what your model expects
    rebuild_pca(n_components=50)