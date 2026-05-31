import streamlit as st


def require_login():
    if not st.session_state.get("authenticated", False):
        st.switch_page("login.py")