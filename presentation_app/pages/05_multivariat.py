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
    "Aufbauend auf den partiellen Korrelationen zeigt die Basisregression, "
    "dass Einkommensniveau und ökonomische Dynamik auch im gemeinsamen Modell "
    "robuste Zusammenhänge mit der E-Auto-Quote aufweisen."
),

    bullets=[
        "R² ≈ 0,54: Die ökonomischen Variablen erklären einen großen Teil der regionalen Varianz.",
    "Lohn pro Stunde positiv (β ≈ 0,0008, p < .001) unter Kontrolle von Wachstum und Altersstruktur.",
    "Lohnwachstum positiv (β ≈ 0,0015, p < .001); der Alterseffekt trägt keine zusätzliche Varianz bei.",
    "Standardisiert: Lohnwachstum (β ≈ 0,45) wirkt stärker als Einkommensniveau (β ≈ 0,41).",
    "Die Regression generalisiert die Logik der partiellen Korrelation auf mehrere Einflussfaktoren.",
],
)

data = build_panel_data()
render_correlation_explorer(data, key_prefix="multivariat")
end_slide()
