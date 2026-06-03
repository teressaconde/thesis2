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
# AAD PER-FOLD RESULTS
# =========================

baseline_folds = [
    ("Fold 1", 0.8105, 0.8132, 0.8127, 0.12),
    ("Fold 2", 0.8386, 0.8401, 0.8398, 0.12),
    ("Fold 3", 0.7895, 0.7919, 0.7909, 0.12),
    ("Fold 4", 0.8175, 0.8187, 0.8180, 0.12),
    ("Fold 5", 0.8486, 0.8497, 0.8489, 0.12),
]

enhanced_folds = [
    ("Fold 1", 0.8491, 0.8512, 0.8509, 2.74),
    ("Fold 2", 0.8491, 0.8497, 0.8492, 4.74),
    ("Fold 3", 0.8526, 0.8549, 0.8530, 2.53),
    ("Fold 4", 0.8456, 0.8473, 0.8459, 2.51),
    ("Fold 5", 0.8732, 0.8739, 0.8724, 2.45),
]


# =========================
# TABLE 8 SUMMARY RESULTS
# =========================

aad_summary = [
    {
        "metric": "Accuracy",
        "baseline": 82.09,
        "enhanced": 85.39,
        "change": "+3.30%",
        "status": "good",
    },
    {
        "metric": "Precision (W)",
        "baseline": 82.48,
        "enhanced": 85.58,
        "change": "+3.10%",
        "status": "good",
    },
    {
        "metric": "Recall (W)",
        "baseline": 82.09,
        "enhanced": 85.39,
        "change": "+3.30%",
        "status": "good",
    },
    {
        "metric": "F1-Score (Weighted)",
        "baseline": 82.21,
        "enhanced": 85.43,
        "change": "+3.22%",
        "status": "good",
    },
    {
        "metric": "F1-Score (Macro)",
        "baseline": 82.27,
        "enhanced": 85.54,
        "change": "+3.27%",
        "status": "good",
    },
    {
        "metric": "Std (Accuracy)",
        "baseline": 0.0209,
        "enhanced": 0.0099,
        "change": "-0.0110",
        "status": "good",
        "unit": "std",
    },
    {
        "metric": "Train Time",
        "baseline": 0.12,
        "enhanced": 3.00,
        "change": "+2.88s",
        "status": "warning",
        "unit": "s",
    },
]

so762_summary = [
    {
        "metric": "Accuracy",
        "baseline": "70.52%",
        "enhanced": "72.28%",
        "change": "+1.76%",
        "status": "good",
    },
    {
        "metric": "Precision (W)",
        "baseline": "67.43%",
        "enhanced": "67.86%",
        "change": "+0.43%",
        "status": "good",
    },
    {
        "metric": "Recall (W)",
        "baseline": "70.52%",
        "enhanced": "72.28%",
        "change": "+1.76%",
        "status": "good",
    },
    {
        "metric": "F1-Score (Weighted)",
        "baseline": "68.52%",
        "enhanced": "67.06%",
        "change": "-1.46%",
        "status": "warning",
    },
    {
        "metric": "F1-Score (Macro)",
        "baseline": "43.00%",
        "enhanced": "38.00%",
        "change": "-5.00%",
        "status": "warning",
    },
    {
        "metric": "Std (Accuracy)",
        "baseline": "—",
        "enhanced": "—",
        "change": "—",
        "status": "neutral",
    },
    {
        "metric": "Train Time",
        "baseline": "1.01s",
        "enhanced": "2.61s",
        "change": "+1.60s",
        "status": "warning",
    },
]

aad_std = [
    ("Accuracy", "0.0209", "0.0099"),
    ("F1-Score (Macro)", "0.0205", "0.0096"),
    ("F1-Score (Weighted)", "0.0205", "0.0094"),
    ("Train Time", "0.00s", "0.88s"),
]


# =========================
# HTML BUILDERS
# =========================

def summary_card(metric):
    unit = metric.get("unit", "%")

    if unit == "s":
        baseline_value = f"{metric['baseline']:.2f}s"
        enhanced_value = f"{metric['enhanced']:.2f}s"
    elif unit == "std":
        baseline_value = f"±{metric['baseline']:.4f}"
        enhanced_value = f"±{metric['enhanced']:.4f}"
    else:
        baseline_value = f"{metric['baseline']:.2f}%"
        enhanced_value = f"{metric['enhanced']:.2f}%"

    return f"""
    <div class="summary-card">
        <div class="summary-title">{metric["metric"]}</div>

        <div class="summary-values">
            <div>
                <strong class="blue-value">{baseline_value}</strong>
                <span>Baseline SVM</span>
            </div>

            <div class="divider"></div>

            <div>
                <strong class="green-value">{enhanced_value}</strong>
                <span>Enhanced SVM</span>
            </div>
        </div>

        <div class="summary-change {metric["status"]}">
            <span>Change:</span>
            <strong>{metric["change"]}</strong>
        </div>
    </div>
    """


def so762_card(metric):
    return f"""
    <div class="summary-card so-card">
        <div class="summary-title">{metric["metric"]}</div>

        <div class="summary-values">
            <div>
                <strong class="blue-value">{metric["baseline"]}</strong>
                <span>Baseline SVM</span>
            </div>

            <div class="divider"></div>

            <div>
                <strong class="green-value">{metric["enhanced"]}</strong>
                <span>Enhanced SVM</span>
            </div>
        </div>

        <div class="summary-change {metric["status"]}">
            <span>Change:</span>
            <strong>{metric["change"]}</strong>
        </div>
    </div>
    """


def fold_table(title, rows, theme):
    body = ""

    for fold, accuracy, f1_macro, f1_weighted, train_time in rows:
        body += f"""
        <tr>
            <td>{fold}</td>
            <td>{accuracy:.4f}</td>
            <td>{f1_macro:.4f}</td>
            <td>{f1_weighted:.4f}</td>
            <td>{train_time:.2f}s</td>
        </tr>
        """

    return f"""
    <div class="fold-card {theme}">
        <h3>{title}</h3>

        <table class="result-table">
            <thead>
                <tr>
                    <th>Fold</th>
                    <th>Accuracy</th>
                    <th>F1 Macro</th>
                    <th>F1 Weighted</th>
                    <th>Train Time</th>
                </tr>
            </thead>

            <tbody>
                {body}
            </tbody>
        </table>
    </div>
    """


def std_table(rows):
    body = ""

    for metric, baseline, enhanced in rows:
        body += f"""
        <tr>
            <td>{metric}</td>
            <td>{baseline}</td>
            <td>{enhanced}</td>
        </tr>
        """

    return f"""
    <table class="result-table">
        <thead>
            <tr>
                <th>Metric</th>
                <th>Baseline SVM</th>
                <th>Enhanced SVM</th>
            </tr>
        </thead>

        <tbody>
            {body}
        </tbody>
    </table>
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
                        Comparison between Baseline SVM and Enhanced SVM using
                        SMO + Hybrid RFF–Nyström on AAD and SpeechOcean762.
                    </p>
                </div>
            </div>

            <div class="mc-header-meta">
                <div class="meta-item">
                    <div class="meta-icon">▣</div>
                    <div>
                        <span>Datasets</span>
                        <strong>AAD & SO762</strong>
                    </div>
                </div>

                <div class="meta-item">
                    <div class="meta-icon">◎</div>
                    <div>
                        <span>Evaluation</span>
                        <strong>AAD: 5-Fold CV | SO762: Train–Test Split</strong>
                    </div>
                </div>
            </div>
        </div>

        <div class="mc-tabs">
            <a class="active" href="#overview">Overview</a>
            <a href="#aad">AAD Results</a>
            <a href="#so762">SO762 Results</a>
        </div>
    </section>
    """
)


# =========================
# AAD DATASET RESULTS
# =========================

render_html(
    f"""
    <section class="mc-card" id="overview">
        <div class="section-heading">
            <div class="section-icon">⌘</div>
            <div>
                <h2>AAD Dataset Results</h2>
                <p>Mean results from 5-fold stratified cross-validation.</p>
            </div>
        </div>

        <div class="summary-grid">
            {''.join(summary_card(item) for item in aad_summary)}
        </div>

        <div class="insight-box success-insight">
            <h3>AAD Summary Insights</h3>
            <ul>
                <li>Enhanced SVM improved accuracy from <strong>82.09%</strong> to <strong>85.39%</strong>.</li>
                <li>Precision increased from <strong>82.48%</strong> to <strong>85.58%</strong>.</li>
                <li>Recall increased from <strong>82.09%</strong> to <strong>85.39%</strong>.</li>
                <li>Weighted F1 increased from <strong>82.21%</strong> to <strong>85.43%</strong>.</li>
                <li>Macro F1 increased from <strong>82.27%</strong> to <strong>85.54%</strong>.</li>
                <li>Accuracy standard deviation decreased from <strong>±0.0209</strong> to <strong>±0.0099</strong>, showing more stable results.</li>
                <li>The enhanced model required more training time because of RFF–Nyström feature construction and SMO optimization.</li>
            </ul>
        </div>
    </section>
    """
)


# =========================
# SO762 CARD RESULTS
# =========================

render_html(
    f"""
    <section class="mc-card" id="so762">
        <div class="section-heading">
            <div class="section-icon">▥</div>
            <div>
                <h2>SO762 Dataset Results</h2>
                <p>Train-test split results for the imbalanced SpeechOcean762 dataset.</p>
            </div>
        </div>

        <div class="summary-grid so-summary-grid">
            {''.join(so762_card(item) for item in so762_summary)}
        </div>

        <div class="insight-box warning-insight">
            <h3>SO762 Insights</h3>
            <ul>
                <li>Enhanced SVM improved accuracy from <strong>70.52%</strong> to <strong>72.28%</strong>.</li>
                <li>Precision increased slightly from <strong>67.43%</strong> to <strong>67.86%</strong>.</li>
                <li>Recall increased from <strong>70.52%</strong> to <strong>72.28%</strong>.</li>
                <li>Weighted F1 decreased from <strong>68.52%</strong> to <strong>67.06%</strong>.</li>
                <li>Macro F1 decreased from <strong>43.00%</strong> to <strong>38.00%</strong>, showing that minority classes remain difficult.</li>
                <li>SO762 standard deviation is not available because the result uses a train-test split instead of 5-fold cross-validation.</li>
                <li>The SO762 dataset is strongly imbalanced, which affects F1-score performance.</li>
            </ul>
        </div>
    </section>
    """
)


# =========================
# AAD PER-FOLD TABLES
# =========================

render_html(
    f"""
    <section class="mc-card" id="aad">
        <div class="section-heading">
            <div class="section-icon">▦</div>
            <div>
                <h2>Per-Fold Breakdown (AAD Dataset)</h2>
                <p>Exact fold-by-fold results from baseline and enhanced SVM training.</p>
            </div>
        </div>

        <div class="fold-grid">
            {fold_table("Baseline SVM", baseline_folds, "blue-theme")}
            {fold_table("Enhanced SVM", enhanced_folds, "green-theme")}
        </div>

        <div class="insight-box success-insight">
            <h3>Per-Fold Insights</h3>
            <ul>
                <li>Enhanced SVM is consistently higher than Baseline SVM across all five folds.</li>
                <li>The strongest enhanced result occurs in <strong>Fold 5</strong> with <strong>0.8732 accuracy</strong>.</li>
                <li>Baseline SVM shows more variation, with its lowest accuracy at <strong>0.7895</strong> in Fold 3.</li>
                <li>Enhanced SVM has more stable fold performance, supported by its lower standard deviation.</li>
            </ul>
        </div>
    </section>
    """
)


# =========================
# STANDARD DEVIATION
# =========================

render_html(
    f"""
    <section class="mc-card">
        <div class="section-heading">
            <div class="section-icon">σ</div>
            <div>
                <h2>Standard Deviation Summary</h2>
                <p>Lower standard deviation indicates more stable cross-validation performance.</p>
            </div>
        </div>

        {std_table(aad_std)}

        <div class="success-note">
            ✓ Enhanced SVM has lower standard deviation for Accuracy, F1 Macro, and F1 Weighted.
        </div>
    </section>
    """
)


# =========================
# KEY INSIGHTS
# =========================

render_html(
    """
    <section class="mc-card">
        <div class="section-heading">
            <div class="section-icon">💡</div>
            <div>
                <h2>Key Insights</h2>
                <p>Summary interpretation based on the final model comparison results.</p>
            </div>
        </div>

        <ul class="insight-list">
            <li>Enhanced SVM improves AAD accuracy, precision, recall, weighted F1, and macro F1.</li>
            <li>Enhanced SVM has lower AAD accuracy standard deviation, showing more stable cross-validation performance.</li>
            <li>SO762 accuracy, precision, and recall improve, but macro and weighted F1 decrease due to strong class imbalance.</li>
            <li>Training time increases because the enhanced approach uses hybrid RFF–Nyström features and SMO optimization.</li>
        </ul>
    </section>
    """
)