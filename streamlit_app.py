# ============================================================
# ITD112 Laboratory Exercise 1
# Integrating Soil and Weather APIs
# ============================================================

import hashlib
import json
import time
from pathlib import Path
from datetime import date

import numpy as np
import pandas as pd
import requests
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ITD112 | Soil and Weather Integration",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       PAGE
       ====================================================== */

    .main {
        background-color: #ffffff;
    }

    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }


    /* ======================================================
       SIDEBAR
       ====================================================== */

    [data-testid="stSidebar"] {
        background-color: #f5f7f7;
        border-right: 1px solid #e1e6e6;
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #20292b;
        font-weight: 600;
    }


    /* ======================================================
       HEADINGS
       ====================================================== */

    h1 {
        color: #202729;
        font-weight: 650;
        letter-spacing: -0.8px;
        margin-bottom: 0.4rem;
    }

    h2 {
        color: #273537;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 0.8rem;
    }

    h3 {
        color: #344244;
        font-weight: 600;
    }


    /* ======================================================
       BODY TEXT
       ====================================================== */

    p {
        color: #4f5c5e;
        line-height: 1.65;
    }


    /* ======================================================
       PRIMARY BUTTON
       ====================================================== */

    .stButton > button {
        background-color: #176f78 !important;
        color: #ffffff !important;
        border: 1px solid #176f78 !important;
        border-radius: 7px;
        padding: 0.55rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }

    .stButton > button p {
        color: #ffffff !important;
    }

    .stButton > button span {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        background-color: #125c63 !important;
        border-color: #125c63 !important;
        color: #ffffff !important;
    }

    .stButton > button:hover p,
    .stButton > button:hover span {
        color: #ffffff !important;
    }


    /* ======================================================
       DOWNLOAD BUTTONS
       ====================================================== */

    .stDownloadButton > button {
        background-color: #ffffff !important;
        color: #176f78 !important;
        border: 1px solid #176f78 !important;
        border-radius: 7px;
        font-weight: 500;
    }

    .stDownloadButton > button p,
    .stDownloadButton > button span {
        color: #176f78 !important;
    }

    .stDownloadButton > button:hover {
        background-color: #f0f6f6 !important;
        border-color: #125c63 !important;
        color: #125c63 !important;
    }


    /* ======================================================
       INPUTS
       ====================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 7px;
    }

    div[data-baseweb="input"] > div {
        border-radius: 7px;
    }


    /* ======================================================
       METRICS
       ====================================================== */

    [data-testid="stMetric"] {
        background-color: #f7f9f9;
        border: 1px solid #e3e8e8;
        border-radius: 8px;
        padding: 14px;
    }


    /* ======================================================
       DATAFRAMES
       ====================================================== */

    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
    }


    /* ======================================================
       ALERTS
       ====================================================== */

    [data-testid="stAlert"] {
        border-radius: 8px;
    }


    /* ======================================================
       INFO CARDS
       ====================================================== */

    .info-card {
        background-color: #f6f8f8;
        border: 1px solid #e1e7e7;
        border-radius: 10px;
        padding: 1.2rem 1.3rem;
        height: 100%;
    }

    .info-card-title {
        color: #176f78;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .info-card-text {
        color: #536062;
        font-size: 0.92rem;
        line-height: 1.6;
    }


    /* ======================================================
       HERO SECTION
       ====================================================== */

    .hero {
        background-color: #f4f7f7;
        border: 1px solid #e0e6e6;
        border-radius: 12px;
        padding: 1.8rem 2rem;
        margin-top: 1.2rem;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        color: #176f78;
        font-size: 1.15rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .hero-text {
        color: #4f5c5e;
        font-size: 0.98rem;
        line-height: 1.7;
        margin-bottom: 0;
    }


    /* ======================================================
       WORKFLOW
       ====================================================== */

    .workflow-box {
        background-color: #ffffff;
        border: 1px solid #e2e7e7;
        border-radius: 9px;
        padding: 1rem;
        min-height: 150px;
    }

    .workflow-number {
        color: #176f78;
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }

    .workflow-title {
        color: #263234;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }

    .workflow-text {
        color: #657173;
        font-size: 0.85rem;
        line-height: 1.5;
    }


    /* ======================================================
       TABLE
       ====================================================== */

    .source-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 0.5rem;
    }

    .source-table th {
        text-align: left;
        padding: 0.7rem;
        background-color: #f4f7f7;
        border-bottom: 1px solid #dfe5e5;
        color: #354244;
        font-weight: 600;
    }

    .source-table td {
        padding: 0.7rem;
        border-bottom: 1px solid #e8ecec;
        color: #536062;
    }


    /* ======================================================
       DIVIDER
       ====================================================== */

    hr {
        border: none;
        border-top: 1px solid #e5e9e9;
        margin: 2rem 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# CONFIGURATION
# ============================================================

SITES = pd.DataFrame(
    [
        ("Iligan City", 8.200, 124.300),
        ("Malaybalay", 8.150, 125.130),
        ("Valencia", 7.900, 125.090),
        ("Davao (Calinan)", 7.190, 125.460),
        ("General Santos", 6.150, 125.150),
    ],
    columns=["site", "lat", "lon"],
)

SOIL_URL = (
    "https://rest.isric.org/"
    "soilgrids/v2.0/properties/query"
)

WEATHER_URL = (
    "https://archive-api.open-meteo.com/v1/archive"
)

SOIL_PROPERTIES = [
    "clay",
    "sand",
    "silt",
    "phh2o",
    "soc",
]

SOIL_DEPTH = "0-5cm"

SOIL_DEPTHS = [
    "0-5cm",
    "5-15cm",
    "15-30cm",
]

DAILY_VARS = [
    "temperature_2m_mean",
    "precipitation_sum",
    "et0_fao_evapotranspiration",
]

TIMEZONE = "Asia/Manila"

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

SOILGRIDS_PAUSE_S = 12

MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]


# ============================================================
# LANDING PAGE
# ============================================================

st.title("Integrating APIs: Soil and Weather Data")

st.write(
    "A Streamlit dashboard for combining soil properties "
    "from SoilGrids with historical weather data from "
    "Open-Meteo across selected sites in Mindanao."
)

st.divider()

# ------------------------------------------------------------
# About the application
# ------------------------------------------------------------

st.header("About the Application")

st.write(
    "This application demonstrates an API integration "
    "workflow using two public data services with different "
    "response structures. SoilGrids provides soil properties "
    "for selected coordinates, while Open-Meteo provides "
    "daily historical weather records for a selected period."
)

st.write(
    "The application retrieves, parses, and combines these "
    "datasets into a single analytical dataset. The results "
    "are then used to examine temperature, rainfall, "
    "evaporative demand, soil texture, water balance, and "
    "the relationship between soil and weather conditions."
)


# ------------------------------------------------------------
# Data sources
# ------------------------------------------------------------

st.header("Data Sources")

source1, source2 = st.columns(2)

with source1:

    st.subheader("SoilGrids 2.0")

    st.write(
        "SoilGrids provides the soil properties used in "
        "the analysis, including clay, sand, silt, soil "
        "pH, and soil organic carbon."
    )

    st.caption(
        "Source: ISRIC SoilGrids 2.0"
    )


with source2:

    st.subheader("Open-Meteo")

    st.write(
        "Open-Meteo provides the historical daily weather "
        "data used in the analysis, including temperature, "
        "precipitation, and reference ET0."
    )

    st.caption(
        "Source: Open-Meteo Historical Weather API"
    )


# ------------------------------------------------------------
# What the application produces
# ------------------------------------------------------------

st.header("Analysis")

analysis1, analysis2, analysis3 = st.columns(3)

with analysis1:

    st.subheader("Temperature")

    st.write(
        "Daily temperature trends with a "
        "7-day rolling mean."
    )


with analysis2:

    st.subheader("Rainfall and ET0")

    st.write(
        "Monthly rainfall compared with "
        "reference evaporative demand."
    )


with analysis3:

    st.subheader("Rainfall Variability")

    st.write(
        "Monthly distributions of daily rainfall."
    )


analysis4, analysis5, analysis6 = st.columns(3)

with analysis4:

    st.subheader("Soil Texture")

    st.write(
        "Relative proportions of sand, silt, "
        "and clay in the topsoil."
    )


with analysis5:

    st.subheader("Water Balance")

    st.write(
        "The difference between precipitation "
        "and reference ET0."
    )


with analysis6:

    st.subheader("Site Comparison")

    st.write(
        "A map comparing selected sites using "
        "soil organic carbon and rainfall."
    )


# ------------------------------------------------------------
# Integration workflow
# ------------------------------------------------------------

st.header("Integration Workflow")

st.write(
    "The application follows a simple data pipeline:"
)

workflow1, workflow2, workflow3, workflow4 = st.columns(4)

with workflow1:

    st.subheader("1. Input")

    st.write(
        "Select sites and a historical date range."
    )


with workflow2:

    st.subheader("2. Retrieve")

    st.write(
        "Request soil and weather data from "
        "the two APIs."
    )


with workflow3:

    st.subheader("3. Integrate")

    st.write(
        "Join the soil properties with the "
        "daily weather records."
    )


with workflow4:

    st.subheader("4. Analyse")

    st.write(
        "Generate charts, review the data, "
        "and export CSV files."
    )


# ------------------------------------------------------------
# Optional challenge
# ------------------------------------------------------------

st.header("Optional Extension")

st.write(
    "The application also includes an optional soil-depth "
    "analysis. It retrieves SoilGrids data for 0–5 cm, "
    "5–15 cm, and 15–30 cm and compares how soil texture "
    "changes through the profile."
)


# ------------------------------------------------------------
# Getting started
# ------------------------------------------------------------

st.info(
    "Select your sites and date range in the sidebar, "
    "then click Run the integration to begin."
)


# ============================================================
# REQUEST BUILDING
# ============================================================

def full_url(url, params):

    return requests.Request(
        "GET",
        url,
        params=params,
    ).prepare().url


def build_weather_request(
    sites,
    start,
    end,
):

    params = {
        "latitude": ",".join(
            str(v)
            for v in sites["lat"]
        ),
        "longitude": ",".join(
            str(v)
            for v in sites["lon"]
        ),
        "start_date": start,
        "end_date": end,
        "daily": ",".join(
            DAILY_VARS
        ),
        "timezone": TIMEZONE,
    }

    return {
        "api": "Open-Meteo",
        "label": "All selected sites",
        "url": WEATHER_URL,
        "params": params,
        "full_url": full_url(
            WEATHER_URL,
            params,
        ),
    }


def build_soil_request(
    site,
    lat,
    lon,
    depth=SOIL_DEPTH,
):

    params = [
        ("lat", lat),
        ("lon", lon),
        ("depth", depth),
        ("value", "mean"),
    ]

    params += [
        ("property", prop)
        for prop in SOIL_PROPERTIES
    ]

    return {
        "api": "SoilGrids",
        "label": site,
        "depth": depth,
        "url": SOIL_URL,
        "params": params,
        "full_url": full_url(
            SOIL_URL,
            params,
        ),
    }


# ============================================================
# HTTP SESSION
# ============================================================

@st.cache_resource
def http_session():

    retry = Retry(
        total=3,
        backoff_factor=2,
        status_forcelist=(
            429,
            500,
            502,
            503,
            504,
        ),
        allowed_methods=("GET",),
    )

    session = requests.Session()

    session.mount(
        "https://",
        HTTPAdapter(
            max_retries=retry
        ),
    )

    session.headers[
        "User-Agent"
    ] = "itd112-lab1/1.0"

    return session


def send(req):

    key = hashlib.sha1(
        (
            req["url"]
            + json.dumps(
                req["params"],
                sort_keys=True,
                default=str,
            )
        ).encode()
    ).hexdigest()

    path = CACHE_DIR / f"{key}.json"


    if path.exists():

        text = path.read_text(
            encoding="utf-8"
        )

        return {
            "status": None,
            "from_cache": True,
            "data": json.loads(text),
            "elapsed": 0,
            "size": len(text),
        }


    start_time = time.time()

    response = http_session().get(
        req["url"],
        params=req["params"],
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    elapsed = (
        time.time()
        - start_time
    )

    path.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    return {
        "status": response.status_code,
        "from_cache": False,
        "data": data,
        "elapsed": elapsed,
        "size": len(response.content),
    }


# ============================================================
# PARSING
# ============================================================

def parse_weather(
    data,
    sites,
):

    results = (
        data
        if isinstance(data, list)
        else [data]
    )

    frames = []

    for site, result in zip(
        sites["site"],
        results,
    ):

        daily = result.get(
            "daily",
            {},
        )

        df = pd.DataFrame(
            daily
        )

        df.insert(
            0,
            "site",
            site,
        )

        frames.append(df)

    if not frames:

        return pd.DataFrame()

    return pd.concat(
        frames,
        ignore_index=True,
    )


def parse_soil(
    data,
    site,
):

    rows = []

    layers = (
        data
        .get("properties", {})
        .get("layers", [])
    )

    for layer in layers:

        prop = layer.get(
            "name"
        )

        if prop not in SOIL_PROPERTIES:
            continue

        depths = layer.get(
            "depths",
            []
        )

        if not depths:
            continue

        depth_data = depths[0]

        raw_mean = (
            depth_data
            .get("values", {})
            .get("mean")
        )

        unit = layer.get(
            "unit_measure",
            {}
        )

        d_factor = unit.get(
            "d_factor",
            1,
        )

        if raw_mean is None:

            value = np.nan

        else:

            try:

                value = (
                    float(raw_mean)
                    / float(d_factor)
                )

            except (
                TypeError,
                ValueError,
                ZeroDivisionError,
            ):

                value = np.nan

        rows.append(
            {
                "site": site,
                "property": prop,
                "raw_mean": raw_mean,
                "mapped_units":
                    unit.get(
                        "mapped_units"
                    ),
                "d_factor": d_factor,
                "value": value,
                "target_units":
                    unit.get(
                        "target_units"
                    ),
            }
        )

    return pd.DataFrame(
        rows
    )


def soil_table(
    soil_long,
    sites,
):

    if soil_long.empty:

        return sites.copy()

    wide = (
        soil_long
        .pivot(
            index="site",
            columns="property",
            values="value",
        )
        .reindex(
            columns=SOIL_PROPERTIES
        )
        .reset_index()
    )

    wide.columns.name = None

    return sites.merge(
        wide,
        on="site",
        how="left",
    )


# ============================================================
# OPTIONAL DEPTH PARSING
# ============================================================

def parse_soil_depths(
    data,
    site,
    requested_depth,
):

    rows = []

    layers = (
        data
        .get("properties", {})
        .get("layers", [])
    )

    for layer in layers:

        prop = layer.get(
            "name"
        )

        if prop not in SOIL_PROPERTIES:
            continue

        unit = layer.get(
            "unit_measure",
            {}
        )

        d_factor = unit.get(
            "d_factor",
            1,
        )

        for depth_data in layer.get(
            "depths",
            []
        ):

            depth_label = depth_data.get(
                "label",
                requested_depth,
            )

            if depth_label != requested_depth:
                continue

            raw_mean = (
                depth_data
                .get("values", {})
                .get("mean")
            )

            if raw_mean is None:

                value = np.nan

            else:

                try:

                    value = (
                        float(raw_mean)
                        / float(d_factor)
                    )

                except (
                    TypeError,
                    ValueError,
                    ZeroDivisionError,
                ):

                    value = np.nan

            rows.append(
                {
                    "site": site,
                    "depth": depth_label,
                    "property": prop,
                    "raw_mean": raw_mean,
                    "mapped_units":
                        unit.get(
                            "mapped_units"
                        ),
                    "d_factor": d_factor,
                    "value": value,
                    "target_units":
                        unit.get(
                            "target_units"
                        ),
                }
            )

    return pd.DataFrame(
        rows
    )


def fetch_soil_depths(
    sites
):

    all_rows = []

    total_requests = (
        len(sites)
        * len(SOIL_DEPTHS)
    )

    request_number = 0

    for _, site_row in sites.iterrows():

        site = site_row["site"]
        lat = site_row["lat"]
        lon = site_row["lon"]

        for depth in SOIL_DEPTHS:

            request_number += 1

            req = build_soil_request(
                site,
                lat,
                lon,
                depth,
            )

            st.write(
                f"Fetching SoilGrids: "
                f"{site} — {depth} "
                f"({request_number}/"
                f"{total_requests})"
            )

            try:

                result = send(req)

            except requests.RequestException as exc:

                st.error(
                    f"SoilGrids failed for "
                    f"{site} ({depth}): "
                    f"{exc}"
                )

                continue

            parsed = parse_soil_depths(
                result["data"],
                site,
                depth,
            )

            if not parsed.empty:

                all_rows.append(
                    parsed
                )

            if (
                request_number
                < total_requests
                and not result[
                    "from_cache"
                ]
            ):

                time.sleep(
                    SOILGRIDS_PAUSE_S
                )

    if not all_rows:

        return pd.DataFrame()

    return pd.concat(
        all_rows,
        ignore_index=True,
    )


# ============================================================
# INTEGRATION
# ============================================================

def integrate(
    weather,
    soil,
):

    daily = weather.merge(
        soil,
        on="site",
        how="left",
    )

    daily["time"] = pd.to_datetime(
        daily["time"]
    )

    daily["month"] = (
        daily["time"]
        .dt.month
    )

    daily[
        "water_balance_mm"
    ] = (
        daily["precipitation_sum"]
        - daily[
            "et0_fao_evapotranspiration"
        ]
    )

    summary = (
        daily
        .groupby(
            "site",
            sort=False,
        )
        .agg(
            rain_mm=(
                "precipitation_sum",
                "sum",
            ),
            et0_mm=(
                "et0_fao_evapotranspiration",
                "sum",
            ),
            water_balance_mm=(
                "water_balance_mm",
                "sum",
            ),
            temp_mean_c=(
                "temperature_2m_mean",
                "mean",
            ),
        )
        .reset_index()
        .merge(
            soil,
            on="site",
            how="left",
        )
    )

    return daily, summary


# ============================================================
# CHARTS
# ============================================================

def chart_q1(
    daily,
    site,
):

    df = (
        daily[
            daily["site"] == site
        ]
        .copy()
        .sort_values("time")
    )

    df["rolling_7d"] = (
        df[
            "temperature_2m_mean"
        ]
        .rolling(
            7,
            min_periods=1,
        )
        .mean()
    )

    fig = go.Figure()

    fig.add_scatter(
        x=df["time"],
        y=df[
            "temperature_2m_mean"
        ],
        mode="lines",
        name="Daily mean temperature",
    )

    fig.add_scatter(
        x=df["time"],
        y=df["rolling_7d"],
        mode="lines",
        name="7-day rolling mean",
        line=dict(width=3),
    )

    fig.update_layout(
        title=(
            f"Temperature Over Time — "
            f"{site}"
        ),
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        hovermode="x unified",
    )

    return fig


def chart_q2(
    daily,
    site,
):

    df = daily[
        daily["site"] == site
    ].copy()

    monthly = (
        df
        .groupby("month")
        [
            [
                "precipitation_sum",
                "et0_fao_evapotranspiration",
            ]
        ]
        .sum()
        .reindex(
            range(1, 13),
            fill_value=0,
        )
    )

    fig = go.Figure()

    fig.add_bar(
        x=MONTHS,
        y=monthly[
            "precipitation_sum"
        ],
        name="Rainfall",
    )

    fig.add_scatter(
        x=MONTHS,
        y=monthly[
            "et0_fao_evapotranspiration"
        ],
        name="Reference ET0",
        mode="lines+markers",
        line=dict(width=3),
    )

    fig.update_layout(
        title=(
            f"Rainfall vs Evaporative Demand — "
            f"{site}"
        ),
        xaxis_title="Month",
        yaxis_title="mm per month",
        yaxis=dict(
            rangemode="tozero"
        ),
        hovermode="x unified",
    )

    return fig


def chart_q3(
    daily,
    site,
):

    df = daily[
        daily["site"] == site
    ].copy()

    df["month_number"] = (
        pd.to_datetime(
            df["time"]
        ).dt.month
    )

    df["month_name"] = (
        pd.to_datetime(
            df["time"]
        ).dt.strftime("%b")
    )

    df = df.sort_values(
        "month_number"
    )

    return px.box(
        df,
        x="month_name",
        y="precipitation_sum",
        category_orders={
            "month_name": MONTHS
        },
        points="outliers",
        title=(
            f"Daily Rainfall Variability — "
            f"{site}"
        ),
        labels={
            "month_name": "Month",
            "precipitation_sum":
                "Daily rainfall (mm)",
        },
    )


def chart_q4(
    summary
):

    texture = (
        summary
        .set_index("site")
        [
            [
                "sand",
                "silt",
                "clay",
            ]
        ]
        .dropna()
    )

    if texture.empty:
        return None

    texture = (
        texture
        .div(
            texture.sum(
                axis=1
            ),
            axis=0,
        )
        .mul(100)
    )

    texture = texture.sort_values(
        "clay"
    )

    fig = go.Figure()

    for prop in [
        "sand",
        "silt",
        "clay",
    ]:

        fig.add_bar(
            x=texture.index,
            y=texture[prop],
            name=prop.capitalize(),
        )

    fig.update_layout(
        barmode="stack",
        title="Topsoil Texture (0–5 cm)",
        xaxis_title="Site",
        yaxis_title="Texture (%)",
        yaxis=dict(
            range=[0, 100]
        ),
    )

    return fig


def chart_q5(
    summary
):

    df = summary.dropna(
        subset=[
            "clay",
            "soc",
            "water_balance_mm",
        ]
    ).copy()

    if df.empty:
        return None

    fig = go.Figure()

    max_soc = df["soc"].max()

    if (
        pd.isna(max_soc)
        or max_soc <= 0
    ):

        sizes = np.full(
            len(df),
            20,
        )

    else:

        sizes = (
            14
            + 26
            * df["soc"]
            / max_soc
        )

    fig.add_scatter(
        x=df["clay"],
        y=df["water_balance_mm"],
        mode="markers+text",
        text=df["site"],
        textposition="top center",
        marker=dict(
            size=sizes,
            opacity=0.8,
        ),
        name="Sites",
        hovertemplate=(
            "<b>%{text}</b><br>"
            "Clay: %{x:.2f}%<br>"
            "Water balance: %{y:.2f} mm"
            "<extra></extra>"
        ),
    )

    if len(df) >= 5:

        x = df["clay"].to_numpy()
        y = (
            df[
                "water_balance_mm"
            ]
            .to_numpy()
        )

        if np.std(x) > 0:

            slope, intercept = np.polyfit(
                x,
                y,
                1,
            )

            r = np.corrcoef(
                x,
                y,
            )[0, 1]

            xs = np.linspace(
                x.min(),
                x.max(),
                100,
            )

            fig.add_scatter(
                x=xs,
                y=slope * xs
                + intercept,
                mode="lines",
                name=(
                    f"Linear fit "
                    f"(r = {r:.2f}, "
                    f"n = {len(df)})"
                ),
            )

    fig.add_hline(
        y=0,
        annotation_text="rainfall = ET0",
    )

    fig.update_layout(
        title="Soil vs Water Stress",
        xaxis_title="Clay (%)",
        yaxis_title="Water balance (mm)",
    )

    return fig


def chart_q6(
    summary
):

    df = summary.dropna(
        subset=[
            "lat",
            "lon",
            "soc",
            "rain_mm",
        ]
    ).copy()

    if df.empty:
        return None

    try:

        fig = px.scatter_map(
            df,
            lat="lat",
            lon="lon",
            color="soc",
            size="rain_mm",
            hover_name="site",
            zoom=5,
            height=550,
            title=(
                "Mindanao Sites — "
                "SOC and Rainfall"
            ),
            labels={
                "soc": "SOC",
                "rain_mm":
                    "Rainfall (mm)",
            },
        )

    except AttributeError:

        fig = px.scatter_mapbox(
            df,
            lat="lat",
            lon="lon",
            color="soc",
            size="rain_mm",
            hover_name="site",
            zoom=5,
            height=550,
            title=(
                "Mindanao Sites — "
                "SOC and Rainfall"
            ),
        )

        fig.update_layout(
            mapbox_style="open-street-map"
        )

    return fig


def chart_depth_texture(
    soil_depth,
    selected_site,
):

    df = soil_depth[
        soil_depth["site"]
        == selected_site
    ].copy()

    if df.empty:

        st.warning(
            f"No depth data available "
            f"for {selected_site}."
        )

        return

    texture = df[
        df["property"].isin(
            [
                "sand",
                "silt",
                "clay",
            ]
        )
    ].copy()

    if texture.empty:

        st.warning(
            "No sand, silt, or clay "
            "data were returned."
        )

        return

    wide = (
        texture
        .pivot_table(
            index="depth",
            columns="property",
            values="value",
            aggfunc="first",
        )
        .reset_index()
    )

    for prop in [
        "sand",
        "silt",
        "clay",
    ]:

        if prop not in wide.columns:

            wide[prop] = np.nan

    total = (
        wide["sand"].fillna(0)
        + wide["silt"].fillna(0)
        + wide["clay"].fillna(0)
    )

    valid = total > 0

    for prop in [
        "sand",
        "silt",
        "clay",
    ]:

        wide.loc[
            valid,
            prop,
        ] = (
            wide.loc[
                valid,
                prop,
            ].fillna(0)
            / total[valid]
            * 100
        )

    depth_order = {
        "0-5cm": 0,
        "5-15cm": 1,
        "15-30cm": 2,
    }

    wide["depth_order"] = (
        wide["depth"]
        .map(depth_order)
        .fillna(99)
    )

    wide = wide.sort_values(
        "depth_order"
    )

    chart_data = wide[
        [
            "depth",
            "sand",
            "silt",
            "clay",
        ]
    ].melt(
        id_vars="depth",
        var_name="texture",
        value_name="percentage",
    )

    fig = px.bar(
        chart_data,
        x="depth",
        y="percentage",
        color="texture",
        text_auto=".1f",
        title=(
            f"Soil Texture by Depth — "
            f"{selected_site}"
        ),
        labels={
            "depth": "Soil depth",
            "percentage": "Texture (%)",
            "texture": "Texture",
        },
    )

    fig.update_layout(
        barmode="stack",
        yaxis=dict(
            range=[0, 100]
        ),
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )


# ============================================================
# SIDEBAR INPUTS
# ============================================================

st.sidebar.header(
    "Inputs"
)

chosen = st.sidebar.multiselect(
    "Sites",
    SITES["site"].tolist(),
    default=SITES[
        "site"
    ].tolist()[:3],
)

start = st.sidebar.date_input(
    "Start date",
    date(2025, 1, 1),
)

end = st.sidebar.date_input(
    "End date",
    date(2025, 12, 31),
)

sites = SITES[
    SITES["site"].isin(
        chosen
    )
].reset_index(drop=True)


fetch = st.sidebar.button(
    "Run the integration",
    type="primary",
)


# ============================================================
# RUN PIPELINE
# ============================================================

if fetch:

    if sites.empty:

        st.error(
            "Please select at least one site."
        )

        st.stop()

    if start > end:

        st.error(
            "Start date must be on or "
            "before the end date."
        )

        st.stop()


    # ========================================================
    # BUILD THE REQUESTS
    # ========================================================

    st.header(
        "Build the Requests"
    )

    weather_req = build_weather_request(
        sites,
        str(start),
        str(end),
    )

    soil_reqs = [
        build_soil_request(
            row["site"],
            row["lat"],
            row["lon"],
            SOIL_DEPTH,
        )
        for _, row
        in sites.iterrows()
    ]


    with st.expander(
        "Open-Meteo request",
        expanded=False,
    ):

        st.code(
            weather_req["full_url"],
            language="text",
        )


    with st.expander(
        "SoilGrids requests",
        expanded=False,
    ):

        for req in soil_reqs:

            st.caption(
                req["label"]
            )

            st.code(
                req["full_url"],
                language="text",
            )


    # ========================================================
    # SEND THE REQUESTS
    # ========================================================

    st.header(
        "Send the Requests"
    )

    response_log = []


    # Open-Meteo

    try:

        weather_result = send(
            weather_req
        )

        response_log.append(
            {
                "API": "Open-Meteo",
                "Site": "All selected sites",
                "Depth": "",
                "Status":
                    weather_result.get(
                        "status"
                    ),
                "Cache":
                    (
                        "Saved copy"
                        if weather_result[
                            "from_cache"
                        ]
                        else "Fresh request"
                    ),
                "Time (s)":
                    round(
                        weather_result.get(
                            "elapsed",
                            0,
                        ),
                        3,
                    ),
            }
        )

    except requests.RequestException as exc:

        st.error(
            f"Open-Meteo request failed: "
            f"{exc}"
        )

        st.stop()


    # SoilGrids

    soil_results = []

    progress = st.progress(0)

    for i, req in enumerate(
        soil_reqs
    ):

        try:

            result = send(req)

            soil_results.append(
                result
            )

            response_log.append(
                {
                    "API": "SoilGrids",
                    "Site": req["label"],
                    "Depth": SOIL_DEPTH,
                    "Status":
                        result.get(
                            "status"
                        ),
                    "Cache":
                        (
                            "Saved copy"
                            if result[
                                "from_cache"
                            ]
                            else "Fresh request"
                        ),
                    "Time (s)":
                        round(
                            result.get(
                                "elapsed",
                                0,
                            ),
                            3,
                        ),
                }
            )

        except requests.RequestException as exc:

            st.error(
                f"SoilGrids failed for "
                f"{req['label']}: {exc}"
            )

            soil_results.append(
                None
            )

        progress.progress(
            (i + 1)
            / len(soil_reqs)
        )

        if (
            i < len(soil_reqs) - 1
            and soil_results[-1]
            is not None
            and not soil_results[-1][
                "from_cache"
            ]
        ):

            time.sleep(
                SOILGRIDS_PAUSE_S
            )

    progress.empty()


    st.subheader(
        "Response Log"
    )

    st.dataframe(
        pd.DataFrame(
            response_log
        ),
        use_container_width=True,
        hide_index=True,
    )


    # ========================================================
    # PARSE THE JSON
    # ========================================================

    st.header(
        "Parse the JSON"
    )

    weather = parse_weather(
        weather_result["data"],
        sites,
    )


    soil_frames = []

    for req, result in zip(
        soil_reqs,
        soil_results,
    ):

        if result is None:
            continue

        parsed = parse_soil(
            result["data"],
            req["label"],
        )

        if not parsed.empty:

            soil_frames.append(
                parsed
            )


    if soil_frames:

        soil_long = pd.concat(
            soil_frames,
            ignore_index=True,
        )

    else:

        soil_long = pd.DataFrame()


    soil = soil_table(
        soil_long,
        sites,
    )


    st.subheader(
        "SoilGrids Conversion Audit"
    )

    if not soil_long.empty:

        st.dataframe(
            soil_long,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.warning(
            "No SoilGrids data were returned."
        )


    st.subheader(
        "Soil Table"
    )

    st.dataframe(
        soil,
        use_container_width=True,
        hide_index=True,
    )


    if "clay" in soil.columns:

        missing = soil.loc[
            soil["clay"].isna(),
            "site",
        ].tolist()

        if missing:

            st.warning(
                "SoilGrids returned null for: "
                + ", ".join(missing)
                + ". The coordinate may fall "
                  "over water, a built-up area, "
                  "or a gap in the soil map."
            )


    # ========================================================
    # INTEGRATE THE TWO SOURCES
    # ========================================================

    st.header(
        "Integrate the Two Sources"
    )

    if weather.empty:

        st.error(
            "No weather data were returned."
        )

        st.stop()


    daily, summary = integrate(
        weather,
        soil,
    )


    st.session_state[
        "daily"
    ] = daily

    st.session_state[
        "summary"
    ] = summary

    st.session_state[
        "soil"
    ] = soil


    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Weather rows",
        len(weather),
    )

    metric2.metric(
        "Integrated rows",
        len(daily),
    )

    metric3.metric(
        "Sites",
        len(summary),
    )


# ============================================================
# DISPLAY RESULTS AFTER RUN
# ============================================================

if (
    "daily" in st.session_state
    and "summary" in st.session_state
):

    daily = st.session_state[
        "daily"
    ]

    summary = st.session_state[
        "summary"
    ]


    # ========================================================
    # ANALYSIS
    # ========================================================

    st.header(
        "Analysis"
    )


    # --------------------------------------------------------
    # Q1
    # --------------------------------------------------------

    st.subheader(
        "How does temperature change over time?"
    )

    q1_site = st.selectbox(
        "Select a site",
        summary["site"].tolist(),
        key="q1_site",
    )

    st.plotly_chart(
        chart_q1(
            daily,
            q1_site,
        ),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # Q2
    # --------------------------------------------------------

    st.subheader(
        "Does rainfall meet evaporative demand?"
    )

    q2_site = st.selectbox(
        "Select a site",
        summary["site"].tolist(),
        key="q2_site",
    )

    st.plotly_chart(
        chart_q2(
            daily,
            q2_site,
        ),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # Q3
    # --------------------------------------------------------

    st.subheader(
        "How variable is daily rainfall?"
    )

    q3_site = st.selectbox(
        "Select a site",
        summary["site"].tolist(),
        key="q3_site",
    )

    st.plotly_chart(
        chart_q3(
            daily,
            q3_site,
        ),
        use_container_width=True,
    )


    # --------------------------------------------------------
    # Q4
    # --------------------------------------------------------

    st.subheader(
        "What is the topsoil texture at each site?"
    )

    fig_q4 = chart_q4(
        summary
    )

    if fig_q4 is not None:

        st.plotly_chart(
            fig_q4,
            use_container_width=True,
        )

    else:

        st.warning(
            "Not enough soil data for this analysis."
        )


    # --------------------------------------------------------
    # Q5
    # --------------------------------------------------------

    st.subheader(
        "Does soil moderate water stress?"
    )

    fig_q5 = chart_q5(
        summary
    )

    if fig_q5 is not None:

        st.plotly_chart(
            fig_q5,
            use_container_width=True,
        )

    else:

        st.warning(
            "Not enough complete soil and "
            "weather data for this analysis."
        )


    # --------------------------------------------------------
    # Q6
    # --------------------------------------------------------

    st.subheader(
        "Where are the sites, and how do they differ?"
    )

    fig_q6 = chart_q6(
        summary
    )

    if fig_q6 is not None:

        st.plotly_chart(
            fig_q6,
            use_container_width=True,
        )

    else:

        st.warning(
            "Not enough complete data for the map."
        )


    # ========================================================
    # OPTIONAL CHALLENGE
    # ========================================================

    st.divider()

    st.header(
        "Optional Challenge — Soil Texture by Depth"
    )

    st.write(
        "This extension retrieves SoilGrids data at "
        "0–5 cm, 5–15 cm, and 15–30 cm and compares "
        "the relative texture composition through the "
        "soil profile."
    )


    depth_site = st.selectbox(
        "Select a site",
        summary["site"].tolist(),
        key="depth_site",
    )


    if st.button(
        "Fetch Soil Depth Profile",
        key="fetch_depth",
    ):

        st.info(
            "The first uncached run may take several "
            "minutes because SoilGrids requests are "
            "intentionally spaced out."
        )

        with st.spinner(
            "Fetching SoilGrids depth data..."
        ):

            soil_depth = fetch_soil_depths(
                sites
            )


        if soil_depth.empty:

            st.error(
                "No SoilGrids depth data were returned."
            )

        else:

            st.session_state[
                "soil_depth"
            ] = soil_depth

            st.success(
                "Soil depth profile retrieved successfully."
            )


    if (
        "soil_depth"
        in st.session_state
    ):

        soil_depth = st.session_state[
            "soil_depth"
        ]

        st.subheader(
            "Depth Profile Data"
        )

        st.dataframe(
            soil_depth,
            use_container_width=True,
            hide_index=True,
        )

        st.subheader(
            "Texture Changes with Depth"
        )

        chart_depth_texture(
            soil_depth,
            depth_site,
        )


    # ========================================================
    # EXPORT
    # ========================================================

    st.divider()

    st.header(
        "Export"
    )

    st.write(
        "Download the integrated results for "
        "further analysis or inclusion in your report."
    )


    # Summary export

    summary_export = summary.copy()

    summary_numeric = (
        summary_export
        .select_dtypes(
            include=np.number
        )
        .columns
    )

    summary_export[
        summary_numeric
    ] = (
        summary_export[
            summary_numeric
        ].round(2)
    )


    # Daily export

    daily_export = daily.drop(
        columns=["month"],
        errors="ignore",
    ).copy()


    # Clean date format

    daily_export["time"] = (
        pd.to_datetime(
            daily_export["time"]
        )
        .dt.strftime(
            "%Y-%m-%d"
        )
    )


    # Round numbers

    daily_numeric = (
        daily_export
        .select_dtypes(
            include=np.number
        )
        .columns
    )

    daily_export[
        daily_numeric
    ] = (
        daily_export[
            daily_numeric
        ].round(2)
    )


    export_col1, export_col2 = st.columns(2)


    with export_col1:

        st.download_button(
            "Download Site Summary CSV",
            summary_export.to_csv(
                index=False
            ),
            "site_summary.csv",
            "text/csv",
            use_container_width=True,
        )


    with export_col2:

        st.download_button(
            "Download Integrated Daily CSV",
            daily_export.to_csv(
                index=False
            ),
            "integrated_daily.csv",
            "text/csv",
            use_container_width=True,
        )


    