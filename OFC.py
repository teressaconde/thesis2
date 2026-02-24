import streamlit as st
import base64
from html import escape


st.set_page_config(page_title="Oral Fluency Classification", layout="wide")


if "dataset" not in st.session_state:
	st.session_state.dataset = "Avalinguo"


if str(st.query_params.get("remove_audio", "0")) == "1":
	st.session_state.pop("uploaded_audio_obj", None)
	st.session_state.pop("uploaded_audio_data", None)
	st.session_state.pop("audio_uploader", None)
	st.query_params.clear()
	st.rerun()


st.markdown(
	"""
	<style>
	@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

header[data-testid="stHeader"] {
		display: none !important;
	}

	.stApp {
		background-color: #ececec;
		font-family: 'Inter', sans-serif;
		overflow-x: hidden;
	}

	.block-container {
		max-width: 1240px;
		padding-top: 0.6rem;
		padding-bottom: 2.5rem;
	}

	div[data-testid="stVerticalBlock"]:has(.header-bar) {
		gap: 0;
	}

	.header-bar {
		width: 100vw;
		margin-left: calc(50% - 50vw);
		margin-right: calc(50% - 50vw);
		margin-bottom: 2.55rem;
		background: #274d98;
		height: 94px;
		display: flex;
		align-items: center;
		padding-left: max(32px, calc((100vw - 1240px) / 2 + 70px));
		border-top: 1px solid #1c3a76;
		box-sizing: border-box;
	}

	.header-title {
		color: #ffffff;
		font-size: 50px;
		font-weight: 800;
		line-height: 1;
		margin: 0;
		letter-spacing: 0.3px;
	}

	.dataset-wrap {
		display: flex;
		justify-content: center;
		align-items: center;
		margin-bottom: 22px;
		gap: 18px;
	}

	.stButton > button {
		border-radius: 999px;
		font-weight: 700;
		font-size: 17px;
		padding: 8px 24px;
		line-height: 1;
		min-height: 38px;
		border: 2px solid #2e56a4;
		transition: none;
	}

	.upload-shell {
		max-width: 660px;
		margin: 0 auto;
	}

	.stButton > button[kind="primary"] {
		color: #ffffff;
		background: #2e56a4;
	}

	.stButton > button[kind="secondary"] {
		color: #2e56a4;
		background: #ececec;
	}

	div[data-testid="stFileUploader"] {
		position: relative;
	}

	div[data-testid="stFileUploader"] section,
	div[data-testid="stFileUploaderDropzone"],
	section[data-testid="stFileUploaderDropzone"] {
		position: relative;
		border: 2.5px dashed #5a7fc3 !important;
		border-radius: 12px !important;
		background: #d2d8e5 !important;
		min-height: 180px !important;
		display: flex;
		align-items: center;
		justify-content: center;
		padding-top: 0;
		box-shadow: none !important;
		background-image: none !important;
	}

	div[data-testid="stFileUploader"] button,
	div[data-testid="stFileUploaderDropzone"] button,
	section[data-testid="stFileUploaderDropzone"] button {
		position: absolute !important;
		inset: 0 !important;
		opacity: 0 !important;
		width: 100% !important;
		height: 100% !important;
		z-index: 4 !important;
	}

	div[data-testid="stFileUploaderDropzone"] section {
		padding: 0;
	}

	div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzoneInstructions"],
	div[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"],
	section[data-testid="stFileUploaderDropzone"] [data-testid="stFileUploaderDropzoneInstructions"] {
		opacity: 0 !important;
		pointer-events: none !important;
	}

	div[data-testid="stFileUploader"] section::before,
	div[data-testid="stFileUploaderDropzone"]::before,
	section[data-testid="stFileUploaderDropzone"]::before {
		content: "";
		position: absolute;
		top: 22px;
		left: 50%;
		transform: translateX(-50%);
		width: 86px;
		height: 66px;
		background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 90 90'><rect x='8' y='28' width='50' height='40' rx='6' fill='%23b4b8c2'/><rect x='26' y='18' width='32' height='18' rx='4' fill='%23c2c6cf'/><rect x='44' y='22' width='50' height='44' rx='7' fill='%23a8adb8'/><rect x='56' y='12' width='28' height='16' rx='3' fill='%23c7cbd3'/><circle cx='97' cy='44' r='11' fill='%238d929d'/><rect x='92' y='55' width='10' height='22' rx='4' transform='rotate(24 97 66)' fill='%23989daa'/></svg>");
		background-size: contain;
		background-repeat: no-repeat;
		background-position: center;
		opacity: 0.9;
		z-index: 2;
		pointer-events: none;
	}

	div[data-testid="stFileUploader"] section::after,
	div[data-testid="stFileUploaderDropzone"]::after,
	section[data-testid="stFileUploaderDropzone"]::after {
		content: "Upload speech audio here";
		position: absolute;
		left: 50%;
		top: 112px;
		transform: translateX(-50%);
		white-space: nowrap;
		text-align: center;
		font-size: 18px;
		line-height: 1.25;
		font-weight: 700;
		color: #8e949e;
		z-index: 2;
		pointer-events: none;
	}

	div[data-testid="stFileUploader"]::after {
		content: "Supported formats: MP3, WAV · Clear speech recommended";
		position: absolute;
		left: 50%;
		top: 139px;
		transform: translateX(-50%);
		white-space: nowrap;
		text-align: center;
		font-size: 11px;
		line-height: 1.25;
		font-weight: 500;
		color: #9aa0ab;
		z-index: 2;
		pointer-events: none;
	}

	.uploaded-card {
		height: 178px;
		border: 1.8px solid #5a7fc3;
		border-radius: 12px;
		background: #d2d8e5;
		padding: 22px 24px;
		display: flex;
		align-items: center;
		gap: 20px;
		box-sizing: border-box;
	}

	.audio-icon {
		width: 90px;
		height: 90px;
		border-radius: 12px;
		background: #828282;
		color: #ffffff;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 48px;
		flex-shrink: 0;
	}

	.audio-details {
		flex: 1;
		display: flex;
		flex-direction: column;
		justify-content: center;
		color: #7b7b7b;
	}

	.audio-name {
		font-size: 34px;
		font-weight: 700;
		line-height: 1.1;
		margin: 0 0 8px 0;
	}

	.audio-size {
		font-size: 18px;
		margin: 0 0 6px 0;
	}

	.audio-player-inline {
		width: 100%;
		height: 34px;
		border-radius: 10px;
	}

	.audio-close {
		color: #8f8f8f;
		margin-left: 8px;
		font-size: 36px;
		font-weight: 500;
		line-height: 1;
		text-decoration: none;
		display: inline-flex;
		align-items: center;
		justify-content: center;
		padding-bottom: 0;
		box-sizing: border-box;
		opacity: 0.75;
	}

	.audio-close:hover {
		color: #6f6f6f;
		opacity: 1;
	}

	.arrow-holder {
		min-height: 180px;
		display: flex;
		justify-content: center;
		align-items: center;
	}

	.arrow-circle {
		width: 72px;
		height: 72px;
		border-radius: 50%;
		background: #2e56a4;
		color: #ffffff;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: 40px;
		font-weight: 700;
	}

	.result-card {
		border: 2px solid #5a7fc3;
		border-radius: 18px;
		padding: 18px 22px 14px;
		min-height: 290px;
		background: #ececec;
	}

	.result-title-green {
		color: #37c424 !important;
		font-size: 40px;
		font-weight: 800;
		margin: 0 0 28px 0;
		line-height: 1;
	}

	.result-title-red {
		color: #ff1f4e !important;
		font-size: 40px;
		font-weight: 800;
		margin: 0 0 28px 0;
		line-height: 1;
	}

	.result-text-green {
		color: #37c424 !important;
		font-size: 22px;
		line-height: 1.35;
		font-weight: 500;
		margin: 0;
		text-align: left;
		word-spacing: normal;
	}

	.result-text-red {
		color: #ff1f4e !important;
		font-size: 22px;
		line-height: 1.35;
		font-weight: 500;
		margin: 0;
		text-align: left;
		word-spacing: normal;
	}

	@media (max-width: 90px) {
		.header-title { font-size: 38px; }
		.stButton > button { font-size: 15px; }
		.result-title-green, .result-title-red { font-size: 36px; }
		.result-text-green, .result-text-red { font-size: 18px; }
		.audio-name { font-size: 26px; }
	}
	</style>
	""",
	unsafe_allow_html=True,
)

st.markdown(
	"""
	<div class="header-bar">
		<h1 class="header-title">Oral Fluency Classification</h1>
	</div>
	""",
	unsafe_allow_html=True,
)

margin_l, top_left, arrow_col, margin_r = st.columns([1.25, 8.6, 1.0, 1.25], gap="small")

with top_left:
	# Dataset buttons centered above the upload area
	btn_pad_l, btn_left, btn_right, btn_pad_r = st.columns([2.2, 2, 2, 2.2], gap="small")
	with btn_left:
		if st.button(
			"Avalinguo",
			type="primary" if st.session_state.dataset == "Avalinguo" else "secondary",
			use_container_width=True,
		):
			st.session_state.dataset = "Avalinguo"
	with btn_right:
		if st.button(
			"SpeechOcean",
			type="primary" if st.session_state.dataset == "SpeechOcean" else "secondary",
			use_container_width=True,
		):
			st.session_state.dataset = "SpeechOcean"

	uploaded_audio_data = st.session_state.get("uploaded_audio_data")
	st.markdown('<div class="upload-shell">', unsafe_allow_html=True)

	if uploaded_audio_data is None:
		uploaded_audio = st.file_uploader(
			"Upload speech audio",
			type=["wav", "mp3"],
			label_visibility="collapsed",
			key="audio_uploader",
		)
		if uploaded_audio is not None:
			st.session_state.uploaded_audio_obj = uploaded_audio
			file_ext = uploaded_audio.name.split(".")[-1].lower() if "." in uploaded_audio.name else "wav"
			audio_mime = "audio/wav" if file_ext == "wav" else "audio/mpeg"
			st.session_state.uploaded_audio_data = {
				"name": uploaded_audio.name,
				"size": uploaded_audio.size,
				"mime": audio_mime,
				"bytes": uploaded_audio.getvalue(),
			}
			st.rerun()

	if uploaded_audio_data is not None:
		size_mb = uploaded_audio_data["size"] / (1024 * 1024)
		audio_mime = uploaded_audio_data["mime"]
		audio_b64 = base64.b64encode(uploaded_audio_data["bytes"]).decode("utf-8")
		audio_src = f"data:{audio_mime};base64,{audio_b64}"
		safe_name = escape(uploaded_audio_data["name"])
		st.markdown(
			f"""
			<div class="uploaded-card">
				<div class="audio-icon">♪</div>
				<div class="audio-details">
					<p class="audio-name">{safe_name}</p>
					<p class="audio-size">{size_mb:.1f} MB</p>
					<audio controls class="audio-player-inline" src="{audio_src}"></audio>
				</div>
				<a class="audio-close" href="?remove_audio=1" title="Remove audio">×</a>
			</div>
			""",
			unsafe_allow_html=True,
		)

	st.markdown('</div>', unsafe_allow_html=True)

with arrow_col:
	st.markdown('<div class="arrow-holder">', unsafe_allow_html=True)
	go_clicked = st.button("➜", key="go_results", disabled=uploaded_audio_data is None)
	st.markdown('</div>', unsafe_allow_html=True)

	if go_clicked and uploaded_audio_data is not None:
		st.switch_page("pages/2.py")

st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)

bottom_left, bottom_right = st.columns([1, 1], gap="large")

with bottom_left:
	st.markdown(
		"""
		<div class="result-card">
			<h2 class="result-title-green">Baseline SVM</h2>
			<p class="result-text-green">
				The features are mapped into a higher-dimensional space using a non-linear kernel,
				where similarity relationships between samples are computed. A quadratic programming
				solver then identifies key support vectors and determines the decision boundary,
				which is used to classify speech samples into their corresponding fluency categories.
			</p>
		</div>
		""",
		unsafe_allow_html=True,
	)

with bottom_right:
	st.markdown(
		"""
		<div class="result-card">
			<h2 class="result-title-red">Proposed SVM</h2>
			<p class="result-text-red">
				These features are mapped into a hybrid feature space using Random Fourier Features
				and the Nyström method to efficiently represent non-linear speech patterns.
				The resulting features are then passed to an SVM classifier trained using Sequential
				Minimal Optimization, which enables efficient model training. The trained model
				classifies the input speech into its corresponding oral fluency category.
			</p>
		</div>
		""",
		unsafe_allow_html=True,
	)
