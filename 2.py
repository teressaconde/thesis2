"""\
Streamlit UI — Oral Fluency Classification (Screen 2 / Results)

Run:
	streamlit run 2.py

This file focuses on the design/layout to match the provided HTML mock.
"""

from __future__ import annotations

import html
import textwrap
from dataclasses import dataclass

import streamlit as st


@dataclass(frozen=True)
class Metric:
	label: str
	percent: int


def _format_size(num_bytes: int) -> str:
	mb = num_bytes / (1024 * 1024)
	if mb >= 10:
		return f"{mb:.1f} MB"
	return f"{mb:.2f} MB"


def inject_css() -> None:
	st.markdown(
		"""
		<style>
		@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;600;700&display=swap');
		@import url('https://fonts.googleapis.com/css2?family=Figtree:wght@700&display=swap');

		:root {
			--ofc-page-bg: #ffffff;
			--ofc-header-bg: #254B96;
			--ofc-page-outer-padding: 24px;
		}

		header, footer, #MainMenu { display: none !important; }

		body, .stApp {
			background: var(--ofc-page-bg);
			font-family: "Rubik", system-ui, -apple-system, Arial, sans-serif;
			overflow-x: hidden;
		}

		/* Remove Streamlit's default top padding so the header touches the top */
		div[data-testid="stAppViewContainer"] > .main,
		div[data-testid="stAppViewContainer"] > .main .block-container {
			padding-top: 0 !important;
		}

		.block-container {
			max-width: 1440px;
			margin: 0 auto;
			padding: 0;
		}

		/* Header (match 1.py full-bleed bar) */
		.ofc-header {
			background: var(--ofc-header-bg);
			color: white;
			font-size: 40px;
			font-weight: 700;
			padding: 32px calc(64px + var(--ofc-page-outer-padding));
			width: 100vw;
			margin-left: calc(50% - 50vw);
			margin-right: calc(50% - 50vw);
			box-sizing: border-box;
		}

		.ofc-page {
			padding: 60px calc(64px + var(--ofc-page-outer-padding)) 48px;
			box-sizing: border-box;
		}

		/* Center column that holds upload-summary + result */
		.center-col {
			width: 640px;
			margin: 0 auto;
		}

		/* Uploaded file card */
		.file-card {
			width: 640px;
			height: 120px;
			margin-left: auto;
			margin-right: auto;
			background: rgba(151, 186, 255, 0.17);
			border-radius: 12px;
			outline: 1px solid #254B96;
			outline-offset: -0.5px;
			display: flex;
			align-items: center;
			justify-content: space-between;
			padding: 20px 18px 20px 24px;
			box-sizing: border-box;
			position: relative;
		}

		.file-close-icon {
			width: 24px;
			height: 24px;
			border-radius: 9999px;
			display: grid;
			place-items: center;
			color: #818181;
			border: 1px solid rgba(129, 129, 129, 0.55);
			font-size: 14px;
			line-height: 1;
			user-select: none;
		}

		.file-left {
			display: flex;
			align-items: center;
			gap: 18px;
		}

		.file-icon {
			width: 64.67px;
			height: 80px;
			border-radius: 12px;
			background: #818181;
			display: grid;
			place-items: center;
			flex: 0 0 auto;
		}

		.file-name {
			color: #111111;
			font-size: 20px;
			font-weight: 500;
			line-height: 1.2;
		}

		.file-size {
			color: #111111;
			font-size: 14px;
			font-weight: 300;
			margin-top: 6px;
		}

		/* Result card */
		.result-card {
			width: 640px;
			height: 180px;
			border-radius: 24px;
			border: 2px solid #254B96;
			box-sizing: border-box;
			margin-left: auto;
			margin-right: auto;
			margin-top: 32px;
			padding: 18px 24px;
		}

		.result-title {
			color: #254B96;
			font-size: 32px;
			font-weight: 600;
			margin-bottom: 22px;
		}

		.result-row {
			display: flex;
			align-items: center;
			justify-content: center;
			padding: 0;
		}

		.result-row-inner {
			display: grid;
			grid-template-columns: auto auto;
			column-gap: 160px;
			align-items: center;
		}

		.result-key, .result-value {
			color: #254B96;
			font-size: 24px;
			font-weight: 500;
		}

		/* Two big panels row */
		.panels-row {
			display: grid;
			grid-template-columns: 640px 640px;
			gap: 32px;
			justify-content: center;
			margin-top: 40px;
		}

		.panel {
			width: 640px;
			height: 520px;
			border-radius: 24px;
			box-sizing: border-box;
			padding: 22px 28px;
			background: white;
		}

		.panel.proposed {
			border: 2px solid #44CD1B;
		}

		.panel.baseline {
			border: 2px solid #E51F1F;
		}

		.panel-title.proposed {
			color: #44CE1B;
			font-size: 32px;
			font-weight: 600;
			margin-bottom: 18px;
		}

		.panel-title.baseline {
			color: #E51F1F;
			font-size: 32px;
			font-weight: 600;
			margin-bottom: 18px;
		}

		.metrics-grid {
			display: grid;
			grid-template-columns: 148px 148px;
			gap: 44px 120px;
			justify-content: center;
			padding-top: 30px;
		}

		.metric {
			width: 148px;
			height: 148px;
			border-radius: 9999px;
			position: relative;
			display: grid;
			place-items: center;
			box-sizing: border-box;
			--p: 80;
			--track: #E6E6E6;
			--accent: #58B90A;
			background: conic-gradient(var(--accent) calc(var(--p) * 1%), var(--track) 0);
		}

		.metric::after {
			content: "";
			position: absolute;
			inset: 16px;
			border-radius: 9999px;
			background: white;
			z-index: 0;
		}

		.metric.proposed { --accent: #58B90A; }
		.metric.baseline { --accent: #EF6D85; }

		.metric-content {
			position: relative;
			z-index: 1;
			text-align: center;
			font-family: "Figtree", system-ui, -apple-system, Arial, sans-serif;
			font-weight: 700;
			line-height: 22px;
			display: flex;
			flex-direction: column;
			align-items: center;
			justify-content: center;
		}

		.metric-label.proposed, .metric-value.proposed {
			color: #9BF62D;
		}

		.metric-label.baseline, .metric-value.baseline {
			color: #EF6D85;
		}

		.metric-label {
			font-size: 18px;
			margin-bottom: 6px;
		}

		.metric-value {
			font-size: 20px;
		}

		/* Reduce Streamlit default spacing around markdown blocks */
		div[data-testid="stMarkdownContainer"] > p { margin-bottom: 0; }
		</style>
		""",
		unsafe_allow_html=True,
	)


def render_metric(metric: Metric, variant: str) -> str:
	safe_label = html.escape(metric.label)
	safe_value = html.escape(f"{metric.percent} %")
	percent = max(0, min(100, int(metric.percent)))
	return textwrap.dedent(
		f"""
		<div class="metric {variant}" style="--p:{percent}">
			<div class="metric-content">
				<div class="metric-label {variant}">{safe_label}</div>
				<div class="metric-value {variant}">{safe_value}</div>
			</div>
		</div>
		"""
	).strip()


def main() -> None:
	st.set_page_config(page_title="Oral Fluency Classification", layout="wide")
	inject_css()

	st.markdown('<div class="ofc-header">Oral Fluency Classification</div>', unsafe_allow_html=True)
	st.markdown('<div class="ofc-page">', unsafe_allow_html=True)

	# Design-first flow:
	# - If no file has been uploaded yet, show the uploader.
	# - After upload, show this "results" screen UI.
	uploaded = st.session_state.get("uploaded_audio")
	if uploaded is None:
		uploaded_widget = st.file_uploader(
			"Upload audio",
			type=["wav", "mp3"],
			label_visibility="collapsed",
			key="audio_file",
		)
		if uploaded_widget is not None:
			st.session_state["uploaded_audio"] = {
				"name": uploaded_widget.name,
				"bytes": uploaded_widget.getvalue(),
			}
			# Default placeholders
			st.session_state.setdefault("fluency_result", "Intermediate")
			st.session_state.setdefault(
				"metrics_proposed",
				{"Accuracy": 80, "Precision": 80, "Recall": 80, "F1-Score": 80},
			)
			st.session_state.setdefault(
				"metrics_baseline",
				{"Accuracy": 80, "Precision": 80, "Recall": 80, "F1-Score": 80},
			)
			st.rerun()
		st.markdown("</div>", unsafe_allow_html=True)
		return

	# Support either a dict payload from 1.py or an UploadedFile.
	if isinstance(uploaded, dict):
		filename = str(uploaded.get("name") or "audio.wav")
		audio_bytes = uploaded.get("bytes") or b""
		size_text = _format_size(len(audio_bytes)) if audio_bytes else ""
	else:
		filename = getattr(uploaded, "name", "audio.wav")
		try:
			size_text = _format_size(uploaded.getbuffer().nbytes)
		except Exception:
			size_text = ""

	fluency_value = st.session_state.get("fluency_result", "Intermediate")
	metrics_proposed = st.session_state.get(
		"metrics_proposed",
		{"Accuracy": 80, "Precision": 80, "Recall": 80, "F1-Score": 80},
	)
	metrics_baseline = st.session_state.get(
		"metrics_baseline",
		{"Accuracy": 80, "Precision": 80, "Recall": 80, "F1-Score": 80},
	)

	
	spacer_left, center, spacer_right = st.columns([1, 2, 1])
	with center:
		st.markdown('<div class="center-col">', unsafe_allow_html=True)

		file_card_left = textwrap.dedent(
			f"""
			<div class="file-card">
				<div class="file-left">
					<div class="file-icon">♪</div>
					<div>
						<div class="file-name">{html.escape(filename)}</div>
						<div class="file-size">{html.escape(size_text)}</div>
					</div>
				</div>
				<div class="file-close-icon">×</div>
			</div>
			"""
		).strip()
		st.markdown(file_card_left, unsafe_allow_html=True)

		result_html = textwrap.dedent(
			"""
			<div class="result-card">
				<div class="result-title">Result</div>
				<div class="result-row">
					<div class="result-row-inner">
						<div class="result-key">Fluency&nbsp;&nbsp;:</div>
						<div class="result-value">{fluency}</div>
					</div>
				</div>
			</div>
			"""
		).strip()
		st.markdown(result_html.format(fluency=html.escape(str(fluency_value))), unsafe_allow_html=True)
		st.markdown("</div>", unsafe_allow_html=True)

	proposed_metrics = [
		Metric("Accuracy", int(metrics_proposed.get("Accuracy", 0))),
		Metric("Precision", int(metrics_proposed.get("Precision", 0))),
		Metric("Recall", int(metrics_proposed.get("Recall", 0))),
		Metric("F1-Score", int(metrics_proposed.get("F1-Score", 0))),
	]
	baseline_metrics = [
		Metric("Accuracy", int(metrics_baseline.get("Accuracy", 0))),
		Metric("Precision", int(metrics_baseline.get("Precision", 0))),
		Metric("Recall", int(metrics_baseline.get("Recall", 0))),
		Metric("F1-Score", int(metrics_baseline.get("F1-Score", 0))),
	]

	proposed_grid = "".join(render_metric(m, "proposed") for m in proposed_metrics)
	baseline_grid = "".join(render_metric(m, "baseline") for m in baseline_metrics)

	panels_html = textwrap.dedent(
		f"""
		<div class="panels-row">
			<div class="panel proposed">
				<div class="panel-title proposed">Proposed SVM</div>
				<div class="metrics-grid">{proposed_grid}</div>
			</div>
			<div class="panel baseline">
				<div class="panel-title baseline">Baseline SVM</div>
				<div class="metrics-grid">{baseline_grid}</div>
			</div>
		</div>
		"""
	).strip()
	st.markdown(panels_html, unsafe_allow_html=True)

	st.markdown("</div>", unsafe_allow_html=True)


if __name__ == "__main__":
	main()

