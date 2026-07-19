from pathlib import Path
import difflib
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_PATH = BASE_DIR / "dataset" / "processed" / "featured_courses.csv"
MODEL_DIR = BASE_DIR / "models" / "saved_models"

courses_df = pd.read_csv(DATA_PATH)

feature_matrix = joblib.load(MODEL_DIR / "feature_matrix.pkl")
nearest_neighbors = joblib.load(MODEL_DIR / "nearest_neighbors.pkl")
kmeans_model = joblib.load(MODEL_DIR / "kmeans_model.pkl")


def find_course(query):

    query = str(query).strip().lower()

    titles = (
        courses_df["course_title"]
        .fillna("")
        .astype(str)
        .tolist()
    )

    match = difflib.get_close_matches(
        query,
        titles,
        n=1,
        cutoff=0.4
    )

    if match:
        return courses_df[
            courses_df["course_title"].astype(str).str.lower() == match[0]
        ].index[0]

    matched = courses_df[
        courses_df["course_title"]
        .fillna("")
        .astype(str)
        .str.lower()
        .str.contains(query, na=False)
    ]

    if not matched.empty:
        return matched.index[0]

    return None


def recommend_courses(course_name, top_n=10):

    course_index = find_course(course_name)

    if course_index is None:
        return pd.DataFrame()

    distances, indices = nearest_neighbors.kneighbors(
        feature_matrix[course_index],
        n_neighbors=min(top_n + 5, len(courses_df))
    )

    recommendations = courses_df.iloc[indices.flatten()].copy()

    recommendations = recommendations[
        recommendations.index != course_index
    ]

    recommendations = recommendations.drop_duplicates(
        subset="course_title"
    )

    recommendations["similarity_score"] = (
        1 - distances.flatten()[1:len(recommendations) + 1]
    )

    recommendations["recommendation_score"] = (
        recommendations["similarity_score"] * 0.7
        + recommendations["popularity_score"] * 0.3
    )

    recommendations = recommendations.sort_values(
        by="recommendation_score",
        ascending=False
    )

    recommendations = recommendations.head(top_n)

    recommendations["why_recommended"] = (
        "Similar content + Popular course"
    )

    return recommendations[
        [
            "course_title",
            "course_organization",
            "course_rating",
            "course_difficulty",
            "course_Certificate_type",
            "course_students_enrolled",
            "cluster",
            "recommendation_score",
            "why_recommended"
        ]
    ]


if __name__ == "__main__":

    while True:

        course = input("\nEnter Course Name (or 'exit'): ")

        if course.lower() == "exit":
            break

        result = recommend_courses(course)

        if result.empty:
            print("\nCourse not found.\n")
        else:
            print(result.to_string(index=False))