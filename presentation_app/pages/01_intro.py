from __future__ import annotations

import streamlit as st
from styles import apply_base_styles
from ui_sections import end_slide, start_slide


st.set_page_config(page_title="Intro", layout="wide")
apply_base_styles()

start_slide(
    title="Regionale Determinanten der E-Auto-Quote in Deutschland",
    lead=(
        "Eine animierte Story aus dem 02_Analyse-Notebook"),
    bullets=[
        "Fragestellung: Welche regionalen Strukturen erklären die E-Auto-Quote?",
        "Zeitraum: 2020–2023, Kreisebene.",
        "Datenbasis: Pkw-Bestand, VGR, Bevölkerungsdaten.",
        "Interaktive Kartenansicht im Kapitel »Daten & Variablen«.",
    ],
)
end_slide()
