import streamlit as st
from pages import regional_explorer

st.set_page_config(page_title="Regional Explorer - CarbonTrack", layout="wide")
regional_explorer.render()
