from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    silhouette_score,
    davies_bouldin_score,
    calinski_harabasz_score,
)
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "processed" / "featured_courses.csv"
MODEL_DIR = BASE_DIR / "models" / "saved_models"

MODEL_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATA_PATH)

tfidf = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

tfidf_matrix = tfidf.fit_transform(df["combined_features"])

best_score = -1
best_model = None
best_clusters = None

for k in range(5, 11):

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=20
    )

    labels = model.fit_predict(tfidf_matrix)

    score = silhouette_score(tfidf_matrix, labels)

    if score > best_score:
        best_score = score
        best_model = model
        best_clusters = labels

df["cluster"] = best_clusters

dense_matrix = tfidf_matrix.toarray()

metrics = {
    "clusters": int(best_model.n_clusters),
    "silhouette_score": float(
        silhouette_score(tfidf_matrix, best_clusters)
    ),
    "davies_bouldin_score": float(
        davies_bouldin_score(dense_matrix, best_clusters)
    ),
    "calinski_harabasz_score": float(
        calinski_harabasz_score(dense_matrix, best_clusters)
    )
}

numeric_features = df[
    [
        "course_rating",
        "students_enrolled_numeric",
        "difficulty_encoded",
        "certificate_encoded",
        "popularity_score",
    ]
]

scaler = StandardScaler()

scaler.fit(numeric_features)

nearest_model = NearestNeighbors(
    metric="cosine",
    algorithm="brute",
    n_neighbors=10
)

nearest_model.fit(tfidf_matrix)

joblib.dump(tfidf, MODEL_DIR / "tfidf_vectorizer.pkl")
joblib.dump(tfidf_matrix, MODEL_DIR / "feature_matrix.pkl")
joblib.dump(best_model, MODEL_DIR / "kmeans_model.pkl")
joblib.dump(nearest_model, MODEL_DIR / "nearest_neighbors.pkl")
joblib.dump(scaler, MODEL_DIR / "scaler.pkl")

with open(MODEL_DIR / "metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

df.to_csv(DATA_PATH, index=False)

print("\n========== MODEL METRICS ==========")
print(f"Clusters               : {metrics['clusters']}")
print(f"Silhouette Score       : {metrics['silhouette_score']:.4f}")
print(f"Davies-Bouldin Index   : {metrics['davies_bouldin_score']:.4f}")
print(f"Calinski-Harabasz      : {metrics['calinski_harabasz_score']:.4f}")

print("\nModels trained and saved successfully.")