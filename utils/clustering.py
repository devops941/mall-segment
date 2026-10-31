import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def max_valid_k(n_samples: int) -> int:
    """Largest k that K-Means can fit and silhouette_score can evaluate."""
    return max(2, min(10, int(n_samples) - 1))


def compute_wcss(X: np.ndarray, k_range=range(1, 11)) -> list[float]:
    wcss = []
    for k in k_range:
        if k > len(X):
            continue
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
        km.fit(X)
        wcss.append(km.inertia_)
    return wcss


def compute_silhouette(X: np.ndarray, k_range=range(2, 11)) -> list[float]:
    scores = []
    for k in k_range:
        # silhouette_score needs at least k+1 samples (one cluster would be a singleton).
        if k >= len(X):
            continue
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
        labels = km.fit_predict(X)
        scores.append(silhouette_score(X, labels))
    return scores


def run_kmeans(X: np.ndarray, k: int, scale: bool = False):
    k = max(1, min(int(k), len(X)))
    if scale:
        scaler = StandardScaler()
        X_fit = scaler.fit_transform(X)
    else:
        X_fit = X
        scaler = None

    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    labels = km.fit_predict(X_fit)
    centers = km.cluster_centers_

    if scale and scaler is not None:
        centers = scaler.inverse_transform(centers)

    return labels, centers, km


def prepare_features(df: pd.DataFrame, feature_cols: list[str], scale: bool = False):
    X = df[feature_cols].values
    if scale:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        return X, X_scaled, scaler
    return X, X, None
