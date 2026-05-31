import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from textwrap import dedent

st.set_page_config(
    page_title="Login | Oral Fluency Classification",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).parent
CSS_FILE = BASE_DIR / "assets" / "login.css"
LEFT_HTML_FILE = BASE_DIR / "assets" / "login_left.html"


def load_css(path: Path):
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_left_panel(css_path: Path, html_path: Path):
    css = css_path.read_text(encoding="utf-8")
    html = html_path.read_text(encoding="utf-8")

    component_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                overflow: hidden;
                background: transparent;
            }}

            {css}

            .left-panel {{
                height: 760px !important;
                min-height: 760px !important;
                border-radius: 20px 0 0 20px;
            }}
        </style>
    </head>
    <body>
        {html}
    </body>
    </html>
    """

    components.html(component_html, height=760, scrolling=False)


def authenticate(username: str, password: str) -> bool:
    expected_user = "admin"
    expected_pass = "admin123"

    return username.strip() == expected_user and password == expected_pass


if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "login_error" not in st.session_state:
    st.session_state.login_error = ""

if st.session_state.authenticated:
    st.switch_page("pages/dashboard.py")


load_css(CSS_FILE)

left_col, right_col = st.columns([1, 1], gap="small")

with left_col:
    load_left_panel(CSS_FILE, LEFT_HTML_FILE)

with right_col:
    st.markdown('<div class="right-column-marker"></div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="language-pill">🌐 English⌄</div>'
        '<div class="form-box-streamlit">'
        '<div class="eyebrow">Welcome back 👋</div>'
        '<h2 class="login-heading">Sign in to your account</h2>'
        '<p class="login-support">Access your dashboard to analyze audio, view results, and track fluency insights.</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    if st.session_state.login_error:
        st.markdown(
            f'<div class="alert-box">{st.session_state.login_error}</div>',
            unsafe_allow_html=True,
        )

    with st.form("login_form", clear_on_submit=False):
        st.markdown(
            '<div class="field-label">Email or Username</div>',
            unsafe_allow_html=True,
        )

        username = st.text_input(
            "Email or Username",
            placeholder="Enter your email or username",
            label_visibility="collapsed",
        )

        st.markdown(
            '<div class="field-label">Password</div>',
            unsafe_allow_html=True,
        )

        password = st.text_input(
            "Password",
            placeholder="Enter your password",
            type="password",
            label_visibility="collapsed",
        )

        remember_col, forgot_col = st.columns([1, 1])

        with remember_col:
            st.checkbox("Remember me")

        with forgot_col:
            st.markdown(
                '<div style="text-align:right; padding-top:4px;"><a class="forgot" href="#">Forgot password?</a></div>',
                unsafe_allow_html=True,
            )

        submitted = st.form_submit_button("🔒  Sign In")

    if submitted:
        if authenticate(username, password):
            st.session_state.authenticated = True
            st.session_state.login_error = ""
            st.switch_page("pages/dashboard.py")
        else:
            st.session_state.login_error = "Invalid username or password."
            st.rerun()

    st.markdown(
        '<div class="divider">or</div>',
        unsafe_allow_html=True,
    )

    if st.button("👥  Request Access"):
        st.info("Access request workflow can be connected later.")

    st.markdown(
        '<div class="security-note">'
        '<div class="security-icon">♡</div>'
        '<div>'
        '<strong>Secure access for researchers, educators, and analysts.</strong>'
        '<p>All data is encrypted and handled with the highest standards of privacy and security.</p>'
        '</div>'
        '</div>'
        '<div class="login-footer">🔒 © 2024 Oral Fluency Classification. All rights reserved.</div>',
        unsafe_allow_html=True,
    )