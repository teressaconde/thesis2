"""Streamlit multipage entry for Screen 2.

This delegates to the canonical implementation in the workspace root `2.py`.
Run the app via:
    streamlit run 1.py
"""

from __future__ import annotations

from pathlib import Path

screen_path = Path(__file__).resolve().parents[1] / "2.py"
code = screen_path.read_text(encoding="utf-8")
exec(compile(code, str(screen_path), "exec"), globals(), globals())
