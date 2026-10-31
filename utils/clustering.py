import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score


def compute_wcss(X: np.ndarray, k_range=range(1, 11)) -> list[float]:
    wcss = []
    for k in k_range:
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
        km.fit(X)
        wcss.append(km.inertia_)
    return wcss


def compute_silhouette(X: np.ndarray, k_range=range(2, 11)) -> list[float]:
    scores = []
    for k in k_range:
        km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
        labels = km.fit_predict(X)
        scores.append(silhouette_score(X, labels))
    return scores


def run_kmeans(X: np.ndarray, k: int, scale: bool = False):
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
