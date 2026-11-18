import streamlit as st
from pages import data_quality

st.set_page_config(page_title="Data Quality - CarbonTrack", layout="wide")
data_quality.render()
