import streamlit as st

def init_state():
    if 'gallery' not in st.session_state:
        st.session_state.gallery = []
    if 'detection_logs' not in st.session_state:
        st.session_state.detection_logs = []

def clear_state():
    st.session_state.gallery = []
    st.session_state.detection_logs = []
    st.rerun()