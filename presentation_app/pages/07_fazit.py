from __future__ import annotations

import streamlit as st

from styles import apply_base_styles
from ui_sections import end_slide, start_slide


st.set_page_config(page_title="Fazit", layout="wide")
apply_base_styles()

start_slide(
    title="Diskussion & Fazit",
    lead=(
        "Die E-Auto-Quote wird maßgeblich durch den Zeittrend bestimmt, "
        "bleibt jedoch regional sozial und ökonomisch differenziert."
    ),
    bullets=[
        "Der Zeittrend treibt die Diffusion, regionale Unterschiede bleiben jedoch bestehen.",
        "Einkommensniveau und insbesondere ökonomische Dynamik erklären einen Großteil dieser Differenzen.",
        "Demografische Strukturen wirken vor allem indirekt und verlieren im gemeinsamen Modell an Eigenständigkeit.",
        "Ausblick: Infrastrukturvariablen und kausale Designs zur Mechanismenklärung.",
    ],
)
end_slide()
