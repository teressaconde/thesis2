import streamlit as st

st.set_page_config(
    page_title="Dashboard | Oral Fluency Classification",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


from components.sidebar import load_sidebar_css, render_sidebar


load_sidebar_css()
render_sidebar(active_page="Dashboard")


# =========================
# DASHBOARD CONTENT
# =========================

st.title("Oral Fluency Classification Dashboard")

st.write(
    "Manage speech audio uploads, run fluency assessment, compare Baseline SVM "
    "and Enhanced SVM, and review dataset and model performance records."
)

st.divider()


# =========================
# SUMMARY CARDS
# =========================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Uploaded Audio", "0")

with col2:
    st.metric("Active Model", "SVM")

with col3:
    st.metric("Datasets", "2")

with col4:
    st.metric("System Status", "Ready")

st.divider()


# =========================
# QUICK ACTIONS
# =========================

st.subheader("Quick Actions")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    st.markdown("### Upload Audio")
    st.write("Upload WAV or MP3 speech audio for preprocessing and feature extraction.")

    if st.button("Go to Upload Audio", use_container_width=True):
        st.switch_page("pages/upload_audio.py")

with action_col2:
    st.markdown("### View Results")
    st.write("Open the analysis dashboard to view predictions, probabilities, and classification.")

    if st.button("Go to Results", use_container_width=True):
        st.switch_page("pages/results.py")

with action_col3:
    st.markdown("### Compare Models")
    st.write("Review Baseline SVM and Enhanced SVM performance metrics.")

    if st.button("Compare Models", use_container_width=True):
        st.switch_page("pages/model_comparison.py")

st.divider()


# =========================
# SYSTEM OVERVIEW
# =========================

st.subheader("System Overview")

overview_col1, overview_col2 = st.columns(2)

with overview_col1:
    st.info(
        "This system supports oral fluency classification using MFCC feature extraction, "
        "Baseline SVM, and Enhanced SVM with SMO and Hybrid RFF–Nyström."
    )

with overview_col2:
    st.success("System is ready. Use the Upload Audio page to begin speech analysis.")