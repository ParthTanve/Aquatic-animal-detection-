import streamlit as st
from utils.state_manager import clear_state

def render_sidebar():
    st.sidebar.title("🛠 Settings")
    conf = st.sidebar.slider("Confidence", 0.1, 1.0, 0.25)
    iou = st.sidebar.slider("IoU (Overlap)", 0.1, 1.0, 0.45)
    
    if st.sidebar.button("🗑 Clear Session"):
        clear_state()
        
    return conf, iou