import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
from recommendation.recommender import recommend_courses
from database.history import save_history

st.set_page_config(
    page_title="Course Recommendation",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Course Recommendation System")

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

user = st.session_state["user"]

st.success(f"Welcome, {user['name']} 👋")

course = st.text_input(
    "Search Course",
    placeholder="Example: Python, Machine Learning, Data Science..."
)

if st.button("Get Recommendations", use_container_width=True):

    if not course.strip():
        st.warning("Please enter a course name.")
        st.stop()

    recommendations = recommend_courses(course)

    if recommendations.empty:
        st.error("No matching course found.")
        st.stop()

    save_history(user["id"], course)

    st.subheader("Recommended Courses")

    for i, (_, row) in enumerate(recommendations.iterrows(), start=1):

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"### {i}. {row['course_title']}")
                st.write(f"**Organization:** {row['course_organization']}")
                st.write(f"**Difficulty:** {row['course_difficulty']}")
                st.write(f"**Certificate:** {row['course_Certificate_type']}")
                st.write(f"**Students Enrolled:** {row['course_students_enrolled']}")

            with col2:
                st.metric("⭐ Rating", f"{row['course_rating']:.1f}")
                st.metric("Cluster", row["cluster"])

            if "recommendation_score" in row:
                st.progress(
                    min(max(float(row["recommendation_score"]), 0.0), 1.0),
                    text=f"Recommendation Score: {row['recommendation_score']:.2f}"
                )

            if "why_recommended" in row:
                st.info(f"Why Recommended: {row['why_recommended']}")