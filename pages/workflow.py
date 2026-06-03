import streamlit as st
from pathlib import Path
from textwrap import dedent

st.set_page_config(
    page_title="Workflow | Oral Fluency Classification",
    page_icon="🔀",
    layout="wide",
    initial_sidebar_state="expanded",
)

from components.sidebar import load_sidebar_css, render_sidebar

load_sidebar_css()
render_sidebar(active_page="Workflow")

BASE_DIR = Path(__file__).resolve().parent.parent
WORKFLOW_CSS = BASE_DIR / "assets" / "workflow.css"


def load_css(path: Path):
    css = path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_html(html: str):
    html = dedent(html).strip()
    html = "\n".join(line.lstrip() for line in html.splitlines())
    st.markdown(html, unsafe_allow_html=True)


load_css(WORKFLOW_CSS)


render_html(
    """
    <main class="workflow-page">
        <section class="workflow-hero-card">
            <div class="hero-left">
                <div class="hero-icon">
                    <svg viewBox="0 0 24 24" fill="none">
                        <rect x="9" y="3" width="6" height="5" rx="1.4" stroke="currentColor" stroke-width="2"/>
                        <rect x="4" y="16" width="6" height="5" rx="1.4" stroke="currentColor" stroke-width="2"/>
                        <rect x="14" y="16" width="6" height="5" rx="1.4" stroke="currentColor" stroke-width="2"/>
                        <path d="M12 8V12M12 12H7M12 12H17M7 12V16M17 12V16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                </div>

                <div>
                    <h1>System Workflow</h1>
                    <p>
                        Step-by-step process of the Oral Fluency Classification system
                        from audio input to final fluency assessment.
                    </p>
                </div>
            </div>

            <div class="hero-summary">
                <div class="summary-item">
                    <div class="summary-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <ellipse cx="12" cy="5" rx="7" ry="3" stroke="currentColor" stroke-width="2"/>
                            <path d="M5 5V12C5 13.7 8.1 15 12 15C15.9 15 19 13.7 19 12V5" stroke="currentColor" stroke-width="2"/>
                            <path d="M5 12V19C5 20.7 8.1 22 12 22C15.9 22 19 20.7 19 19V12" stroke="currentColor" stroke-width="2"/>
                        </svg>
                    </div>
                    <span>Datasets</span>
                    <strong>AAD &amp; SO762</strong>
                </div>

                <div class="summary-item">
                    <div class="summary-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M4 13V11" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
                            <path d="M8 16V8" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
                            <path d="M12 19V5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
                            <path d="M16 16V8" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
                            <path d="M20 13V11" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
                        </svg>
                    </div>
                    <span>Features</span>
                    <strong>66-D MFCC</strong>
                </div>

                <div class="summary-item">
                    <div class="summary-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M9.5 4.5C7.8 3.2 5.2 4.3 5.3 6.8C3.2 6.7 2.3 9.2 3.8 10.4C2.2 11.9 3.1 14.7 5.4 14.5C5.8 17 9.5 17.4 9.5 14.8V4.5Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M14.5 4.5C16.2 3.2 18.8 4.3 18.7 6.8C20.8 6.7 21.7 9.2 20.2 10.4C21.8 11.9 20.9 14.7 18.6 14.5C18.2 17 14.5 17.4 14.5 14.8V4.5Z" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                            <path d="M3.5 11H6.5L7.5 8.8L9 13L10 11H14L15 13L16.5 8.8L17.5 11H20.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
                        </svg>
                    </div>
                    <span>Models</span>
                    <strong>Baseline SVM &amp;<br>Enhanced SVM</strong>
                </div>

                <div class="summary-item">
                    <div class="summary-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="2"/>
                            <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                            <path d="M17.5 6.5L21 3M18 3H21V6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <span>Goal</span>
                    <strong>Fluency<br>Classification</strong>
                </div>
            </div>
        </section>

        <section class="workflow-card general-card">
            <h2>General Workflow</h2>

            <div class="general-flow">
                <div class="flow-step step-blue">
                    <div class="step-number">1</div>
                    <div class="step-box">
                        <div class="step-icon">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M12 16V6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                                <path d="M8 10L12 6L16 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M7 17H6.5C4.6 17 3 15.4 3 13.5C3 11.8 4.2 10.4 5.8 10.1C6.4 7.7 8.6 6 11.2 6C13.7 6 15.8 7.6 16.5 9.8H17C19.2 9.8 21 11.6 21 13.8C21 16 19.2 17.8 17 17.8H16.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <span>Upload Audio</span>
                    </div>
                </div>

                <div class="flow-arrow">→</div>

                <div class="flow-step step-purple">
                    <div class="step-number">2</div>
                    <div class="step-box">
                        <div class="step-icon">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M12 3L21 8L12 13L3 8L12 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
                                <path d="M5 12L12 16L19 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M5 16L12 20L19 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <span>Select Dataset /<br>Model</span>
                    </div>
                </div>

                <div class="flow-arrow">→</div>

                <div class="flow-step step-cyan">
                    <div class="step-number">3</div>
                    <div class="step-box">
                        <div class="step-icon">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M4 13V11M8 16V8M12 19V5M16 16V8M20 13V11" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <span>Preprocess<br>Audio</span>
                    </div>
                </div>

                <div class="flow-arrow">→</div>

                <div class="flow-step step-green">
                    <div class="step-number">4</div>
                    <div class="step-box">
                        <div class="step-icon">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M5 20V13M10 20V8M15 20V11M20 20V5" stroke="currentColor" stroke-width="2.3" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <span>Extract MFCC<br>Features</span>
                    </div>
                </div>

                <div class="flow-arrow">→</div>

                <div class="flow-step step-orange">
                    <div class="step-number">5</div>
                    <div class="step-box">
                        <div class="step-icon">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M12 15.5A3.5 3.5 0 1 0 12 8.5A3.5 3.5 0 0 0 12 15.5Z" stroke="currentColor" stroke-width="2"/>
                                <path d="M19.4 15A8 8 0 0 0 19.5 9L21 7.8L19 4.3L17.2 5A8 8 0 0 0 12 3L11.7 1H7.7L7.4 3A8 8 0 0 0 4.8 5L3 4.3L1 7.8L2.5 9A8 8 0 0 0 2.6 15L1 16.2L3 19.7L4.8 19A8 8 0 0 0 10 21L10.3 23H14.3L14.6 21A8 8 0 0 0 19.2 19L21 19.7L23 16.2L21.4 15Z" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/>
                            </svg>
                        </div>
                        <span>Run<br>Classification</span>
                    </div>
                </div>

                <div class="flow-arrow">→</div>

                <div class="flow-step step-red">
                    <div class="step-number">6</div>
                    <div class="step-box">
                        <div class="step-icon">
                            <svg viewBox="0 0 24 24" fill="none">
                                <path d="M12 3V12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                                <path d="M21 12A9 9 0 1 1 12 3" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <span>View<br>Results</span>
                    </div>
                </div>
            </div>
        </section>

        <section class="workflow-card pipeline-card">
            <div class="section-title-center">
                <h2>Enhanced SVM Technical Pipeline</h2>
                <p>Proposed model pipeline using hybrid RFF–Nyström kernel approximation and SMO optimization.</p>
            </div>

            <div class="pipeline-flow">
                <div class="pipeline-node mfcc-node">
                    <div class="node-icon blue-node-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M5 20V14M10 20V10M15 20V6M20 20V12" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/>
                        </svg>
                    </div>
                    <strong>MFCC Features</strong>
                    <span>(66-D)</span>
                </div>

                <div class="split-connector">
                    <div class="split-line top"></div>
                    <div class="split-line bottom"></div>
                </div>

                <div class="branch-stack">
                    <div class="branch-card rff-branch">
                        <div class="branch-title">
                            <span class="dot-grid">▦</span>
                            <strong>RFF Path</strong>
                        </div>
                        <div class="branch-inner">Random Fourier<br>Features (RFF)</div>
                    </div>

                    <div class="branch-card nys-branch">
                        <div class="branch-title green-title">
                            <span class="dot-grid">✣</span>
                            <strong>Nyström Path</strong>
                        </div>
                        <div class="branch-inner">Nyström<br>Approximation</div>
                    </div>
                </div>

                <div class="merge-connector"></div>

                <div class="pipeline-node hybrid-node">
                    <div class="node-icon purple-node-icon">◇</div>
                    <strong>Hybrid Feature Space</strong>
                    <span>Construction</span>
                </div>

                <div class="pipeline-arrow">→</div>

                <div class="pipeline-node norm-node">
                    <div class="node-icon amber-node-icon">Σ</div>
                    <strong>Second</strong>
                    <span>Normalization</span>
                </div>

                <div class="pipeline-arrow">→</div>

                <div class="pipeline-node smo-node">
                    <div class="node-icon orange-node-icon">↗</div>
                    <strong>SMO Optimization</strong>
                
                </div>

                <div class="pipeline-arrow">→</div>

                <div class="pipeline-node prediction-node">
                    <div class="node-icon red-node-icon">◎</div>
                    <strong>Fluency</strong>
                    <span>Prediction</span>
                </div>
            </div>
        </section>

        <section class="lower-grid">
            <div class="workflow-card dataset-card">
                <h2>Dataset-Specific Evaluation Path</h2>

                <div class="dataset-mini-grid">
                    <div class="dataset-mini blue-dataset">
                        <div class="dataset-icon-mini">
                            <svg viewBox="0 0 24 24" fill="none">
                                <circle cx="8" cy="9" r="3" stroke="currentColor" stroke-width="2"/>
                                <circle cx="16" cy="9" r="3" stroke="currentColor" stroke-width="2"/>
                                <path d="M4 20C4.6 16.8 6.8 15 10 15H14C17.2 15 19.4 16.8 20 20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <h3>AAD Dataset</h3>
                        <ul>
                            <li>Balanced dataset</li>
                            <li>3 classes (Low, Intermediate, High)</li>
                            <li>5-Fold Stratified Cross-Validation</li>
                        </ul>
                    </div>

                    <div class="dataset-mini green-dataset">
                        <div class="dataset-icon-mini green-icon-mini">
                            <svg viewBox="0 0 24 24" fill="none">
                                <circle cx="8" cy="9" r="3" stroke="currentColor" stroke-width="2"/>
                                <circle cx="16" cy="9" r="3" stroke="currentColor" stroke-width="2"/>
                                <path d="M4 20C4.6 16.8 6.8 15 10 15H14C17.2 15 19.4 16.8 20 20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            </svg>
                        </div>
                        <h3>SO762 Dataset</h3>
                        <ul>
                            <li>Imbalanced dataset</li>
                            <li>4 classes (Class 0, Class 1, Class 2, Class 3)</li>
                            <li>Predefined Train–Test Split</li>
                        </ul>
                    </div>
                </div>
            </div>

            <div class="workflow-card comparison-card">
                <h2>Workflow Comparison</h2>

                <table class="workflow-table">
                    <thead>
                        <tr>
                            <th>Aspect</th>
                            <th>Baseline SVM</th>
                            <th>Enhanced SVM</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Kernel Handling</td>
                            <td>Exact RBF Kernel</td>
                            <td>Hybrid RFF–Nyström Approximation</td>
                        </tr>
                        <tr>
                            <td>Optimization</td>
                            <td>Standard SVC / libsvm</td>
                            <td>SMO Optimization with LinearSVC Solver</td>
                        </tr>
                        <tr>
                            <td>Feature Space</td>
                            <td>66-D MFCC</td>
                            <td>Hybrid feature space</td>
                        </tr>
                        <tr>
                            <td>Complexity</td>
                            <td>More expensive on larger data</td>
                            <td>More scalable</td>
                        </tr>
                        <tr>
                            <td>Strength</td>
                            <td>Simple baseline</td>
                            <td>Better stability and generalization</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="workflow-card outputs-card">
            <h2>System Outputs</h2>

            <div class="output-grid">
                <div class="output-item blue-output">
                    <div class="output-icon">
                        <svg viewBox="0 0 24 24" fill="none">
                            <path d="M4 20H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                            <path d="M6 17V12M11 17V9M16 17V5" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>
                            <path d="M6 10L11 7L16 3L20 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                    </div>
                    <div>
                        <h3>Predicted Fluency Level</h3>
                        <p>Final fluency class or score group prediction.</p>
                    </div>
                </div>

                <div class="output-item green-output">
                    <div class="output-icon green-output-icon">✓</div>
                    <div>
                        <h3>Confidence Score</h3>
                        <p>Overall confidence of the prediction.</p>
                    </div>
                </div>

                <div class="output-item purple-output">
                    <div class="output-icon purple-output-icon">◔</div>
                    <div>
                        <h3>Class Probabilities</h3>
                        <p>Probability distribution across all possible classes.</p>
                    </div>
                </div>

                <div class="output-item orange-output">
                    <div class="output-icon orange-output-icon">✪</div>
                    <div>
                        <h3>Performance Metrics</h3>
                        <p>Comprehensive evaluation of model performance.</p>
                    </div>
                </div>
            </div>

            <div class="metric-strip">
                <div><span>◎</span>Accuracy</div>
                <div><span>⌖</span>Precision</div>
                <div><span>↻</span>Recall</div>
                <div><span>∿</span>F1-Score</div>
                <div class="pdf-pill"><span>PDF</span>Downloadable<br>PDF Report</div>
            </div>
        </section>
    </main>
    """
)