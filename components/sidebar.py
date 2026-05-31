import streamlit as st
from pathlib import Path
from textwrap import dedent

BASE_DIR = Path(__file__).resolve().parent.parent
SIDEBAR_CSS = BASE_DIR / "assets" / "sidebar.css"


def load_sidebar_css():
    css = SIDEBAR_CSS.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


ICONS = {
    "Dashboard": """
    <svg viewBox="0 0 24 24" fill="none">
        <path d="M3 11.5L12 4L21 11.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M5.5 10.5V20H18.5V10.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M9.5 20V14H14.5V20" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """,
    "Upload Audio": """
    <svg viewBox="0 0 24 24" fill="none">
        <path d="M12 15V4" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M8 8L12 4L16 8" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        <path d="M4 14V19C4 20.1 4.9 21 6 21H18C19.1 21 20 20.1 20 19V14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
    </svg>
    """,
    "Results": """
    <svg viewBox="0 0 24 24" fill="none">
        <path d="M7 3H15L20 8V21H7V3Z" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
        <path d="M15 3V8H20" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>
        <path d="M10 17L13 14L15 16L18 12" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """,
    "Model Comparison": """
    <svg viewBox="0 0 24 24" fill="none">
        <path d="M4 20V10" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M10 20V6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M16 20V13" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M22 20H2" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M4 10L10 6L16 13L21 8" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """,
    "Analytics": """
    <svg viewBox="0 0 24 24" fill="none">
        <path d="M4 19V14" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M9 19V9" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M14 19V12" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M19 19V5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
    </svg>
    """,
    "Datasets": """
    <svg viewBox="0 0 24 24" fill="none">
        <rect x="4" y="5" width="16" height="15" rx="2" stroke="currentColor" stroke-width="2.2"/>
        <path d="M8 3V7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M16 3V7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M4 10H20" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
    </svg>
    """,
    "Workflow": """
    <svg viewBox="0 0 24 24" fill="none">
        <circle cx="6" cy="6" r="2.5" stroke="currentColor" stroke-width="2.2"/>
        <circle cx="18" cy="6" r="2.5" stroke="currentColor" stroke-width="2.2"/>
        <circle cx="6" cy="18" r="2.5" stroke="currentColor" stroke-width="2.2"/>
        <circle cx="18" cy="18" r="2.5" stroke="currentColor" stroke-width="2.2"/>
        <path d="M8.5 6H15.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M8.5 18H15.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
    </svg>
    """,
    "Settings": """
    <svg viewBox="0 0 24 24" fill="none">
        <path d="M12 15.5A3.5 3.5 0 1 0 12 8.5A3.5 3.5 0 0 0 12 15.5Z" stroke="currentColor" stroke-width="2.2"/>
        <path d="M19.4 15A1.7 1.7 0 0 0 21 14H21.1A2 2 0 0 0 21.1 10H21A1.7 1.7 0 0 0 19.4 9A1.7 1.7 0 0 0 19.75 7.05L19.8 7A2 2 0 0 0 17 4.2L16.95 4.25A1.7 1.7 0 0 0 15 4.6A1.7 1.7 0 0 0 14 3V2.9A2 2 0 0 0 10 2.9V3A1.7 1.7 0 0 0 9 4.6A1.7 1.7 0 0 0 7.05 4.25L7 4.2A2 2 0 0 0 4.2 7L4.25 7.05A1.7 1.7 0 0 0 4.6 9A1.7 1.7 0 0 0 3 10H2.9A2 2 0 0 0 2.9 14H3A1.7 1.7 0 0 0 4.6 15A1.7 1.7 0 0 0 4.25 16.95L4.2 17A2 2 0 0 0 7 19.8L7.05 19.75A1.7 1.7 0 0 0 9 19.4A1.7 1.7 0 0 0 10 21V21.1A2 2 0 0 0 14 21.1V21A1.7 1.7 0 0 0 15 19.4A1.7 1.7 0 0 0 16.95 19.75L17 19.8A2 2 0 0 0 19.8 17L19.75 16.95A1.7 1.7 0 0 0 19.4 15Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """,
    "About System": """
    <svg viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2.2"/>
        <path d="M12 10.5V17" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M12 7H12.01" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
    </svg>
    """,
}


def render_sidebar(active_page: str = "Dashboard"):
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand">
                <div class="sidebar-logo">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M9.5 4.5C7.8 3.2 5.2 4.3 5.3 6.8C3.2 6.7 2.3 9.2 3.8 10.4C2.2 11.9 3.1 14.7 5.4 14.5C5.8 17 9.5 17.4 9.5 14.8V4.5Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14.5 4.5C16.2 3.2 18.8 4.3 18.7 6.8C20.8 6.7 21.7 9.2 20.2 10.4C21.8 11.9 20.9 14.7 18.6 14.5C18.2 17 14.5 17.4 14.5 14.8V4.5Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M3.5 11H6.5L7.5 8.8L9 13L10 11H14L15 13L16.5 8.8L17.5 11H20.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                </div>
                <div>
                    <div class="sidebar-title">Oral Fluency<br>Classification</div>
                    <div class="sidebar-subtitle">SVM-Based Fluency<br>Assessment System</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        nav_items = [
            ("Dashboard", "dashboard"),
            ("Upload Audio", "upload_audio"),
            ("Results", "results"),
            ("Model Comparison", "model_comparison"),
            ("Analytics", "analytics"),
            ("Datasets", "datasets"),
            ("Workflow", "workflow"),
            ("Settings", "settings"),
            ("About System", "about"),
        ]

        nav_html = '<div class="sidebar-nav-links">'

        for label, url in nav_items:
            active_class = "active" if label == active_page else ""
            nav_html += f"""
<a class="sidebar-link {active_class}" href="/{url}" target="_self">
    <span class="sidebar-link-icon">{ICONS[label]}</span>
    <span class="sidebar-link-text">{label}</span>
</a>
"""

        nav_html += "</div>"

        st.markdown(dedent(nav_html).strip(), unsafe_allow_html=True)

        st.markdown(
            """
            <div class="user-card">
                <div class="avatar">👤</div>
                <div>
                    <div class="user-name">Researcher</div>
                    <div class="user-email">researcher@umindanao.edu.ph</div>
                    <div class="online">
                        <span class="online-dot"></span>
                        <span>Online</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("↪  Logout", key="logout_button", use_container_width=True):
            st.session_state.authenticated = False
            st.switch_page("login.py")