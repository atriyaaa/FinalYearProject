

import pandas as pd
import joblib
import shap
import numpy as np
import matplotlib.pyplot as plt
import os

def explain_model(model, X_train, X_test, feature_names=None):
    print("📦 Running XAI explain_model()...")
    output_dir = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/plots"
    os.makedirs(output_dir, exist_ok=True)
    
    # === Use feature importances from the model
    importances = model.feature_importances_
    
    if len(importances) != X_train.shape[1]:
        raise ValueError(f"❌ Feature mismatch: model has {len(importances)} importances, but data has {X_train.shape[1]} columns.")
    
    # === Select top N features
    top_n = min(500, X_train.shape[1])
    top_indices = np.argsort(importances)[-top_n:]
    
    # === Handle DataFrame or ndarray for X_train
    if isinstance(X_train, pd.DataFrame):  # Pandas DataFrame
        X_top = X_train.iloc[:, top_indices]
        top_features = [X_train.columns[i] for i in top_indices]
    else:  # NumPy array (PCA)
        X_top = X_train[:, top_indices]
        if feature_names:
            top_features = [feature_names[i] for i in top_indices]
        else:
            top_features = [f"PC{i+1}" for i in top_indices]
    
    # === Run SHAP TreeExplainer
    print("🔍 Running SHAP explanations...")
    explainer = shap.TreeExplainer(model, feature_perturbation="interventional")
    
    # Convert to numpy array if needed
    X_top_array = X_top if isinstance(X_top, np.ndarray) else X_top.values
    
    # Take a smaller sample to prevent memory issues
    sample_size = min(100, X_top_array.shape[0])
    sample_indices = np.random.choice(X_top_array.shape[0], sample_size, replace=False)
    X_sample = X_top_array[sample_indices]
    
    shap_values = explainer.shap_values(X_sample, check_additivity=False)
    
    # Handle multi-class shap values (which come as a list of arrays)
    if isinstance(shap_values, list):
        # For multi-class, we'll just use the first class for visualization
        # or we can sum across all classes
        print(f"Multi-class SHAP values detected ({len(shap_values)} classes)")
        shap_values_viz = np.abs(np.array(shap_values)).mean(axis=0)
    else:
        shap_values_viz = shap_values
    
    # === Save SHAP summary plot
    print("📈 Saving SHAP summary plot...")
    plt.figure(figsize=(10, 8))
    
    if isinstance(shap_values, list):
        # For multi-class problems
        shap.summary_plot(shap_values[0], X_sample, feature_names=top_features, show=False)
    else:
        # For binary classification
        shap.summary_plot(shap_values_viz, X_sample, feature_names=np.array(top_features), show=False)

    
    plt.savefig(f"{output_dir}/shap_summary_plot.png", bbox_inches="tight")
    plt.close()
    
    # === Save top 20 feature importance chart
    print("📊 Saving top 20 feature importance chart...")
    top_20_count = min(20, len(importances))
    top_20_indices = np.argsort(importances)[-top_20_count:]
    
    if isinstance(X_train, pd.DataFrame):
        top_20_features = [X_train.columns[i] for i in top_20_indices]
    else:
        top_20_features = [feature_names[i] for i in top_20_indices] if feature_names else [f"PC{i+1}" for i in top_20_indices]
    
    top_20_scores = importances[top_20_indices]
    
    plt.figure(figsize=(10, 6))
    plt.barh(range(top_20_count), top_20_scores[::-1])
    plt.yticks(range(top_20_count), top_20_features[::-1])
    plt.xlabel("Importance Score")
    plt.title("Top 20 Important Features (Random Forest)")
    plt.tight_layout()
    plt.savefig(f"{output_dir}/top_20_feature_importance.png")
    plt.close()
    
    print("✅ XAI analysis complete. Plots saved to:", output_dir)

# === Allow standalone run for testing ===
if __name__ == "__main__":
    print("🚀 xai.py started...")
    model_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/best_model.pkl"
    dataset_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv"
    feature_names_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/feature_names.pkl"
    
    model = joblib.load(model_path)
    df = pd.read_csv(dataset_path)
    X = df.drop(columns=["subtype"])
    feature_names = joblib.load(feature_names_path)
    
    # Optional PCA transformation for standalone test
    pca_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/pca.pkl"
    if os.path.exists(pca_path):
        print("📉 Applying PCA for standalone test...")
        pca = joblib.load(pca_path)
        X_pca = pca.transform(X)
        explain_model(model, X_pca, X_pca, feature_names=[f"PC{i+1}" for i in range(X_pca.shape[1])])
    else:
        explain_model(model, X, X, feature_names=X.columns.tolist())