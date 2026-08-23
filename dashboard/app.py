"""
Bird Species Observation Analysis — Interactive Streamlit Dashboard
Run with: streamlit run app.py
"""
import pandas as pd
import plotly.express as px
import plotly.io as pio
import streamlit as st
from pathlib import Path

st.set_page_config(page_title="Bird Species Observation Analysis",
                    page_icon="🐦", layout="wide")

DATA_PATH = Path(__file__).parent.parent / "data" / "bird_observations_clean.csv"

# ============================================================
# THEME — dark / professional / coral accent / 3D motion
# ============================================================
BG = "#0B0C10"
PANEL = "#16171D"
BORDER = "#2A2C35"
CORAL = "#F1614F"
NAVY = "#F3F4F8"
TEXT = "#E7E8EE"
MUTED = "#9497A6"
BLUE = "#5B85FF"

PLOTLY_TEMPLATE = "plotly_dark"
CHART_COLORWAY = [CORAL, BLUE, "#2FD1A8", "#F2C158", "#A88AF0", "#4FC3E0"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, [class*="css"] {{
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}}

/* ---------- Perspective stage so children can rotate in 3D ---------- */
.stApp {{
    background:
        radial-gradient(1200px 600px at 8% -10%, rgba(241,97,79,0.10) 0%, transparent 55%),
        radial-gradient(1000px 500px at 105% 0%, rgba(91,133,255,0.10) 0%, transparent 55%),
        {BG};
}}
[data-testid="stAppViewContainer"] > .main {{
    perspective: 1400px;
}}

section[data-testid="stSidebar"] {{
    background-color: {PANEL};
    border-right: 1px solid {BORDER};
}}

h1, h2, h3 {{ color: {NAVY} !important; font-weight: 800 !important; }}
p, span, label, div {{ color: {TEXT}; }}

/* ---------- Hero header ---------- */
.hero-wrap {{ animation: heroDrop 0.45s cubic-bezier(.2,.8,.2,1) both; }}
.hero-title {{
    font-size: 2.5rem;
    font-weight: 800;
    color: {NAVY};
    letter-spacing: -0.5px;
    border-left: 6px solid {CORAL};
    padding-left: 18px;
    margin-bottom: 0;
}}
.hero-caption {{
    color: {MUTED};
    padding-left: 24px;
    font-size: 1rem;
    margin-top: 6px;
}}
@keyframes heroDrop {{
    0% {{ opacity: 0.55; transform: translateY(-24px) rotateX(20deg); }}
    100% {{ opacity: 1; transform: translateY(0) rotateX(0); }}
}}

/* ---------- KPI metric cards: 3D tilt-in, staggered, hover lift ---------- */
div[data-testid="stMetric"] {{
    background: linear-gradient(180deg, #191B22 0%, #131419 100%);
    border: 1px solid {BORDER};
    border-top: 3px solid {CORAL};
    border-radius: 12px;
    padding: 16px 18px 12px 18px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.35);
    transform-style: preserve-3d;
    animation: cardTiltIn 0.4s cubic-bezier(.2,.8,.2,1) both;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}}
div[data-testid="stMetric"]:hover {{
    transform: translateY(-4px) rotateX(4deg) scale(1.02);
    box-shadow: 0 16px 30px rgba(0,0,0,0.5);
}}
div[data-testid="column"]:nth-of-type(1) div[data-testid="stMetric"] {{ animation-delay: 0.02s; }}
div[data-testid="column"]:nth-of-type(2) div[data-testid="stMetric"] {{ animation-delay: 0.10s; }}
div[data-testid="column"]:nth-of-type(3) div[data-testid="stMetric"] {{ animation-delay: 0.18s; }}
div[data-testid="column"]:nth-of-type(4) div[data-testid="stMetric"] {{ animation-delay: 0.26s; }}
div[data-testid="column"]:nth-of-type(5) div[data-testid="stMetric"] {{ animation-delay: 0.34s; }}
@keyframes cardTiltIn {{
    0% {{ opacity: 0.6; transform: translateY(18px) rotateX(-20deg) scale(0.96); }}
    100% {{ opacity: 1; transform: translateY(0) rotateX(0) scale(1); }}
}}

div[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
    text-transform: uppercase;
    font-size: 0.7rem !important;
    letter-spacing: 0.6px;
    font-weight: 700 !important;
}}
div[data-testid="stMetricValue"] {{
    color: {CORAL} !important;
    font-weight: 800 !important;
}}

/* ---------- Tabs ---------- */
button[data-baseweb="tab"] {{
    color: {MUTED} !important;
    font-weight: 700;
    font-size: 0.9rem;
    transition: color 0.2s ease, transform 0.2s ease;
}}
button[data-baseweb="tab"]:hover {{ color: {CORAL} !important; transform: translateY(-1px); }}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {CORAL} !important; }}
div[data-baseweb="tab-highlight"] {{ background-color: {CORAL} !important; height: 3px !important; border-radius: 3px; }}
div[data-baseweb="tab-border"] {{ background-color: {BORDER} !important; }}

/* ---------- Entrance for each tab panel's content, replays on every switch ---------- */
/* No rotateX/translateZ here: 3D-transforming a container that wraps the Plotly
   iframe blurs the chart's SVG text while compositing. Keep this 2D-safe. */
div[data-baseweb="tab-panel"] {{
    animation: panelFlyIn 0.4s cubic-bezier(.22,.9,.3,1.1) both;
}}
@keyframes panelFlyIn {{
    0%   {{ opacity: 0.7; transform: translateY(20px) scale(0.99); }}
    100% {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

/* Stagger the row blocks / charts within an active panel */
div[data-baseweb="tab-panel"]:not([hidden]) div[data-testid="stVerticalBlockBorderWrapper"],
div[data-baseweb="tab-panel"]:not([hidden]) div[data-testid="stHorizontalBlock"] {{
    animation: blockRiseIn 0.35s cubic-bezier(.22,.9,.3,1.1) both;
}}
div[data-baseweb="tab-panel"]:not([hidden]) div[data-testid="stHorizontalBlock"]:nth-of-type(1) {{ animation-delay: 0.05s; }}
div[data-baseweb="tab-panel"]:not([hidden]) div[data-testid="stHorizontalBlock"]:nth-of-type(2) {{ animation-delay: 0.14s; }}
div[data-baseweb="tab-panel"]:not([hidden]) div[data-testid="stHorizontalBlock"]:nth-of-type(3) {{ animation-delay: 0.22s; }}
@keyframes blockRiseIn {{
    0%   {{ opacity: 0.65; transform: translateY(18px) scale(0.985); }}
    100% {{ opacity: 1; transform: translateY(0) scale(1); }}
}}

/* ---------- Chart containers: card look + hover pop (2D-safe, no rotateX — ---------- */
/* the chart renders inside an iframe; rotating that plane blurs its text.  */
div[data-testid="stPlotlyChart"] {{
    background: {PANEL};
    border: 1px solid {BORDER};
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    transition: transform 0.3s cubic-bezier(.2,.8,.2,1), box-shadow 0.3s ease;
}}
div[data-testid="stPlotlyChart"]:hover {{
    transform: translateY(-6px) scale(1.012);
    box-shadow: 0 20px 36px rgba(0,0,0,0.45);
}}

/* ---------- Dataframe ---------- */
div[data-testid="stDataFrame"] {{
    border: 1px solid {BORDER};
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.3);
}}

/* ---------- Sidebar ---------- */
.stMultiSelect label, .stCheckbox label {{
    color: {NAVY} !important;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.72rem;
    letter-spacing: 0.6px;
}}
.sidebar-title {{
    color: {CORAL};
    font-weight: 800;
    letter-spacing: 0.5px;
    font-size: 1.15rem;
    border-bottom: 2px solid {BORDER};
    padding-bottom: 10px;
    margin-bottom: 18px;
}}

hr {{ border-color: {BORDER} !important; }}
</style>
""", unsafe_allow_html=True)


px.defaults.template = PLOTLY_TEMPLATE
px.defaults.color_discrete_sequence = CHART_COLORWAY

def style_fig(fig):
    """Apply the dark/coral theme consistently to every chart."""
    fig.update_layout(
        paper_bgcolor=PANEL,
        plot_bgcolor=PANEL,
        font=dict(family="Plus Jakarta Sans, sans-serif", color=TEXT, size=12),
        title_font=dict(family="Plus Jakarta Sans, sans-serif", color=NAVY, size=15),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=TEXT)),
        margin=dict(t=50, l=10, r=10, b=10),
    )
    fig.update_xaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=MUTED)
    fig.update_yaxes(gridcolor=BORDER, zerolinecolor=BORDER, color=MUTED)
    return fig


def show(fig):
    st.plotly_chart(style_fig(fig), use_container_width=True)


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
    return df


df = load_data()

# ---------------- Sidebar filters ----------------
st.sidebar.markdown('<div class="sidebar-title">◆ Filters</div>', unsafe_allow_html=True)

habitats = sorted(df["Location_Type"].dropna().unique())
sel_habitat = st.sidebar.multiselect("Habitat", habitats, default=habitats)

units = sorted(df["Admin_Unit_Code"].dropna().unique())
sel_units = st.sidebar.multiselect("Administrative Unit", units, default=units)

years = sorted(df["Year"].dropna().unique())
sel_years = st.sidebar.multiselect("Year", years, default=years)

species_list = sorted(df["Common_Name"].dropna().unique())
sel_species = st.sidebar.multiselect("Species (optional)", species_list, default=[])

watchlist_only = st.sidebar.checkbox("PIF Watchlist species only", value=False)

# ---------------- Apply filters ----------------
f = df[
    df["Location_Type"].isin(sel_habitat)
    & df["Admin_Unit_Code"].isin(sel_units)
    & df["Year"].isin(sel_years)
]
if sel_species:
    f = f[f["Common_Name"].isin(sel_species)]
if watchlist_only:
    f = f[f["PIF_Watchlist_Status"] == True]

# ---------------- Header ----------------
st.markdown('''
<div class="hero-wrap">
    <div class="hero-title">Bird Species Observation Analysis</div>
    <div class="hero-caption">Forest vs. Grassland biodiversity across 11 National Park Service administrative units</div>
</div>
''', unsafe_allow_html=True)
st.write("")

# ---------------- KPI row ----------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total Observations", f"{len(f):,}")
c2.metric("Unique Species", f"{f['Scientific_Name'].nunique():,}")
c3.metric("Admin Units", f"{f['Admin_Unit_Code'].nunique()}")
c4.metric("Watchlist Species", f"{f.loc[f['PIF_Watchlist_Status']==True,'Scientific_Name'].nunique()}")
avg_temp = f["Temperature"].mean()
c5.metric("Avg Temp (°C)", f"{avg_temp:.1f}" if pd.notna(avg_temp) else "—")

st.divider()

# ---------------- Tabs ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Species Analysis", "Temporal Trends", "Environmental Factors", "Conservation"]
)

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        richness = f.groupby("Location_Type")["Scientific_Name"].nunique().reset_index()
        fig = px.bar(richness, x="Location_Type", y="Scientific_Name",
                     color="Location_Type", title="Species Richness by Habitat",
                     labels={"Scientific_Name": "Unique species"})
        show(fig)
    with col2:
        unit_counts = f.groupby(["Admin_Unit_Code", "Location_Type"]).size().reset_index(name="count")
        fig = px.bar(unit_counts, x="Admin_Unit_Code", y="count", color="Location_Type",
                     title="Observations by Administrative Unit", barmode="stack")
        show(fig)

    obs_map = f.groupby(["Plot_Name", "Location_Type"]).size().reset_index(name="Observations")
    st.subheader("Top Plots by Observation Count")
    st.dataframe(obs_map.sort_values("Observations", ascending=False).head(20),
                 use_container_width=True, hide_index=True)

with tab2:
    col1, col2 = st.columns(2)
    with col1:
        top_species = f["Common_Name"].value_counts().head(15).reset_index()
        top_species.columns = ["Common_Name", "Count"]
        fig = px.bar(top_species.sort_values("Count"), x="Count", y="Common_Name",
                     orientation="h", title="Top 15 Most Observed Species")
        show(fig)
    with col2:
        sex_counts = f["Sex"].value_counts().reset_index()
        sex_counts.columns = ["Sex", "Count"]
        fig = px.pie(sex_counts, names="Sex", values="Count", title="Sex Distribution")
        show(fig)

    id_method = f["ID_Method"].value_counts().reset_index()
    id_method.columns = ["ID_Method", "Count"]
    fig = px.bar(id_method, x="ID_Method", y="Count", title="Detection / Activity Method")
    show(fig)

with tab3:
    monthly = f.groupby(["Month_Name", "Location_Type"]).size().reset_index(name="count")
    month_order = ["January","February","March","April","May","June","July",
                   "August","September","October","November","December"]
    fig = px.line(monthly, x="Month_Name", y="count", color="Location_Type", markers=True,
                  category_orders={"Month_Name": month_order},
                  title="Monthly Observation Trends")
    show(fig)

    yearly = f.groupby(["Year", "Location_Type"]).size().reset_index(name="count")
    fig = px.bar(yearly, x="Year", y="count", color="Location_Type", barmode="group",
                 title="Yearly Observation Counts")
    show(fig)

with tab4:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.histogram(f, x="Temperature", color="Location_Type", nbins=20,
                            title="Temperature Distribution by Habitat")
        show(fig)
    with col2:
        fig = px.histogram(f, x="Humidity", color="Location_Type", nbins=20,
                            title="Humidity Distribution by Habitat")
        show(fig)

    disturbance = f["Disturbance"].value_counts().reset_index()
    disturbance.columns = ["Disturbance", "Count"]
    fig = px.bar(disturbance, x="Disturbance", y="Count", title="Observation Count by Disturbance Level")
    show(fig)

with tab5:
    watch = f[f["PIF_Watchlist_Status"] == True]
    st.metric("Watchlist Observations", f"{len(watch):,}",
              f"{(len(watch)/max(len(f),1))*100:.1f}% of filtered data")

    watch_species = watch.groupby(["Common_Name", "Location_Type"]).size().reset_index(name="Count")
    fig = px.bar(watch_species.sort_values("Count", ascending=False).head(15),
                 x="Common_Name", y="Count", color="Location_Type",
                 title="Top Watchlist Species by Observation Count")
    show(fig)

    stewardship = f["Regional_Stewardship_Status"].value_counts().reset_index()
    stewardship.columns = ["Regional_Stewardship_Status", "Count"]
    fig = px.pie(stewardship, names="Regional_Stewardship_Status", values="Count",
                 title="Regional Stewardship Status Share")
    show(fig)

st.divider()
st.markdown(
    f'<span style="color:{MUTED};font-size:0.8rem;">'
    'Data source: NPS bird monitoring surveys — Forest &amp; Grassland plots across 11 administrative units.'
    '</span>',
    unsafe_allow_html=True,
)
