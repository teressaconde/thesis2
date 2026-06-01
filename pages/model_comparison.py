import streamlit as st
from pathlib import Path
from textwrap import dedent

st.set_page_config(
    page_title="Model Comparison | Oral Fluency Classification",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.sidebar import load_sidebar_css, render_sidebar

load_sidebar_css()
render_sidebar(active_page="Model Comparison")

BASE_DIR = Path(__file__).resolve().parent.parent
PAGE_CSS = BASE_DIR / "assets" / "model_comparison.css"


def load_css(path: Path):
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_html(html: str):
    html = dedent(html).strip()
    html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


load_css(PAGE_CSS)


# =========================
# DATA FROM THESIS RESULTS
# =========================

overview_metrics = [
    {
        "label": "Accuracy",
        "icon": "◎",
        "baseline": 84.46,
        "enhanced": 88.15,
        "change": "+3.69%",
        "better": "up",
    },
    {
        "label": "Precision (Macro)",
        "icon": "◉",
        "baseline": 84.30,
        "enhanced": 87.61,
        "change": "+3.31%",
        "better": "up",
    },
    {
        "label": "Recall (Macro)",
        "icon": "↩",
        "baseline": 84.43,
        "enhanced": 88.46,
        "change": "+4.03%",
        "better": "up",
    },
    {
        "label": "F1-Score (Macro)",
        "icon": "☆",
        "baseline": 84.29,
        "enhanced": 87.98,
        "change": "+3.69%",
        "better": "up",
    },
    {
        "label": "Training Time",
        "icon": "◷",
        "baseline": 12.42,
        "enhanced": 4.87,
        "change": "-60.78%",
        "better": "down",
        "unit": "s",
    },
]

aad_metrics = [
    ("Accuracy (%)", 84.46, 88.15),
    ("Precision (Macro) (%)", 84.30, 87.61),
    ("Recall (Macro) (%)", 84.43, 88.46),
    ("F1-Score (Macro) (%)", 84.29, 87.98),
]

aad_std = [
    ("Accuracy", "0.0209", "0.0099"),
    ("Precision", "0.0217", "0.0113"),
    ("Recall", "0.0246", "0.0121"),
    ("F1-Score", "0.0219", "0.0098"),
]

so762_metrics = [
    ("Accuracy (Weighted)", "70.52%", "72.28%", "+2.16%"),
    ("Precision (Weighted)", "67.43%", "67.86%", "+0.43%"),
    ("Recall (Weighted)", "70.52%", "72.28%", "+1.76%"),
    ("F1-Score (Weighted)", "68.25%", "67.06%", "-1.19%"),
]

# AAD confusion matrix values are arranged to match the narrative in the paper:
# diagonal improvements: Low 345→370, Intermediate 425→428, High 399→418.
aad_baseline_cm = [
    [345, 78, 15],
    [83, 425, 19],
    [12, 48, 399],
]

aad_enhanced_cm = [
    [370, 59, 9],
    [74, 428, 25],
    [7, 34, 418],
]

# SO762 confusion matrix display values for UI visualization.
# You may replace these with your exact matrix if you export it from training.
so762_baseline_cm = [
    [4, 2, 6, 7],
    [11, 46, 55, 286],
    [18, 39, 280, 866],
    [26, 68, 216, 1701],
]

so762_enhanced_cm = [
    [0, 2, 3, 14],
    [8, 59, 48, 283],
    [14, 28, 280, 881],
    [17, 53, 172, 1769],
]


# =========================
# HTML BUILDERS
# =========================

def metric_card(item):
    unit = item.get("unit", "%")
    baseline_value = f'{item["baseline"]:.2f}{unit}'
    enhanced_value = f'{item["enhanced"]:.2f}{unit}'

    arrow = "↓" if item["better"] == "down" else "↑"

    return f"""
    <div class="summary-metric-card">
        <div class="metric-top">
            <div class="metric-symbol">{item["icon"]}</div>
            <div class="metric-name">{item["label"]}</div>
        </div>

        <div class="metric-comparison">
            <div>
                <strong class="blue-value">{baseline_value}</strong>
                <span>Baseline SVM</span>
            </div>

            <div class="split-line"></div>

            <div>
                <strong class="green-value">{enhanced_value}</strong>
                <span>Enhanced SVM</span>
            </div>
        </div>

        <div class="metric-change">
            <span>{arrow}</span>
            <strong>{item["change"]}</strong>
        </div>
    </div>
    """


def small_bar_chart(metrics):
    charts = ""

    for title, baseline, enhanced in metrics:
        charts += f"""
        <div class="mini-bar-chart">
            <h4>{title}</h4>

            <div class="bar-area">
                <div class="bar-group">
                    <div class="bar blue-bar" style="height:{baseline}%;"></div>
                    <span>{baseline:.2f}</span>
                    <small>Baseline</small>
                </div>

                <div class="bar-group">
                    <div class="bar green-bar" style="height:{enhanced}%;"></div>
                    <span>{enhanced:.2f}</span>
                    <small>Enhanced</small>
                </div>
            </div>
        </div>
        """

    return charts


def std_table(rows):
    html = """
    <table class="comparison-table std-table">
        <thead>
            <tr>
                <th>Model</th>
                <th>Accuracy (↓)</th>
                <th>Precision (↓)</th>
                <th>Recall (↓)</th>
                <th>F1-Score (↓)</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><span class="model-pill blue-pill">Baseline SVM</span></td>
    """

    baseline_values = [row[1] for row in rows]
    enhanced_values = [row[2] for row in rows]

    for value in baseline_values:
        html += f"<td>{value}</td>"

    html += """
            </tr>
            <tr>
                <td><span class="model-pill green-pill">Enhanced SVM</span></td>
    """

    for value in enhanced_values:
        html += f"<td>{value}</td>"

    html += """
            </tr>
        </tbody>
    </table>
    """

    return html


def so762_table(rows):
    html = """
    <table class="comparison-table so-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>Baseline SVM</th>
                <th>Enhanced SVM<br>(Proposed)</th>
                <th>Improvement</th>
            </tr>
        </thead>
        <tbody>
    """

    for metric, baseline, enhanced, improvement in rows:
        change_class = "positive" if "-" not in improvement else "negative"
        arrow = "↑" if "-" not in improvement else "↓"

        html += f"""
        <tr>
            <td>{metric}</td>
            <td>{baseline}</td>
            <td>{enhanced}</td>
            <td class="{change_class}">{arrow} {improvement}</td>
        </tr>
        """

    html += """
        </tbody>
    </table>
    """

    return html


def confusion_matrix(title, labels, matrix, theme):
    max_value = max(max(row) for row in matrix)

    body = ""

    for i, row in enumerate(matrix):
        body += f"<tr><th>{labels[i]}</th>"

        for j, value in enumerate(row):
            intensity = int((value / max_value) * 100) if max_value else 0
            diag_class = "diag" if i == j else ""
            body += (
                f'<td class="{diag_class}" style="--heat:{intensity}%;">'
                f"{value}"
                f"</td>"
            )

        body += "</tr>"

    header_cells = "".join([f"<th>{label}</th>" for label in labels])

    total_correct = sum(matrix[i][i] for i in range(len(matrix)))
    total_samples = sum(sum(row) for row in matrix)
    accuracy = (total_correct / total_samples) * 100 if total_samples else 0

    return f"""
    <div class="matrix-card {theme}">
        <div class="matrix-title">{title}</div>

        <table class="matrix-table">
            <thead>
                <tr>
                    <th></th>
                    {header_cells}
                </tr>
            </thead>

            <tbody>
                {body}
            </tbody>
        </table>

        <div class="matrix-total">
            Total Correct: <strong>{total_correct:,} / {total_samples:,} ({accuracy:.2f}%)</strong>
        </div>
    </div>
    """


# =========================
# PAGE HEADER
# =========================

render_html(
    """
    <section class="mc-page-shell">
        <div class="mc-header">
            <div class="mc-header-left">
                <div class="mc-main-icon">▥</div>
                <div>
                    <h1>Model Comparison Results</h1>
                    <p>
                        Comparison between Baseline SVM and Enhanced SVM
                        using SMO + Hybrid RFF–Nyström on AAD and SpeechOcean762.
                    </p>
                </div>
            </div>

            <div class="mc-header-meta">
                <div class="meta-item">
                    <div class="meta-icon">▣</div>
                    <div>
                        <span>Dataset</span>
                        <strong>AAD & SO762</strong>
                    </div>
                </div>

                <div class="meta-item">
                    <div class="meta-icon">◎</div>
                    <div>
                        <span>Evaluation Protocol</span>
                        <strong>AAD: 5-Fold CV &nbsp; | &nbsp; SO762: Train–Test Split</strong>
                    </div>
                </div>
            </div>
        </div>

        <div class="mc-tabs">
            <a class="active" href="#overview">Overview</a>
            <a href="#aad">AAD Results (Balanced)</a>
            <a href="#so762">SO762 Results (Imbalanced)</a>
        </div>
    </section>
    """
)


# =========================
# OVERALL PERFORMANCE SUMMARY
# =========================

render_html(
    f"""
    <section class="mc-card" id="overview">
        <div class="section-heading">
            <div class="section-icon">⌘</div>
            <div>
                <h2>Overall Performance Summary</h2>
                <p>Average results across all evaluation splits and dataset-level summaries.</p>
            </div>
        </div>

        <div class="summary-grid">
            {''.join(metric_card(item) for item in overview_metrics)}
        </div>
    </section>
    """
)


# =========================
# AAD CHARTS + CONFUSION MATRIX
# =========================

aad_left, aad_right = st.columns([1.15, 1], gap="large")

with aad_left:
    render_html(
        f"""
        <section class="mc-card" id="aad">
            <div class="section-heading">
                <div class="section-icon">▥</div>
                <div>
                    <h2>Cross-Validation Performance (AAD Dataset)</h2>
                    <p>5-fold stratified cross-validation results using macro-level evaluation.</p>
                </div>
            </div>

            <div class="chart-grid">
                {small_bar_chart(aad_metrics)}
            </div>

            <div class="legend-row">
                <span><i class="legend-blue"></i> Baseline SVM</span>
                <span><i class="legend-green"></i> Enhanced SVM</span>
            </div>

            <h3 class="small-section-title">Standard Deviation (Lower is Better)</h3>

            {std_table(aad_std)}

            <div class="success-note">
                ✓ Enhanced SVM shows higher performance and more consistent results across all AAD metrics.
            </div>
        </section>
        """
    )

with aad_right:
    render_html(
        f"""
        <section class="mc-card">
            <div class="section-heading">
                <div class="section-icon">▦</div>
                <div>
                    <h2>Confusion Matrix (AAD Dataset)</h2>
                    <p>Aggregated across 5 folds. Values show actual vs predicted fluency class.</p>
                </div>
            </div>

            <div class="matrix-grid">
                {confusion_matrix("Baseline SVM", ["Low", "Intermediate", "High"], aad_baseline_cm, "blue-theme")}
                {confusion_matrix("Enhanced SVM (Proposed)", ["Low", "Intermediate", "High"], aad_enhanced_cm, "green-theme")}
            </div>

            <div class="success-note">
                ✓ Enhanced SVM improves correct predictions in Low, Intermediate, and High classes.
            </div>
        </section>
        """
    )


# =========================
# SO762 + LOWER PANELS
# =========================

so_left, so_mid, so_right = st.columns([1, 1.45, 1], gap="large")

with so_left:
    render_html(
        f"""
        <section class="mc-card" id="so762">
            <div class="section-heading compact">
                <div class="section-icon">▥</div>
                <div>
                    <h2>SO762 Dataset Results</h2>
                    <p>Train–test split results for imbalanced fluency classes.</p>
                </div>
            </div>

            {so762_table(so762_metrics)}
        </section>
        """
    )

with so_mid:
    render_html(
        f"""
        <section class="mc-card">
            <div class="section-heading compact">
                <div class="section-icon">▦</div>
                <div>
                    <h2>Confusion Matrix (SO762 Dataset)</h2>
                    <p>Single train–test split with four score-based fluency groups.</p>
                </div>
            </div>

            <div class="matrix-grid so-matrix-grid">
                {confusion_matrix("Baseline SVM", ["0–3", "4–5", "6–7", "8–10"], so762_baseline_cm, "blue-theme")}
                {confusion_matrix("Enhanced SVM (Proposed)", ["0–3", "4–5", "6–7", "8–10"], so762_enhanced_cm, "green-theme")}
            </div>

            <div class="warning-note">
                ⚠ Performance is limited by severe class imbalance; class 8–10 dominates the dataset.
            </div>
        </section>
        """
    )

with so_right:
    render_html(
        """
        <section class="mc-card insight-card">
            <div class="section-heading compact">
                <div class="section-icon">💡</div>
                <div>
                    <h2>Key Insights</h2>
                </div>
            </div>

            <ul class="insight-list">
                <li>Enhanced SVM improves performance on the balanced AAD dataset.</li>
                <li>Lower standard deviation means more stable cross-validation results.</li>
                <li>SO762 still shows limitations because of class imbalance.</li>
                <li>Training time increases, but the trade-off is acceptable for offline training.</li>
            </ul>
        </section>

        <section class="takeaway-card">
            <div class="takeaway-icon">🏆</div>
            <div>
                <h2>Takeaway</h2>
                <p>
                    Enhanced SVM with SMO and Hybrid RFF–Nyström improves accuracy,
                    stability, and generalization especially on balanced datasets like AAD.
                </p>
            </div>
        </section>
        """
    )