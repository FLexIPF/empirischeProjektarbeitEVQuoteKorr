from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data_loader import DATA_DIR, YEAR_RANGE
from map_utils import (
    build_color_scale,
    enrich_geojson,
    geometry_centroid,
    render_map,
)

VARIABLE_GROUPS = {
    "zielvariable": ["e_auto_quote"],
    "mobilitaetsniveau": ["pkw_pro_1000"],
    "einkommensniveau": ["lohn_pro_stunde", "entgelt_pro_stunde"],
    "wirtschaftsstruktur_beschaeftigung": [
        "anteil_dl_besch",
        "anteil_pg_besch",
        "anteil_vg_besch",
    ],
    "arbeitsintensitaet": ["arbeitsstunden_pro_arb"],
    "dynamik": ["lohn_wachstum"],
    "demografie": ["anteil_18_35", "anteil_65_plus"],
}

VARIABLE_METADATA = {
    "e_auto_quote": {
        "label": "E-Auto-Quote",
        "format": "percent",
        "time": True,
    },
    "pkw_pro_1000": {
        "label": "Pkw pro 1.000 Einwohner",
        "format": "number",
        "time": True,
    },
    "lohn_pro_stunde": {
        "label": "Lohn pro Stunde",
        "format": "currency",
        "time": True,
    },
    "entgelt_pro_stunde": {
        "label": "Entgelt pro Stunde",
        "format": "currency",
        "time": True,
    },
    "anteil_dl_besch": {
        "label": "Anteil Dienstleistungsbeschäftigung",
        "format": "percent",
        "time": True,
    },
    "anteil_pg_besch": {
        "label": "Anteil Produzierendes Gewerbe (Beschäftigung)",
        "format": "percent",
        "time": True,
    },
    "anteil_vg_besch": {
        "label": "Anteil Verarbeitendes Gewerbe (Beschäftigung)",
        "format": "percent",
        "time": True,
    },
    "arbeitsstunden_pro_arb": {
        "label": "Arbeitsstunden pro Arbeitnehmer",
        "format": "number",
        "time": True,
    },
    "lohn_wachstum": {
        "label": "Lohnwachstum (in %)",
        "format": "percent",
        "time": True,
    },
    "anteil_18_35": {
        "label": "Anteil 18–35",
        "format": "percent",
        "time": False,
    },
    "anteil_65_plus": {
        "label": "Anteil 65+",
        "format": "percent",
        "time": False,
    },
}


@dataclass
class SlideImage:
    filename: str
    caption: str


def start_slide(title: str, lead: str, bullets: List[str] | None = None) -> None:
    st.markdown('<div class="slide-container">', unsafe_allow_html=True)
    st.subheader(title)
    st.markdown(lead)
    if bullets:
        st.markdown("\n".join([f"- {bullet}" for bullet in bullets]))


def end_slide() -> None:
    st.markdown("</div>", unsafe_allow_html=True)


def format_value(value: float | int | None, value_format: str) -> str | None:
    if value is None or pd.isna(value):
        return None
    if value_format == "percent":
        return (
            f"{float(value) * 100:,.2f} %"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    if value_format == "currency":
        return (
            f"{float(value):,.2f} €"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )
    return (
        f"{float(value):,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def render_images(images: Iterable[SlideImage], columns: int = 2) -> None:
    images = list(images)
    if not images:
        return
    rows = [images[i : i + columns] for i in range(0, len(images), columns)]
    for row in rows:
        cols = st.columns(len(row))
        for col, item in zip(cols, row):
            path = DATA_DIR / item.filename
            with col:
                if path.exists():
                    st.image(str(path), caption=item.caption, use_container_width=True)
                else:
                    st.warning(f"Bild fehlt: {item.filename}")


def render_map_section(data: pd.DataFrame, geojson: dict, key_prefix: str) -> None:
    st.markdown(
        "**Interaktive Karte:** Differenz zur minimalen E-Auto-Quote nach Kreis und Jahr"
    )
    selected_year = st.slider(
        "Jahr auswählen",
        min_value=YEAR_RANGE[0],
        max_value=YEAR_RANGE[1],
        value=int(data["jahr"].max()),
        step=1,
        key=f"{key_prefix}_map_year",
    )
    year_data = data.loc[
        data["jahr"] == selected_year, ["kreis_id", "e_auto_quote"]
    ].dropna()
    if year_data.empty:
        st.info("Für das gewählte Jahr liegen keine E-Auto-Quoten vor.")
        return
    min_value = year_data["e_auto_quote"].min()
    diff_to_min = year_data["e_auto_quote"] - min_value
    value_lookup = dict(zip(year_data["kreis_id"], diff_to_min))
    quote_lookup = {
        kreis_id: format_value(value, "percent")
        for kreis_id, value in zip(year_data["kreis_id"], year_data["e_auto_quote"])
    }
    vmin, vmax = build_color_scale(diff_to_min)
    geojson_with_values, missing = enrich_geojson(
        geojson,
        value_lookup,
        vmin,
        vmax,
        "e_auto_quote_diff",
        color_range=([59, 130, 246], [239, 68, 68]),
    )
    for feature in geojson_with_values.get("features", []):
        props = feature.get("properties", {})
        kreis_id = props.get("kreis_id")
        props["e_auto_quote_display"] = quote_lookup.get(kreis_id)
    if missing:
        st.caption(
            "Fehlende Kreis-IDs im Datensatz: "
            + ", ".join(sorted({m for m in missing if m}))
        )
    render_map(
        geojson_with_values,
        tooltip_label="Differenz zur Minimalquote",
        value_key="e_auto_quote_diff",
        extra_tooltip_label="E-Auto-Quote",
        extra_value_key="e_auto_quote_display",
        highlighted_kreis=None,
    )


def render_trend_chart(data: pd.DataFrame) -> None:
    st.markdown("**Zeittrend (aus den Pkw-Daten aggregiert)**")
    trend = (
        data.groupby("jahr", as_index=False)["e_auto_quote"].mean().rename(
            columns={"e_auto_quote": "E-Auto-Quote"}
        )
    )
    st.line_chart(trend, x="jahr", y="E-Auto-Quote")


def render_counts_table(data: pd.DataFrame) -> None:
    st.markdown("**Beobachtungen pro Jahr (Pkw-Datensatz)**")
    counts = data.groupby("jahr")["kreis_id"].count().reset_index(name="n")
    st.dataframe(counts, use_container_width=True)


def render_variable_explorer(
    data: pd.DataFrame, geojson: dict, key_prefix: str
) -> None:
    st.markdown("**Variable Explorer (aus 02_Analyse)**")
    available_groups = {
        group: [var for var in variables if var in data.columns]
        for group, variables in VARIABLE_GROUPS.items()
    }
    available_groups = {
        group: variables for group, variables in available_groups.items() if variables
    }
    if not available_groups:
        st.warning("Keine der erwarteten Variablen ist im Datensatz vorhanden.")
        return
    group_label = st.selectbox(
        "Variablengruppe auswählen",
        list(available_groups.keys()),
        key=f"{key_prefix}_group_select",
    )
    group_variables = available_groups[group_label]
    variable_labels = [
        VARIABLE_METADATA[var]["label"]
        for var in group_variables
        if var in VARIABLE_METADATA
    ]
    variable_label = st.selectbox(
        "Variable auswählen",
        variable_labels,
        key=f"{key_prefix}_var_select",
    )
    variable_col = next(
        var
        for var in group_variables
        if VARIABLE_METADATA.get(var, {}).get("label") == variable_label
    )
    variable_info = VARIABLE_METADATA[variable_col]
    if variable_info["time"]:
        selected_year = st.slider(
            "Jahr filtern",
            min_value=YEAR_RANGE[0],
            max_value=YEAR_RANGE[1],
            value=int(data["jahr"].max()),
            step=1,
            key=f"{key_prefix}_year_select",
        )
        filtered = data.loc[data["jahr"] == selected_year].copy()
    else:
        filtered = data.sort_values("jahr").drop_duplicates("kreis_id", keep="last")
        st.caption("Hinweis: Diese Variable ist zeitinvariant (Stand 2024).")

    bundesland_options = sorted(
        bundesland
        for bundesland in filtered["bundesland"].dropna().unique()
        if bundesland
    )
    selected_bundesland = st.selectbox(
        "Bundesland filtern (optional)",
        ["Alle"] + bundesland_options,
        key=f"{key_prefix}_bundesland_select",
    )
    if selected_bundesland != "Alle":
        filtered = filtered.loc[filtered["bundesland"] == selected_bundesland].copy()

    kreis_lookup = {
        feature["properties"]["kreis_id"]: feature["properties"]["name"]
        for feature in geojson.get("features", [])
    }
    kreis_options = sorted(
        [(kreis_id, name) for kreis_id, name in kreis_lookup.items() if kreis_id],
        key=lambda item: item[1],
    )
    highlighted_kreis = None
    selection = st.selectbox(
        "Kreis hervorheben (Label auf der Karte)",
        options=["Keiner"] + [name for _, name in kreis_options],
        key=f"{key_prefix}_kreis_select",
    )
    if selection != "Keiner":
        selected_kreis_id = next(
            kreis_id for kreis_id, name in kreis_options if name == selection
        )
        selected_feature = next(
            feature
            for feature in geojson.get("features", [])
            if feature["properties"].get("kreis_id") == selected_kreis_id
        )
        lon, lat = geometry_centroid(selected_feature["geometry"])
        highlighted_kreis = {
            "name": selection,
            "position": [lon, lat],
        }

    if filtered.empty:
        st.info("Keine Daten für die aktuelle Auswahl vorhanden.")
        return

    mean_value = float(filtered[variable_col].mean())
    median_value = float(filtered[variable_col].median())
    metric_cols = st.columns(2)
    metric_cols[0].metric(
        "Deutschland: Mittelwert",
        format_value(mean_value, variable_info["format"]) or "-",
    )
    metric_cols[1].metric(
        "Deutschland: Median",
        format_value(median_value, variable_info["format"]) or "-",
    )
    reference_label = st.selectbox(
        "Kartenbezug auswählen",
        ["Mittelwert", "Median"],
        key=f"{key_prefix}_reference_select",
    )
    reference_value = mean_value if reference_label == "Mittelwert" else median_value
    filtered = filtered.copy()
    filtered["diff_to_reference"] = filtered[variable_col] - reference_value
    filtered["value_display"] = filtered[variable_col].apply(
        lambda value: format_value(value, variable_info["format"])
    )
    value_lookup = dict(zip(filtered["kreis_id"], filtered["diff_to_reference"]))
    display_lookup = dict(zip(filtered["kreis_id"], filtered["value_display"]))
    vmin, vmax = build_color_scale(filtered["diff_to_reference"])
    top_three = (
        filtered.nlargest(3, "diff_to_reference")[["kreis_id", "kreis_name"]]
        .dropna(subset=["kreis_id"])
        .set_index("kreis_id")["kreis_name"]
        .to_dict()
    )
    bottom_three = (
        filtered.nsmallest(3, "diff_to_reference")[["kreis_id", "kreis_name"]]
        .dropna(subset=["kreis_id"])
        .set_index("kreis_id")["kreis_name"]
        .to_dict()
    )
    geojson_with_values, missing = enrich_geojson(
        geojson,
        value_lookup,
        vmin,
        vmax,
        "diff_to_reference",
        color_range=([59, 130, 246], [239, 68, 68]),
        diverging=True,
    )
    for feature in geojson_with_values.get("features", []):
        props = feature.get("properties", {})
        kreis_id = props.get("kreis_id")
        props["value_display"] = display_lookup.get(kreis_id)
        if kreis_id in bottom_three:
            props["fill_color"] = [250, 204, 21, 220]
        elif kreis_id in top_three:
            props["fill_color"] = [34, 197, 94, 220]
    if missing:
        st.caption(
            "Fehlende Kreis-IDs im Datensatz: "
            + ", ".join(sorted({m for m in missing if m}))
        )
    render_map(
        geojson_with_values,
        tooltip_label=f"{variable_label} (Abweichung vom {reference_label})",
        value_key="diff_to_reference",
        extra_tooltip_label=variable_label,
        extra_value_key="value_display",
        highlighted_kreis=highlighted_kreis,
    )
    st.caption(
        "Farblogik: Blau = unter dem Referenzwert, Rot = darüber. "
        "Top 3 höchsten Abweichungen = Grün, Top 3 niedrigsten Abweichungen = Gelb."
    )

    col_left, col_right = st.columns([2, 1])
    with col_left:
        fig = px.histogram(
            filtered,
            x=variable_col,
            nbins=40,
            title=f"Verteilung: {variable_label}",
        )
        st.plotly_chart(fig, use_container_width=True)
    with col_right:
        summary = (
            filtered[
                [
                    "kreis_name",
                    "kreis_id",
                    "bundesland",
                    variable_col,
                    "diff_to_reference",
                ]
            ]
            .dropna()
            .sort_values(variable_col)
            .rename(
                columns={
                    "kreis_name": "Kreis",
                    "kreis_id": "Kreis-ID",
                    "bundesland": "Bundesland",
                    variable_col: variable_label,
                    "diff_to_reference": f"Abweichung vom {reference_label}",
                }
            )
        )
        min_row = summary.head(1).copy()
        bottom_five = summary.head(5).copy()
        top_five = summary.tail(5).sort_values(variable_label, ascending=False).copy()

        st.markdown("**Minimum**")
        st.dataframe(min_row, use_container_width=True)
        st.markdown("**Top 5 (höchste Werte)**")
        st.dataframe(top_five, use_container_width=True)
        st.markdown("**Bottom 5 (niedrigste Werte)**")
        st.dataframe(bottom_five, use_container_width=True)


def render_bivariate_explorer(data: pd.DataFrame, key_prefix: str) -> None:
    st.markdown("**Regression Explorer (bivariat)**")
    candidate_vars = [
        var
        for group, variables in VARIABLE_GROUPS.items()
        for var in variables
        if group != "zielvariable"
    ]
    candidate_vars = [var for var in candidate_vars if var in data.columns]
    candidate_labels = [
        VARIABLE_METADATA[var]["label"]
        for var in candidate_vars
        if var in VARIABLE_METADATA
    ]
    if not candidate_labels:
        st.warning("Keine erklärenden Variablen im Datensatz gefunden.")
        return
    x_label = st.selectbox(
        "Erklärende Variable",
        candidate_labels,
        key=f"{key_prefix}_reg_var_select",
    )
    x_col = next(
        var
        for var in candidate_vars
        if VARIABLE_METADATA.get(var, {}).get("label") == x_label
    )
    years = sorted(data["jahr"].dropna().unique().tolist())
    selected_years = st.multiselect(
        "Jahre auswählen",
        options=years,
        default=[max(years)] if years else [],
        key=f"{key_prefix}_reg_year_multi_select",
    )
    show_ols = st.checkbox(
        "OLS-Linien pro Jahr anzeigen",
        value=True,
        key=f"{key_prefix}_reg_show_ols",
    )
    reg_df = data.loc[data["jahr"].isin(selected_years)].copy()
    reg_df = reg_df.dropna(subset=[x_col, "e_auto_quote"])

    if reg_df.empty:
        st.info("Keine Daten für die ausgewählten Jahre vorhanden.")
        return

    year_title = ", ".join(str(year) for year in selected_years)
    fig = px.scatter(
        reg_df,
        x=x_col,
        y="e_auto_quote",
        color="jahr" if len(selected_years) > 1 else None,
        hover_name="kreis_name",
        labels={x_col: x_label, "e_auto_quote": "E-Auto-Quote", "jahr": "Jahr"},
        title=f"E-Auto-Quote vs. {x_label} ({year_title})",
    )

    if show_ols:
        regression_stats = []
        for year, group in reg_df.groupby("jahr"):
            if len(group) < 2:
                continue
            x_vals = group[x_col].to_numpy()
            y_vals = group["e_auto_quote"].to_numpy()
            slope, intercept = np.polyfit(x_vals, y_vals, 1)
            line_x = np.linspace(x_vals.min(), x_vals.max(), 200)
            line_y = slope * line_x + intercept
            fig.add_trace(
                go.Scatter(
                    x=line_x,
                    y=line_y,
                    mode="lines",
                    name=f"OLS {year}",
                )
            )
            r_value = np.corrcoef(x_vals, y_vals)[0, 1]
            r_squared = r_value**2 if np.isfinite(r_value) else np.nan
            regression_stats.append(
                {
                    "Jahr": int(year),
                    "Steigung": slope,
                    "Achsenabschnitt": intercept,
                    "R²": r_squared,
                    "n": len(group),
                }
            )
        if regression_stats:
            stats_df = pd.DataFrame(regression_stats).sort_values("Jahr")
            st.dataframe(stats_df, use_container_width=True)
        else:
            st.caption("Zu wenige Datenpunkte für eine Regression in den gewählten Jahren.")

    st.plotly_chart(fig, use_container_width=True)


def render_correlation_explorer(data: pd.DataFrame, key_prefix: str) -> None:
    st.markdown("**Korrelationen & Variablenfilter**")
    corr_vars = [
        var
        for group, variables in VARIABLE_GROUPS.items()
        for var in variables
        if var in data.columns
    ]
    corr_labels = [
        VARIABLE_METADATA[var]["label"]
        for var in corr_vars
        if var in VARIABLE_METADATA
    ]
    if not corr_labels:
        st.warning("Keine Variablen im Datensatz gefunden.")
        return
    default_corr = []
    if "e_auto_quote" in corr_vars:
        default_corr = [VARIABLE_METADATA["e_auto_quote"]["label"]]
    elif corr_labels:
        default_corr = [corr_labels[0]]
    selected_labels = st.multiselect(
        "Variablen für Korrelationsmatrix",
        corr_labels,
        default=default_corr,
        key=f"{key_prefix}_corr_select",
    )
    if selected_labels:
        corr_cols = list(
            dict.fromkeys(
                [
                    var
                    for var in corr_vars
                    if VARIABLE_METADATA.get(var, {}).get("label") in selected_labels
                ]
            )
        )
        corr_df = data[corr_cols].corr()
        heatmap = px.imshow(
            corr_df,
            text_auto=".2f",
            color_continuous_scale="RdBu",
            zmin=-1,
            zmax=1,
            title="Korrelationsmatrix",
        )
        st.plotly_chart(heatmap, use_container_width=True)

        corr_input = list(dict.fromkeys([*corr_cols, "e_auto_quote"]))
        corr_with_target = (
            data[corr_input]
            .corr()["e_auto_quote"]
            .drop("e_auto_quote", errors="ignore")
            .reset_index()
            .rename(columns={"index": "Variable", "e_auto_quote": "Korrelation"})
        )
        st.dataframe(corr_with_target, use_container_width=True)
    else:
        st.info("Bitte mindestens eine Variable auswählen.")


def render_panel_table(data: pd.DataFrame) -> None:
    st.markdown("**Panel-Dataframe (Ausschnitt)**")
    bundesland_options = sorted(
        bundesland for bundesland in data["bundesland"].dropna().unique() if bundesland
    )
    selected_bundesland = st.selectbox(
        "Bundesland filtern",
        ["Alle"] + bundesland_options,
        key="panel_bundesland_filter",
    )
    filtered = data.copy()
    if selected_bundesland != "Alle":
        filtered = filtered.loc[filtered["bundesland"] == selected_bundesland]
    st.dataframe(filtered.head(20), use_container_width=True)
