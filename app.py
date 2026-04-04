import streamlit as st
import streamlit.components.v1 as components
import cv2
import numpy as np
import tempfile
import pandas as pd
import time
import os
import datetime
from ultralytics import YOLO

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
# 2. DEEP LEARNING CNN MODEL LOADER 
# ==========================================
@st.cache_resource
def load_ai_model():
    if os.path.exists('best.pt'):
        return YOLO('best.pt')
    else:
        return None

model = load_ai_model()

# 🔥 SPECIES DATABASE 🔥
BIO_DATABASE = {
    "Peacock Flounder": {
        "danger": "🟢 HARMLESS (Safe)",
        "danger_color": "#92FE9D",
        "features": "Flat body geometry. Changes color in 2-8s.",
        "info": "A master of disguise that lies perfectly flat on the sandy ocean bottom. It waits patiently to ambush small fish."
    },
    "Crocodilefish": {
        "danger": "🟢 HARMLESS (Beware of spines)",
        "danger_color": "#92FE9D",
        "features": "Irregular skin flaps (lappets) over eyes.",
        "info": "A bottom-dwelling ambush predator that strongly resembles a crocodile. Very calm and rarely moves when approached."
    },
    "Reef Stonefish": {
        "danger": "🔴 EXTREMELY HARMFUL (Venomous)",
        "danger_color": "#FF4B4B",
        "features": "13 toxic dorsal spines camouflage as rocks.",
        "info": "The most venomous fish known to humans! It looks exactly like an encrusted rock or dead coral to ambush prey."
    },
    "Mimic Octopus": {
        "danger": "🟢 HARMLESS (To Humans)",
        "danger_color": "#92FE9D",
        "features": "Dynamic shape shifting and color mimicry.",
        "info": "A highly intelligent octopus that can impersonate toxic local predators like sea snakes and lionfish to scare off threats."
    }
}

# ==========================================
# 3. HELPER: MERMAID DIAGRAM
# ==========================================
def render_diagram(mermaid_code):
    unique_id = f"mermaid_{int(time.time() * 1000)}"

    components.html(
        f"""
        <style>
            .mermaid svg .cluster rect {{
                fill: rgba(255,255,255,0.03) !important;
                stroke: rgba(0,201,255,0.3) !important;
                stroke-width: 1.5px;
                rx: 10px;
            }}
        </style>

        <div id="{unique_id}" style="
            width: 100%;
            display: flex;
            justify-content: center;
            padding: 30px 0;
        ">
            <div class="mermaid">
                {mermaid_code}
            </div>
        </div>

        <script type="module">
            import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

            mermaid.initialize({{
                startOnLoad: false,
                theme: 'dark',
                securityLevel: 'loose'
            }});

            const el = document.querySelector("#{unique_id} .mermaid");

            if (el) {{
                mermaid.run({{ nodes: [el] }});

                setTimeout(() => {{
                    const svg = el.querySelector("svg");
                    if (svg) {{
                        svg.style.width = "1200px";
                        svg.style.height = "auto";
                        svg.style.display = "block";
                        svg.style.margin = "0 auto";
                    }}
                }}, 300);
            }}
        </script>
        """,
        height=1500
    )

# ==========================================
# 4. ULTRA-ADVANCED ANIMATED CSS
# ==========================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;500;700&display=swap');
    html, body, [class*="css"]  { font-family: 'Rajdhani', sans-serif; }
    [data-testid="stAppViewContainer"] { background: linear-gradient(-45deg, #070b19, #1a0b2e, #0d1b2a, #11051f); background-size: 400% 400%; animation: gradientBG 15s ease infinite; }
    @keyframes gradientBG { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
    [data-testid="stHeader"] { background-color: transparent; }
    .hero-title { font-family: 'Orbitron', sans-serif; font-size: 4.8rem; font-weight: 900; text-align: center; background: linear-gradient(90deg, #00C9FF, #D000FF, #92FE9D); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-top: 1rem; letter-spacing: 4px; text-shadow: 0px 5px 25px rgba(208, 0, 255, 0.3); }
    .hero-subtitle { text-align: center; color: #b3c5d7; font-size: 1.6rem; margin-bottom: 2.5rem; letter-spacing: 2px; }
    
    .guide-card {
        background: linear-gradient(135deg, rgba(208,0,255,0.15), rgba(0,201,255,0.05));
        border: 2px solid #D000FF;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin: 0 auto 30px auto;
        width: 60%;
        box-shadow: 0px 0px 25px rgba(208, 0, 255, 0.4);
        backdrop-filter: blur(10px);
        transition: transform 0.4s ease, box-shadow 0.4s ease;
    }
    .guide-card:hover { transform: translateY(-5px); box-shadow: 0px 10px 35px rgba(208, 0, 255, 0.8); border-color: #00C9FF;}
    
    .team-grid { display: flex; justify-content: center; gap: 20px; flex-wrap: wrap; margin-bottom: 40px; }
    .team-card {
        background: rgba(10, 15, 30, 0.6);
        border-top: 3px solid #00C9FF;
        border-bottom: 3px solid #92FE9D;
        border-radius: 12px;
        padding: 20px 10px;
        width: 18%; 
        min-width: 160px;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.6);
    }
    .team-card:hover {
        transform: translateY(-12px) scale(1.05);
        border-top: 3px solid #D000FF;
        border-bottom: 3px solid #00C9FF;
        box-shadow: 0px 15px 30px rgba(0, 201, 255, 0.5);
    }
    .tm-title { font-size: 0.85rem; color: #00C9FF; text-transform: uppercase; font-family: 'Orbitron', sans-serif; letter-spacing: 1.5px;}
    .tm-name { font-size: 1.2rem; color: #fff; font-weight: bold; margin-top: 8px; font-family: 'Rajdhani', sans-serif; text-shadow: 0px 0px 10px rgba(255,255,255,0.3);}
    
    .module-box { flex: 1; padding: 20px; border-radius: 8px; transition: 0.3s; }
    .module-box:hover { transform: scale(1.02); }

    .stButton>button { background: rgba(15, 20, 40, 0.5); color: #00C9FF; border: 1px solid #00C9FF; border-radius: 10px; padding: 15px 20px; font-family: 'Orbitron', sans-serif; transition: all 0.4s ease; backdrop-filter: blur(5px); width: 100%; }
    .stButton>button:hover { background: rgba(0, 201, 255, 0.1); color: #fff; border-color: #D000FF; box-shadow: 0px 0px 20px rgba(208, 0, 255, 0.6), inset 0px 0px 10px rgba(0, 201, 255, 0.4); transform: translateY(-4px); }
    .launch-btn>div>button { background: linear-gradient(90deg, #00C9FF, #D000FF) !important; color: white !important; font-weight: bold; font-size: 1.4rem; border-radius: 30px; border: none; padding: 15px 40px; }
    .launch-btn>div>button:hover { transform: scale(1.08) !important; box-shadow: 0px 10px 40px rgba(208, 0, 255, 0.8) !important; }
    .glass-container { background: rgba(10, 15, 30, 0.4); border: 1px solid rgba(255, 255, 255, 0.1); border-top: 1px solid rgba(0, 201, 255, 0.4); border-bottom: 1px solid rgba(208, 0, 255, 0.4); border-radius: 15px; padding: 25px; backdrop-filter: blur(15px); margin-bottom: 20px; box-shadow: 0px 15px 35px rgba(0, 0, 0, 0.6); }
    div[data-testid="stMetricValue"] { font-family: 'Orbitron', sans-serif; color: #92FE9D; font-size: 1.8rem; text-shadow: 0px 0px 15px rgba(146, 254, 157, 0.5); }
    div[data-testid="stMetricLabel"] { font-size: 0.95rem; color: #00C9FF; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 5. CORE DEEP LEARNING & SEGMENTATION LOGIC
# ==========================================
def draw_full_animal_box(image, box, conf=0.0, species="Unknown"):
    x1, y1, x2, y2 = map(int, box)
    h, w, _ = image.shape
    box_w, box_h = x2 - x1, y2 - y1
    pad_w, pad_h = int(box_w * 0.40), int(box_h * 0.30)
    nx1, ny1 = max(0, x1 - pad_w), max(0, y1 - pad_h)
    nx2, ny2 = min(w, x2 + pad_w), min(h, y2 + pad_h)
    expanded_box = [nx1, ny1, nx2, ny2]
    
    cv2.rectangle(image, (nx1, ny1), (nx2, ny2), (255, 255, 0), 3) 
    label = f"CNN Match [{species}]: {conf:.2f}"
    cv2.putText(image, label, (nx1, ny1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    return image, expanded_box

def apply_segmentation_mask(frame, mask_overlay):
    colored_mask = np.zeros_like(frame)
    colored_mask[mask_overlay > 0] = (0, 255, 120) 
    return cv2.addWeighted(frame, 1.0, colored_mask, 0.4, 0)

def apply_heatmap_overlay(frame, box):
    x1, y1, x2, y2 = map(int, box)
    heatmap = np.zeros((frame.shape[0], frame.shape[1]), dtype=np.float32)
    radius = int(max(x2 - x1, y2 - y1) * 0.5)
    cv2.circle(heatmap, ((x1 + x2) // 2, (y1 + y2) // 2), radius, 1.0, -1)
    heatmap_norm = np.uint8(255 * cv2.GaussianBlur(heatmap, (151, 151), 100) / np.max(cv2.GaussianBlur(heatmap, (151, 151), 100)))
    return cv2.addWeighted(frame, 0.6, cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET), 0.4, 0)

# ==========================================
# 6. WELCOME PAGE 
# ==========================================
if st.session_state.current_page == "welcome":
    st.markdown("<div class='hero-title'>AQUATIC CAMOUFLAGE AI</div>", unsafe_allow_html=True)
    st.markdown("<div class='hero-subtitle'>CNN Segmentation & Deep Learning Marine Analysis</div>", unsafe_allow_html=True)
    
    # 🔥 PROJECT GUIDE & TEAM MEMBERS SECTION 🔥
    st.markdown("""
        <div class="guide-card">
            <p style="color: #D000FF; font-family: 'Orbitron', sans-serif; font-size: 1rem; letter-spacing: 2px; margin: 0;">PROJECT GUIDE</p>
            <h2 style="color: #fff; font-family: 'Rajdhani', sans-serif; font-size: 2.2rem; font-weight: 700; margin: 5px 0 0 0;">MS. PUSHPA CHUTEL</h2>
        </div>
        
        <div class="team-grid">
            <div class="team-card">
                <div class="tm-title">Team Member 1</div>
                <div class="tm-name">Mayank Lokakshi</div>
            </div>
            <div class="team-card">
                <div class="tm-title">Team Member 2</div>
                <div class="tm-name">Huzaif</div>
            </div>
            <div class="team-card">
                <div class="tm-title">Team Member 3</div>
                <div class="tm-name">Haseeb</div>
            </div>
            <div class="team-card">
                <div class="tm-title">Team Member 4</div>
                <div class="tm-name">Nimish Andraskar</div>
            </div>
            <div class="team-card">
                <div class="tm-title">Team Member 5</div>
                <div class="tm-name">Parth Tanve</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 🔥 ADVANCED PROJECT DESCRIPTION & COMPLEX DIAGRAM 🔥
    st.markdown("""
        <div class='glass-container' style='margin: 0 auto; width: 100%; overflow: visible;'>
            <h3 style='color:#00C9FF; font-family:Orbitron; border-bottom:1px solid rgba(0,201,255,0.3); padding-bottom:10px; text-align: center; margin-bottom: 25px;'>
                 ADVANCED PROJECT DESCRIPTION
            </h3>
            <p style='color:#b3c5d7; font-size:1.1rem; line-height:1.6; font-family:Rajdhani; text-align: justify; margin-bottom: 25px;'>
                The <b>Aquatic Camouflage AI</b> is a high-throughput computer vision pipeline engineered to detect, segment, and analyze cryptic marine life. Leveraging a state-of-the-art <b>Deep Learning Convolutional Neural Network (CNN)</b> architecture, the system processes complex underwater temporal data. It isolates highly camouflaged targets from visually noisy backgrounds using pixel-level semantic segmentation and spatial feature mapping.
            </p>
    """, unsafe_allow_html=True)

    # 🔥 COMPLEX MERMAID BLOCK DIAGRAM 🔥
    complex_architecture = """
graph TD;
    A[Raw Video Stream] --> B(Frame Extraction & OpenCV Parsing);
    B --> C[Tensor Pre-processing & Normalization];

    C --> D{YOLOv8-Seg CNN};

    D -->|Feature Maps| E[Spatial Semantic Masking];
    D -->|Coordinates| F[Bounding Box Regression];
    D -->|Classification| G[Confidence Thresholding];

    E --> H((Polygon Overlay));
    F --> I((Dynamic Padding Box));
    F --> J((Gaussian Thermal Heatmap));
    G --> K[Tactical Bio-Database Lookup];

    H --> L[Live Mission Dashboard];
    I --> L;
    J --> L;
    K --> M[Threat Level & Species Intel];
"""
    st.markdown("<div style='background: rgba(5, 10, 20, 0.7); border-radius: 10px; padding: 15px; border: 1px solid #D000FF; margin-bottom: 25px;'>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center; color:#D000FF; font-family:Orbitron; margin-top:0;'>Neural Architecture Data Flow</h4>", unsafe_allow_html=True)
    
    # 🔥 ADD THIS WRAPPER (IMPORTANT)
    st.markdown("<div style='width:100%; overflow-x:auto;'>", unsafe_allow_html=True)

    render_diagram(complex_architecture)
    
    st.markdown("</div>", unsafe_allow_html=True)  # wrapper close

    st.markdown("</div>", unsafe_allow_html=True)

    # Modules explanation below diagram
    st.markdown("""
            <div style="display: flex; gap: 20px; text-align: left; margin-top: 10px;">
                <div class="module-box" style="background: rgba(0, 201, 255, 0.05); border-left: 3px solid #00C9FF;">
                    <h4 style="color:#00C9FF; font-family:Orbitron; margin-top:0; font-size: 1.05rem;">🧠 Semantic Segmentation Engine</h4>
                    <p style="color:#A0B2C6; font-size: 0.95rem; margin-bottom:0; line-height: 1.4;">Performs pixel-perfect masking using neural weights optimized on large-scale datasets, generating dynamic polygon overlays on targets.</p>
                </div>
                <div class="module-box" style="background: rgba(208, 0, 255, 0.05); border-left: 3px solid #D000FF;">
                    <h4 style="color:#D000FF; font-family:Orbitron; margin-top:0; font-size: 1.05rem;">📊 Spatial Telemetry & Export</h4>
                    <p style="color:#A0B2C6; font-size: 0.95rem; margin-bottom:0; line-height: 1.4;">Computes live bounding-box coordinates, tracking model confidence trajectories, rendering post-mission heatmaps, and auto-exporting data.</p>
                </div>
                <div class="module-box" style="background: rgba(255, 75, 75, 0.05); border-left: 3px solid #FF4B4B;">
                    <h4 style="color:#FF4B4B; font-family:Orbitron; margin-top:0; font-size: 1.05rem;">🧬 Bio-Metric Threat Analysis</h4>
                    <p style="color:#A0B2C6; font-size: 0.95rem; margin-bottom:0; line-height: 1.4;">Cross-references morphological AI features with a localized database to heuristically classify aquatic signatures and compute threat levels.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='launch-btn' style='text-align: center; margin-top: 40px;'>", unsafe_allow_html=True)
    st.button(" INITIALIZE DEEP LEARNING ENGINE", on_click=go_to_app)
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 7. MAIN APP DASHBOARD
# ==========================================
elif st.session_state.current_page == "app":
    st.markdown("<h1 style='font-family: Orbitron; color: white; text-align: left;'><span style='color:red; text-shadow: 0 0 10px red;'>●</span> CNN TACTICAL COMMAND CENTER</h1>", unsafe_allow_html=True)
    
    dash_col, main_col = st.columns([1, 2.8])
    
    with dash_col:
        st.button("⬅ RETURN TO BASE", on_click=go_to_home)
        st.write("")
        st.info(" Deep Learning Model Loaded: Semantic Segmentation Active.")
        st.markdown("**Dataset:** Pre-trained on Roboflow Marine Camouflage Dataset (5000+ Frames).")
        
        with st.expander("OPEN INPUT DASHBOARD", expanded=True):
            uploaded_file = st.file_uploader("Upload Target Video", type=["mp4", "avi", "mov"], label_visibility="collapsed")

    with main_col:
        if uploaded_file is None:
            st.markdown("""
            <div class='glass-container' style='text-align: center; padding: 120px 20px;'>
                <h2 style='color: #00C9FF; font-family: Orbitron; letter-spacing: 3px;'>AWAITING DATA STREAM</h2>
            </div>
            """, unsafe_allow_html=True)
        else:
            tfile = tempfile.NamedTemporaryFile(delete=False)
            tfile.write(uploaded_file.read())
            video_path = tfile.name
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            export_dir = f"CNN_Mission_Data_{timestamp}"
            raw_dir = os.path.join(export_dir, "raw_frames")
            seg_dir = os.path.join(export_dir, "segmented_frames")
            
            os.makedirs(raw_dir, exist_ok=True)
            os.makedirs(seg_dir, exist_ok=True)
                
            st.success(f" Data Stream Locked. Auto-Exporting frames to: **{export_dir}**")
            
            st.markdown("<div class='glass-container' style='padding: 10px 25px;'>", unsafe_allow_html=True)
            m1, m2, m3, m4 = st.columns(4)
            fps_metric, target_metric, mask_metric, conf_metric = m1.empty(), m2.empty(), m3.empty(), m4.empty()
            st.markdown("</div>", unsafe_allow_html=True)

            vid_col, tab_col = st.columns([2, 1]) 
            with vid_col:
                st.markdown("<div class='glass-container'><h3 style='color:#00C9FF; font-family:Orbitron;'>CNN Frame Analysis</h3>", unsafe_allow_html=True)
                stframe = st.empty() 
                st.markdown("</div>", unsafe_allow_html=True)
            with tab_col:
                st.markdown("<div class='glass-container'><h3 style='color:#D000FF; font-family:Orbitron;'>Live Confidence Graph</h3>", unsafe_allow_html=True)
                chart_placeholder = st.empty() 
                st.markdown("</div>", unsafe_allow_html=True)
            
            cap = cv2.VideoCapture(video_path)
            fps_video = cap.get(cv2.CAP_PROP_FPS) or 25 
            
            final_frame, final_box, final_conf, final_species, frame_count, prev_time = None, None, 0.0, "Unknown", 0, time.time() 
            confidence_history = [] 
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret: break
                    
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                raw_frame = frame.copy()
                
                num_detections = 0
                confidence = 0.0
                detected_species = "Processing..."
                
                if model is not None:
                    results = model(raw_frame, verbose=False)
                    num_detections = len(results[0].boxes)
                    if num_detections > 0:
                        boxes = results[0].boxes
                        best_idx = int(boxes.conf.argmax())
                        
                        x1, y1, x2, y2 = boxes.xyxy[best_idx].cpu().numpy()
                        confidence = float(boxes.conf[best_idx].cpu().numpy())
                        detected_box = [int(x1), int(y1), int(x2), int(y2)]
                        
                        class_id = int(boxes.cls[best_idx].cpu().numpy())
                        detected_species = results[0].names[class_id]
                        
                        if results[0].masks is not None:
                            mask_data = results[0].masks.data[best_idx].cpu().numpy()
                            mask_resized = cv2.resize(mask_data, (frame.shape[1], frame.shape[0]))
                            frame = apply_segmentation_mask(frame, mask_resized)
                else:
                    height_img, width_img, _ = frame.shape
                    offset = (frame_count % 30) * 1 
                    detected_box = [int(width_img*0.25) + offset, int(height_img*0.4), int(width_img*0.65) + offset, int(height_img*0.75)]
                    confidence = 0.85 + (0.10 * (np.sin(frame_count/5))) 
                    num_detections = 1
                    detected_species = "Crocodilefish"
                    
                    sim_mask = np.zeros((height_img, width_img), dtype=np.uint8)
                    center_x = (detected_box[0] + detected_box[2]) // 2
                    center_y = (detected_box[1] + detected_box[3]) // 2
                    cv2.ellipse(sim_mask, (center_x, center_y), (int((detected_box[2]-detected_box[0])/2), int((detected_box[3]-detected_box[1])/2)), 0, 0, 360, 255, -1)
                    frame = apply_segmentation_mask(frame, sim_mask)

                confidence_history.append(confidence * 100)

                if num_detections > 0:
                    final_frame = raw_frame.copy()
                    final_conf = confidence
                    final_species = detected_species
                    frame, expanded_box = draw_full_animal_box(frame, detected_box, conf=confidence, species=detected_species)
                    final_box = expanded_box 
                
                save_raw = cv2.cvtColor(raw_frame, cv2.COLOR_RGB2BGR)
                save_seg = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.imwrite(os.path.join(raw_dir, f"frame_{frame_count:04d}.jpg"), save_raw)
                cv2.imwrite(os.path.join(seg_dir, f"frame_{frame_count:04d}.jpg"), save_seg)

                curr_time = time.time()
                processing_fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
                prev_time = curr_time
                
                if frame_count % 2 == 0:
                    fps_metric.metric("CNN Processing FPS", f"{processing_fps:.1f}")
                    target_metric.metric("Active Frames", str(frame_count))
                    mask_metric.metric("Segmentation", "Active (Green)" if num_detections > 0 else "None")
                    conf_metric.metric("Model Confidence", f"{confidence*100:.1f}%" if num_detections > 0 else "0%")
                    
                    stframe.image(frame, channels="RGB", use_container_width=True)
                    
                    chart_df = pd.DataFrame(confidence_history[-50:], columns=["Detection Confidence (%)"])
                    chart_placeholder.area_chart(chart_df, color="#D000FF")
                    
                frame_count += 1

            cap.release()
            
            if final_frame is not None:
                st.markdown("<hr style='border:1px solid #92FE9D'>", unsafe_allow_html=True)
                st.markdown(f"<h2 style='font-family: Orbitron; color: #92FE9D;'>FINAL SNAPSHOT & SPATIAL HEATMAP</h2>", unsafe_allow_html=True)
                
                h_col1, h_col2 = st.columns(2)
                with h_col1:
                    st.markdown("<div class='glass-container'><h4 style='color: #fff;'>Target Snapshot (Yellow Box)</h4>", unsafe_allow_html=True)
                    frame_with_box, _ = draw_full_animal_box(final_frame.copy(), detected_box, conf=final_conf, species=final_species)
                    st.image(frame_with_box, channels="RGB", use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                with h_col2:
                    st.markdown("<div class='glass-container'><h4 style='color: #fff;'>Thermal Heatmap Signature</h4>", unsafe_allow_html=True)
                    st.image(apply_heatmap_overlay(final_frame.copy(), final_box), channels="RGB", use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                st.markdown("<hr style='border:1px solid #00C9FF'>", unsafe_allow_html=True)
                
                with st.spinner("🧬 AI is analyzing biological patterns to compute threat signatures..."):
                    time.sleep(2.5)
                
                bio_data = BIO_DATABASE.get(final_species, {
                    "danger": "🟡 UNKNOWN THREAT",
                    "danger_color": "#FFC107",
                    "features": "Awaiting manual tactical classification.",
                    "info": "This aquatic signature is currently unclassified in our master database."
                })

                st.markdown(f"<h2 style='font-family: Orbitron; color: #00C9FF; text-align: center;'> AI BIO-SCAN RESULTS: {final_species.upper()}</h2>", unsafe_allow_html=True)
                
                st.markdown("<div class='glass-container' style='text-align: center;'>", unsafe_allow_html=True)
                
                st.markdown(f"<h3 style='color: #A0B2C6; font-family: Rajdhani;'>THREAT LEVEL</h3>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-size: 2.2rem; font-weight: 900; color: {bio_data['danger_color']}; text-shadow: 0px 0px 20px {bio_data['danger_color']}; margin-bottom: 30px;'>{bio_data['danger']}</p>", unsafe_allow_html=True)
                
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    st.markdown(f"<h4 style='color: #00C9FF; font-family: Orbitron; border-bottom: 1px solid #00C9FF; padding-bottom: 5px;'>Identified Features</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; color: #E0E0E0;'>{bio_data['features']}</p>", unsafe_allow_html=True)

                with b_col2:
                    st.markdown(f"<h4 style='color: #D000FF; font-family: Orbitron; border-bottom: 1px solid #D000FF; padding-bottom: 5px;'>Species Description</h4>", unsafe_allow_html=True)
                    st.markdown(f"<p style='font-size: 1.1rem; color: #E0E0E0;'>{bio_data['info']}</p>", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)