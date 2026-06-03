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
                        <path d="M4 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M8 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M12 19V5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M16 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M20 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
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