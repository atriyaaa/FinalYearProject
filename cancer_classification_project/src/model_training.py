# Import necessary libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, roc_auc_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
import joblib
import lime.lime_tabular
import shap
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# Load and preprocess data
def load_and_preprocess_data(folder_path):
    print("Loading and preprocessing data...")
    data = pd.concat(
        [pd.read_csv(os.path.join(folder_path, file)) for file in os.listdir(folder_path) if file.endswith('.csv')],
        ignore_index=True
    )
    label_col = 'Subtype'
    if label_col not in data.columns:
        raise ValueError(f"Label column '{label_col}' not found in dataset.")
    
    # Replace nan in labels
    data[label_col] = data[label_col].fillna('Unknown')
    data[label_col] = data[label_col].astype(str)

    # Features and target
    X = data.drop(columns=[label_col])
    y = data[label_col]

    # Handle categorical features
    categorical_columns = X.select_dtypes(include=['object', 'category']).columns
    X = pd.get_dummies(X, columns=categorical_columns, drop_first=True)

    # Handle missing values
    imputer = SimpleImputer(strategy='mean')
    X = pd.DataFrame(imputer.fit_transform(X), columns=X.columns)

    # Encode target labels
    le = LabelEncoder()
    y = le.fit_transform(y)

    # Standardise features
    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    # Save preprocessing objects
    joblib.dump(scaler, os.path.join(MODELS_DIR, 'scaler.pkl'))
    joblib.dump(le, os.path.join(MODELS_DIR, 'label_encoder.pkl'))
    joblib.dump(imputer, os.path.join(MODELS_DIR, 'imputer.pkl'))

    print("Data loaded and preprocessed.")
    return train_test_split(X, y, test_size=0.2, stratify=y, random_state=42), scaler, le

# Handle class imbalance
def handle_class_imbalance(X_train, y_train):
    print("Handling class imbalance...")
    smote = SMOTE(random_state=42, k_neighbors=2)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
    print(f"Class distribution after SMOTE: {dict(pd.Series(y_resampled).value_counts())}")
    print("Class imbalance handled.")
    return X_resampled, y_resampled

# Apply PCA
def apply_pca(X, n_components=50):
    print("Applying PCA...")
    pca = PCA(n_components=n_components, random_state=42)
    X_pca = pca.fit_transform(X)
    print(f"Explained variance ratio (first {n_components} components): {pca.explained_variance_ratio_.sum():.2f}")
    print("PCA applied.")
    return X_pca, pca

# Apply t-SNE
def apply_tsne(X, y, sample_size=2000):
    print("Applying t-SNE...")
    if len(X) > sample_size:
        indices = np.random.choice(len(X), sample_size, replace=False)
        X, y = X[indices], y[indices]
    tsne = TSNE(n_components=2, random_state=42)
    X_tsne = tsne.fit_transform(X)
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(X_tsne[:, 0], X_tsne[:, 1], c=y, cmap='viridis', alpha=0.7)
    plt.colorbar(scatter, label="Classes")
    plt.title("t-SNE Visualization")
    plt.xlabel("t-SNE Component 1")
    plt.ylabel("t-SNE Component 2")
    plt.savefig(os.path.join(MODELS_DIR, 'tsne_visualisation.png'))
    plt.show()
    print("t-SNE visualization saved.")
    return X_tsne

# Hyperparameter tuning
def tune_hyperparameters(model, param_grid, X_train, y_train):
    print("Starting hyperparameter tuning...")
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=3, scoring='accuracy', verbose=1)
    grid_search.fit(X_train, y_train)
    print("Hyperparameter tuning completed.")
    return grid_search.best_estimator_

# Train neural network
def train_neural_network(X_train, y_train, X_val, y_val, input_dim, num_classes):
    print("Training Neural Network...")
    model = Sequential([
        Dense(128, activation='relu', input_shape=(input_dim,)),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=20,
        batch_size=32,
        verbose=1
    )
    print("Neural Network trained.")
    return model

#train SVM
def train_svm(X_train, X_test, y_train, y_test):
    print("Training SVM model...")

    # Create and train the SVM model
    svm_model = SVC(kernel='linear', probability=True, random_state=42)
    svm_model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = svm_model.predict(X_test)
    print("\nClassification Report for SVM:")
    print(classification_report(y_test, y_pred))

    print("\nConfusion Matrix for SVM:")
    print(confusion_matrix(y_test, y_pred))

    # Save the model
    joblib.dump(svm_model, 'models/svm_model.pkl')
    print("SVM model saved at 'models/svm_model.pkl'")

    return svm_model

#tune SVM
def tune_svm(X_train, y_train):
    print("Tuning SVM hyperparameters...")
    
    # Parameter grid for tuning
    param_grid = {
        'C': [0.1, 1, 10, 100],
        'kernel': ['linear', 'rbf', 'poly'],
        'gamma': ['scale', 'auto']
    }

    # Perform grid search
    grid_search = GridSearchCV(SVC(probability=True, random_state=42), param_grid, cv=3, scoring='accuracy', n_jobs=-1)
    grid_search.fit(X_train, y_train)

    print("Best Parameters:", grid_search.best_params_)
    return grid_search.best_estimator_

# #explain model with LIME
# def explain_with_lime(model, X_train, X_test, feature_names):
#     print("Generating LIME explanations...")
    
#     explainer = lime.lime_tabular.LimeTabularExplainer(X_train, training_labels=y_train, mode='classification', feature_names=feature_names)

#     # Explain one test instance
#     idx = 0  # Change the index as needed
#     exp = explainer.explain_instance(X_test[idx], model.predict_proba, num_features=10)

#     # Visualise explanation
#     exp.show_in_notebook(show_all=False)
#     exp.save_to_file('lime_explanation.html')
#     print("LIME explanation saved at 'lime_explanation.html'")

def explain_with_shap_and_lime(model, X_test_pca, X_train_pca, y_test, feature_names, label_encoder):
    print("--- Generating Explanations with SHAP and LIME ---\n")

    # Generating SHAP explanations
    print("Generating SHAP explanations...")
    background = X_train_pca[np.random.choice(X_train_pca.shape[0], 100, replace=False)]
    explainer = shap.KernelExplainer(model.predict_proba, background)
    shap_values = explainer.shap_values(X_test_pca[:50])  # Use first 50 samples for explanation

    # Ensure feature names are aligned with PCA components
    shap.summary_plot(shap_values, X_test_pca[:50], feature_names=feature_names, show=False)
    plt.savefig(os.path.join(MODELS_DIR, 'shap_summary_plot_combined.png'))
    print("SHAP explanations saved.")

    # Generating LIME explanations
    print("\nGenerating LIME explanations...")
    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        X_train_pca, 
        training_labels=y_train, 
        mode='classification', 
        feature_names=feature_names
    )
    idx = 0  # Example index to explain
    lime_exp = lime_explainer.explain_instance(
        X_test_pca[idx], 
        model.predict_proba, 
        num_features=10
    )
    lime_exp.save_to_file('lime_explanation_combined.html')
    print("LIME explanation saved.")


# Evaluate the model
def evaluate_model(model, X_test, y_test, label_encoder, is_neural_network=False):
    print("Evaluating model...\n")
    # Get predictions
    y_pred = model.predict(X_test)

    # Handle neural network predictions (convert probabilities to class indices)
    if is_neural_network:
        y_pred = np.argmax(y_pred, axis=1)

    # Get the unique classes in both test and predicted data
    unique_classes_test = np.unique(y_test)
    unique_classes_pred = np.unique(y_pred)

    # Get the intersection of classes to handle mismatches
    valid_classes = np.intersect1d(unique_classes_test, unique_classes_pred)
    
    # Update target names to only include valid classes
    target_names = label_encoder.inverse_transform(valid_classes)

    # Generate Classification Report
    print("Classification Report:")
    print(classification_report(
        y_test,
        y_pred,
        labels=valid_classes,
        target_names=target_names
    ))

    # Plot Confusion Matrix
    print("\nPlotting Confusion Matrix...")
    ConfusionMatrixDisplay.from_predictions(
        y_test,
        y_pred,
        labels=valid_classes,  # Ensure only valid classes are used
        display_labels=target_names,
        cmap='viridis',
        xticks_rotation=90
    )
    plt.title("Confusion Matrix")
    plt.show()
    print("Model evaluation completed.")


# # Explain model predictions with SHAP
# def explain_with_shap(model, X):
#     print("Generating SHAP explanations...")

#     # Use KernelExplainer for SVM and other model types
#     if isinstance(model, SVC):
#         # KernelExplainer requires a background dataset (a subset of the training data)
#         background = X[np.random.choice(X.shape[0], 100, replace=False)]  # Use 100 samples as background
#         explainer = shap.KernelExplainer(model.predict_proba, background)
#     else:
#         # Default to TreeExplainer for tree-based models
#         explainer = shap.TreeExplainer(model)

#     # Compute SHAP values
#     shap_values = explainer.shap_values(X[:100])  # Use the first 100 samples for explanation

#     # Plot SHAP summary
#     shap.summary_plot(shap_values, X[:100], show=False)
#     plt.savefig(os.path.join(MODELS_DIR, 'shap_summary_plot_svm.png'))
#     print("SHAP explanations saved.")


# Main pipeline
if __name__ == "__main__":
    (X_train, X_test, y_train, y_test), scaler, le = load_and_preprocess_data(DATA_DIR)
    X_train, y_train = handle_class_imbalance(X_train, y_train)
    X_train_pca, pca = apply_pca(X_train)
    X_test_pca = pca.transform(X_test)
    apply_tsne(X_train_pca, y_train)
    feature_names = [f"PC{i+1}" for i in range(X_test_pca.shape[1])]

    # Train Random Forest with tuning
    rf_model = RandomForestClassifier(random_state=42, class_weight='balanced')
    param_grid_rf = {'n_estimators': [100, 200], 'max_depth': [10, 20], 'min_samples_split': [2, 5]}
    best_rf_model = tune_hyperparameters(rf_model, param_grid_rf, X_train_pca, y_train)

    # Evaluate Random Forest
    evaluate_model(best_rf_model, X_test_pca, y_test, le)
    explain_with_shap_and_lime(best_rf_model, X_test_pca, X_train_pca, y_test, feature_names, le)

    # Save the trained model
    joblib.dump(best_rf_model, os.path.join(MODELS_DIR, 'rf_model.pkl'))
    print(f"Random Forest model saved at '{os.path.join(MODELS_DIR, 'rf_model.pkl')}'")

    # Train Neural Network
    nn_model = train_neural_network(X_train_pca, y_train, X_test_pca, y_test, input_dim=X_train_pca.shape[1], num_classes=len(np.unique(y_train)))

    # Evaluate Neural Network
    evaluate_model(nn_model, X_test_pca, y_test, le, is_neural_network=True)

    # Save Neural Network
    nn_model.save(os.path.join(MODELS_DIR, 'nn_model.h5'))
    print(f"Neural Network model saved at '{os.path.join(MODELS_DIR, 'nn_model.h5')}'")

    # Train SVM Model
    print("\n--- SVM Training ---")
    svm_model = train_svm(X_train_pca, X_test_pca, y_train, y_test)

    explain_with_shap_and_lime(svm_model, X_test_pca)