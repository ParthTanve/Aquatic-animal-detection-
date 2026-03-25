from ultralytics import YOLO
import streamlit as st

class AquaticDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = self.load_model(model_path)

    @st.cache_resource
    def load_model(_self, path):
        return YOLO(path)

    def predict(self, frame, conf, iou):
        return self.model(frame, conf=conf, iou=iou, verbose=False)[0]