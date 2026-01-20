from __future__ import annotations

import streamlit as st

from styles import apply_base_styles


st.set_page_config(page_title="E-Auto-Quote Story", layout="wide")
apply_base_styles()

st.title("Interaktive Präsentation: E-Auto-Quote")

st.markdown(
    """
    **Navigation:** Nutze die Seitenleiste von Streamlit, um zwischen den Kapiteln
    zu wechseln.
    """
)
