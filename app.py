import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AEGIS-GUARD | Tactical AI Command",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ADVANCED CYBERPUNK / MILITARY HUD STYLES ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Share+Tech+Mono&display=swap');

    /* Global Dark Theme Background */
    .stApp {
        background-color: #03070d;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(0, 255, 204, 0.05) 0%, transparent 80%),
            linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        color: #00ffcc;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Headings styling */
    h1, h2, h3, h4, .stTitle {
        font-family: 'Orbitron', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #00ffcc !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }

    /* Glassmorphism Metric Cards */
    .hud-card {
        background: rgba(6, 18, 26, 0.7);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 255, 204, 0.3);
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.15), inset 0 0 15px rgba(0, 255, 204, 0.05);
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        transition: all 0.3s ease;
    }
    .hud-card:hover {
        border-color: #00ffcc;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.4);
        transform: translateY(-2px);
    }
    .hud-card-critical {
        background: rgba(30, 5, 12, 0.7);
        border: 1px solid rgba(255, 0, 85, 0.5);
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.2);
    }
    .hud-card-critical:hover {
        border-color: #ff0055;
        box-shadow: 0 0 25px rgba(255, 0, 85, 0.5);
    }

    /* Glowing Tactical Action Buttons */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(0, 0, 0, 0.8)) !important;
        border: 1px solid #00ffcc !important;
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.85rem !important;
        letter-spacing: 1.5px;
        border-radius: 4px !important;
        padding: 10px 16px !important;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.2);
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: #00ffcc !important;
        color: #03070d !important;
        font-weight: 900 !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.8) !important;
    }

    /* Sidebar Custom Styling */
    section[data-testid="stSidebar"] {
        background-color: #020408 !important;
        border-right: 1px solid rgba(0, 255, 204, 0.2);
    }

    /* Radar Animation */
    .radar-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 15px 0;
    }
    .radar {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        border: 1px solid #00ffcc;
        background: radial-gradient(circle, rgba(0,255,204,0.15) 0%, rgba(0,0,0,0.9) 70%),
                    repeating-radial-gradient(circle, transparent 0, transparent 18px, rgba(0,255,204,0.15) 19px);
        position: relative;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.3);
    }
    .radar::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 50%;
        background: conic-gradient(from 0deg, transparent 0deg, transparent 280deg, rgba(0,255,204,0.8) 360deg);
        animation: radar-sweep 2.5s linear infinite;
    }
    @keyframes radar-sweep {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Live Telemetry Marquee Bar */
    .ticker-wrap {
        width: 100%;
        background: rgba(0, 255, 204, 0.05);
        border-top: 1px solid rgba(0, 255, 204, 0.3);
        border-bottom: 1px solid rgba(0, 255, 204, 0.3);
        padding: 6px 0;
        margin-bottom: 20px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# Helper Function for Tactical Log Entries
def render_terminal_log(message, level="INFO"):
    color = "#00ffcc" if level == "INFO" else "#ff0055"
    st.markdown(f"""
    <div style="
        background: rgba(5, 15, 22, 0.9);
        border-left: 3px solid {color};
        padding: 8px 12px;
        font-family: 'Share Tech Mono', monospace;
        font-size: 0.85rem;
        color: {color};
        margin-bottom: 6px;
        border-radius: 0 4px 4px 0;
        box-shadow: 0 0 8px rgba(0,0,0,0.5);
    ">
        <span style="opacity: 0.6;">[{time.strftime('%H:%M:%S')}]</span> 
        <strong>[{level}]</strong> {message}
    </div>
    """, unsafe_allow_html=True)

# Session State Setup
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "logs" not in st.session_state:
    st.session_state["logs"] = []

# --- 1. LOGIN PORTAL ---
if not st.session_state["logged_in"]:
    st.title("🛡️ AEGIS-GUARD TACTICAL OS")
    st.caption("AIR-GAPPED AI BORDER DEFENSE MATRIX v4.2")
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.markdown("""
        <div class="hud-card" style="text-align: left; margin-bottom: 20px;">
            <h3 style="margin-top:0;">🔐 OPERATOR AUTHENTICATION</h3>
            <p style="font-size:0.8rem; color:#888;">ENTER TACTICAL CREDENTIALS TO INITIALIZE AIR-GAPPED MESH NODE.</p>
        </div>
        """, unsafe_allow_html=True)
        
        user = st.text_input("CALL SIGN", value="COMMAND-01")
        pin = st.text_input("ACCESS PIN", type="password", value="1234")
        role = st.selectbox("ASSIGNED ROLE", ["Base Command Officer", "Field Patrol Operator", "System Administrator"])
        
        if st.button("INITIALIZE SYSTEM ACCESS"):
            if user and pin:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.session_state["role"] = role
                st.rerun()

# --- 2. MAIN TACTICAL COMMAND CONSOLE ---
else:
    # Top Live Telemetry Scrolling Ticker
    st.markdown("""
    <div class="ticker-wrap">
        <marquee scrollamount="6" style="font-family: 'Share Tech Mono', monospace; color: #00ffcc; font-size: 0.85rem;">
            ● AIR-GAPPED MESH NODE #01 ACTIVE &nbsp;&nbsp;&nbsp;
            ● ENCRYPTION: AES-256-GCM &nbsp;&nbsp;&nbsp;
            ● SATELLITE SYNC: 100% &nbsp;&nbsp;&nbsp;
            ● LOCAL EDGE LATENCY: 1.2ms &nbsp;&nbsp;&nbsp;
            ● AI CV MODEL: YOLOV8-TACTICAL ENHANCED &nbsp;&nbsp;&nbsp;
            ● PERIMETER STATUS: HIGH ALERT
        </marquee>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar Controls
    st.sidebar.markdown("### 🎛️ SYSTEM CONTROL")
    st.sidebar.markdown(f"**OPERATOR:** `{st.session_state['user']}`")
    st.sidebar.markdown(f"**ROLE:** `{st.session_state['role']}`")
    
    if st.sidebar.button("TERMINATE SESSION"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    
    # Animated Radar HUD
    st.sidebar.markdown("""
    <div class="radar-container">
        <div class="radar"></div>
        <div style="font-size: 0.7rem; color: #00ffcc; letter-spacing: 2px; margin-top: 8px; font-weight: bold;">
            RADAR SWEEP: ACTIVE
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📡 SECTOR SELECTION")
    sector = st.sidebar.selectbox("DEFENSE SECTOR", ["Sector 4-B (High Threat)", "Sector 1-A (Clear Outpost)", "Border Gate West"])
    sensor_mode = st.sidebar.radio("CV SPECTRUM FILTER", ["Real-Time Thermal", "Infrared Night Vision", "Standard Motion Bounding"])
    enable_audio = st.sidebar.checkbox("🔊 Audio Detection Alerts", value=True)

    # Main HUD Header
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,255,204,0.3); padding-bottom: 10px; margin-bottom: 20px;">
        <div>
            <h2 style="margin: 0;">🛡️ AEGIS-GUARD TACTICAL CONSOLE</h2>
            <div style="font-size: 0.8rem; color: #888;">AIR-GAPPED THREAT DETECTION & EDGE PROCESSING</div>
        </div>
        <div style="text-align: right;">
            <span style="background: rgba(0,255,204,0.15); color: #00ffcc; border: 1px solid #00ffcc; padding: 4px 10px; border-radius: 4px; font-size: 0.75rem;">
                ● LIVE DEFENSE MATRIX
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 4 Key HUD Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="hud-card">
            <div style="font-size: 0.7rem; color: #888; letter-spacing: 1px;">TARGET DISTANCE</div>
            <div style="font-size: 1.6rem; font-family: 'Orbitron'; font-weight: 800; color: #00ffcc;">142.4 M</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="hud-card">
            <div style="font-size: 0.7rem; color: #888; letter-spacing: 1px;">AI CONFIDENCE</div>
            <div style="font-size: 1.6rem; font-family: 'Orbitron'; font-weight: 800; color: #00ffcc;">96.2%</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="hud-card">
            <div style="font-size: 0.7rem; color: #888; letter-spacing: 1px;">FRAME RATE</div>
            <div style="font-size: 1.6rem; font-family: 'Orbitron'; font-weight: 800; color: #00ffcc;">60 FPS</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        is_threat = "Sector 4-B" in sector
        card_class = "hud-card-critical" if is_threat else "hud-card"
        threat_text = "LEVEL 4 BREACH" if is_threat else "SECURE"
        text_color = "#ff0055" if is_threat else "#00ffcc"
        st.markdown(f"""
        <div class="{card_class}">
            <div style="font-size: 0.7rem; color: {text_color}; letter-spacing: 1px;">THREAT LEVEL</div>
            <div style="font-size: 1.6rem; font-family: 'Orbitron'; font-weight: 800; color: {text_color};">{threat_text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📹 LIVE VIDEO FEED & SCOPE OVERLAY")
        use_camera = st.checkbox("ACTIVATE CAMERA FEED", value=True)
        frame_window = st.image([])

        if use_camera:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                box_color = (0, 255, 0)
                status_text = "CV TARGET LOCK: ACTIVE"

                if sensor_mode == "Real-Time Thermal":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
                    box_color = (0, 255, 255)
                    status_text = "THERMAL HEAT SIGNATURE LOCK"
                elif sensor_mode == "Infrared Night Vision":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_SUMMER)
                    box_color = (0, 255, 0)
                    status_text = "INFRARED MOTION LOCK"

                h, w, _ = frame.shape
                cx, cy = w // 2, h // 2

                # HUD Crosshairs & Markers
                cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), box_color, 2)
                cv2.putText(frame, status_text, (w//4, h//4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 2)
                cv2.circle(frame, (cx, cy), 35, box_color, 1)
                cv2.line(frame, (cx - 45, cy), (cx + 45, cy), box_color, 1)
                cv2.line(frame, (cx, cy - 45), (cx, cy + 45), box_color, 1)

                frame_window.image(frame, channels="BGR", use_container_width=True)

                if sensor_mode == "Real-Time Thermal" and enable_audio:
                    st.components.v1.html(
                        '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-07a.mp3" type="audio/mpeg"></audio>',
                        height=0
                    )
            cap.release()
        else:
            st.info("CAM SYSTEM STANDBY. CHECK BOX TO START STREAM.")

        st.markdown("### 📍 GPS INCURSION MAP")
        map_data = pd.DataFrame({'lat': [28.5355], 'lon': [77.3910]})
        st.map(map_data, zoom=10)

    with col2:
        st.markdown("### 🚨 SECTOR INCURSION ALERT")
        if "Sector 4-B" in sector:
            st.error("⚠️ CRITICAL ALERT: Perimeter Breach Detected at Coordinates 28.5355° N, 77.3910° E")
        else:
            st.success("✅ SECTOR PERIMETER CLEAR")

        st.markdown("---")
        st.markdown("### ⚡ TACTICAL PROTOCOLS")
        
        if st.session_state["role"] in ["Base Command Officer", "System Administrator"]:
            if st.button("🚨 TRIGGER SILENT ALARM"):
                timestamp = time.strftime("%H:%M:%S")
                log_msg = f"Silent Alarm Initiated by {st.session_state['user']}"
                st.session_state["logs"].append(log_msg)
                st.error("🚨 SIREN ACTIVATED AT BASE COMMAND!")
                st.components.v1.html(
                    '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>',
                    height=0
                )

            st.write("")
            if st.button("📡 BROADCAST MESH SIGNAL"):
                timestamp = time.strftime("%H:%M:%S")
                log_msg = f"Mesh Radio Emergency Broadcast Sent"
                st.session_state["logs"].append(log_msg)
                st.info("Broadcast dispatched to all local mesh nodes.")
        else:
            st.info("🔒 ROLE RESTRICTED: Read-Only Access")

        st.markdown("---")
        st.markdown("### 📋 AUDIT TERMINAL")
        render_terminal_log("AIR-GAPPED MESH ROUTER ONLINE", "INFO")
        
        if st.session_state["logs"]:
            for log in reversed(st.session_state["logs"]):
                render_terminal_log(log, "WARN" if "Alarm" in log else "INFO")
        else:
            st.caption("No breach events logged in this session.")
