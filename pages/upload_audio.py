import streamlit as st
from pathlib import Path
from textwrap import dedent
import wave
import contextlib

st.set_page_config(
    page_title="Upload Audio | Oral Fluency Classification",
    page_icon="⬆️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.sidebar import load_sidebar_css, render_sidebar

load_sidebar_css()
render_sidebar(active_page="Upload Audio")

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_CSS = BASE_DIR / "assets" / "upload_audio.css"
NOTE_IMAGE = BASE_DIR / "assets" / "audio_note.jpg"


def load_css(path: Path):
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_html(html: str):
    html = dedent(html).strip()
    html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


def get_query_model():
    model = st.query_params.get("model", None)

    if isinstance(model, list):
        model = model[0] if model else None

    if model in ["AAD", "SpeechOcean"]:
        return model

    return None


def get_wav_info(uploaded_file):
    try:
        uploaded_file.seek(0)

        temp_path = BASE_DIR / "temp_uploaded_audio.wav"
        temp_path.write_bytes(uploaded_file.read())

        with contextlib.closing(wave.open(str(temp_path), "rb")) as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
            duration = frames / float(rate)

        uploaded_file.seek(0)

        return {
            "duration": f"{duration:.2f} sec",
            "sample_rate": f"{rate:,} Hz",
            "channels": "Mono" if channels == 1 else "Stereo",
        }

    except Exception:
        uploaded_file.seek(0)
        return {
            "duration": "Not available",
            "sample_rate": "Not available",
            "channels": "Not available",
        }


load_css(UPLOAD_CSS)

if "selected_dataset" not in st.session_state:
    st.session_state.selected_dataset = "AAD"

query_model = get_query_model()
if query_model:
    st.session_state.selected_dataset = query_model

selected_dataset = st.session_state.selected_dataset
selected_model_text = "AAD Model" if selected_dataset == "AAD" else "SpeechOcean Model"


# =========================
# HEADER
# =========================

render_html(
    """
    <div class="upload-header-row">
        <div>
            <h1 class="upload-title">Upload Audio</h1>
            <p class="upload-subtitle">
                Upload a speech audio file and select the dataset/model to use for fluency classification.
            </p>
        </div>

        <div class="format-card">
            <div class="format-icon">i</div>
            <div>
                <div class="format-title">Accepted Formats</div>
                <div class="format-text">WAV, MP3</div>
                <div class="format-text">Max file size: 500 MB</div>
            </div>
        </div>
    </div>
    """
)


# =========================
# MODEL SELECTION
# =========================

aad_class = "selected" if selected_dataset == "AAD" else ""
speech_class = "selected-green" if selected_dataset == "SpeechOcean" else ""

render_html(
    f"""
    <section class="upload-card model-section">
        <div class="section-title-row">
            <div class="step-circle">1</div>
            <div>
                <h2>Select Dataset / Model</h2>
                <p>Choose the dataset and model you want to use for classification.</p>
            </div>
        </div>

        <div class="model-grid">
            <a class="model-card {aad_class}" href="?model=AAD" target="_self">
                <div class="radio-circle"></div>

                <div class="model-icon blue">
                    <span>≋</span>
                </div>

                <div class="model-content">
                    <div class="model-heading-row">
                        <h3>AAD Model</h3>
                        <span class="model-badge blue-badge">Balanced</span>
                    </div>

                    <p class="model-name">Avalinguo Audio Dataset (AAD)</p>
                    <p class="model-desc">Trained on balanced data across fluency levels.</p>

                    <div class="model-note blue-note">
                        ✓ Best for balanced evaluation scenarios.
                    </div>
                </div>
            </a>

            <a class="model-card {speech_class}" href="?model=SpeechOcean" target="_self">
                <div class="radio-circle"></div>

                <div class="model-icon green">
                    <span>≋</span>
                </div>

                <div class="model-content">
                    <div class="model-heading-row">
                        <h3>SpeechOcean Model</h3>
                        <span class="model-badge gray-badge">Imbalanced</span>
                    </div>

                    <p class="model-name">SpeechOcean762 (SO762)</p>
                    <p class="model-desc">Trained on real-world imbalanced data.</p>

                    <div class="model-note green-note">
                        ✓ Best for real-world, imbalanced evaluation.
                    </div>
                </div>
            </a>
        </div>

        <div class="info-banner">
            <div class="info-dot">i</div>
            <div>
                The selected model is <strong>{selected_model_text}</strong>. It will be used to extract features,
                make predictions, and evaluate fluency.
            </div>
        </div>
    </section>
    """
)


# =========================
# UPLOAD AUDIO + PREVIEW
# =========================

upload_col, preview_col = st.columns([2.2, 1], gap="large")

with upload_col:
    with st.container(border=True):
        render_html(
            """
            <div class="section-title-row upload-title-inside">
                <div class="step-circle">2</div>
                <div>
                    <h2>Upload Audio File</h2>
                    <p>Upload a single audio file for preprocessing and fluency classification.</p>
                </div>
            </div>
            """
        )

        uploaded_file = st.file_uploader(
            "Drag and drop your audio file here",
            type=["wav", "mp3"],
            label_visibility="collapsed",
            key="audio_upload",
        )

        render_html(
            """
            <div class="supported-text">
                Supported formats: WAV, MP3 &nbsp;•&nbsp; Maximum file size: 500 MB
            </div>
            """
        )

with preview_col:
    with st.container(border=True):
        render_html('<div class="preview-card-inner"><h2>Audio Preview</h2>')

        if uploaded_file is None:
            render_html(
                """
                <div class="empty-preview">
                    <p>No audio uploaded yet.</p>
                    <p>Upload an audio file to see the waveform and details.</p>
                </div>

                <div class="preview-divider"></div>

                <h3 class="file-info-title">File Information</h3>

                <div class="file-info-list">
                    <div><span>▧ File Name</span><strong>-</strong></div>
                    <div><span>◷ Duration</span><strong>-</strong></div>
                    <div><span>≋ Sample Rate</span><strong>-</strong></div>
                    <div><span>≡ Channels</span><strong>-</strong></div>
                    <div><span>▣ File Size</span><strong>-</strong></div>
                </div>
                """
            )

        else:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            file_ext = uploaded_file.name.split(".")[-1].lower()

            if file_ext == "wav":
                audio_info = get_wav_info(uploaded_file)
            else:
                audio_info = {
                    "duration": "MP3 preview only",
                    "sample_rate": "Not available",
                    "channels": "Not available",
                }

            render_html('<div class="audio-note-area">')

            if NOTE_IMAGE.exists():
                st.image(str(NOTE_IMAGE), width=700)
            else:
                render_html('<div class="audio-note-fallback">🎵</div>')

            render_html("</div>")

            st.audio(uploaded_file)

            render_html(
                f"""
                <div class="preview-divider"></div>

                <h3 class="file-info-title">File Information</h3>

                <div class="file-info-list">
                    <div><span>▧ File Name</span><strong>{uploaded_file.name}</strong></div>
                    <div><span>◷ Duration</span><strong>{audio_info["duration"]}</strong></div>
                    <div><span>≋ Sample Rate</span><strong>{audio_info["sample_rate"]}</strong></div>
                    <div><span>≡ Channels</span><strong>{audio_info["channels"]}</strong></div>
                    <div><span>▣ File Size</span><strong>{file_size_mb:.2f} MB</strong></div>
                </div>
                """
            )

        render_html("</div>")


# =========================
# NEXT STEP
# =========================

with st.container(border=True):
    next_text_col, next_button_col = st.columns([2.8, 1], gap="large")

    with next_text_col:
        render_html(
            """
            <div class="section-title-row next-title-row">
                <div class="step-circle">3</div>
                <div>
                    <h2>Next Steps</h2>
                    <p>After uploading, you can proceed to preprocess and classify the audio.</p>
                </div>
            </div>
            """
        )

    with next_button_col:
        with st.container(key="preprocess_area"):
            classify_clicked = st.button(
                "Preprocess & Classify  →",
                key="preprocess_classify",
                use_container_width=True,
            )

if classify_clicked:
    if uploaded_file is None:
        st.warning("Please upload an audio file first before preprocessing.")
    else:
        uploaded_file.seek(0)
        audio_bytes = uploaded_file.read()
        uploaded_file.seek(0)

        st.session_state.uploaded_audio_data = {
            "name": uploaded_file.name,
            "size": uploaded_file.size,
            "mime": uploaded_file.type or "audio/wav",
            "bytes": audio_bytes,
        }

        st.session_state.selected_model = selected_dataset

        st.switch_page("pages/results.py")