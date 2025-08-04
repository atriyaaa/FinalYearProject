import pandas as pd
import numpy as np
import joblib
import os
import sys

def check_model_compatibility():
    """
    Checks the compatibility between the saved model, PCA, and feature data.
    Useful for diagnosing issues with the pipeline.
    """
    print("🔍 Checking model compatibility...")
    
    # Define paths
    base_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project"
    model_path = f"{base_path}/models/best_model.pkl"
    pca_path = f"{base_path}/models/pca.pkl"
    feature_names_path = f"{base_path}/models/feature_names.pkl"
    
    # Check if files exist
    files_exist = {
        "Model": os.path.exists(model_path),
        "PCA": os.path.exists(pca_path),
        "Feature names": os.path.exists(feature_names_path)
    }
    
    print("📁 Files status:")
    for file_name, exists in files_exist.items():
        status = "✅ Found" if exists else "❌ Missing"
        print(f" - {file_name}: {status}")
    
    # If any file is missing, we can't continue
    if not all(files_exist.values()):
        print("❌ Some required files are missing. Please run the full pipeline first.")
        sys.exit(1)
    
    # Load the files
    try:
        model = joblib.load(model_path)
        pca = joblib.load(pca_path)
        feature_names = joblib.load(feature_names_path)
        
        print("\n📊 Components summary:")
        print(f" - Model type: {type(model).__name__}")
        
        # Check if model has n_features_in_ attribute
        if hasattr(model, 'n_features_in_'):
            print(f" - Model expects {model.n_features_in_} input features")
        
        print(f" - PCA outputs {pca.n_components_} components")
        print(f" - PCA was trained on {pca.n_features_in_} original features")
        print(f" - Feature names file contains {len(feature_names)} features")
        
        # Check compatibility
        print("\n✅ Compatibility check:")
        
        if hasattr(model, 'n_features_in_'):
            if model.n_features_in_ == pca.n_components_:
                print(" - ✅ Model and PCA dimensions match")
            else:
                print(f" - ❌ Dimension mismatch: Model expects {model.n_features_in_} features, but PCA outputs {pca.n_components_}")
                print("   🔧 Solution: Rebuild PCA with exactly {model.n_features_in_} components")
        
        if pca.n_features_in_ <= len(feature_names):
            print(" - ✅ PCA has enough feature names")
        else:
            print(f" - ❌ PCA was trained with {pca.n_features_in_} features, but feature names list only has {len(feature_names)}")
            
        print("\n🔧 Recommended actions:")
        
        if hasattr(model, 'n_features_in_') and model.n_features_in_ != pca.n_components_:
            print(f" 1. Run rebuild_pca.py with n_components={model.n_features_in_}")
            print("    Command: /usr/local/bin/python3 /Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/src/rebuild_pca.py")
        else:
            print(" - No issues detected that require action")
            
        return True
            
    except Exception as e:
        print(f"❌ Error during compatibility check: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    check_model_compatibility()