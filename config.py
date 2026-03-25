import streamlit as st

APP_TITLE = "Aquatic AI Pro"
THEME_COLOR = "#00fbff"

def apply_custom_css():
    st.markdown(f"""
        <style>
        .main {{ background-color: #0e1117; }}
        .animated-heading {{
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(270deg, {THEME_COLOR}, #0072ff, {THEME_COLOR});
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: gradient-animation 5s ease infinite;
            text-align: center;
        }}
        @keyframes gradient-animation {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        </style>
    """, unsafe_allow_html=True)