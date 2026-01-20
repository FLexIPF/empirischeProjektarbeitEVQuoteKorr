from __future__ import annotations

import streamlit as st

from styles import apply_base_styles
from ui_sections import end_slide, start_slide


st.set_page_config(page_title="Fazit", layout="wide")
apply_base_styles()

start_slide(
    title="Diskussion & Fazit",
    lead=(
        "Die E-Auto-Quote ist stark zeitgetrieben, bleibt aber regional durch "
        "Einkommens- und Altersstrukturen differenziert."
    ),
    bullets=[
        "Zeittrend + soziale Differenzierung prägen die Diffusion.",
        "Ältere Bevölkerungsstruktur wirkt hemmend, auch unter Zeitkontrolle.",
        "Ausblick: Infrastruktur- und kausale Designs ergänzen die Analyse.",
    ],
)
end_slide()
