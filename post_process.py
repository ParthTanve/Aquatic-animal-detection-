import cv2
import numpy as np
import streamlit as st

def generate_heatmap(raw_data):
    heatmap_norm = cv2.normalize(raw_data, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    heatmap_color = cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET)
    return cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)