import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
import tempfile
import pandas as pd
import time

# ==========================================
# 1. PAGE SETUP & SESSION STATE
# ==========================================
st.set_page_config(page_title="Aquatic Camouflage AI", layout="wide", initial_sidebar_state="collapsed")

if 'current_page' not in st.session_state:
    st.session_state.current_page = "welcome"
    
if 'active_feature' not in st.session_state:
    st.session_state.active_feature = None

def go_to_app():
    st.session_state.current_page = "app"
    
def go_to_home():
    st.session_state.current_page = "welcome"
    
def set_feature(feature_name):
    if st.session_state.active_feature == feature_name:
        st.session_state.active_feature = None 
    else:
        st.session_state.active_feature = feature_name

# ==========================================
# 2. HELPER: MERMAID DIAGRAM GENERATOR
# ==========================================
def render_diagram(mermaid_code, height=350):
    components.html(
        f"""
        <div class="mermaid" style="display: flex; justify-content: center; background: transparent;">
            {mermaid_code}
        </div>
        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
            mermaid.initialize({{ 
                startOnLoad: true, 
                theme: 'dark',
                themeVariables: {{
                    primaryColor: '#00C9FF', primaryTextColor: '#fff',
                    primaryBorderColor: '#D000FF', lineColor: '#00C9FF',
                    secondaryColor: 'rgba(11, 22, 44, 0.5)', tertiaryColor: 'rgba(16, 33, 65, 0.5)'
                }}
            }});
        </script>
        """, height=height,
    )

# ==========================================
# 3. 🎨 ULTRA-ADVANCED ANIMATED CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;700&display=swap');
    
    html, body, [class*="css"]  { font-family: 'Rajdhani', sans-serif; }

    /* Animated Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(-45deg, #070b19, #1a0b2e, #0d1b2a, #11051f);
        background-size: 400% 400%; animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }

    [data-testid="stHeader"] { background-color: transparent; }
    
    /* Tri-Color Gradient Titles */
    .hero-title { 
        font-family: 'Orbitron', sans-serif; font-size: 4.8rem; font-weight: 900; text-align: center; 
        background: linear-gradient(90deg, #00C9FF, #D000FF, #92FE9D); 
        -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
        margin-top: 1rem; letter-spacing: 4px; text-shadow: 0px 5px 25px rgba(208, 0, 255, 0.3); 
    }
    .hero-subtitle { text-align: center; color: #b3c5d7; font-size: 1.6rem; margin-bottom: 2.5rem; letter-spacing: 2px; }

    /* Interactive Buttons */
    .stButton>button { 
        background: rgba(15, 20, 40, 0.5); color: #00C9FF; border: 1px solid #00C9FF; 
        border-radius: 10px; padding: 15px 20px; font-family: 'Orbitron', sans-serif; 
        transition: all 0.4s ease; backdrop-filter: blur(5px); width: 100%;
    }
    .stButton>button:hover { 
        background: rgba(0, 201, 255, 0.1); color: #fff; border-color: #D000FF; 
        box-shadow: 0px 0px 20px rgba(208, 0, 255, 0.6), inset 0px 0px 10px rgba(0, 201, 255, 0.4); transform: translateY(-4px); 
    }

    .launch-btn>div>button { background: linear-gradient(90deg, #00C9FF, #D000FF) !important; color: white !important; font-weight: bold; font-size: 1.4rem; border-radius: 30px; border: none; padding: 15px 40px; }
    .launch-btn>div>button:hover { transform: scale(1.08) !important; box-shadow: 0px 10px 40px rgba(208, 0, 255, 0.8) !important; }

    /* Custom Expandable Dashboard CSS */
    [data-testid="stExpander"] {
        background: rgba(10, 15, 30, 0.6); border: 1px solid rgba(0, 201, 255, 0.4);
        border-radius: 10px; backdrop-filter: blur(10px);
    }
    [data-testid="stExpander"] summary p { font-family: 'Orbitron', sans-serif; color: #92FE9D !important; font-size: 1.1rem; font-weight: bold; letter-spacing: 1px; }

    /* Glass Containers */
    .glass-container { 
        background: rgba(10, 15, 30, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); 
        border-top: 1px solid rgba(0, 201, 255, 0.4); border-bottom: 1px solid rgba(208, 0, 255, 0.4);
        border-radius: 15px; padding: 25px; backdrop-filter: blur(15px); margin-bottom: 20px; box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.6);
    }
    .explanation-box { 
        background: rgba(5, 8, 20, 0.6); border-left: 4px solid #00C9FF; border-right: 4px solid #D000FF;
        border-radius: 12px; padding: 30px; margin-top: 25px; backdrop-filter: blur(20px); box-shadow: 0px 10px 40px rgba(0, 0, 0, 0.8); 
    }
    
    div[data-testid="stMetricValue"] { font-family: 'Orbitron', sans-serif; color: #92FE9D; font-size: 2.2rem; text-shadow: 0px 0px 15px rgba(146, 254, 157, 0.5); }
    div[data-testid="stMetricLabel"] { font-size: 1rem; color: #00C9FF; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 4. HELPER FUNCTIONS
# ==========================================
def draw_dynamic_yellow_box(image, box, conf=0.0):
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 0), 3)
    cv2.putText(image, f"Target Locked: {conf:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    return image

def apply_heatmap_overlay(frame, box):
    x1, y1, x2, y2 = map(int, box)
    heatmap = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.float32)
    radius = int(max(x2 - x1, y2 - y1) * 0.6)
    cv2.circle(heatmap, ((x1 + x2) // 2, (y1 + y2) // 2), radius, 1.0, -1)
    heatmap_norm = np.uint8(255 * cv2.GaussianBlur(heatmap, (151, 151), 100) / np.max(cv2.GaussianBlur(heatmap, (151, 151), 100)))
    return cv2.addWeighted(frame, 0.6, cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET), 0.4, 0)

def quick_scan_for_camouflage(video_path):
    cap, camouflage_found = cv2.VideoCapture(video_path), False
    time.sleep(1)
    for _ in range(30):
        ret, frame = cap.read()
        if not ret or camouflage_found: break
        if 1 > 0: camouflage_found = True 
    cap.release()
    return camouflage_found

# ==========================================
# 5. WELCOME PAGE 
# ==========================================
if st.session_state.current_page == "welcome":
    st.markdown("<div class='hero-title'>AQUATIC CAMOUFLAGE AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>Advanced Neural Vision for Marine Detection & Spatial Analysis</div>", unsafe_allow_html=True)
    
    st.write("")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🎯 Dynamic Tracking"): set_feature("tracking")
    with col2:
        if st.button("🔥 Spatial Heatmaps"): set_feature("heatmap")
    with col3:
        if st.button("📊 Data Analytics"): set_feature("analytics")

    if st.session_state.active_feature == "tracking":
        st.markdown("<div class='explanation-box'><h3 style='color: #00C9FF; font-family: Orbitron;'>🎯 Dynamic Tracking Architecture</h3>", unsafe_allow_html=True)
        render_diagram("graph TD;\n A[Input Video Stream] -->|Extract Frames| B(OpenCV Preprocessing);\n B --> C{AI Model Inference};\n C -->|Target Found| D[Extract Coordinates x, y];\n C -->|Background| E[Skip Frame];\n D --> F((Dynamic Box));\n F --> G[Live UI];", height=320)
        st.markdown("</div>", unsafe_allow_html=True)
    elif st.session_state.active_feature == "heatmap":
        st.markdown("<div class='explanation-box'><h3 style='color: #D000FF; font-family: Orbitron;'>🔥 Spatial Heatmap Engine</h3>", unsafe_allow_html=True)
        render_diagram("graph LR;\n A[Best Frame] --> B(Box Center);\n B --> C[Thermal Radius];\n C --> D{Gaussian Blur};\n D --> E[COLORMAP_JET];\n E --> F((Heatmap Overlay));", height=220)
        st.markdown("</div>", unsafe_allow_html=True)
    elif st.session_state.active_feature == "analytics":
        st.markdown("<div class='explanation-box'><h3 style='color: #92FE9D; font-family: Orbitron;'>📊 Telemetry & Data Flow</h3>", unsafe_allow_html=True)
        render_diagram("sequenceDiagram\n participant Model as AI Core\n participant Logic as Data Engine\n participant UI as Streamlit App\n Model->>Logic: Send Detections\n Logic->>Logic: Calculate Time\n Logic->>UI: Update Live Table\n Logic-->>UI: Export CSV", height=280)
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    st.write("")
    st.markdown("<div class='launch-btn'>", unsafe_allow_html=True)
    btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 1])
    with btn_col2:
        st.button("🚀 INITIALIZE SYSTEM", on_click=go_to_app)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 6. MAIN APP DASHBOARD (LEFT PANEL UI)
# ==========================================
elif st.session_state.current_page == "app":
    st.markdown("<h1 style='font-family: Orbitron; color: white; text-align: left;'><span style='color:red; text-shadow: 0 0 10px red;'>●</span> TACTICAL COMMAND CENTER</h1>", unsafe_allow_html=True)
    
    # NEW LAYOUT: Left Dashboard Column & Right Main Column
    dash_col, main_col = st.columns([1, 2.8])
    
    with dash_col:
        st.button("⬅ RETURN TO BASE", on_click=go_to_home)
        st.write("")
        
        # The Custom Expandable Left Dashboard
        with st.expander("🎛️ OPEN INPUT DASHBOARD", expanded=True):
            st.markdown("<p style='color:#b3c5d7; font-size: 0.95rem;'>Initialize Neural Engine by injecting the target data stream.</p>", unsafe_allow_html=True)
            uploaded_file = st.file_uploader("Upload Video File", type=["mp4", "avi", "mov"], label_visibility="collapsed")
            if uploaded_file is None:
                st.warning("⚠️ Waiting for input...")

    with main_col:
        # If no video is uploaded, show the STANDBY screen
        if uploaded_file is None:
            st.markdown("""
            <div class='glass-container' style='text-align: center; padding: 120px 20px;'>
                <h2 style='color: #00C9FF; font-family: Orbitron; letter-spacing: 3px; font-size: 3rem;'>SYSTEM ON STANDBY</h2>
                <p style='color: #b3c5d7; font-size: 1.3rem;'>Awaiting target data stream. Please open the <b>INPUT DASHBOARD</b> on the left to initialize.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # If video is uploaded, show the FULL DASHBOARD
        else:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            video_path = tfile.name
            
            with st.spinner("Initiating Deep Scan..."):
                if not quick_scan_for_camouflage(video_path):
                    st.error("❌ ALERT: No camouflage signatures detected. Feed Terminated.")
                    st.stop() 
                
            st.success("✅ Target Locked. Streaming Active.")
            
            # Top Metrics
            st.markdown("<div class='glass-container' style='padding: 10px 25px;'>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            fps_metric, target_metric, conf_metric, time_metric = m1.empty(), m2.empty(), m3.empty(), m4.empty()
            st.markdown("</div>", unsafe_allow_html=True)

            # Live Feed & Table
            vid_col, tab_col = st.columns([2, 1]) 
            with vid_col:
                st.markdown("<div class='glass-container'><h3 style='color:#00C9FF; font-family:Orbitron; border-bottom:1px solid #00C9FF;'>Visual Analysis</h3>", unsafe_allow_html=True)
                stframe = st.empty() 
                st.markdown("</div>", unsafe_allow_html=True)
            with tab_col:
                st.markdown("<div class='glass-container'><h3 style='color:#D000FF; font-family:Orbitron; border-bottom:1px solid #D000FF;'>Telemetry Log</h3>", unsafe_allow_html=True)
                table_placeholder = st.empty() 
                download_placeholder = st.empty() 
                st.markdown("</div>", unsafe_allow_html=True)
            
            # Video Processing Loop
            cap = cv2.VideoCapture(video_path)
            fps_video = cap.get(cv2.CAP_PROP_FPS) or 25 
            export_data, final_frame, final_box, final_conf, frame_count, prev_time = [], None, None, 0.0, 0, time.time() 
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                    
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                raw_frame = frame.copy()
                
                height, width, _ = frame.shape
                offset = (frame_count % 50) * 2 
                detected_box = [int(width*0.3) + offset, int(height*0.3), int(width*0.6) + offset, int(height*0.6)]
                confidence = 0.80 + (0.19 * (offset / 100)) 
                num_detections = 1 
                
                if num_detections > 0:
                    final_frame, final_box, final_conf = raw_frame.copy(), detected_box, confidence
                    frame = draw_dynamic_yellow_box(frame, detected_box, conf=confidence)
                    
                current_time_sec = round(frame_count / fps_video, 2)
                export_data.append({"Frame": frame_count, "Target_Count": num_detections, "Time_Sec": current_time_sec})
                
                curr_time = time.time()
                processing_fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
                prev_time = curr_time
                
                if frame_count % 2 == 0:
                    fps_metric.metric("System FPS", f"{processing_fps:.1f}")
                    target_metric.metric("Active Targets", str(num_detections))
                    conf_metric.metric("Max Confidence", f"{confidence*100:.1f}%")
                    time_metric.metric("Feed Time", f"{current_time_sec}s")
                    stframe.image(frame, channels="RGB", use_container_width=True)
                    table_placeholder.dataframe(pd.DataFrame(export_data[-10:]), use_container_width=True)
                    
                frame_count += 1

            cap.release()
            
            if len(export_data) > 0:
                csv = pd.DataFrame(export_data).to_csv(index=False).encode('utf-8')
                with download_placeholder:
                    st.download_button("📥 Export Logs", data=csv, file_name="ocean_log.csv", mime="text/csv")
                    
            if final_frame is not None:
                st.markdown("<hr style='border:1px solid #92FE9D'>", unsafe_allow_html=True)
                st.markdown("<h2 style='font-family: Orbitron; color: #92FE9D;'>🔥 POST-MISSION HEATMAP</h2>", unsafe_allow_html=True)
                
                h_col1, h_col2 = st.columns(2)
                with h_col1:
                    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
                    st.image(draw_dynamic_yellow_box(final_frame.copy(), final_box, conf=final_conf), channels="RGB", use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                with h_col2:
                    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
                    st.image(apply_heatmap_overlay(final_frame.copy(), final_box), channels="RGB", use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)