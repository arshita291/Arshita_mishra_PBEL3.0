import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from app.authentication.auth import login_user

st.set_page_config(page_title="Login", page_icon="🔐")

st.title("🔐 Student Login")

with st.form("login_form"):
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    submitted = st.form_submit_button("Login")

    if submitted:
        user = login_user(email, password)

        if user:
            st.session_state["user"] = user
            st.success(f"Welcome {user['name']}")
            st.success("Login Successful")
            st.switch_page("pages/Recommendation.py")
        else:
            st.error("Invalid Email or Password.")
            st.markdown("---")

if st.button("Don't have an account? Register"):
    st.switch_page("pages/Register.py")
    st.session_state["user"] = user
