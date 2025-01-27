from sklearn.feature_selection import SelectKBest, f_classif

def select_features(X, y, k=20):
    selector = SelectKBest(score_func=f_classif, k=k)
    X_selected = selector.fit_transform(X, y)
    return X_selected, selector.get_support()
