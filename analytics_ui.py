import streamlit as st
import pandas as pd

def render_stats_columns():
    col_vid, col_stats = st.columns([2, 1])
    with col_vid:
        vid_placeholder = st.empty()
        chart_placeholder = st.empty()
    with col_stats:
        st.subheader("Live Metrics")
        m1 = st.empty()
        m2 = st.empty()
        prog = st.progress(0)
    return vid_placeholder, chart_placeholder, m1, m2, prog