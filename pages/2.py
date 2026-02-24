import base64
from html import escape

import streamlit as st


st.set_page_config(page_title="Oral Fluency Classification", layout="wide")


if "dataset" not in st.session_state:
    st.session_state.dataset = "Avalinguo"


if str(st.query_params.get("remove_audio", "0")) == "1":
    st.session_state.pop("uploaded_audio_obj", None)
    st.session_state.pop("uploaded_audio_data", None)
    st.session_state.pop("audio_uploader", None)
    st.query_params.clear()
    st.switch_page("OFC.py")


uploaded_audio_data = st.session_state.get("uploaded_audio_data")
if uploaded_audio_data is None:
    st.switch_page("OFC.py")


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    .stApp {
        background-color: #ececec;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }

    .block-container {
        max-width: 1240px;
        padding-top: 0.6rem;
        padding-bottom: 2.5rem;
    }

    div[data-testid="stVerticalBlock"]:has(.header-bar) {
        gap: 0;
    }

    .header-bar {
        width: 100vw;
        margin-left: calc(50% - 50vw);
        margin-right: calc(50% - 50vw);
        margin-bottom: 2.55rem;
        background: #274d98;
        height: 94px;
        display: flex;
        align-items: center;
        padding-left: max(32px, calc((100vw - 1240px) / 2 + 70px));
        border-top: 1px solid #1c3a76;
        box-sizing: border-box;
    }

    .header-title {
        color: #ffffff;
        font-size: 50px;
        font-weight: 800;
        line-height: 1;
        margin: 0;
        letter-spacing: 0.3px;
    }

    .stButton > button {
        border-radius: 999px;
        font-weight: 700;
        font-size: 17px;
        padding: 8px 24px;
        line-height: 1;
        min-height: 38px;
        border: 2px solid #2e56a4;
        transition: none;
    }

    .stButton > button[kind="primary"] {
        color: #ffffff;
        background: #2e56a4;
    }

    .stButton > button[kind="secondary"] {
        color: #2e56a4;
        background: #ececec;
    }

    .upload-shell {
        max-width: 660px;
        margin: 0 auto;
    }

    .uploaded-card {
        height: 178px;
        border: 1.8px solid #5a7fc3;
        border-radius: 12px;
        background: #d2d8e5;
        padding: 22px 24px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-sizing: border-box;
    }

    .audio-icon {
        width: 90px;
        height: 90px;
        border-radius: 12px;
        background: #828282;
        color: #ffffff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 48px;
        flex-shrink: 0;
    }

    .audio-details {
        flex: 1;
        display: flex;
        flex-direction: column;
        justify-content: center;
        color: #7b7b7b;
    }

    .audio-name {
        font-size: 34px;
        font-weight: 700;
        line-height: 1.1;
        margin: 0 0 8px 0;
    }

    .audio-size {
        font-size: 18px;
        margin: 0 0 6px 0;
    }

    .audio-player-inline {
        width: 100%;
        height: 34px;
        border-radius: 10px;
    }

    .audio-close {
        color: #8f8f8f;
        margin-left: 8px;
        font-size: 36px;
        font-weight: 500;
        line-height: 1;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        opacity: 0.75;
    }

    .audio-close:hover {
        color: #6f6f6f;
        opacity: 1;
    }

    .result-card {
        border: 2px solid #5a7fc3;
        border-radius: 18px;
        padding: 18px 22px 14px;
        min-height: 290px;
        background: #ececec;
    }

    .result-title-green {
        color: #37c424 !important;
        font-size: 40px;
        font-weight: 800;
        margin: 0 0 28px 0;
        line-height: 1;
    }

    .result-title-red {
        color: #ff1f4e !important;
        font-size: 40px;
        font-weight: 800;
        margin: 0 0 28px 0;
        line-height: 1;
    }

    .result-center {
        font-size: 34px !important;
        font-weight: 800 !important;
        margin: 20px 0 36px 0 !important;
        text-align: center !important;
        line-height: 1.1 !important;
    }

    .result-center-green {
        color: #37c424 !important;
    }

    .result-center-red {
        color: #ff1f4e !important;
    }

    .metrics {
        display: grid;
        grid-template-columns: 1fr 1fr;
        row-gap: 16px;
        column-gap: 24px;
        font-size: 18px;
        font-weight: 700;
    }

    .metrics-green {
        color: #37c424;
    }

    .metrics-red {
        color: #ff1f4e;
    }

    .metric-item {
        display: flex;
        justify-content: space-between;
        gap: 8px;
    }

    @media (max-width: 1200px) {
        .header-title { font-size: 38px; }
        .stButton > button { font-size: 15px; }
        .result-title-green, .result-title-red { font-size: 36px; }
        .result-center { font-size: 30px !important; }
        .metrics { font-size: 14px; }
        .audio-name { font-size: 26px; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="header-bar">
        <h1 class="header-title">Oral Fluency Classification</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

side_l, col_left, col_right, side_r = st.columns([3.4, 1.5, 1.5, 3.4], gap="small")

with col_left:
    if st.button(
        "Avalinguo",
        type="primary" if st.session_state.dataset == "Avalinguo" else "secondary",
        use_container_width=True,
    ):
        st.session_state.dataset = "Avalinguo"
        st.rerun()

with col_right:
    if st.button(
        "SpeechOcean",
        type="primary" if st.session_state.dataset == "SpeechOcean" else "secondary",
        use_container_width=True,
    ):
        st.session_state.dataset = "SpeechOcean"
        st.rerun()

margin_l, top_mid, margin_r = st.columns([1.25, 8.6, 1.25], gap="small")

with top_mid:
    size_mb = uploaded_audio_data["size"] / (1024 * 1024)
    audio_b64 = base64.b64encode(uploaded_audio_data["bytes"]).decode("utf-8")
    audio_src = f"data:{uploaded_audio_data['mime']};base64,{audio_b64}"
    safe_name = escape(uploaded_audio_data["name"])
    st.markdown('<div class="upload-shell">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="uploaded-card">
            <div class="audio-icon">♪</div>
            <div class="audio-details">
                <p class="audio-name">{safe_name}</p>
                <p class="audio-size">{size_mb:.1f} MB</p>
                <audio controls class="audio-player-inline" src="{audio_src}"></audio>
            </div>
            <a class="audio-close" href="/?remove_audio=1" title="Remove audio">×</a>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

if st.session_state.dataset == "Avalinguo":
    baseline_result = "Low"
    proposed_result = "Intermediate"
else:
    baseline_result = "0 - 3"
    proposed_result = "6 - 7"

bottom_left, bottom_right = st.columns([1, 1], gap="large")

with bottom_left:
    st.markdown(
        f"""
        <div class="result-card">
            <h2 class="result-title-green">Baseline SVM</h2>
            <p class="result-center result-center-green">Result: &nbsp;&nbsp;{baseline_result}</p>
            <div class="metrics metrics-green">
                <div class="metric-item"><span>Accuracy:</span><span>80%</span></div>
                <div class="metric-item"><span>Recall:</span><span>80%</span></div>
                <div class="metric-item"><span>Precision:</span><span>80%</span></div>
                <div class="metric-item"><span>F1-Score:</span><span>80%</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with bottom_right:
    st.markdown(
        f"""
        <div class="result-card">
            <h2 class="result-title-red">Proposed SVM</h2>
            <p class="result-center result-center-red">Result: &nbsp;&nbsp;{proposed_result}</p>
            <div class="metrics metrics-red">
                <div class="metric-item"><span>Accuracy:</span><span>80%</span></div>
                <div class="metric-item"><span>Recall:</span><span>80%</span></div>
                <div class="metric-item"><span>Precision:</span><span>80%</span></div>
                <div class="metric-item"><span>F1-Score:</span><span>80%</span></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
