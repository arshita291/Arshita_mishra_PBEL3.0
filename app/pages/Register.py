import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

from app.authentication.auth import register_user

st.set_page_config(page_title="Register", page_icon="📝")

st.title("📝 Student Registration")

with st.form("register_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    submitted = st.form_submit_button("Register")

    if submitted:
        if not name or not email or not password:
            st.error("All fields are required.")

        elif password != confirm_password:
            st.error("Passwords do not match.")

        else:
            success = register_user(name, email, password)

            if success:
                st.success("Registration Successful.")

            else:
                st.error("Email already exists.")
                st.markdown("---")

if st.button("Already registered? Login"):
    st.switch_page("pages/Login.py")