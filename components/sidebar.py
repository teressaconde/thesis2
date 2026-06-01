import streamlit as st
from pathlib import Path
from textwrap import dedent

BASE_DIR = Path(__file__).resolve().parent.parent
SIDEBAR_CSS = BASE_DIR / "assets" / "sidebar.css"


def load_sidebar_css():
    css = SIDEBAR_CSS.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_html(html: str):
    html = dedent(html).strip()
    html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


def render_sidebar(active_page: str = "Dashboard"):
    with st.sidebar:
        render_html(
            """
            <div class="sidebar-brand">
                <div class="sidebar-logo">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M9.5 4.5C7.8 3.2 5.2 4.3 5.3 6.8C3.2 6.7 2.3 9.2 3.8 10.4C2.2 11.9 3.1 14.7 5.4 14.5C5.8 17 9.5 17.4 9.5 14.8V4.5Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14.5 4.5C16.2 3.2 18.8 4.3 18.7 6.8C20.8 6.7 21.7 9.2 20.2 10.4C21.8 11.9 20.9 14.7 18.6 14.5C18.2 17 14.5 17.4 14.5 14.8V4.5Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M3.5 11H6.5L7.5 8.8L9 13L10 11H14L15 13L16.5 8.8L17.5 11H20.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>

                <div class="sidebar-brand-text">
                    <div class="sidebar-title">Oral Fluency<br>Classification</div>
                    <div class="sidebar-subtitle">SVM-Based Fluency<br>Assessment System</div>
                </div>
            </div>
            """
        )

        st.page_link("dashboard.py", label="Dashboard", icon=":material/home:")
        st.page_link("pages/upload_audio.py", label="Upload Audio", icon=":material/cloud_upload:")
        st.page_link("pages/model_comparison.py", label="Model Comparison", icon=":material/balance:")
        st.page_link("pages/datasets.py", label="Datasets", icon=":material/database:")
        st.page_link("pages/workflow.py", label="Workflow", icon=":material/account_tree:")
        st.page_link("pages/about.py", label="About System", icon=":material/info:")

        render_html(
            """
            <div class="user-card">
                <div class="avatar">
                    <div class="avatar-face">👨‍💼</div>
                </div>

                <div class="user-details">
                    <div class="user-role">Researcher</div>
                    <div class="user-name">Arjun Dev</div>
                    <div class="user-email">arjun.dev@research.edu</div>
                    <div class="online">
                        <span class="online-dot"></span>
                        <span>Online</span>
                    </div>
                </div>
            </div>
            """
        )

        if st.button("↪  Logout", key="logout_button", use_container_width=True):
            st.switch_page("dashboard.py")