import streamlit as st
from pathlib import Path
from textwrap import dedent
from datetime import datetime

st.set_page_config(
    page_title="Dashboard | Oral Fluency Classification",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.sidebar import load_sidebar_css, render_sidebar

load_sidebar_css()
render_sidebar(active_page="Dashboard")


BASE_DIR = Path(__file__).resolve().parent
DASHBOARD_CSS = BASE_DIR / "assets" / "dashboard.css"


def load_css(path: Path):
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_html(html: str):
    html = dedent(html).strip()
    html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


load_css(DASHBOARD_CSS)


# =========================
# SESSION DATA
# =========================

uploaded_audio_data = st.session_state.get("uploaded_audio_data")
selected_dataset = st.session_state.get(
    "selected_model",
    st.session_state.get("selected_dataset", "AAD"),
)

if selected_dataset in ["Avalinguo", "AAD", "AAD Model"]:
    selected_dataset_label = "AAD Model"
else:
    selected_dataset_label = "SpeechOcean762 Model"


if uploaded_audio_data:
    current_audio_name = uploaded_audio_data.get("name", "Uploaded audio")
    current_audio_size = uploaded_audio_data.get("size", 0) / (1024 * 1024)
    current_audio_mime = uploaded_audio_data.get("mime", "audio/wav")
    session_status = "Audio uploaded and ready for classification."
    session_badge = "Ready"
else:
    current_audio_name = "No audio uploaded yet"
    current_audio_size = 0
    current_audio_mime = "-"
    session_status = "Upload an audio file to start fluency classification."
    session_badge = "Waiting"


today = datetime.now()
date_display = today.strftime("%B %d, %Y")
time_display = today.strftime("%A, %I:%M %p")


# =========================
# PAGE UI
# =========================

render_html(
    f"""
    <main class="dashboard-page">

        <section class="dashboard-header">
            <div>
                <h1>Dashboard</h1>
                <p>Monitor your oral fluency classification system overview and performance.</p>
            </div>

            <div class="date-card">
                <div class="date-icon">
                    <svg viewBox="0 0 24 24" fill="none">
                        <rect x="4" y="5" width="16" height="15" rx="2" stroke="currentColor" stroke-width="2"/>
                        <path d="M8 3V7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <path d="M16 3V7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                        <path d="M4 10H20" stroke="currentColor" stroke-width="2"/>
                        <path d="M8 14H10M12 14H14M16 14H18M8 17H10M12 17H14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>
                    </svg>
                </div>

                <div>
                    <strong>{date_display}</strong>
                    <span>{time_display}</span>
                </div>
            </div>
        </section>


        <section class="metric-grid">
            <div class="metric-card">
                <div class="metric-icon blue-icon">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M4 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M8 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M12 19V5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M16 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M20 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                </div>
                <div>
                    <span>Feature Type</span>
                    <strong>66-D</strong>
                    <small class="blue-text">MFCC Features</small>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-icon green-icon">✓</div>
                <div>
                    <span>Available Models</span>
                    <strong>2</strong>
                    <small class="green-text">Baseline & Enhanced SVM</small>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-icon yellow-icon">▣</div>
                <div>
                    <span>Datasets</span>
                    <strong>2</strong>
                    <small class="yellow-text">AAD and SO762</small>
                </div>
            </div>

            <div class="metric-card">
                <div class="metric-icon purple-icon">◎</div>
                <div>
                    <span>Selected Model</span>
                    <strong class="model-value">{selected_dataset_label}</strong>
                    <small class="purple-text">Current session</small>
                </div>
            </div>
        </section>


        <section class="main-grid">
            <div class="dashboard-card session-card">
                <div class="card-header-row">
                    <h2>Current Session</h2>
                    <span class="status-label {session_badge.lower()}">{session_badge}</span>
                </div>

                <div class="session-content">
                    <div class="session-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M4 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                            <path d="M8 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                            <path d="M12 19V5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                            <path d="M16 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                            <path d="M20 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        </svg>
                    </div>

                    <div>
                        <h3>{current_audio_name}</h3>
                        <p>{session_status}</p>

                        <div class="session-details">
                            <div>
                                <span>Selected Model</span>
                                <strong>{selected_dataset_label}</strong>
                            </div>

                            <div>
                                <span>File Type</span>
                                <strong>{current_audio_mime}</strong>
                            </div>

                            <div>
                                <span>File Size</span>
                                <strong>{current_audio_size:.2f} MB</strong>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="action-row">
                    <a class="primary-action" href="/upload_audio" target="_self">
                        Upload Audio
                    </a>

                    <a class="secondary-action" href="/results" target="_self">
                        View Results
                    </a>
                </div>
            </div>


            <div class="dashboard-card model-summary-card">
                <div class="card-header-row">
                    <h2>Model Summary</h2>
                    <span class="select-pill">Thesis Results</span>
                </div>

                <div class="model-summary-grid">
                    <div class="model-box baseline-box">
                        <div class="model-icon blue-icon-small">SVM</div>
                        <h3>Baseline SVM</h3>
                        <p>Uses exact RBF kernel with standard SVC / libsvm optimization.</p>
                        <div class="model-stat">
                            <span>AAD Accuracy</span>
                            <strong>82.09%</strong>
                        </div>
                    </div>

                    <div class="model-box enhanced-box">
                        <div class="model-icon green-icon-small">SVM</div>
                        <h3>Enhanced SVM</h3>
                        <p>Uses Hybrid RFF–Nyström kernel approximation with SMO optimization.</p>
                        <div class="model-stat">
                            <span>AAD Accuracy</span>
                            <strong>85.39%</strong>
                        </div>
                    </div>
                </div>
            </div>
        </section>


        <section class="chart-grid">
            <div class="dashboard-card distribution-card">
                <div class="card-header-row">
                    <h2>AAD Class Distribution</h2>
                    <span class="select-pill">Balanced</span>
                </div>

                <div class="distribution-content">
                    <div class="donut-chart aad-donut">
                        <div class="donut-center">
                            <strong>1,424</strong>
                            <span>Total</span>
                        </div>
                    </div>

                    <div class="legend-list">
                        <div>
                            <i class="legend-dot low-dot"></i>
                            <div>
                                <strong>Low</strong>
                                <span>438 samples</span>
                            </div>
                        </div>

                        <div>
                            <i class="legend-dot medium-dot"></i>
                            <div>
                                <strong>Intermediate</strong>
                                <span>527 samples</span>
                            </div>
                        </div>

                        <div>
                            <i class="legend-dot high-dot"></i>
                            <div>
                                <strong>High</strong>
                                <span>459 samples</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div class="dashboard-card distribution-card">
                <div class="card-header-row">
                    <h2>SO762 Class Distribution</h2>
                    <span class="select-pill">Imbalanced</span>
                </div>

                <div class="distribution-content">
                    <div class="donut-chart so-donut">
                        <div class="donut-center">
                            <strong>5,000</strong>
                            <span>Total</span>
                        </div>
                    </div>

                    <div class="legend-list">
                        <div>
                            <i class="legend-dot low-dot"></i>
                            <div>
                                <strong>Class 0</strong>
                                <span>52 samples</span>
                            </div>
                        </div>

                        <div>
                            <i class="legend-dot yellow-dot"></i>
                            <div>
                                <strong>Class 1</strong>
                                <span>398 samples</span>
                            </div>
                        </div>

                        <div>
                            <i class="legend-dot medium-dot"></i>
                            <div>
                                <strong>Class 2</strong>
                                <span>1,203 samples</span>
                            </div>
                        </div>

                        <div>
                            <i class="legend-dot high-dot"></i>
                            <div>
                                <strong>Class 3</strong>
                                <span>3,347 samples</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>


        <section class="lower-grid">
            <div class="dashboard-card performance-card">
                <div class="card-header-row">
                    <h2>Model Performance Overview</h2>
                    <span class="select-pill">AAD Dataset</span>
                </div>

                <div class="performance-table-wrap">
                    <table class="performance-table">
                        <thead>
                            <tr>
                                <th>Metric</th>
                                <th>Baseline SVM</th>
                                <th>Enhanced SVM</th>
                                <th>Change</th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr>
                                <td>Accuracy</td>
                                <td>82.09%</td>
                                <td>85.39%</td>
                                <td class="positive">+3.30%</td>
                            </tr>

                            <tr>
                                <td>Precision</td>
                                <td>82.48%</td>
                                <td>85.58%</td>
                                <td class="positive">+3.10%</td>
                            </tr>

                            <tr>
                                <td>Recall</td>
                                <td>82.09%</td>
                                <td>85.39%</td>
                                <td class="positive">+3.30%</td>
                            </tr>

                            <tr>
                                <td>F1-Score</td>
                                <td>82.21%</td>
                                <td>85.43%</td>
                                <td class="positive">+3.22%</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <a class="card-link-button" href="/model_comparison" target="_self">
                    View Model Comparison <span>›</span>
                </a>
            </div>


            <div class="dashboard-card dataset-card">
                <div class="card-header-row">
                    <h2>Dataset Summary</h2>
                    <span class="select-pill">Public Datasets</span>
                </div>

                <div class="dataset-summary-item">
                    <div class="dataset-icon blue-dataset-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <ellipse cx="12" cy="5" rx="7" ry="3" stroke="currentColor" stroke-width="2"/>
                            <path d="M5 5V12C5 13.7 8.1 15 12 15C15.9 15 19 13.7 19 12V5" stroke="currentColor" stroke-width="2"/>
                            <path d="M5 12V19C5 20.7 8.1 22 12 22C15.9 22 19 20.7 19 19V12" stroke="currentColor" stroke-width="2"/>
                        </svg>
                    </div>

                    <div class="dataset-info">
                        <h3>AAD Dataset</h3>

                        <div class="dataset-stats">
                            <div>
                                <span>Total Samples</span>
                                <strong class="blue-text">1,424</strong>
                            </div>

                            <div>
                                <span>Classes</span>
                                <strong>3</strong>
                            </div>

                            <div>
                                <span>Speech Type</span>
                                <strong>Spontaneous</strong>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="dataset-summary-item">
                    <div class="dataset-icon purple-dataset-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <ellipse cx="12" cy="5" rx="7" ry="3" stroke="currentColor" stroke-width="2"/>
                            <path d="M5 5V12C5 13.7 8.1 15 12 15C15.9 15 19 13.7 19 12V5" stroke="currentColor" stroke-width="2"/>
                            <path d="M5 12V19C5 20.7 8.1 22 12 22C15.9 22 19 20.7 19 19V12" stroke="currentColor" stroke-width="2"/>
                        </svg>
                    </div>

                    <div class="dataset-info">
                        <h3>SO762 Dataset</h3>

                        <div class="dataset-stats">
                            <div>
                                <span>Total Samples</span>
                                <strong class="purple-text">5,000</strong>
                            </div>

                            <div>
                                <span>Classes</span>
                                <strong>4</strong>
                            </div>

                            <div>
                                <span>Speech Type</span>
                                <strong>Read Speech</strong>
                            </div>
                        </div>
                    </div>
                </div>

                <a class="card-link-button" href="/datasets" target="_self">
                    View All Datasets <span>›</span>
                </a>
            </div>
            
        </section>

    </main>
    """
)