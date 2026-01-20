from __future__ import annotations

import streamlit as st

from styles import apply_base_styles
from ui_sections import SlideImage, end_slide, render_images, start_slide


st.set_page_config(page_title="Zeitdimension", layout="wide")
apply_base_styles()

start_slide(
    title="Zeitdimension",
    lead=(
        "Zeitdummies zeigen einen starken Diffusionstrend (R² ≈ 0,71) und "
        "dominieren die kurzfristige Dynamik."
    ),
    bullets=[
        "Jahreseffekte vs. 2020: 2021 ≈ +0,22 pp; 2022 ≈ +0,75 pp; 2023 ≈ +1,4 pp.",
        "Einkommen bleibt positiv (β ≈ 0,0005, p < .001), Lohnwachstum n. s.",
        "Anteil 65+ deutlich negativ (β ≈ −0,0425, p < .001).",
        "Within-Year-Korrelationen steigen: r ≈ 0,14 (2020) → 0,63 (2022).",
    ],
)

render_images(
    [
        SlideImage(
            "WITHIN-YEAR_KORRELATIONEN.png",
            "Within-Year-Korrelationen zwischen Lohn und E-Auto-Quote.",
        ),
        SlideImage(
            "REGRESSIOZeitkontjahr.png",
            "Regression mit Jahres-Dummies (Basisjahr 2020).",
        ),
    ]
)
end_slide()
