"""CarbonTrack - Agricultural Intelligence for Carbon Project Development."""
import os
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="CarbonTrack - Agricultural Carbon Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Ensure data pipelines have run
data_path = "data/processed/"
required_files = [
    "faostat_rice_cleaned.csv",
    "regional_analysis.csv",
    "district_analysis.csv",
    "research_priority_scores.csv"
]
missing_files = [f for f in required_files if not os.path.exists(os.path.join(data_path, f))]
if missing_files:
    from ingestion.faostat import fetch_faostat_data
    from processing.cleaning import clean_faostat_data
    from ingestion.des_india import save_all_des_datasets
    from analytics.regional_analysis import analyze_regional_trends
    from analytics.research_priority import calculate_research_priority

    fetch_faostat_data()
    clean_faostat_data()
    save_all_des_datasets()
    analyze_regional_trends()
    calculate_research_priority()

# Brand styling
st.markdown(
    """
    <style>
    :root {
        --bg: #F6F5F0;
        --surface: #FFFFFF;
        --text: #20231F;
        --muted: #777B72;
        --green: #356B4A;
        --light-green: #E6EEE7;
        --terracotta: #B66A4A;
        --border: #E4E2DA;
    }
    .stApp { background-color: var(--bg); }
    .block-container { padding: 1.5rem 2rem; max-width: 1400px; }
    h1 { font-size: 2.1rem; font-weight: 600; color: var(--text); letter-spacing: -0.02em; }
    h2 { font-size: 1.4rem; font-weight: 600; color: var(--text); margin-top: 1.5rem; }
    h3 { font-size: 1.1rem; font-weight: 600; color: var(--text); }
    .stMarkdown p, .stMarkdown li { color: var(--text); }
    .stMarkdown a { color: var(--green); text-decoration: none; font-weight: 500; }
    .stAlert { background-color: var(--light-green); border: 1px solid var(--border); }
    .stMetric { background-color: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 1rem; box-shadow: 0 1px 3px rgba(0,0,0,0.03); }
    .stMetric label { color: var(--muted); font-size: 0.85rem; }
    .stMetric div[data-testid="stMetricValue"] { color: var(--text); font-size: 1.6rem; font-weight: 600; }
    .stDataFrame { border: 1px solid var(--border); border-radius: 8px; }
    .stDownloadButton > button { border: 1px solid var(--border); border-radius: 6px; background-color: var(--surface); }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🌱 CarbonTrack")
    st.caption("Agricultural Carbon Intelligence Platform")
    st.divider()

    st.markdown("### Navigation")
    page = st.radio(
        "Go to",
        [
            "Overview",
            "Regional Explorer",
            "AWD Project Intelligence",
            "Research Report Generator",
            "Data Sources & Quality"
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### Verified Data Status")
    files = os.listdir(data_path) if os.path.exists(data_path) else []
    if files:
        st.success(f"{len(files)} dataset(s) loaded")
        for f in sorted(files):
            st.caption(f"✓ {f}")
    else:
        st.warning("No data loaded. Initializing...")

    st.divider()
    st.markdown("### Geographic Focus")
    st.caption("📍 Country: **India**")
    st.caption("🌾 Crop: **Paddy Rice**")
    st.caption("🎯 Climate Focus: **Methane (CH₄) Abatement via AWD**")

# Main content router
if page == "Overview":
    from pages import overview
    overview.render()
elif page == "Regional Explorer":
    from pages import regional_explorer
    regional_explorer.render()
elif page == "AWD Project Intelligence":
    from pages import awd_intelligence
    awd_intelligence.render()
elif page == "Research Report Generator":
    from pages import report_generator
    report_generator.render()
elif page == "Data Sources & Quality":
    from pages import data_quality
    data_quality.render()
