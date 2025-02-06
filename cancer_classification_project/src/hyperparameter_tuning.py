from sklearn.model_selection import GridSearchCV

def tune_hyperparameters(model, param_grid, X_train, y_train, scoring='accuracy', cv=5):
    """
    Perform hyperparameter tuning using GridSearchCV.

    Args:
        model: Estimator to tune (e.g., RandomForestClassifier()).
        param_grid: Dictionary of hyperparameters to test.
        X_train: Training features.
        y_train: Training labels.
        scoring: Scoring metric for GridSearchCV (default: 'accuracy').
        cv: Number of cross-validation folds (default: 5).

    Returns:
        best_model: Model with the best hyperparameters.
        best_params: Dictionary of best hyperparameters.
    """
    try:
        print("Starting hyperparameter tuning...")
        grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=cv, scoring=scoring, verbose=1)
        grid_search.fit(X_train, y_train)
        print("Hyperparameter tuning completed.")
        print(f"Best Parameters: {grid_search.best_params_}")
        return grid_search.best_estimator_, grid_search.best_params_
    except Exception as e:
        print(f"Hyperparameter tuning failed: {e}")
        return None, None

# Example usage
if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split

    # Load example dataset
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define model and parameter grid
    model = RandomForestClassifier(random_state=42)
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [5, 10, None],
        'min_samples_split': [2, 5]
    }

    # Tune hyperparameters
    best_model, best_params = tune_hyperparameters(model, param_grid, X_train, y_train)
    if best_model:
        print(f"Best Parameters: {best_params}")
        print(f"Best Model: {best_model}")
