import base64
import io
from html import escape

import numpy as np
import librosa
import joblib
import streamlit as st

st.set_page_config(page_title="Oral Fluency Classification", layout="wide")
# Hide sidebar
st.markdown("<style> [data-testid='stSidebarNav'] {display: none;} section[data-testid='stSidebar'] {display: none;} </style>", unsafe_allow_html=True)

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


@st.cache_resource
def load_aad_models():
    return {
        "baseline_scaler":  joblib.load("models/AAD/AAD_baseline_scaler.pkl"),
        "baseline":         joblib.load("models/AAD/AAD_baseline.pkl"),
        "mfcc_scaler":      joblib.load("models/AAD/AAD_proposed_mfcc_scaler.pkl"),
        "rff":              joblib.load("models/AAD/AAD_proposed_rff.pkl"),
        "nystrom":          joblib.load("models/AAD/AAD_proposed_nystrom.pkl"),
        "hybrid_scaler":    joblib.load("models/AAD/AAD_proposed_hybrid_scaler.pkl"),
        "proposed":         joblib.load("models/AAD/AAD_proposed.pkl"),
    }


def extract_mfcc_from_bytes(audio_bytes, sr=16000, n_mfcc=22):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=sr)
    n_fft      = int(0.025 * sr)
    hop_length = int(0.010 * sr)
    mfcc       = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc, n_fft=n_fft, hop_length=hop_length)
    delta      = librosa.feature.delta(mfcc)
    delta2     = librosa.feature.delta(mfcc, order=2)
    return np.mean(np.vstack([mfcc, delta, delta2]), axis=1).reshape(1, -1)


CLASS_LABELS = {0: "Low", 1: "Intermediate", 2: "High"}

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()

def predict_aad(audio_bytes):
    m        = load_aad_models()
    features = extract_mfcc_from_bytes(audio_bytes)

    X_b     = m["baseline_scaler"].transform(features)
    pred_b  = m["baseline"].predict(X_b)[0]
    proba_b = m["baseline"].predict_proba(X_b)[0]
    label_b = CLASS_LABELS[pred_b]
    conf_b  = proba_b[pred_b] * 100

    X_p      = m["mfcc_scaler"].transform(features)
    X_rff    = m["rff"].transform(X_p)
    X_nys    = m["nystrom"].transform(X_p)
    X_hybrid = np.hstack((0.7 * X_rff, 0.3 * X_nys))
    X_hybrid = m["hybrid_scaler"].transform(X_hybrid)
    pred_p   = m["proposed"].predict(X_hybrid)[0]
    scores_p = m["proposed"].decision_function(X_hybrid)[0]
    proba_p  = softmax(scores_p)
    label_p  = CLASS_LABELS[pred_p]
    conf_p   = proba_p[pred_p] * 100

    return label_b, conf_b, proba_b, label_p, conf_p, proba_p


def build_card(title, color, label, conf, proba, acc, rec, prec, f1):
    bars = "".join([
        f'<div style="display:flex;align-items:center;gap:10px;margin-bottom:7px;">'
        f'<span style="font-size:13px;font-weight:700;color:{color};width:90px;flex-shrink:0;">{CLASS_LABELS[i]}</span>'
        f'<div style="flex:1;height:10px;border-radius:999px;background:#ddd;overflow:hidden;">'
        f'<div style="width:{proba[i]*100:.1f}%;height:100%;border-radius:999px;background:{color};"></div>'
        f'</div>'
        f'<span style="font-size:13px;font-weight:700;color:{color};width:44px;text-align:right;">{proba[i]*100:.1f}%</span>'
        f'</div>'
        for i in range(len(CLASS_LABELS))
    ])

    return (
        f'<div style="border:2px solid #5a7fc3;border-radius:18px;padding:22px 24px;background:#ececec;font-family:Inter,sans-serif;">'
        f'<div style="font-size:36px;font-weight:800;color:{color};margin:0 0 14px 0;">{title}</div>'
        f'<div style="font-size:30px;font-weight:800;color:{color};text-align:center;margin:0 0 5px 0;">Result: &nbsp;{label}</div>'
        f'<div style="font-size:14px;font-weight:600;color:#888;text-align:center;margin:0 0 16px 0;">Confidence: {conf:.1f}%</div>'
        f'<hr style="border:none;border-top:1.5px solid #d0d0d0;margin:0 0 12px 0;">'
        f'<div style="font-size:11px;font-weight:700;color:#999;text-transform:uppercase;letter-spacing:0.6px;margin:0 0 10px 0;">Class Probabilities</div>'
        f'{bars}'
        f'<hr style="border:none;border-top:1.5px solid #d0d0d0;margin:14px 0 12px 0;">'
        f'<div style="font-size:11px;font-weight:700;color:#999;text-transform:uppercase;letter-spacing:0.6px;margin:0 0 12px 0;">Overall Model Metrics</div>'
        f'<div style="display:grid;grid-template-columns:1fr 1fr;row-gap:10px;column-gap:16px;">'
        f'<div style="display:flex;justify-content:space-between;font-size:15px;font-weight:700;color:{color};"><span>Accuracy:</span><span>{acc}</span></div>'
        f'<div style="display:flex;justify-content:space-between;font-size:15px;font-weight:700;color:{color};"><span>Recall:</span><span>{rec}</span></div>'
        f'<div style="display:flex;justify-content:space-between;font-size:15px;font-weight:700;color:{color};"><span>Precision:</span><span>{prec}</span></div>'
        f'<div style="display:flex;justify-content:space-between;font-size:15px;font-weight:700;color:{color};"><span>F1-Score:</span><span>{f1}</span></div>'
        f'</div>'
        f'</div>'
    )


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
header[data-testid="stHeader"] { display:none !important; }
.stApp { background-color:#ececec; font-family:'Inter',sans-serif; overflow-x:hidden; }
.block-container { max-width:1240px; padding-top:0.6rem; padding-bottom:2.5rem; }
.header-bar {
    width:100vw; margin-left:calc(50% - 50vw); margin-right:calc(50% - 50vw);
    margin-bottom:2.55rem; background:#274d98; height:94px; display:flex;
    align-items:center; padding-left:max(32px, calc((100vw - 1240px) / 2 + 70px));
    border-top:1px solid #1c3a76; box-sizing:border-box;
}
.header-title { color:#fff; font-size:50px; font-weight:800; line-height:1; margin:0; }
.stButton > button { border-radius:999px; font-weight:700; font-size:17px; padding:8px 24px; min-height:38px; border:2px solid #2e56a4; transition:none; }
.stButton > button[kind="primary"]   { color:#fff; background:#2e56a4; }
.stButton > button[kind="secondary"] { color:#2e56a4; background:#ececec; }
.upload-shell { max-width:660px; margin:0 auto; }
.uploaded-card { height:178px; border:1.8px solid #5a7fc3; border-radius:12px; background:#d2d8e5; padding:22px 24px; display:flex; align-items:center; gap:20px; box-sizing:border-box; }
.audio-icon { width:90px; height:90px; border-radius:12px; background:#828282; color:#fff; display:flex; align-items:center; justify-content:center; font-size:48px; flex-shrink:0; }
.audio-details { flex:1; display:flex; flex-direction:column; justify-content:center; color:#7b7b7b; }
.audio-name { font-size:34px; font-weight:700; line-height:1.1; margin:0 0 8px 0; }
.audio-size { font-size:18px; margin:0 0 6px 0; }
.audio-player-inline { width:100%; height:34px; border-radius:10px; }
.audio-close { color:#8f8f8f; margin-left:8px; font-size:36px; font-weight:500; text-decoration:none; display:inline-flex; align-items:center; justify-content:center; opacity:0.75; }
.audio-close:hover { color:#6f6f6f; opacity:1; }
.unavailable-card { border:2px dashed #aaa; border-radius:18px; padding:18px 22px; min-height:320px; background:#ececec; display:flex; flex-direction:column; align-items:center; justify-content:center; color:#aaa; font-size:20px; font-weight:700; text-align:center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="header-bar"><h1 class="header-title">Oral Fluency Classification</h1></div>', unsafe_allow_html=True)

side_l, col_left, col_right, side_r = st.columns([3.4, 1.5, 1.5, 3.4], gap="small")
with col_left:
    if st.button("Avalinguo", type="primary" if st.session_state.dataset == "Avalinguo" else "secondary", use_container_width=True):
        st.session_state.dataset = "Avalinguo"
        st.rerun()
with col_right:
    if st.button("SpeechOcean", type="primary" if st.session_state.dataset == "SpeechOcean" else "secondary", use_container_width=True):
        st.session_state.dataset = "SpeechOcean"
        st.rerun()

margin_l, top_mid, margin_r = st.columns([1.25, 8.6, 1.25], gap="small")
with top_mid:
    size_mb   = uploaded_audio_data["size"] / (1024 * 1024)
    audio_b64 = base64.b64encode(uploaded_audio_data["bytes"]).decode("utf-8")
    audio_src = f"data:{uploaded_audio_data['mime']};base64,{audio_b64}"
    safe_name = escape(uploaded_audio_data["name"])
    st.markdown('<div class="upload-shell">', unsafe_allow_html=True)
    st.markdown(f'<div class="uploaded-card"><div class="audio-icon">♪</div><div class="audio-details"><p class="audio-name">{safe_name}</p><p class="audio-size">{size_mb:.1f} MB</p><audio controls class="audio-player-inline" src="{audio_src}"></audio></div><a class="audio-close" href="/?remove_audio=1" title="Remove audio">×</a></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

bottom_left, bottom_right = st.columns([1, 1], gap="large")

if st.session_state.dataset == "Avalinguo":
    with st.spinner("🔄 Extracting features and classifying..."):
        try:
            label_b, conf_b, proba_b, label_p, conf_p, proba_p = predict_aad(uploaded_audio_data["bytes"])
            predict_error = None
        except Exception as e:
            predict_error = str(e)

    if predict_error:
        st.error(f"Prediction failed: {predict_error}")
    else:
        with bottom_left:
            st.markdown(build_card("Baseline SVM", "#37c424", label_b, conf_b, proba_b, "82.09%", "82.09%", "82.34%", "82.06%"), unsafe_allow_html=True)
        with bottom_right:
            st.markdown(build_card("Proposed SVM", "#ff1f4e", label_p, conf_p, proba_p, "85.39%", "85.39%", "85.52%", "85.38%"), unsafe_allow_html=True)
else:
    with bottom_left:
        st.markdown('<div class="unavailable-card"><div style="font-size:48px;margin-bottom:12px;">🚧</div><div>SpeechOcean model</div><div style="font-size:15px;font-weight:500;color:#bbb;margin-top:8px;">Coming soon</div></div>', unsafe_allow_html=True)
    with bottom_right:
        st.markdown('<div class="unavailable-card"><div style="font-size:48px;margin-bottom:12px;">🚧</div><div>SpeechOcean model</div><div style="font-size:15px;font-weight:500;color:#bbb;margin-top:8px;">Coming soon</div></div>', unsafe_allow_html=True)