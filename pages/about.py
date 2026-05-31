import streamlit as st
from pathlib import Path
from textwrap import dedent

st.set_page_config(
    page_title="About System | Oral Fluency Classification",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from auth_guard import require_login
from components.sidebar import load_sidebar_css, render_sidebar

# require_login()
load_sidebar_css()
render_sidebar(active_page="About System")


BASE_DIR = Path(__file__).resolve().parent.parent
ABOUT_CSS = BASE_DIR / "assets" / "about.css"
ABOUT_HTML = BASE_DIR / "assets" / "about.html"


def load_css(path: Path):
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_html(path: Path):
    html = path.read_text(encoding="utf-8")

    # Important: prevents Streamlit Markdown from treating HTML as code
    html = dedent(html).strip()
    html = "\n".join(line.lstrip() for line in html.splitlines())

    st.markdown(html, unsafe_allow_html=True)


load_css(ABOUT_CSS)
load_html(ABOUT_HTML)