import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI Recommendation Analytics Dashboard")

DATA_PATH = ROOT / "dataset" / "processed" / "featured_courses.csv"
METRICS_PATH = ROOT / "models" / "saved_models" / "metrics.json"

df = pd.read_csv(DATA_PATH)

with open(METRICS_PATH) as f:
    metrics = json.load(f)

st.subheader("Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Courses", len(df))
c2.metric("Organizations", df["course_organization"].nunique())
c3.metric("Average Rating", f"{df['course_rating'].mean():.2f}")
c4.metric("Clusters", metrics["clusters"])

st.divider()

st.subheader("Model Evaluation")

m1, m2, m3 = st.columns(3)

m1.metric(
    "Silhouette Score",
    f"{metrics['silhouette_score']:.4f}"
)

m2.metric(
    "Davies-Bouldin Index",
    f"{metrics['davies_bouldin_score']:.4f}"
)

m3.metric(
    "Calinski-Harabasz Score",
    f"{metrics['calinski_harabasz_score']:.2f}"
)

st.divider()

left, right = st.columns(2)

with left:

    difficulty = (
        df["course_difficulty"]
        .value_counts()
        .reset_index()
    )

    difficulty.columns = [
        "Difficulty",
        "Courses"
    ]

    fig = px.bar(
        difficulty,
        x="Difficulty",
        y="Courses",
        title="Courses by Difficulty"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    certificate = (
        df["course_Certificate_type"]
        .value_counts()
        .reset_index()
    )

    certificate.columns = [
        "Certificate",
        "Courses"
    ]

    fig = px.pie(
        certificate,
        names="Certificate",
        values="Courses",
        title="Certificate Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

left, right = st.columns(2)

with left:

    top_org = (
        df["course_organization"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    top_org.columns = [
        "Organization",
        "Courses"
    ]

    fig = px.bar(
        top_org,
        x="Organization",
        y="Courses",
        title="Top Organizations"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    cluster = (
        df["cluster"]
        .value_counts()
        .sort_index()
        .reset_index()
    )

    cluster.columns = [
        "Cluster",
        "Courses"
    ]

    fig = px.bar(
        cluster,
        x="Cluster",
        y="Courses",
        title="Cluster Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()

fig = px.scatter(
    df,
    x="students_enrolled_numeric",
    y="course_rating",
    color=df["cluster"].astype(str),
    hover_name="course_title",
    title="Course Clusters",
    labels={
        "students_enrolled_numeric": "Students Enrolled",
        "course_rating": "Rating"
    }
)

st.plotly_chart(fig, use_container_width=True)