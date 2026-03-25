import cv2
import time
import numpy as np
import tempfile
import streamlit as st
from utils.image_utils import draw_neon_box, get_crop

def run_analysis(video_file, detector, conf, iou, placeholders):
    vid_p, chart_p, m1, m2, prog = placeholders
    tfile = tempfile.NamedTemporaryFile(delete=False)
    tfile.write(video_file.read())
    
    cap = cv2.VideoCapture(tfile.name)
    h, w = int(cap.get(4)), int(cap.get(3))
    heatmap = np.zeros((h, w), dtype=np.float32)
    counts = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        results = detector.predict(frame, conf, iou)
        num_found = len(results.boxes)
        counts.append(num_found)
        
        for box in results.boxes:
            heatmap[int(box.xyxy[0][1]):int(box.xyxy[0][3]), 
                    int(box.xyxy[0][0]):int(box.xyxy[0][2])] += 1
            frame = draw_neon_box(frame, box, f"Marine {box.conf[0]:.2f}")
            
            if box.conf[0] > 0.9 and len(st.session_state.gallery) < 9:
                st.session_state.gallery.append(get_crop(frame, box))

        vid_p.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        m1.metric("Objects", num_found)
        if len(counts) % 5 == 0:
            chart_p.area_chart(counts[-50:])
            
    cap.release()
    return heatmap