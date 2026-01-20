from __future__ import annotations

import streamlit as st

from data_loader import build_panel_data, load_geojson
from styles import apply_base_styles
from ui_sections import (
    end_slide,
    render_panel_table,
    render_variable_explorer,
    start_slide,
)


st.set_page_config(page_title="Daten & Variablen", layout="wide")
apply_base_styles()

start_slide(
    title="Daten & Variablenlandschaft",
    lead=(
        "Die Analyse basiert auf einer panelstrukturierten Zusammenführung von "
        "Pkw-, VGR- und Demografievariablen."
    ),
    bullets=[
        "E-Auto-Quote: Anteil elektrischer Pkw am Bestand.",
        "Ökonomie: Lohn pro Stunde, Entgelt pro Stunde, Lohnwachstum.",
        "Demografie: Anteil 18–35 sowie 65+.",
        "Mobilität: Pkw pro 1.000 Einwohner.",
    ],
)

data = build_panel_data()
geojson = load_geojson()
render_variable_explorer(data, geojson, key_prefix="variablen")
render_panel_table(data)
end_slide()
