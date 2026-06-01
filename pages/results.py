import base64
import contextlib
import io
import wave
from html import escape
from pathlib import Path
from textwrap import dedent
from datetime import datetime

import joblib
import librosa
import numpy as np
import streamlit as st

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

st.set_page_config(
    page_title="Classification Results | Oral Fluency Classification",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_CSS = BASE_DIR / "assets" / "results.css"


# =========================
# LOAD CSS / HTML RENDERER
# =========================

def load_css(path: Path):
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_html(html: str):
    html = dedent(html).strip()
    html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


load_css(RESULTS_CSS)


# =========================
# SESSION DATA
# =========================

uploaded_audio_data = st.session_state.get("uploaded_audio_data")

if uploaded_audio_data is None:
    st.warning("No uploaded audio found. Please upload an audio file first.")

    if st.button("Back to Upload"):
        st.switch_page("pages/upload_audio.py")

    st.stop()


selected_dataset = st.session_state.get(
    "selected_model",
    st.session_state.get("selected_dataset", "AAD"),
)

if selected_dataset in ["Avalinguo", "AAD", "AAD Model"]:
    selected_dataset = "AAD"
else:
    selected_dataset = "SpeechOcean"


# =========================
# MODEL LOADERS
# =========================

@st.cache_resource
def load_aad_models():
    model_dir = BASE_DIR / "models" / "AAD"

    return {
        "baseline_scaler": joblib.load(model_dir / "AAD_baseline_scaler.pkl"),
        "baseline": joblib.load(model_dir / "AAD_baseline.pkl"),
        "mfcc_scaler": joblib.load(model_dir / "AAD_proposed_mfcc_scaler.pkl"),
        "rff": joblib.load(model_dir / "AAD_proposed_rff.pkl"),
        "nystrom": joblib.load(model_dir / "AAD_proposed_nystrom.pkl"),
        "hybrid_scaler": joblib.load(model_dir / "AAD_proposed_hybrid_scaler.pkl"),
        "proposed": joblib.load(model_dir / "AAD_proposed.pkl"),
    }


@st.cache_resource
def load_so762_models():
    model_dir = BASE_DIR / "models" / "SO762"

    return {
        "baseline_scaler": joblib.load(model_dir / "SO762_baseline_scaler.pkl"),
        "baseline": joblib.load(model_dir / "SO762_baseline.pkl"),
        "mfcc_scaler": joblib.load(model_dir / "SO762_proposed_mfcc_scaler.pkl"),
        "rff": joblib.load(model_dir / "SO762_proposed_rff.pkl"),
        "nystrom": joblib.load(model_dir / "SO762_proposed_nystrom.pkl"),
        "proposed": joblib.load(model_dir / "SO762_proposed.pkl"),
    }


# =========================
# FEATURE EXTRACTION
# =========================

def extract_mfcc_from_bytes(audio_bytes, sr=16000, n_mfcc=22):
    y, sr = librosa.load(io.BytesIO(audio_bytes), sr=sr)

    n_fft = int(0.025 * sr)
    hop_length = int(0.010 * sr)

    mfcc = librosa.feature.mfcc(
        y=y,
        sr=sr,
        n_mfcc=n_mfcc,
        n_fft=n_fft,
        hop_length=hop_length,
    )

    delta = librosa.feature.delta(mfcc)
    delta2 = librosa.feature.delta(mfcc, order=2)

    features = np.mean(np.vstack([mfcc, delta, delta2]), axis=1)

    return features.reshape(1, -1)


def get_audio_info(audio_bytes, filename):
    file_ext = filename.split(".")[-1].upper()
    size_mb = len(audio_bytes) / (1024 * 1024)

    info = {
        "duration": "Not available",
        "sample_rate": "Not available",
        "channels": "Not available",
        "file_size": f"{size_mb:.2f} MB",
        "format": file_ext,
    }

    try:
        if file_ext.lower() == "wav":
            with contextlib.closing(wave.open(io.BytesIO(audio_bytes), "rb")) as wav_file:
                frames = wav_file.getnframes()
                rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                duration = frames / float(rate)

                info["duration"] = f"{duration:.2f} sec"
                info["sample_rate"] = f"{rate:,} Hz"
                info["channels"] = "Mono" if channels == 1 else "Stereo"

        else:
            y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
            duration = librosa.get_duration(y=y, sr=sr)

            info["duration"] = f"{duration:.2f} sec"
            info["sample_rate"] = f"{sr:,} Hz"
            info["channels"] = "Not available"

    except Exception:
        pass

    return info


def make_waveform_svg(audio_bytes):
    try:
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=16000)
        y = y[: sr * 12]

        if len(y) == 0:
            return ""

        chunks = np.array_split(y, 140)
        values = np.array(
            [np.max(np.abs(chunk)) if len(chunk) else 0 for chunk in chunks]
        )

        if np.max(values) > 0:
            values = values / np.max(values)

        bars = []
        x = 0

        for value in values:
            height = 8 + value * 58
            y_pos = 44 - height / 2

            bars.append(
                f'<rect x="{x}" y="{y_pos:.2f}" width="3" height="{height:.2f}" rx="2" />'
            )

            x += 5

        return f"""
        <svg class="waveform-svg" viewBox="0 0 700 88" preserveAspectRatio="none">
            <g>{''.join(bars)}</g>
        </svg>
        """

    except Exception:
        return """
        <div class="waveform-placeholder">
            Waveform preview unavailable
        </div>
        """


# =========================
# CLASS LABELS
# =========================

AAD_CLASS_LABELS = {
    0: "Low",
    1: "Intermediate",
    2: "High",
}

SO762_CLASS_LABELS = {
    0: "Low",
    1: "Intermediate-Low",
    2: "Intermediate-High",
    3: "High",
}


def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum()


# =========================
# PREDICTION FUNCTIONS
# =========================

def predict_aad(audio_bytes):
    models = load_aad_models()
    features = extract_mfcc_from_bytes(audio_bytes)

    x_baseline = models["baseline_scaler"].transform(features)
    pred_baseline = models["baseline"].predict(x_baseline)[0]
    proba_baseline = models["baseline"].predict_proba(x_baseline)[0]

    label_baseline = AAD_CLASS_LABELS[pred_baseline]
    conf_baseline = proba_baseline[pred_baseline] * 100

    x_proposed = models["mfcc_scaler"].transform(features)
    x_rff = models["rff"].transform(x_proposed)
    x_nys = models["nystrom"].transform(x_proposed)
    x_hybrid = np.hstack((0.7 * x_rff, 0.3 * x_nys))
    x_hybrid = models["hybrid_scaler"].transform(x_hybrid)

    pred_proposed = models["proposed"].predict(x_hybrid)[0]
    scores_proposed = models["proposed"].decision_function(x_hybrid)[0]
    proba_proposed = softmax(scores_proposed)

    label_proposed = AAD_CLASS_LABELS[pred_proposed]
    conf_proposed = proba_proposed[pred_proposed] * 100

    return {
        "baseline": {
            "label": label_baseline,
            "confidence": conf_baseline,
            "probabilities": proba_baseline,
            "metrics": {
                "Accuracy": "82.09%",
                "Recall": "82.09%",
                "Precision": "82.34%",
                "F1-Score": "82.06%",
            },
        },
        "proposed": {
            "label": label_proposed,
            "confidence": conf_proposed,
            "probabilities": proba_proposed,
            "metrics": {
                "Accuracy": "85.39%",
                "Recall": "85.39%",
                "Precision": "85.52%",
                "F1-Score": "85.38%",
            },
        },
        "labels": AAD_CLASS_LABELS,
    }


def predict_so762(audio_bytes):
    models = load_so762_models()
    features = extract_mfcc_from_bytes(audio_bytes)

    x_baseline = models["baseline_scaler"].transform(features)
    proba_baseline = models["baseline"].predict_proba(x_baseline)[0]
    pred_baseline = int(np.argmax(proba_baseline))

    label_baseline = SO762_CLASS_LABELS[pred_baseline]
    conf_baseline = proba_baseline[pred_baseline] * 100

    x_proposed = models["mfcc_scaler"].transform(features)
    x_rff = models["rff"].transform(x_proposed)
    x_nys = models["nystrom"].transform(x_proposed)
    x_hybrid = np.hstack([x_rff, x_nys])

    proba_proposed = models["proposed"].predict_proba(x_hybrid)[0]
    pred_proposed = int(np.argmax(proba_proposed))

    label_proposed = SO762_CLASS_LABELS[pred_proposed]
    conf_proposed = proba_proposed[pred_proposed] * 100

    return {
        "baseline": {
            "label": label_baseline,
            "confidence": conf_baseline,
            "probabilities": proba_baseline,
            "metrics": {
                "Accuracy": "70.52%",
                "Recall": "70.52%",
                "Precision": "67.43%",
                "F1-Score": "68.25%",
            },
        },
        "proposed": {
            "label": label_proposed,
            "confidence": conf_proposed,
            "probabilities": proba_proposed,
            "metrics": {
                "Accuracy": "72.68%",
                "Recall": "72.68%",
                "Precision": "70.14%",
                "F1-Score": "70.30%",
            },
        },
        "labels": SO762_CLASS_LABELS,
    }


# =========================
# HTML BUILDERS
# =========================

def build_file_info(info, filename):
    safe_name = escape(filename)

    return f"""
    <div class="info-table">
        <div class="info-row">
            <span>▧ File Name</span>
            <strong>{safe_name}</strong>
        </div>

        <div class="info-row">
            <span>◷ Duration</span>
            <strong>{info["duration"]}</strong>
        </div>

        <div class="info-row">
            <span>≋ Sample Rate</span>
            <strong>{info["sample_rate"]}</strong>
        </div>

        <div class="info-row">
            <span>≡ Channels</span>
            <strong>{info["channels"]}</strong>
        </div>

        <div class="info-row">
            <span>▣ File Size</span>
            <strong>{info["file_size"]}</strong>
        </div>

        <div class="info-row">
            <span>▧ Format</span>
            <strong>{info["format"]}</strong>
        </div>
    </div>
    """


def build_probability_rows(probabilities, labels, color_class):
    rows = ""

    for index, probability in enumerate(probabilities):
        label = labels[index]
        percent = probability * 100

        rows += f"""
        <div class="prob-row">
            <span class="prob-label">{label}</span>

            <div class="prob-track">
                <div class="prob-fill {color_class}" style="width: {percent:.2f}%;"></div>
            </div>

            <strong>{percent:.2f}%</strong>
        </div>
        """

    return rows


def build_metric_items(metrics, color_class):
    icons = {
        "Accuracy": "◎",
        "Recall": "↻",
        "Precision": "◉",
        "F1-Score": "☆",
    }

    html = ""

    for name, value in metrics.items():
        html += f"""
        <div class="metric-item">
            <div class="metric-icon {color_class}">{icons.get(name, "•")}</div>

            <div>
                <span>{name}</span>
                <strong>{value}</strong>
            </div>
        </div>
        """

    return html


def build_result_card(title, badge, result, labels, theme):
    color_class = "blue" if theme == "blue" else "green"

    return f"""
    <section class="model-result-card {theme}">
        <div class="model-result-header">
            <div class="model-title-wrap">
                <div class="model-circle {color_class}">≋</div>
                <h2>{title}</h2>
            </div>

            <span class="result-badge {color_class}">{badge}</span>
        </div>

        <div class="model-main-grid">
            <div class="prediction-box">
                <span class="box-label">Predicted Fluency Level</span>

                <div class="prediction-row">
                    <strong class="{color_class}-text">{result["label"]}</strong>
                    <div class="mini-chart {color_class}">▥</div>
                </div>

                <span class="confidence-label">Confidence Score</span>

                <div class="confidence-value {color_class}-text">
                    {result["confidence"]:.2f}%
                </div>

                <div class="confidence-track">
                    <div class="confidence-fill {color_class}" style="width: {result["confidence"]:.2f}%;"></div>
                </div>
            </div>

            <div class="probability-box">
                <span class="box-label">Class Probabilities</span>
                {build_probability_rows(result["probabilities"], labels, color_class)}
            </div>
        </div>

        <div class="metric-grid">
            {build_metric_items(result["metrics"], color_class)}
        </div>
    </section>
    """


# =========================
# PDF GENERATOR
# =========================

def create_results_pdf(
    audio_name,
    audio_info,
    selected_dataset,
    prediction_results,
    summary_plain_text,
):
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.55 * inch,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0b1738"),
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#53627c"),
        spaceAfter=14,
    )

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0b1738"),
        spaceBefore=12,
        spaceAfter=8,
    )

    normal_style = ParagraphStyle(
        "NormalCustom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0b1738"),
    )

    story = []

    story.append(Paragraph("Oral Fluency Classification Results", title_style))
    story.append(
        Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            subtitle_style,
        )
    )

    story.append(Paragraph("Uploaded Audio Information", section_style))

    file_table_data = [
        ["File Name", audio_name],
        ["Dataset / Model", selected_dataset],
        ["Duration", audio_info["duration"]],
        ["Sample Rate", audio_info["sample_rate"]],
        ["Channels", audio_info["channels"]],
        ["File Size", audio_info["file_size"]],
        ["Format", audio_info["format"]],
    ]

    file_table = Table(file_table_data, colWidths=[1.8 * inch, 5.0 * inch])
    file_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eaf4ff")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#0b1738")),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dce6f4")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ROWBACKGROUNDS", (1, 0), (1, -1), [colors.white, colors.HexColor("#fbfdff")]),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    story.append(file_table)
    story.append(Spacer(1, 12))

    labels = prediction_results["labels"]

    for model_key, model_title in [
        ("baseline", "Baseline Model (SVM)"),
        ("proposed", "Proposed Model (Hybrid)"),
    ]:
        result = prediction_results[model_key]

        story.append(Paragraph(model_title, section_style))

        result_summary = [
            ["Predicted Fluency Level", result["label"]],
            ["Confidence Score", f'{result["confidence"]:.2f}%'],
        ]

        result_table = Table(result_summary, colWidths=[2.2 * inch, 4.6 * inch])
        result_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef6ff")),
                    ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                    ("FONTNAME", (1, 0), (1, -1), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, -1), 10),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dce6f4")),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 7),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
                ]
            )
        )

        story.append(result_table)
        story.append(Spacer(1, 8))

        probability_data = [["Class", "Probability"]]
        for index, probability in enumerate(result["probabilities"]):
            probability_data.append([labels[index], f"{probability * 100:.2f}%"])

        probability_table = Table(probability_data, colWidths=[3.4 * inch, 3.4 * inch])
        probability_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0b67f8")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dce6f4")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfdff")]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        story.append(Paragraph("Class Probabilities", normal_style))
        story.append(probability_table)
        story.append(Spacer(1, 8))

        metrics_data = [["Metric", "Value"]]
        for metric_name, metric_value in result["metrics"].items():
            metrics_data.append([metric_name, metric_value])

        metrics_table = Table(metrics_data, colWidths=[3.4 * inch, 3.4 * inch])
        metrics_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#22b854")),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                    ("FONTSIZE", (0, 0), (-1, -1), 9),
                    ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#dce6f4")),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#fbfdff")]),
                    ("LEFTPADDING", (0, 0), (-1, -1), 8),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )

        story.append(Paragraph("Overall Model Metrics", normal_style))
        story.append(metrics_table)
        story.append(Spacer(1, 12))

    story.append(Paragraph("Performance Summary", section_style))
    story.append(Paragraph(summary_plain_text, normal_style))

    doc.build(story)

    buffer.seek(0)
    return buffer.getvalue()


# =========================
# RUN PREDICTION
# =========================

audio_bytes = uploaded_audio_data["bytes"]
audio_name = uploaded_audio_data["name"]
audio_mime = uploaded_audio_data.get("mime", "audio/wav")

audio_info = get_audio_info(audio_bytes, audio_name)
waveform_svg = make_waveform_svg(audio_bytes)

try:
    with st.spinner("Extracting MFCC features and classifying your audio..."):
        if selected_dataset == "AAD":
            prediction_results = predict_aad(audio_bytes)
            dataset_label = "AAD"
        else:
            prediction_results = predict_so762(audio_bytes)
            dataset_label = "SO762"

    prediction_error = None

except Exception as error:
    prediction_error = str(error)
    prediction_results = None
    dataset_label = selected_dataset


# =========================
# PAGE HEADER
# =========================

render_html(
    """
    <div class="results-header">
        <div class="header-left">
            <div class="header-icon">✓</div>

            <div>
                <h1>Fluency Classification Results</h1>
                <p>Here are the classification results for your uploaded audio.</p>
            </div>
        </div>

        <a class="back-button" href="/upload_audio" target="_self">← Back to Upload</a>
    </div>
    """
)


# =========================
# TOP AUDIO + FILE INFO
# =========================

audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
audio_src = f"data:{audio_mime};base64,{audio_b64}"
safe_audio_name = escape(audio_name)

top_left, top_right = st.columns([1.08, 1], gap="large")

with top_left:
    render_html(
        f"""
        <section class="result-card uploaded-audio-card">
            <div class="card-title-row">
                <div class="card-icon blue">♫</div>
                <h2>Uploaded Audio</h2>
            </div>

            <div class="audio-name-row">
                <span>{safe_audio_name}</span>
                <strong>{audio_info["format"]}</strong>
            </div>

            <div class="waveform-wrap">
                {waveform_svg}
            </div>

            <div class="waveform-time">
                <span>0:00</span>
                <span>{audio_info["duration"].replace(" sec", "") if "sec" in audio_info["duration"] else "--"}</span>
            </div>

            <audio controls class="results-audio-player" src="{audio_src}"></audio>
        </section>
        """
    )


with top_right:
    render_html(
        f"""
        <section class="result-card file-info-card">
            <div class="card-title-row">
                <div class="card-icon blue">i</div>
                <h2>File Information</h2>
            </div>

            {build_file_info(audio_info, audio_name)}
        </section>
        """
    )


# =========================
# RESULTS
# =========================

if prediction_error:
    st.error(f"Prediction failed: {prediction_error}")

else:
    model_left, model_right = st.columns(2, gap="large")

    with model_left:
        render_html(
            build_result_card(
                title="Baseline Model (SVM)",
                badge="Balanced" if selected_dataset == "AAD" else "Baseline",
                result=prediction_results["baseline"],
                labels=prediction_results["labels"],
                theme="blue",
            )
        )

    with model_right:
        render_html(
            build_result_card(
                title="Proposed Model (Hybrid)",
                badge="Enhanced",
                result=prediction_results["proposed"],
                labels=prediction_results["labels"],
                theme="green",
            )
        )

    proposed_conf = prediction_results["proposed"]["confidence"]
    baseline_conf = prediction_results["baseline"]["confidence"]

    if proposed_conf >= baseline_conf:
        summary_html = (
            'The <strong class="green-text">Proposed Model (Hybrid)</strong> shows stronger confidence '
            'than the <strong class="blue-text">Baseline Model</strong> for this uploaded audio sample.'
        )
        summary_plain_text = (
            "The Proposed Model (Hybrid) shows stronger confidence than the Baseline Model "
            "for this uploaded audio sample."
        )
    else:
        summary_html = (
            'The <strong class="blue-text">Baseline Model</strong> shows stronger confidence '
            'than the <strong class="green-text">Proposed Model (Hybrid)</strong> for this uploaded audio sample.'
        )
        summary_plain_text = (
            "The Baseline Model shows stronger confidence than the Proposed Model (Hybrid) "
            "for this uploaded audio sample."
        )

    pdf_bytes = create_results_pdf(
        audio_name=audio_name,
        audio_info=audio_info,
        selected_dataset=dataset_label,
        prediction_results=prediction_results,
        summary_plain_text=summary_plain_text,
    )

    render_html(
        f"""
        <section class="performance-summary">
            <div class="summary-icon">🏆</div>

            <div class="summary-content">
                <h2>Performance Summary</h2>
                <p>{summary_html}</p>
                <p>The displayed metrics include accuracy, recall, precision, and F1-score for model comparison.</p>
            </div>
        </section>
        """
    )

    action_col1, action_col2, action_col3 = st.columns([1.8, 1, 1], gap="large")

    with action_col2:
        st.download_button(
            label="⇩ Download Results",
            data=pdf_bytes,
            file_name=f"fluency_classification_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mime="application/pdf",
            use_container_width=True,
            key="download_results_pdf",
        )

    with action_col3:
        if st.button("Analyze Another Audio →", use_container_width=True, key="analyze_another_audio"):
            st.session_state.pop("uploaded_audio_data", None)
            st.session_state.pop("uploaded_audio", None)
            st.session_state.pop("audio_upload", None)
            st.switch_page("pages/upload_audio.py")