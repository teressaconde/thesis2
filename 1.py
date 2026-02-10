"""
Streamlit UI for Oral Fluency Classification
Run:
    streamlit run 1.py
"""

from __future__ import annotations
import streamlit as st


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');

        :root {
            --ofc-upload-height: 260px;
            --ofc-page-bg: #ffffff;
            --ofc-header-bg: #254B96;

            --ofc-page-outer-padding: 24px;
            --ofc-footer-space: 96px;

            --ofc-baseline-card-width: 680px;
            --ofc-baseline-card-height: 400px;
            --ofc-proposed-card-width: var(--ofc-baseline-card-width);
            --ofc-proposed-card-height: var(--ofc-baseline-card-height);
        }

        header, footer, #MainMenu { display: none !important; }

        body, .stApp {
            background: var(--ofc-page-bg);
            font-family: "Rubik", system-ui, -apple-system, Arial, sans-serif;
            overflow-x: hidden;
        }

        div[data-testid="stAppViewContainer"] > .main,
        div[data-testid="stAppViewContainer"] > .main .block-container {
            padding-top: 0 !important;
        }

        .block-container {
            max-width: 1440px;
            margin: 0 auto;
            padding: 0;
        }

        .ofc-header {
            background: var(--ofc-header-bg);
            color: white;
            font-size: 40px;
            font-weight: 700;
            padding: 32px calc(64px + var(--ofc-page-outer-padding));
            width: 100vw;
            margin-left: calc(50% - 50vw);
        }

        /* Upload box */
        div[data-testid="stFileUploader"] {
            width: 100%;
            max-width: 820px;
            height: var(--ofc-upload-height);
            margin: 0 auto;
            background: #EEF5FF;
            border-radius: 18px;
            border: 2px dashed #2F6FED;
            position: relative;
            overflow: hidden;
            cursor: pointer;

            /* cloud icon (click still handled by invisible input overlay) */
            background-image:
                url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='96' height='96' viewBox='0 0 24 24' fill='none'%3E%3Cpath d='M7 19h10a4 4 0 0 0 .7-7.94A5.5 5.5 0 0 0 7.1 8.6 4.5 4.5 0 0 0 7 19Z' stroke='%232F6FED' stroke-width='1.9' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-size: 54px;
            background-position: center 56px;
        }

        div[data-testid="stFileUploader"]::before {
            content: "Upload speech audio here";
            position: absolute;
            top: 122px;
            width: 100%;
            text-align: center;
            font-size: 24px;
            font-weight: 600;
            color: #6B7280;
            pointer-events: none;
        }

        div[data-testid="stFileUploader"]::after {
            content: "Supported formats: MP3, WAV · Clear speech recommended";
            position: absolute;
            top: 168px;
            width: 100%;
            text-align: center;
            font-size: 16px;
            color: #9CA3AF;
            pointer-events: none;
        }

        div[data-testid="stFileUploader"] section,
        div[data-testid="stFileUploader"] input[type="file"] {
            opacity: 0;
            position: absolute;
            inset: 0;
            cursor: pointer;
            z-index: 3;
        }

        .arrow-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .arrow-wrapper button {
            width: 80px !important;
            height: 80px !important;
            border-radius: 50% !important;
            background: #254B96 !important;
            color: white !important;
            font-size: 30px !important;
            font-weight: 800;
            border: none;
        }

        .arrow-wrapper button:hover {
            background: #1D4183 !important;
        }

        .panel {
            border-radius: 24px;
            padding: 24px 28px;
            background: white;
            display: flex;
            flex-direction: column;
            width: 100%;
            margin: 0 auto;
        }

        .panel.green {
            border: 2px solid #44CD1B;
            color: #44CD1B;
            max-width: var(--ofc-proposed-card-width);
            height: var(--ofc-proposed-card-height);
        }

        .panel.red {
            border: 2px solid #E51F1F;
            color: #E51F1F;
            max-width: var(--ofc-baseline-card-width);
            height: var(--ofc-baseline-card-height);
        }

        .panel-title {
            font-size: 40px;
            font-weight: 600;
            margin-bottom: 16px;
        }

        .panel-body {
            font-size: 30px;
            line-height: 1.25;
            text-align: justify;
            flex: 1;
            overflow: auto;
        }

        .ofc-main {
            padding: 12px 48px calc(24px + var(--ofc-footer-space));
            margin: 0 12px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Oral Fluency Classification", layout="wide")
    inject_css()

    st.markdown('<div class="ofc-header">Oral Fluency Classification</div>', unsafe_allow_html=True)
    st.markdown('<div class="ofc-main">', unsafe_allow_html=True)

    left_spacer, center, right_spacer = st.columns([1, 2, 1])

    with center:
        col_upload, col_arrow = st.columns([10, 1], vertical_alignment="center")

        with col_upload:
            uploaded = st.file_uploader(
                "Upload audio",
                type=["wav", "mp3"],
                label_visibility="collapsed",
                key="audio_file",
            )

        with col_arrow:
            st.markdown('<div class="arrow-wrapper">', unsafe_allow_html=True)
            go = st.button("→")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown("""
        <div class="panel green">
            <div class="panel-title">Proposed SVM</div>
            <div class="panel-body">
            These features are mapped into a hybrid feature space using Random Fourier Features
            and the Nyström method to efficiently represent non-linear speech patterns.
            The resulting features are passed to an SVM classifier trained using
            Sequential Minimal Optimization.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="panel red">
            <div class="panel-title">Baseline SVM</div>
            <div class="panel-body">
            Features are mapped into a higher-dimensional space using a non-linear kernel.
            A quadratic programming solver identifies key support vectors and determines
            the decision boundary for fluency classification.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if go and uploaded is not None:
        st.session_state["uploaded_audio"] = {
            "name": uploaded.name,
            "bytes": uploaded.getvalue(),
        }
        st.switch_page("pages/2.py")


if __name__ == "__main__":
    main()
