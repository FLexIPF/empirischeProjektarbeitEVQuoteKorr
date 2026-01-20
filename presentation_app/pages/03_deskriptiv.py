from __future__ import annotations

import streamlit as st

from data_loader import build_panel_data
from styles import apply_base_styles
from ui_sections import (
    SlideImage,
    end_slide,
    render_images,
    render_trend_chart,
    start_slide,
)


st.set_page_config(page_title="Deskriptive Muster", layout="wide")
apply_base_styles()

start_slide(
    title="Deskriptive Muster",
    lead=(
        "Die E-Auto-Quote ist regional heterogen und zeigt klaren Zeittrend. "
        "Die Verteilung bleibt selbst innerhalb einzelner Jahre breit gestreut."
    ),
    bullets=[
        "Trend: kontinuierlicher Anstieg der durchschnittlichen E-Auto-Quote.",
        "Streuung: hohe regionale Varianz pro Jahr.",
    ],
)

data = build_panel_data()
render_trend_chart(data)
render_images(
    [
        SlideImage("meaEvQuote20-23.png", "Zeittrend der mittleren E-Auto-Quote."),
        SlideImage("regiostreuEquoteJahr.png", "Regionale Streuung nach Jahr."),
    ]
)
end_slide()
