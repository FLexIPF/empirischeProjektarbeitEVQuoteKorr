from __future__ import annotations

import streamlit as st

from data_loader import build_panel_data
from styles import apply_base_styles
from ui_sections import end_slide, render_correlation_explorer, start_slide


st.set_page_config(page_title="Multivariate Analyse", layout="wide")
apply_base_styles()

start_slide(
    title="Multivariate Analyse",
    lead=(
        "Basisregression ohne Zeitkontrolle: Einkommensniveau und Dynamik "
        "erklären den Großteil der Varianz."
    ),
    bullets=[
        "R² ≈ 0,54; Lohn pro Stunde positiv (β ≈ 0,0008, p < .001).",
        "Lohnwachstum positiv (β ≈ 0,0015, p < .001); Anteil 65+ negativ.",
        "Standardisiert: Lohnwachstum (β ≈ 0,45) > Lohnniveau (β ≈ 0,41).",
        "Korrelationsmatrix zeigt zentrale Variablenbeziehungen.",
    ],
)

data = build_panel_data()
render_correlation_explorer(data, key_prefix="multivariat")
end_slide()
