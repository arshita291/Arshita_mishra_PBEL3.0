import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import pandas as pd
import streamlit as st
from database.database import create_tables

create_tables()

st.set_page_config(
    page_title="Intelligent Recommendation System for E-Learning Platforms",
    page_icon="🎓",
    layout="wide"
)

DATA_PATH = ROOT / "dataset" / "processed" / "featured_courses.csv"

df = pd.read_csv(DATA_PATH)

st.markdown(
    """
    <style>
    .hero{
        background:linear-gradient(135deg,#2563eb,#7c3aed);
        padding:35px;
        border-radius:15px;
        color:white;
        text-align:center;
        margin-bottom:25px;
    }

    .feature{
        background:#f8f9fa;
        padding:20px;
        border-radius:12px;
        border-left:5px solid #2563eb;
        margin-bottom:15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero">
        <h1>🎓 Intelligent Recommendation System for E-Learning Platforms</h1>
        <h4>Personalized Course Recommendation using Machine Learning</h4>
        <p>TF-IDF • K-Means Clustering • Nearest Neighbors • Streamlit</p>
    </div>
    """,
    unsafe_allow_html=True
)

if "user" in st.session_state:
    st.success(f"Welcome, {st.session_state['user']['name']} 👋")
else:
    st.info("Use the left sidebar to Register or Login.")

st.subheader("📈 Dataset Overview")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Courses", len(df))
c2.metric("Organizations", df["course_organization"].nunique())
c3.metric("Average Rating", f"{df['course_rating'].mean():.2f}")
c4.metric("Clusters", df["cluster"].nunique())

st.divider()

st.subheader("✨ Project Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
<div class="feature">
<h4>🤖 Machine Learning</h4>

- TF-IDF Vectorization
- K-Means Clustering
- Nearest Neighbors
- Content-Based Recommendation

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature">
<h4>👤 User Module</h4>

- Registration
- Login
- Student Profile
- Recommendation History

</div>
""", unsafe_allow_html=True)

with col2:
    st.markdown("""
<div class="feature">
<h4>📊 Analytics</h4>

- Interactive Dashboard
- Cluster Visualization
- Model Evaluation
- Plotly Charts

</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="feature">
<h4>💾 Database</h4>

- SQLite
- Secure Authentication
- Recommendation History
- Feedback Ready

</div>
""", unsafe_allow_html=True)

st.divider()

st.subheader("🧠 Machine Learning Workflow")

st.markdown("""
1. Dataset Collection
2. Data Cleaning
3. Feature Engineering
4. TF-IDF Vectorization
5. K-Means Clustering
6. Nearest Neighbor Model
7. Personalized Course Recommendation
""")

st.divider()

st.subheader("🚀 How to Use")

st.markdown("""
- Register a new account.
- Login using your credentials.
- Search for a course.
- View AI-powered recommendations.
- Check your recommendation history.
- Explore the Analytics Dashboard.
""")

st.divider()