import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.metrics import classification_report, ConfusionMatrixDisplay, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.metrics import classification_report, ConfusionMatrixDisplay
from imblearn.over_sampling import SMOTE
from sklearn.impute import SimpleImputer
import joblib
import shap

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
    
    # Check class distribution
    class_counts = pd.Series(y_train).value_counts()
    min_class_size = class_counts.min()
    
    # Adjust k_neighbors based on the smallest class size
    k_neighbors = min(5, min_class_size - 1)
    if k_neighbors < 1:
        raise ValueError("Too few samples in some classes for SMOTE. Consider removing these classes or using a different method.")
    
    print(f"Using k_neighbors={k_neighbors} for SMOTE.")
    
    # Apply SMOTE
    smote = SMOTE(random_state=42, k_neighbors=k_neighbors)
    X_resampled, y_resampled = smote.fit_resample(X_train, y_train)
    
    # Print new class distribution
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
    tsne_output_path = os.path.join(MODELS_DIR, 'tsne_visualisation.png')
    plt.savefig(tsne_output_path)
    plt.show()
    print(f"t-SNE visualization saved at {tsne_output_path}")
    print("t-SNE applied.")

# Train Neural Network
def train_neural_network(X_train, y_train, input_dim, num_classes):
    print("Training Neural Network...")
    model = Sequential([
        Dense(128, activation='relu', input_dim=input_dim),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(optimizer=Adam(learning_rate=0.001),
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, verbose=1)
    print("Neural Network trained.")
    return model

# Hyperparameter tuning
def tune_hyperparameters(model, param_grid, X_train, y_train):
    print("Starting hyperparameter tuning...")
    cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=cv, scoring='accuracy', verbose=1)
    grid_search.fit(X_train, y_train)
    print("Hyperparameter tuning completed.")
    return grid_search.best_estimator_

# Evaluate the model
# Evaluate the model
def evaluate_model(model, X_test, y_test, label_encoder, is_neural_network=False):
    print("Evaluating model...\n")
    
    # Predict probabilities for neural networks, else predict labels directly
    if is_neural_network:
        y_proba = model.predict(X_test)
        y_pred = np.argmax(y_proba, axis=1)  # Convert probabilities to class labels
    else:
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None

    # Get unique classes in the test set
    unique_classes = np.unique(y_test)
    target_names = label_encoder.inverse_transform(unique_classes)
    
    print("Classification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=target_names,
        labels=unique_classes
    ))

    # Compute ROC-AUC if probabilities are available
    if y_proba is not None and y_proba.shape[1] == len(unique_classes):
        roc_auc = roc_auc_score(y_test, y_proba, multi_class='ovo', labels=unique_classes)
        print(f"ROC-AUC Score: {roc_auc:.3f}")
    else:
        print("Skipping ROC-AUC computation due to mismatched number of classes or missing probabilities.")

    # Plot confusion matrix
    disp = ConfusionMatrixDisplay.from_predictions(
        y_test,
        y_pred,
        display_labels=target_names,
        cmap='viridis',
        xticks_rotation=90
    )
    disp.plot()
    plt.title("Confusion Matrix")
    plt.show()
    print("Model evaluation completed.")


# Explain model predictions with SHAP
def explain_with_shap(model, X):
    print("Generating SHAP explanations...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    shap.summary_plot(shap_values, X)
    shap_output_path = os.path.join(MODELS_DIR, 'shap_summary_plot.png')
    plt.savefig(shap_output_path)
    print(f"SHAP explanations saved at {shap_output_path}")

# Main pipeline
if __name__ == "__main__":
    (X_train, X_test, y_train, y_test), scaler, le = load_and_preprocess_data(DATA_DIR)
    X_train, y_train = handle_class_imbalance(X_train, y_train)
    X_train_pca, pca = apply_pca(X_train)
    X_test_pca = pca.transform(X_test)
    apply_tsne(X_train_pca, y_train)

    # Train Random Forest with tuning
    rf_model = RandomForestClassifier(random_state=42, class_weight='balanced')
    param_grid_rf = {'n_estimators': [100, 200], 'max_depth': [10, 20], 'min_samples_split': [2, 5]}
    best_rf_model = tune_hyperparameters(rf_model, param_grid_rf, X_train_pca, y_train)

    # Evaluate Random Forest
    evaluate_model(best_rf_model, X_test_pca, y_test, le)
    explain_with_shap(best_rf_model, X_test_pca)

    # Train and evaluate Neural Network
    nn_model = train_neural_network(X_train_pca, y_train, input_dim=X_train_pca.shape[1], num_classes=len(le.classes_))
    # Evaluate Neural Network
    evaluate_model(nn_model, X_test_pca, y_test, le, is_neural_network=True)


    # Save the trained Random Forest model
    joblib.dump(best_rf_model, os.path.join(MODELS_DIR, 'rf_model.pkl'))
    print(f"Model saved at '{os.path.join(MODELS_DIR, 'rf_model.pkl')}'")
