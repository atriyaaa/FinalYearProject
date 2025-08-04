# import pandas as pd
# import numpy as np
# import joblib
# from sklearn.model_selection import train_test_split
# from sklearn.svm import SVC
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.neural_network import MLPClassifier
# from sklearn.preprocessing import LabelEncoder, StandardScaler
# from sklearn.metrics import accuracy_score
# from sklearn.impute import SimpleImputer
# import os

# def train_model(X=None, y=None):
#     print("🚀 train_model.py started...")

#     if X is None or y is None:
#         print("⚠️ No data passed, loading from file...")
#         data_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv"
#         df = pd.read_csv(data_path)

#         # ✅ Remove rare subtypes
#         subtype_counts = df["subtype"].value_counts()
#         valid_classes = subtype_counts[subtype_counts > 1].index
#         df = df[df["subtype"].isin(valid_classes)]

#         y = df["subtype"]
#         X = df.drop(columns=["subtype"])

#     # ✅ Drop metadata columns
#     metadata_cols = ["barcode", "sex", "vital_status", "age", "age_at_diagnosis"]
#     used_features = [col for col in X.columns if col not in metadata_cols]
#     X = X[used_features]
#     print(f"🧬 Using {len(used_features)} gene features for training.")

#     # ✅ Save feature list now so we can align prediction later
#     feature_names_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/feature_names.pkl"
#     joblib.dump(used_features, feature_names_path)

#     # ✅ Save label encoder (if not already encoded)
#     le = LabelEncoder()
#     y_encoded = le.fit_transform(y)

#     # Save label encoder
#     label_encoders = {"subtype": le}
#     joblib.dump(label_encoders, "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/label_encoders.pkl")

#     # ✅ Train/test split
#     print(f"🔀 Splitting train/test sets... ({X.shape[0]} samples)")
#     X_train, X_test, y_train, y_test = train_test_split(
#         X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
#     )

#     # ✅ Impute + scale
#     imputer = SimpleImputer(strategy="mean")
#     scaler = StandardScaler()

#     X_train = pd.DataFrame(imputer.fit_transform(X_train), columns=used_features)
#     X_test = pd.DataFrame(imputer.transform(X_test), columns=used_features)

#     X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=used_features)
#     X_test = pd.DataFrame(scaler.transform(X_test), columns=used_features)

#     # ✅ Save scaler and imputer
#     joblib.dump(scaler, "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/scaler.pkl")
#     joblib.dump(imputer, "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/imputer.pkl")

#     # === Train models ===
#     models = {
#         "SVM": SVC(kernel="rbf", probability=True),
#         "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
#         "NeuralNet": MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=300, random_state=42)
#     }

#     best_model = None
#     best_score = 0
#     best_name = ""

#     print("🧠 Training models...")
#     for name, model in models.items():
#         model.fit(X_train, y_train)
#         preds = model.predict(X_test)
#         acc = accuracy_score(y_test, preds)
#         print(f"🔍 {name} Accuracy: {acc:.4f}")
#         if acc > best_score:
#             best_score = acc
#             best_model = model
#             best_name = name

#     # ✅ Save best model
#     model_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/best_model.pkl"
#     os.makedirs(os.path.dirname(model_path), exist_ok=True)
#     joblib.dump(best_model, model_path)
#     print(f"✅ Saved best model ({best_name}) with accuracy {best_score:.4f} at: {model_path}")
#     print(f"📦 Saved {len(used_features)} training features to: feature_names.pkl")

#     return best_model

# # For standalone runs
# if __name__ == "__main__":
#     train_model()


import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.decomposition import PCA
import os

def train_model(X=None, y=None):
    print("🚀 train_model.py started...")

    if X is None or y is None:
        print("⚠️ No data passed, loading from file...")
        data_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/datasets/final_clean_dataset.csv"
        df = pd.read_csv(data_path)

        # ✅ Remove rare subtypes
        subtype_counts = df["subtype"].value_counts()
        valid_classes = subtype_counts[subtype_counts > 1].index
        df = df[df["subtype"].isin(valid_classes)]

        y = df["subtype"]
        X = df.drop(columns=["subtype"])

    # ✅ Drop metadata columns
    metadata_cols = ["barcode", "sex", "vital_status", "age", "age_at_diagnosis"]
    used_features = [col for col in X.columns if col not in metadata_cols]
    X = X[used_features]
    print(f"🧬 Using {len(used_features)} gene features for training.")

    # ✅ Save feature names
    feature_names_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/feature_names.pkl"
    joblib.dump(used_features, feature_names_path)

    # ✅ y is already encoded by main.py
    y_encoded = y

    # ✅ Train/test split
    print(f"🔀 Splitting train/test sets... ({X.shape[0]} samples)")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, stratify=y_encoded, random_state=42
    )

    # ✅ Impute + scale
    imputer = SimpleImputer(strategy="mean")
    scaler = StandardScaler()

    X_train = pd.DataFrame(imputer.fit_transform(X_train), columns=used_features)
    X_test = pd.DataFrame(imputer.transform(X_test), columns=used_features)

    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=used_features)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=used_features)

    # ✅ Save scaler and imputer
    joblib.dump(scaler, "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/scaler.pkl")
    joblib.dump(imputer, "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/imputer.pkl")

    # ✅ Apply PCA
    print("📉 Applying PCA...")
    pca = PCA(n_components=50)
    X_train = pca.fit_transform(X_train)
    X_test = pca.transform(X_test)

    joblib.dump(pca, "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/pca.pkl")
    print("✅ PCA saved as pca.pkl")

    # === Train models ===
    models = {
        "SVM": SVC(kernel="rbf", probability=True),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
        "NeuralNet": MLPClassifier(hidden_layer_sizes=(128, 64), max_iter=300, random_state=42)
    }

    best_model = None
    best_score = 0
    best_name = ""

    print("🧠 Training models...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds)
        print(f"🔍 {name} Accuracy: {acc:.4f}")
        if acc > best_score:
            best_score = acc
            best_model = model
            best_name = name

    # ✅ Save best model
    model_path = "/Users/atriyasmac/Downloads/final-year-project/cancer_classification_project/models/best_model.pkl"
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(best_model, model_path)
    print(f"✅ Saved best model ({best_name}) with accuracy {best_score:.4f} at: {model_path}")
    print(f"📦 Saved {len(used_features)} training features to: feature_names.pkl")

    return best_model

# For standalone testing
if __name__ == "__main__":
    train_model()
