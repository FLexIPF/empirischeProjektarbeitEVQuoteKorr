from __future__ import annotations

import streamlit as st

from data_loader import build_panel_data
from styles import apply_base_styles
from ui_sections import end_slide, render_bivariate_explorer, start_slide


st.set_page_config(page_title="Bivariate Zusammenhänge", layout="wide")
apply_base_styles()

start_slide(
    title="Bivariate Zusammenhänge",
    lead=(
        "Die stärksten bivariaten Zusammenhänge finden wir bei Einkommen und "
        "ökonomischer Dynamik; Demografie wirkt moderat negativ."
    ),
    bullets=[
        "Lohnwachstum: r ≈ 0,61 (p < .001).",
        "Lohn/Entgelt pro Stunde: r ≈ 0,57 (p < .001).",
        "Anteil 65+: r ≈ −0,28 (p < .001).",
        "Mobilitätsniveau: r ≈ 0,11 (p < .001).",
    ],
)

data = build_panel_data()
render_bivariate_explorer(data, key_prefix="bivariat")
end_slide()
