from sklearn.model_selection import GridSearchCV

def tune_hyperparameters(model, param_grid, X_train, y_train):
    grid_search = GridSearchCV(estimator=model, param_grid=param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    return grid_search.best_estimator_, grid_search.best_params_

# Example usage
if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier()
    param_grid = {'n_estimators': [100, 200], 'max_depth': [5, 10]}
    best_model, best_params = tune_hyperparameters(model, param_grid, X_train, y_train)
    print(best_params)
