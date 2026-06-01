import streamlit as st
from pathlib import Path
from textwrap import dedent

st.set_page_config(
    page_title="Datasets | Oral Fluency Classification",
    page_icon="🗃️",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.sidebar import load_sidebar_css, render_sidebar

load_sidebar_css()
render_sidebar(active_page="Datasets")

BASE_DIR = Path(__file__).resolve().parent.parent
DATASETS_CSS = BASE_DIR / "assets" / "datasets.css"


def load_css(path: Path):
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_html(html: str):
    html = dedent(html).strip()
    html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


load_css(DATASETS_CSS)


# =========================
# DATA
# =========================

AAD_SOURCE = "https://www.kaggle.com/datasets/petalsonwind/avalinguo-dataset"
SO762_SOURCE = "https://github.com/jimbozhang/speechocean762"

aad_total = 1424
aad_low = 438
aad_intermediate = 527
aad_high = 459

so_total = 5000
so_03 = 1283
so_45 = 398
so_67 = 1203
so_810 = 3347


def percent(value, total):
    return (value / total) * 100


# =========================
# HEADER
# =========================

render_html(
    """
    <section class="datasets-header">
        <div class="datasets-title-wrap">
            <div class="main-page-icon">
                <svg viewBox="0 0 24 24" fill="none">
                    <ellipse cx="12" cy="5" rx="7" ry="3" stroke="currentColor" stroke-width="2"/>
                    <path d="M5 5V12C5 13.7 8.1 15 12 15C15.9 15 19 13.7 19 12V5" stroke="currentColor" stroke-width="2"/>
                    <path d="M5 12V19C5 20.7 8.1 22 12 22C15.9 22 19 20.7 19 19V12" stroke="currentColor" stroke-width="2"/>
                </svg>
            </div>

            <div>
                <h1>Datasets</h1>
                <p>
                    Information about the datasets used in training and evaluating
                    the SVM models for oral fluency classification.
                </p>
            </div>
        </div>

        <div class="about-dataset-card">
            <div class="about-icon">i</div>

            <div>
                <h3>About the Datasets</h3>
                <p>
                    This study uses two publicly available speech datasets:
                    Avalinguo Audio Dataset (AAD) and SpeechOcean762 (SO762).
                    AAD is a balanced dataset with 3 fluency classes, while SO762
                    is an imbalanced dataset with 4 score-based fluency groups.
                </p>
            </div>
        </div>
    </section>

    <div class="dataset-tabs">
        <a class="active" href="#overview">
            <span>▦</span>
            Dataset Overview
        </a>

        <a href="#comparison">
            <span>▥</span>
            Dataset Comparison
        </a>
    </div>
    """
)


# =========================
# DATASET CARDS
# =========================

render_html(
    f"""
    <section class="dataset-card-grid" id="overview">
        <div class="dataset-card aad-card">
            <div class="dataset-card-header">
                <div class="dataset-icon blue-icon">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M4 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M8 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M12 19V5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M16 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M20 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                </div>

                <div class="dataset-heading">
                    <div class="dataset-title-line">
                        <h2>Avalinguo Audio Dataset (AAD)</h2>
                        <span class="badge blue-badge">Balanced</span>
                    </div>

                    <p>
                        Conversational speech dataset collected from non-native English adults
                        with three fluency levels.
                    </p>
                </div>
            </div>

            <div class="stat-row">
                <div>
                    <span>Total Samples</span>
                    <strong class="blue-text">1,424</strong>
                    <small>segments</small>
                </div>

                <div>
                    <span>Speech Type</span>
                    <strong>Spontaneous</strong>
                    <small>conversation</small>
                </div>

                <div>
                    <span>Duration</span>
                    <strong>~2</strong>
                    <small>hours</small>
                </div>

                <div>
                    <span>Sample Rate</span>
                    <strong class="blue-text">16 kHz</strong>
                    <small>16-bit PCM</small>
                </div>

                <div>
                    <span>Format</span>
                    <strong class="format-pill blue-format">WAV</strong>
                    <small>audio</small>
                </div>
            </div>

            <h3 class="subsection-title">Fluency Classes</h3>

            <div class="class-grid three-cols">
                <div class="class-box low">
                    <span class="dot green-dot"></span>
                    <h4>Low</h4>
                    <strong>438</strong>
                    <small>{percent(aad_low, aad_total):.2f}%</small>
                </div>

                <div class="class-box intermediate">
                    <span class="dot yellow-dot"></span>
                    <h4>Intermediate</h4>
                    <strong>527</strong>
                    <small>{percent(aad_intermediate, aad_total):.2f}%</small>
                </div>

                <div class="class-box high">
                    <span class="dot red-dot"></span>
                    <h4>High</h4>
                    <strong>459</strong>
                    <small>{percent(aad_high, aad_total):.2f}%</small>
                </div>
            </div>

            <div class="description-box blue-description">
                <div class="description-icon">▧</div>
                <p>
                    <strong>Description:</strong> AAD contains spontaneous conversational
                    speech samples rated by human experts into Low, Intermediate,
                    and High fluency classes.
                </p>
            </div>
        </div>


        <div class="dataset-card so-card">
            <div class="dataset-card-header">
                <div class="dataset-icon green-icon">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M4 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M8 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M12 19V5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M16 16V8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M20 13V11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/>
                    </svg>
                </div>

                <div class="dataset-heading">
                    <div class="dataset-title-line">
                        <h2>SpeechOcean762 (SO762)</h2>
                        <span class="badge green-badge">Imbalanced</span>
                    </div>

                    <p>
                        Read speech dataset from Mandarin-speaking English learners,
                        scored from 0 to 10.
                    </p>
                </div>
            </div>

            <div class="stat-row">
                <div>
                    <span>Total Samples</span>
                    <strong class="green-text">5,000</strong>
                    <small>utterances</small>
                </div>

                <div>
                    <span>Speakers</span>
                    <strong class="green-text">250</strong>
                    <small>speakers</small>
                </div>

                <div>
                    <span>Duration</span>
                    <strong>~6</strong>
                    <small>hours</small>
                </div>

                <div>
                    <span>Sample Rate</span>
                    <strong class="green-text">16 kHz</strong>
                    <small>16-bit PCM</small>
                </div>

                <div>
                    <span>Format</span>
                    <strong class="format-pill green-format">WAV</strong>
                    <small>audio</small>
                </div>
            </div>

            <h3 class="subsection-title">Fluency Score Groups</h3>

            <div class="class-grid four-cols">
                <div class="class-box so-low">
                    <span class="dot green-dot"></span>
                    <h4>0 – 3</h4>
                    <strong>1,283</strong>
                    <small>{percent(so_03, so_total):.2f}%</small>
                </div>

                <div class="class-box so-midlow">
                    <span class="dot yellow-dot"></span>
                    <h4>4 – 5</h4>
                    <strong>398</strong>
                    <small>{percent(so_45, so_total):.2f}%</small>
                </div>

                <div class="class-box so-mid">
                    <span class="dot orange-dot"></span>
                    <h4>6 – 7</h4>
                    <strong>1,203</strong>
                    <small>{percent(so_67, so_total):.2f}%</small>
                </div>

                <div class="class-box so-high">
                    <span class="dot red-dot"></span>
                    <h4>8 – 10</h4>
                    <strong>3,347</strong>
                    <small>{percent(so_810, so_total):.2f}%</small>
                </div>
            </div>

            <div class="description-box green-description">
                <div class="description-icon">▧</div>
                <p>
                    <strong>Description:</strong> SO762 contains read speech samples
                    scored from 0–10. Class 8–10 dominates the dataset, making it
                    highly imbalanced.
                </p>
            </div>
        </div>
    </section>
    """
)


# =========================
# COMPARISON + DISTRIBUTION
# =========================

render_html(
    f"""
    <section class="comparison-card" id="comparison">
        <div class="comparison-left">
            <div class="section-title-row">
                <div class="small-icon">⚖</div>
                <h2>Dataset Characteristics Comparison</h2>
            </div>

            <table class="dataset-table">
                <thead>
                    <tr>
                        <th>Characteristic</th>
                        <th>AAD (Balanced)</th>
                        <th>SO762 (Imbalanced)</th>
                        <th>Notes</th>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <td>Domain</td>
                        <td>Spontaneous Speech</td>
                        <td>Read Speech</td>
                        <td>AAD is conversational, SO762 is sentence-based read speech.</td>
                    </tr>

                    <tr>
                        <td>Fluency Labels</td>
                        <td>3 Classes<br>Low, Intermediate, High</td>
                        <td>4 Score Groups<br>0–3, 4–5, 6–7, 8–10</td>
                        <td>SO762 uses score-based fluency grouping.</td>
                    </tr>

                    <tr>
                        <td>Class Distribution</td>
                        <td>Roughly Balanced</td>
                        <td>Imbalanced</td>
                        <td>SO762 has a dominant 8–10 score group.</td>
                    </tr>

                    <tr>
                        <td>Evaluation Protocol</td>
                        <td>5-Fold Cross-Validation</td>
                        <td>Train–Test Split</td>
                        <td>AAD uses CV, SO762 uses a predefined split.</td>
                    </tr>

                    <tr>
                        <td>Primary Use</td>
                        <td>Model Training & Evaluation</td>
                        <td>Generalization & Robustness Test</td>
                        <td>SO762 tests model behavior under imbalance.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="comparison-right">
            <div class="section-title-row">
                <h2>Class Distribution Visualization</h2>
            </div>

            <div class="donut-grid">
                <div class="donut-panel">
                    <h3>AAD (Balanced)</h3>

                    <div class="donut aad-donut">
                        <span></span>
                    </div>

                    <div class="legend-list">
                        <div><i class="legend-green"></i> Low ({aad_low})</div>
                        <div><i class="legend-yellow"></i> Intermediate ({aad_intermediate})</div>
                        <div><i class="legend-red"></i> High ({aad_high})</div>
                    </div>
                </div>

                <div class="donut-panel">
                    <h3>SO762 (Imbalanced)</h3>

                    <div class="donut so-donut">
                        <span></span>
                    </div>

                    <div class="legend-list">
                        <div><i class="legend-green"></i> 0 – 3 ({so_03})</div>
                        <div><i class="legend-yellow"></i> 4 – 5 ({so_45})</div>
                        <div><i class="legend-orange"></i> 6 – 7 ({so_67})</div>
                        <div><i class="legend-red"></i> 8 – 10 ({so_810})</div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
)


# =========================
# SOURCE / CITATION
# =========================

render_html(
    f"""
    <section class="source-card">
        <div class="source-left">
            <div class="source-icon">盾</div>

            <div>
                <h2>Data Usage and Citation</h2>
                <p>
                    Both datasets are publicly available for research purposes.
                    Please cite the original sources when using these datasets
                    in your research.
                </p>
            </div>
        </div>

        <div class="source-actions">
            <a class="source-button blue-source" href="{AAD_SOURCE}" target="_blank">
                ↗ View AAD Source
            </a>

            <a class="source-button green-source" href="{SO762_SOURCE}" target="_blank">
                ↗ View SO762 Source
            </a>
        </div>
    </section>
    """
)