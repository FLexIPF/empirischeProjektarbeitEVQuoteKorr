from __future__ import annotations

from typing import Dict, List, Tuple

import pandas as pd
import pydeck as pdk
import streamlit as st


def build_color_scale(values: pd.Series) -> Tuple[float, float]:
    valid = values.dropna()
    if valid.empty:
        return 0.0, 1.0
    return float(valid.min()), float(valid.max())


def value_to_color(
    value: float | None,
    vmin: float,
    vmax: float,
    start_color: List[int] | None = None,
    end_color: List[int] | None = None,
) -> List[int]:
    if value is None or pd.isna(value):
        return [210, 210, 210, 180]
    if vmax == vmin:
        return [33, 102, 172, 200]
    if start_color is None:
        start_color = [247, 251, 255]
    if end_color is None:
        end_color = [33, 102, 172]
    ratio = max(0.0, min(1.0, (value - vmin) / (vmax - vmin)))
    rgb = [
        int(start_color[i] + (end_color[i] - start_color[i]) * ratio)
        for i in range(3)
    ]
    return [*rgb, 200]


def value_to_diverging_color(
    value: float | None,
    vmin: float,
    vmax: float,
    neg_color: List[int] | None = None,
    pos_color: List[int] | None = None,
    neutral_color: List[int] | None = None,
) -> List[int]:
    if value is None or pd.isna(value):
        return [210, 210, 210, 180]
    if neg_color is None:
        neg_color = [37, 99, 235]
    if pos_color is None:
        pos_color = [239, 68, 68]
    if neutral_color is None:
        neutral_color = [241, 245, 249]
    if value >= 0:
        if vmax <= 0:
            return [*neutral_color, 200]
        ratio = max(0.0, min(1.0, value / vmax))
        rgb = [
            int(neutral_color[i] + (pos_color[i] - neutral_color[i]) * ratio)
            for i in range(3)
        ]
        return [*rgb, 200]
    if vmin >= 0:
        return [*neutral_color, 200]
    ratio = max(0.0, min(1.0, value / vmin))
    rgb = [
        int(neutral_color[i] + (neg_color[i] - neutral_color[i]) * ratio)
        for i in range(3)
    ]
    return [*rgb, 200]


def enrich_geojson(
    geojson: dict,
    values: Dict[str, float],
    vmin: float,
    vmax: float,
    value_key: str,
    color_range: Tuple[List[int], List[int]] | None = None,
    diverging: bool = False,
) -> Tuple[dict, List[str]]:
    missing = []
    start_color = None
    end_color = None
    if color_range:
        start_color, end_color = color_range
    for feature in geojson.get("features", []):
        props = feature.setdefault("properties", {})
        kreis_id = props.get("kreis_id")
        value = values.get(kreis_id)
        if kreis_id not in values:
            missing.append(kreis_id)
        props[value_key] = value
        if diverging:
            props["fill_color"] = value_to_diverging_color(
                value, vmin, vmax, start_color, end_color
            )
        else:
            props["fill_color"] = value_to_color(
                value, vmin, vmax, start_color, end_color
            )
    return geojson, missing


def geometry_centroid(geometry: dict) -> Tuple[float, float]:
    coords: List[Tuple[float, float]] = []
    if geometry["type"] == "Polygon":
        rings = geometry.get("coordinates", [])
        for ring in rings:
            coords.extend([(lon, lat) for lon, lat in ring])
    elif geometry["type"] == "MultiPolygon":
        for polygon in geometry.get("coordinates", []):
            for ring in polygon:
                coords.extend([(lon, lat) for lon, lat in ring])
    if not coords:
        return 10.4, 51.0
    lons, lats = zip(*coords)
    return sum(lons) / len(lons), sum(lats) / len(lats)


def render_map(
    geojson: dict,
    tooltip_label: str,
    value_key: str,
    extra_tooltip_label: str | None = None,
    extra_value_key: str | None = None,
    highlighted_kreis: dict | None = None,
) -> None:
    base_layer = pdk.Layer(
        "GeoJsonLayer",
        geojson,
        stroked=True,
        filled=True,
        get_fill_color="properties.fill_color",
        get_line_color=[180, 180, 180],
        line_width_min_pixels=0.5,
        pickable=True,
        auto_highlight=True,
    )

    view_state = pdk.ViewState(latitude=51.0, longitude=10.4, zoom=5.3)

    tooltip_lines = [
        "<b>{name}</b>",
        f"{tooltip_label}: {{{value_key}}}",
    ]
    if extra_tooltip_label and extra_value_key:
        tooltip_lines.append(f"{extra_tooltip_label}: {{{extra_value_key}}}")
    tooltip_lines.append("Bundesland: {state}")
    tooltip = {
        "html": "<br/>".join(tooltip_lines),
        "style": {"backgroundColor": "#1f1f1f", "color": "white"},
    }

    layers = [base_layer]
    if highlighted_kreis:
        layers.append(
            pdk.Layer(
                "TextLayer",
                [highlighted_kreis],
                get_position="position",
                get_text="name",
                get_color=[17, 94, 89],
                get_size=14,
                size_scale=2,
                size_min_pixels=10,
            )
        )
        layers.append(
            pdk.Layer(
                "ScatterplotLayer",
                [highlighted_kreis],
                get_position="position",
                get_radius=20000,
                get_fill_color=[13, 148, 136, 80],
                get_line_color=[13, 148, 136, 180],
                line_width_min_pixels=2,
            )
        )

    deck = pdk.Deck(layers=layers, initial_view_state=view_state, tooltip=tooltip)
    st.pydeck_chart(deck)
