from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "eV-Quote_korAnalyse"

GEOJSON_PATH = DATA_DIR / "counties.json"
PKW_PATH = DATA_DIR / "Pkw.csv"
VGR_PATH = DATA_DIR / "rawDEmNums_df.csv"
BEV_TOTAL_PATH = DATA_DIR / "bevTotal.csv"
BEV_KOHORTEN_PATH = DATA_DIR / "raw_bev_kohorten_2024.csv"
DATASET_ANALYSE_PATH = DATA_DIR / "datasetAnaylse.csv"

YEAR_RANGE = (2020, 2023)


@st.cache_data
def load_geojson() -> dict:
    with GEOJSON_PATH.open(encoding="utf-8") as fh:
        data = json.load(fh)
    for feature in data.get("features", []):
        if "properties" not in feature:
            feature["properties"] = {}
        feature["properties"]["kreis_id"] = str(feature.get("id", "")).zfill(5)
    return data


@st.cache_data
def load_pkw_data() -> pd.DataFrame:
    df = pd.read_csv(PKW_PATH, dtype={"kreis_id": str})
    df["kreis_id"] = df["kreis_id"].astype(str).str.strip().str.zfill(5)
    df["jahr"] = pd.to_datetime(df["stichtag"], errors="coerce").dt.year
    df["pkw_elektrisch"] = pd.to_numeric(df["pkw_elektrisch"], errors="coerce")
    df["pkw_gesamt"] = pd.to_numeric(df["pkw_gesamt"], errors="coerce")
    df["e_auto_quote"] = df["pkw_elektrisch"] / df["pkw_gesamt"]
    df = df.loc[df["jahr"].between(*YEAR_RANGE)].copy()
    return df


@st.cache_data
def load_vgr_data() -> pd.DataFrame:
    df = pd.read_csv(VGR_PATH, sep=";", dtype={"kreis_id": str})
    df["kreis_id"] = df["kreis_id"].astype(str).str.strip().str.zfill(5)
    df["jahr"] = pd.to_numeric(df["jahr"], errors="coerce").astype("Int64")
    for col in df.columns:
        if col not in ["kreis_id", "jahr"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df.loc[
        df[
            "Arbeitnehmerinnen_und_Arbeitnehmer_insgesamt_in_1000_Personen"
        ]
        == 0,
        "Arbeitnehmerinnen_und_Arbeitnehmer_insgesamt_in_1000_Personen",
    ] = pd.NA
    df = df.loc[df["jahr"].between(*YEAR_RANGE)].copy()
    return df


@st.cache_data
def load_bev_total_data() -> pd.DataFrame:
    df = pd.read_csv(BEV_TOTAL_PATH, dtype={"kreis_id": str})
    df["kreis_id"] = df["kreis_id"].astype(str).str.strip().str.zfill(5)
    df["jahr"] = pd.to_numeric(df["jahr"], errors="coerce").astype("Int64")
    df["bev_total"] = pd.to_numeric(df["bev_total"], errors="coerce")
    df = df.loc[df["jahr"].between(*YEAR_RANGE)].copy()
    return df


@st.cache_data
def load_bev_kohorten_data() -> pd.DataFrame:
    df = pd.read_csv(BEV_KOHORTEN_PATH, sep=";", dtype={"kreis_id": str})
    df["kreis_id"] = df["kreis_id"].astype(str).str.strip().str.zfill(5)
    for col in df.columns:
        if col not in ["kreis_id", "kreis_name"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    df["anteil_18_35"] = df["bev_18_35"] / df["bev_total_2024"]
    df["anteil_65_plus"] = df["bev_65_plus"] / df["bev_total_2024"]
    return df


@st.cache_data
def build_panel_data() -> pd.DataFrame:
    geojson = load_geojson()
    if not DATASET_ANALYSE_PATH.exists():
        raise FileNotFoundError(
            "Die Datei datasetanalyse.csv fehlt im Verzeichnis eV-Quote_korAnalyse."
        )

    panel = pd.read_csv(
        DATASET_ANALYSE_PATH, sep=None, engine="python", dtype={"kreis_id": str}
    )
    panel["kreis_id"] = panel["kreis_id"].astype(str).str.strip().str.zfill(5)
    if "jahr" in panel.columns:
        panel["jahr"] = pd.to_numeric(panel["jahr"], errors="coerce").astype("Int64")
        panel = panel.loc[panel["jahr"].between(*YEAR_RANGE)].copy()

    bundesland_lookup = {
        feature["properties"].get("kreis_id"): feature["properties"].get("state")
        for feature in geojson.get("features", [])
    }
    kreis_lookup = {
        feature["properties"].get("kreis_id"): feature["properties"].get("name")
        for feature in geojson.get("features", [])
    }
    if "kreis_name" not in panel.columns:
        panel["kreis_name"] = panel["kreis_id"].map(kreis_lookup)
    else:
        panel["kreis_name"] = panel["kreis_name"].fillna(panel["kreis_id"])
    if "bundesland" not in panel.columns:
        panel["bundesland"] = panel["kreis_id"].map(bundesland_lookup)
    return panel
