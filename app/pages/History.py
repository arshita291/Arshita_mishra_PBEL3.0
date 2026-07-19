import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))

import streamlit as st
from database.history import get_history

st.set_page_config(page_title="Recommendation History", page_icon="📜")

st.title("📜 Recommendation History")

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.stop()

history = get_history(st.session_state["user"]["id"])

if not history:
    st.info("No recommendation history found.")
else:
    for i, (course, date) in enumerate(history, start=1):
        st.write(f"**{i}. {course}**")
        st.caption(date)