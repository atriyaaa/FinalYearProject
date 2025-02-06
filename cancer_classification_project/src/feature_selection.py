from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

def apply_pca(df, n_components=50):
    X = df.iloc[:, 1:-1]  # Exclude label column
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=n_components)
    X_pca = pca.fit_transform(X_scaled)

    print(f"Explained Variance Ratio (PCA): {pca.explained_variance_ratio_.sum()}")
    return X_pca


